import asyncio
import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod

import httpx
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage

from backend.config import settings
from backend.utils.logger import logger, log_async_calls

class BaseLegalTool(ABC):
    """法律工具基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.initialized = False
    
    async def initialize(self):
        """初始化工具"""
        self.initialized = True
        logger.debug(f"Tool {self.name} initialized")
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """执行工具功能"""
        pass

class LegalAnalysisTool(BaseLegalTool):
    """法律案情分析工具"""
    
    def __init__(self):
        super().__init__()
        self.llm = None
    
    async def initialize(self):
        """初始化LLM"""
        await super().initialize()
        llm_config = settings.llm_config
        self.llm = ChatOpenAI(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            model=llm_config["model"],
            temperature=0.1
        )
    
    @log_async_calls("tools")
    async def analyze(self, case_description: str) -> Dict[str, Any]:
        """分析法律案情"""
        try:
            analysis_prompt = f"""
            作为专业的法律分析师，请对以下案情进行详细分析：
            
            案情描述：{case_description}
            
            请从以下角度进行分析：
            1. 案件性质和类型
            2. 涉及的法律关系
            3. 可能适用的法律条文
            4. 争议焦点
            5. 法律风险评估
            6. 证据要求
            7. 时效性考虑
            
            请以JSON格式返回分析结果：
            {{
                "case_type": "案件类型",
                "legal_relations": ["法律关系1", "法律关系2"],
                "applicable_laws": ["相关法条1", "相关法条2"],
                "key_issues": ["争议点1", "争议点2"],
                "risk_assessment": {{
                    "level": "高/中/低",
                    "description": "风险描述"
                }},
                "evidence_requirements": ["证据要求1", "证据要求2"],
                "time_limitations": "时效说明",
                "summary": "案情分析总结"
            }}
            """
            
            response = await self.llm.ainvoke([SystemMessage(content=analysis_prompt)])
            
            try:
                result = json.loads(response.content)
            except json.JSONDecodeError:
                # 如果JSON解析失败，返回文本结果
                result = {
                    "summary": response.content,
                    "case_type": "待分析",
                    "analysis_text": response.content
                }
            
            result["timestamp"] = datetime.now().isoformat()
            result["tool"] = "legal_analysis"
            
            logger.info("Legal analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Legal analysis failed: {e}")
            return {
                "error": str(e),
                "summary": "分析过程中出现错误",
                "timestamp": datetime.now().isoformat(),
                "tool": "legal_analysis"
            }
    
    async def execute(self, case_description: str) -> Dict[str, Any]:
        return await self.analyze(case_description)

class LegalCaseSearchTool(BaseLegalTool):
    """法律案例搜索工具"""
    
    def __init__(self):
        super().__init__()
        self.mock_cases = [
            {
                "id": "case_001",
                "title": "某公司劳动合同纠纷案",
                "court": "北京市朝阳区人民法院",
                "date": "2023-05-15",
                "case_type": "劳动纠纷",
                "summary": "员工因公司违法解除劳动合同申请仲裁，最终获得经济补偿金。",
                "key_points": ["违法解除", "经济补偿", "举证责任"],
                "result": "支持申请人请求"
            },
            {
                "id": "case_002",
                "title": "房屋买卖合同纠纷案",
                "court": "上海市浦东新区人民法院",
                "date": "2023-03-20",
                "case_type": "合同纠纷",
                "summary": "买方因卖方隐瞒房屋抵押情况要求解除合同并赔偿损失。",
                "key_points": ["信息披露", "合同解除", "损害赔偿"],
                "result": "部分支持"
            },
            {
                "id": "case_003",
                "title": "交通事故人身损害赔偿案",
                "court": "广州市天河区人民法院",
                "date": "2023-07-10",
                "case_type": "侵权纠纷",
                "summary": "机动车与行人发生交通事故，法院根据责任认定判决赔偿。",
                "key_points": ["责任认定", "损害赔偿", "保险理赔"],
                "result": "支持原告请求"
            }
        ]
    
    @log_async_calls("tools")
    async def search(self, keywords: str, case_type: str = "") -> Dict[str, Any]:
        """搜索相关案例"""
        try:
            # 模拟搜索延迟
            await asyncio.sleep(0.5)
            
            # 简单的关键词匹配
            relevant_cases = []
            keywords_lower = keywords.lower()
            
            for case in self.mock_cases:
                # 检查关键词是否在案例中
                if (keywords_lower in case["title"].lower() or 
                    keywords_lower in case["summary"].lower() or
                    any(kw in keywords_lower for kw in case["key_points"])):
                    
                    # 如果指定了案例类型，进行过滤
                    if not case_type or case_type in case["case_type"]:
                        relevant_cases.append(case)
            
            # 如果没有找到相关案例，返回随机案例作为示例
            if not relevant_cases:
                relevant_cases = random.sample(self.mock_cases, min(2, len(self.mock_cases)))
            
            result = {
                "query": keywords,
                "case_type_filter": case_type,
                "total_found": len(relevant_cases),
                "cases": relevant_cases,
                "search_suggestions": [
                    "尝试使用更具体的关键词",
                    "可以按案件类型进行筛选",
                    "建议查看相似案例的判决要点"
                ],
                "timestamp": datetime.now().isoformat(),
                "tool": "case_search"
            }
            
            logger.info(f"Case search completed: found {len(relevant_cases)} cases")
            return result
            
        except Exception as e:
            logger.error(f"Case search failed: {e}")
            return {
                "error": str(e),
                "query": keywords,
                "total_found": 0,
                "cases": [],
                "timestamp": datetime.now().isoformat(),
                "tool": "case_search"
            }
    
    async def execute(self, keywords: str, case_type: str = "") -> Dict[str, Any]:
        return await self.search(keywords, case_type)

class LawyerRecommendationTool(BaseLegalTool):
    """律师推荐工具"""
    
    def __init__(self):
        super().__init__()
        self.mock_lawyers = [
            {
                "id": "lawyer_001",
                "name": "张律师",
                "firm": "北京某某律师事务所",
                "specialties": ["劳动法", "合同法", "公司法"],
                "experience_years": 8,
                "education": "中国政法大学法学硕士",
                "location": "北京",
                "rating": 4.8,
                "cases_handled": 156,
                "contact": "zhang@law.com",
                "description": "专注于劳动争议和合同纠纷，具有丰富的诉讼和仲裁经验。"
            },
            {
                "id": "lawyer_002",
                "name": "李律师",
                "firm": "上海某某律师事务所",
                "specialties": ["房地产法", "建筑工程法", "合同法"],
                "experience_years": 12,
                "education": "华东政法大学法学博士",
                "location": "上海",
                "rating": 4.9,
                "cases_handled": 203,
                "contact": "li@law.com",
                "description": "房地产和建筑工程领域的资深律师，成功处理多起重大案件。"
            },
            {
                "id": "lawyer_003",
                "name": "王律师",
                "firm": "广州某某律师事务所",
                "specialties": ["交通事故", "人身损害", "保险理赔"],
                "experience_years": 6,
                "education": "中山大学法学学士",
                "location": "广州",
                "rating": 4.7,
                "cases_handled": 89,
                "contact": "wang@law.com",
                "description": "专业处理交通事故和人身损害赔偿案件，维护当事人合法权益。"
            }
        ]
    
    @log_async_calls("tools")
    async def recommend(self, case_type: str, location: str = "") -> Dict[str, Any]:
        """推荐律师"""
        try:
            # 模拟推荐延迟
            await asyncio.sleep(0.3)
            
            suitable_lawyers = []
            case_type_lower = case_type.lower()
            
            for lawyer in self.mock_lawyers:
                # 检查专业领域匹配
                specialty_match = any(
                    specialty.lower() in case_type_lower or 
                    case_type_lower in specialty.lower()
                    for specialty in lawyer["specialties"]
                )
                
                # 检查地理位置匹配
                location_match = not location or location in lawyer["location"]
                
                if specialty_match or not case_type:
                    score = 0
                    if specialty_match:
                        score += 50
                    if location_match:
                        score += 30
                    score += lawyer["rating"] * 10
                    score += min(lawyer["experience_years"], 15) * 2
                    
                    lawyer_copy = lawyer.copy()
                    lawyer_copy["match_score"] = score
                    suitable_lawyers.append(lawyer_copy)
            
            # 按匹配分数排序
            suitable_lawyers.sort(key=lambda x: x["match_score"], reverse=True)
            
            # 如果没有找到合适的律师，返回评分最高的律师
            if not suitable_lawyers:
                suitable_lawyers = sorted(
                    self.mock_lawyers, 
                    key=lambda x: x["rating"], 
                    reverse=True
                )[:3]
                for lawyer in suitable_lawyers:
                    lawyer["match_score"] = lawyer["rating"] * 10
            
            result = {
                "case_type": case_type,
                "location_preference": location,
                "total_found": len(suitable_lawyers),
                "recommended_lawyers": suitable_lawyers[:5],  # 最多推荐5个
                "selection_criteria": [
                    "专业领域匹配度",
                    "执业经验年限",
                    "客户评价",
                    "地理位置便利性",
                    "案件处理数量"
                ],
                "consultation_tips": [
                    "建议先进行电话咨询了解律师的专业水平",
                    "可以询问律师处理类似案件的经验",
                    "了解律师费用标准和付费方式",
                    "确认律师的执业资格和信誉"
                ],
                "timestamp": datetime.now().isoformat(),
                "tool": "lawyer_recommendation"
            }
            
            logger.info(f"Lawyer recommendation completed: found {len(suitable_lawyers)} lawyers")
            return result
            
        except Exception as e:
            logger.error(f"Lawyer recommendation failed: {e}")
            return {
                "error": str(e),
                "case_type": case_type,
                "total_found": 0,
                "recommended_lawyers": [],
                "timestamp": datetime.now().isoformat(),
                "tool": "lawyer_recommendation"
            }
    
    async def execute(self, case_type: str, location: str = "") -> Dict[str, Any]:
        return await self.recommend(case_type, location)

class WebSearchTool(BaseLegalTool):
    """网络搜索工具"""
    
    def __init__(self):
        super().__init__()
        self.client = None
    
    async def initialize(self):
        await super().initialize()
        self.client = httpx.AsyncClient(timeout=30.0)
    
    @log_async_calls("tools")
    async def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """执行网络搜索"""
        try:
            # 这里可以集成真实的搜索API，如Tavily、DuckDuckGo等
            # 目前返回模拟结果
            await asyncio.sleep(0.8)  # 模拟网络延迟
            
            mock_results = [
                {
                    "title": f"关于'{query}'的法律解释",
                    "url": "https://example-law.com/article1",
                    "snippet": f"根据相关法律规定，{query}涉及的法律问题需要从多个角度进行分析...",
                    "source": "法律资讯网",
                    "date": "2023-10-15"
                },
                {
                    "title": f"{query}相关案例分析",
                    "url": "https://example-court.com/case123",
                    "snippet": f"在处理{query}类型的案件时，法院通常会考虑以下因素...",
                    "source": "法院公报",
                    "date": "2023-09-20"
                },
                {
                    "title": f"专家解读：{query}的法律风险",
                    "url": "https://example-expert.com/analysis",
                    "snippet": f"法律专家指出，{query}可能面临的主要风险包括...",
                    "source": "法律专家网",
                    "date": "2023-08-30"
                }
            ]
            
            result = {
                "query": query,
                "total_results": len(mock_results),
                "results": mock_results[:max_results],
                "search_time": 0.8,
                "suggestions": [
                    "尝试使用更具体的法律术语",
                    "可以添加地区或时间限制",
                    "建议查看官方法律文件"
                ],
                "timestamp": datetime.now().isoformat(),
                "tool": "web_search"
            }
            
            logger.info(f"Web search completed for query: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return {
                "error": str(e),
                "query": query,
                "total_results": 0,
                "results": [],
                "timestamp": datetime.now().isoformat(),
                "tool": "web_search"
            }
    
    async def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        return await self.search(query, max_results)

class ReportGeneratorTool(BaseLegalTool):
    """法律分析报告生成工具"""
    
    def __init__(self):
        super().__init__()
        self.llm = None
    
    async def initialize(self):
        await super().initialize()
        llm_config = settings.llm_config
        self.llm = ChatOpenAI(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            model=llm_config["model"],
            temperature=0.2
        )
    
    @log_async_calls("tools")
    async def generate(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        """生成综合法律分析报告"""
        try:
            report_prompt = f"""
            基于以下执行结果，生成一份专业的法律分析报告：
            
            执行结果：
            {json.dumps(execution_results, ensure_ascii=False, indent=2)}
            
            请生成一份结构化的法律分析报告，包含以下部分：
            
            1. 执行摘要
            2. 案情分析
            3. 法律依据
            4. 风险评估
            5. 建议措施
            6. 注意事项
            7. 后续行动计划
            
            报告应该专业、客观、实用，便于当事人理解和采取行动。
            
            请以JSON格式返回报告：
            {{
                "report_title": "报告标题",
                "executive_summary": "执行摘要",
                "case_analysis": "案情分析",
                "legal_basis": "法律依据",
                "risk_assessment": "风险评估",
                "recommendations": "建议措施",
                "precautions": "注意事项",
                "action_plan": "后续行动计划",
                "report_date": "报告日期",
                "disclaimer": "免责声明"
            }}
            """
            
            response = await self.llm.ainvoke([SystemMessage(content=report_prompt)])
            
            try:
                report_data = json.loads(response.content)
            except json.JSONDecodeError:
                # 如果JSON解析失败，创建基本报告结构
                report_data = {
                    "report_title": "法律分析报告",
                    "executive_summary": "基于提供的信息进行了综合分析",
                    "full_content": response.content,
                    "report_date": datetime.now().strftime("%Y-%m-%d"),
                    "disclaimer": "本报告仅供参考，具体法律问题请咨询专业律师"
                }
            
            # 添加元数据
            report_data.update({
                "generation_timestamp": datetime.now().isoformat(),
                "tool": "report_generator",
                "based_on_results": list(execution_results.keys()),
                "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            })
            
            logger.info("Legal report generated successfully")
            return report_data
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {
                "error": str(e),
                "report_title": "报告生成失败",
                "executive_summary": "生成报告时出现错误，请稍后重试",
                "timestamp": datetime.now().isoformat(),
                "tool": "report_generator"
            }
    
    async def execute(self, execution_results: Dict[str, Any]) -> Dict[str, Any]:
        return await self.generate(execution_results)