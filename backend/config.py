from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    """应用配置类"""
    
    # 基础配置
    app_name: str = "Legal Wise"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # API配置
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api"
    
    # CORS配置
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # LLM配置
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    default_model: str = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    
    # Agent配置
    max_iterations: int = 10
    max_execution_time: int = 300  # 秒
    enable_memory: bool = True
    memory_max_tokens: int = 4000
    
    # 工具配置
    enable_web_search: bool = True
    enable_case_search: bool = True
    enable_lawyer_recommendation: bool = True
    
    # 搜索引擎配置
    search_api: str = "tavily"  # tavily, duckduckgo, brave_search
    tavily_api_key: Optional[str] = None
    brave_search_api_key: Optional[str] = None
    
    # 数据库配置
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    log_max_size: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    
    # 安全配置
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # 文件上传配置
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = [".pdf", ".doc", ".docx", ".txt"]
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 创建必要的目录
        self._create_directories()
        
        # 验证必要的配置
        if not self.deepseek_api_key and not self.openai_api_key:
            raise ValueError(
                "请在.env文件中设置DEEPSEEK_API_KEY或OPENAI_API_KEY"
            )
    
    def _create_directories(self):
        """创建必要的目录"""
        directories = [
            Path(self.log_file).parent,
            Path(self.upload_dir),
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @property
    def llm_config(self) -> dict:
        """获取LLM配置"""
        if self.deepseek_api_key:
            return {
                "api_key": self.deepseek_api_key,
                "base_url": self.deepseek_base_url,
                "model": self.default_model,
                "provider": "deepseek"
            }
        elif self.openai_api_key:
            return {
                "api_key": self.openai_api_key,
                "base_url": self.openai_base_url,
                "model": "gpt-3.5-turbo",
                "provider": "openai"
            }
        else:
            raise ValueError("No valid API key found for LLM provider")
    
    @property
    def search_config(self) -> dict:
        """获取搜索引擎配置"""
        config = {"provider": self.search_api}
        
        if self.search_api == "tavily" and self.tavily_api_key:
            config["api_key"] = self.tavily_api_key
        elif self.search_api == "brave_search" and self.brave_search_api_key:
            config["api_key"] = self.brave_search_api_key
        
        return config

# 全局设置实例
settings = Settings()

# 导出常用配置
LLM_CONFIG = settings.llm_config
SEARCH_CONFIG = settings.search_config
LOG_CONFIG = {
    "level": settings.log_level,
    "file": settings.log_file,
    "max_size": settings.log_max_size,
    "backup_count": settings.log_backup_count,
}