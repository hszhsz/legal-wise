import asyncio
import json
from typing import Dict, Any, List, AsyncGenerator, Optional
from datetime import datetime
import uuid

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from backend.tools.legal_tools import (
    LegalCaseSearchTool,
    LawyerRecommendationTool,
    LegalAnalysisTool,
    WebSearchTool,
    ReportGeneratorTool
)
from backend.config import settings
from backend.utils.logger import logger, log_async_calls

class AgentState(TypedDict):
    """Agent状态定义"""
    messages: Annotated[list, add_messages]
    plan: List[str]
    current_step: int
    execution_results: Dict[str, Any]
    final_answer: str
    case_type: str
    session_id: str
    metadata: Dict[str, Any]

class LegalPlanExecuteAgent:
    """基于LangGraph的法律咨询Plan-and-Execute Agent"""
    
    def __init__(self):
        self.llm = None
        self.tools = {}
        self.graph = None
        self.memory = None
        self.session_id = str(uuid.uuid4())
        
    @log_async_calls("agent")
    async def initialize(self):
        """初始化Agent"""
        try:
            # 初始化LLM
            llm_config = settings.llm_config
            self.llm = ChatOpenAI(
                api_key=llm_config["api_key"],
                base_url=llm_config["base_url"],
                model=llm_config["model"],
                temperature=0.1,
                streaming=True
            )
            
            # 初始化工具
            await self._initialize_tools()
            
            # 初始化记忆
            self.memory = ConversationBufferWindowMemory(
                k=settings.memory_max_tokens,
                return_messages=True
            )
            
            # 构建LangGraph
            self._build_graph()
            
            logger.info("Legal Plan-Execute Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise
    
    async def _initialize_tools(self):
        """初始化工具"""
        self.tools = {
            "case_search": LegalCaseSearchTool(),
            "lawyer_recommendation": LawyerRecommendationTool(),
            "legal_analysis": LegalAnalysisTool(),
            "web_search": WebSearchTool(),
            "report_generator": ReportGeneratorTool()
        }
        
        # 初始化每个工具
        for tool_name, tool in self.tools.items():
            try:
                if hasattr(tool, 'initialize'):
                    await tool.initialize()
                logger.debug(f"Tool {tool_name} initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize tool {tool_name}: {e}")
    
    def _build_graph(self):
        """构建LangGraph工作流"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("executor", self._executor_node)
        workflow.add_node("analyzer", self._analyzer_node)
        workflow.add_node("finalizer", self._finalizer_node)
        
        # 设置入口点
        workflow.set_entry_point("planner")
        
        # 添加边
        workflow.add_edge("planner", "executor")
        workflow.add_edge("executor", "analyzer")
        workflow.add_conditional_edges(
            "analyzer",
            self._should_continue,
            {
                "continue": "executor",
                "finish": "finalizer"
            }
        )
        workflow.add_edge("finalizer", END)
        
        self.graph = workflow.compile()
    
    async def _planner_node(self, state: AgentState) -> AgentState:
        """规划节点 - 分析用户查询并制定执行计划"""
        logger.debug("Executing planner node")
        
        user_query = state["messages"][-1].content
        case_type = state.get("case_type", "general")
        
        planning_prompt = f"""
        作为专业的法律咨询AI助手，请分析以下用户查询并制定详细的执行计划。
        
        用户查询：{user_query}
        案例类型：{case_type}
        
        请制定一个包含以下步骤的执行计划（根据查询内容选择相关步骤）：
        1. 法律案情分析 - 分析用户描述的法律问题
        2. 相关法条检索 - 查找相关的法律条文
        3. 案例检索 - 搜索相似的法律案例
        4. 律师推荐 - 推荐合适的专业律师
        5. 风险评估 - 评估法律风险和可能后果
        6. 解决方案建议 - 提供具体的解决建议
        7. 报告生成 - 生成综合分析报告
        
        请以JSON格式返回执行计划，格式如下：
        {{
            "plan": ["步骤1", "步骤2", "步骤3"],
            "reasoning": "制定此计划的原因"
        }}
        """
        
        try:
            response = await self.llm.ainvoke([SystemMessage(content=planning_prompt)])
            response_content = response.content.strip()
            
            # 尝试提取JSON部分
            if '{' in response_content and '}' in response_content:
                start_idx = response_content.find('{')
                end_idx = response_content.rfind('}') + 1
                json_str = response_content[start_idx:end_idx]
                plan_data = json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in response")
            
            state["plan"] = plan_data["plan"]
            state["current_step"] = 0
            state["execution_results"] = {}
            state["metadata"]["planning_reasoning"] = plan_data.get("reasoning", "")
            
            logger.info(f"Plan created with {len(state['plan'])} steps")
            
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            # 使用默认计划
            state["plan"] = ["法律案情分析", "案例检索", "解决方案建议"]
            state["current_step"] = 0
            state["execution_results"] = {}
        
        return state
    
    async def _executor_node(self, state: AgentState) -> AgentState:
        """执行节点 - 执行当前计划步骤"""
        logger.debug(f"Executing step {state['current_step']}")
        
        if state["current_step"] >= len(state["plan"]):
            return state
        
        current_step = state["plan"][state["current_step"]]
        user_query = state["messages"][-1].content
        
        try:
            result = await self._execute_step(current_step, user_query, state)
            state["execution_results"][current_step] = result
            state["current_step"] += 1
            
            logger.info(f"Step '{current_step}' completed successfully")
            
        except Exception as e:
            logger.error(f"Step '{current_step}' failed: {e}")
            state["execution_results"][current_step] = {
                "error": str(e),
                "status": "failed"
            }
            state["current_step"] += 1
        
        return state
    
    async def _execute_step(self, step: str, query: str, state: AgentState) -> Dict[str, Any]:
        """执行具体步骤"""
        step_lower = step.lower()
        
        if "分析" in step_lower or "案情" in step_lower:
            return await self.tools["legal_analysis"].analyze(query)
        
        elif "检索" in step_lower or "案例" in step_lower:
            return await self.tools["case_search"].search(query, state.get("case_type", ""))
        
        elif "律师" in step_lower or "推荐" in step_lower:
            return await self.tools["lawyer_recommendation"].recommend(
                state.get("case_type", ""), 
                state["metadata"].get("location", "")
            )
        
        elif "搜索" in step_lower or "查找" in step_lower:
            return await self.tools["web_search"].search(query)
        
        elif "报告" in step_lower or "生成" in step_lower:
            return await self.tools["report_generator"].generate(state["execution_results"])
        
        else:
            # 通用LLM处理
            prompt = f"请处理以下法律相关任务：{step}\n\n用户查询：{query}"
            response = await self.llm.ainvoke([SystemMessage(content=prompt)])
            return {"content": response.content, "type": "llm_response"}
    
    async def _analyzer_node(self, state: AgentState) -> AgentState:
        """分析节点 - 分析执行结果并决定是否继续"""
        logger.debug("Executing analyzer node")
        
        # 检查是否所有步骤都已完成
        if state["current_step"] >= len(state["plan"]):
            state["metadata"]["analysis_result"] = "all_steps_completed"
            return state
        
        # 分析当前执行结果的质量
        current_results = state["execution_results"]
        failed_steps = [step for step, result in current_results.items() 
                       if isinstance(result, dict) and result.get("status") == "failed"]
        
        if len(failed_steps) > len(state["plan"]) // 2:
            # 如果失败步骤过多，提前结束
            state["metadata"]["analysis_result"] = "too_many_failures"
            state["current_step"] = len(state["plan"])  # 强制结束
        else:
            state["metadata"]["analysis_result"] = "continue_execution"
        
        return state
    
    def _should_continue(self, state: AgentState) -> str:
        """决定是否继续执行"""
        if state["current_step"] >= len(state["plan"]):
            return "finish"
        
        analysis_result = state["metadata"].get("analysis_result", "continue_execution")
        if analysis_result in ["all_steps_completed", "too_many_failures"]:
            return "finish"
        
        return "continue"
    
    async def _finalizer_node(self, state: AgentState) -> AgentState:
        """最终化节点 - 生成最终答案"""
        logger.debug("Executing finalizer node")
        
        user_query = state["messages"][-1].content
        execution_results = state["execution_results"]
        
        # 构建最终回答
        final_prompt = f"""
        基于以下执行结果，为用户提供一个全面、专业的法律咨询回答。
        
        用户查询：{user_query}
        
        执行结果：
        {json.dumps(execution_results, ensure_ascii=False, indent=2)}
        
        请提供一个结构化的回答，包括：
        1. 问题分析
        2. 相关法律依据
        3. 风险评估
        4. 建议措施
        5. 注意事项
        
        回答应该专业、准确、易懂。
        """
        
        try:
            response = await self.llm.ainvoke([SystemMessage(content=final_prompt)])
            state["final_answer"] = response.content
            
            # 添加到消息历史
            state["messages"].append(AIMessage(content=response.content))
            
            logger.info("Final answer generated successfully")
            
        except Exception as e:
            logger.error(f"Failed to generate final answer: {e}")
            state["final_answer"] = "抱歉，生成最终回答时出现错误，请稍后重试。"
        
        return state
    
    @log_async_calls("agent")
    async def stream_consultation(self, query: str, case_type: str = "general") -> AsyncGenerator[Dict[str, Any], None]:
        """流式法律咨询"""
        try:
            # 初始化状态
            initial_state = {
                "messages": [HumanMessage(content=query)],
                "plan": [],
                "current_step": 0,
                "execution_results": {},
                "final_answer": "",
                "case_type": case_type,
                "session_id": self.session_id,
                "metadata": {
                    "start_time": datetime.now().isoformat(),
                    "location": "未指定"
                }
            }
            
            # 发送开始事件
            yield {
                "type": "start",
                "content": "开始分析您的法律问题...",
                "timestamp": datetime.now().isoformat()
            }
            
            # 执行工作流
            async for event in self.graph.astream(initial_state):
                for node_name, node_output in event.items():
                    if node_name == "planner":
                        plan_str = ', '.join(node_output['plan'])
                        yield {
                            "type": "planning",
                            "content": "制定执行计划：" + plan_str,
                            "data": {"plan": node_output["plan"]},
                            "timestamp": datetime.now().isoformat()
                        }
                    
                    elif node_name == "executor":
                        current_step = node_output["current_step"] - 1
                        if current_step >= 0 and current_step < len(node_output["plan"]):
                            step_name = node_output["plan"][current_step]
                            yield {
                                "type": "execution",
                                "content": "正在执行：" + step_name,
                                "data": {
                                    "step": step_name,
                                    "step_number": current_step + 1,
                                    "total_steps": len(node_output["plan"])
                                },
                                "timestamp": datetime.now().isoformat()
                            }
                    
                    elif node_name == "finalizer":
                        yield {
                            "type": "final_answer",
                            "content": node_output["final_answer"],
                            "data": {
                                "execution_results": node_output["execution_results"],
                                "session_id": node_output["session_id"]
                            },
                            "timestamp": datetime.now().isoformat()
                        }
            
            # 发送完成事件
            yield {
                "type": "complete",
                "content": "咨询完成",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error("Error in stream_consultation: %s", error_msg)
            yield {
                "type": "error",
                "content": "处理过程中出现错误：" + error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_case(self, case_description: str) -> Dict[str, Any]:
        """分析法律案情"""
        return await self.tools["legal_analysis"].analyze(case_description)
    
    async def search_cases(self, keywords: str, case_type: str = "") -> Dict[str, Any]:
        """搜索相关案例"""
        return await self.tools["case_search"].search(keywords, case_type)
    
    async def recommend_lawyers(self, case_type: str, location: str = "") -> Dict[str, Any]:
        """推荐律师"""
        return await self.tools["lawyer_recommendation"].recommend(case_type, location)
    
    async def generate_report(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成法律分析报告"""
        return await self.tools["report_generator"].generate(case_data)
    
    async def get_status(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return {
            "session_id": self.session_id,
            "initialized": self.llm is not None,
            "tools_count": len(self.tools),
            "memory_enabled": self.memory is not None,
            "graph_built": self.graph is not None,
            "timestamp": datetime.now().isoformat()
        }