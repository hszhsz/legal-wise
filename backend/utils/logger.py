import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from backend.config import settings

def setup_logger(
    name: str = "rightify",
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logging.Logger:
    """设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        max_size: 日志文件最大大小（字节）
        backup_count: 备份文件数量
        format_string: 日志格式字符串
    
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 默认格式
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )
    
    formatter = logging.Formatter(format_string)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# 创建默认日志记录器
logger = setup_logger(
    name="rightify",
    level=settings.log_level,
    log_file=settings.log_file,
    max_size=settings.log_max_size,
    backup_count=settings.log_backup_count
)

# 为不同模块创建专用日志记录器
agent_logger = setup_logger("rightify.agent")
api_logger = setup_logger("rightify.api")
tools_logger = setup_logger("rightify.tools")

# 导出常用函数
def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器"""
    return logging.getLogger(f"rightify.{name}")

def log_function_call(func_name: str, args: dict = None, kwargs: dict = None):
    """记录函数调用"""
    args_str = f"args={args}" if args else ""
    kwargs_str = f"kwargs={kwargs}" if kwargs else ""
    params = ", ".join(filter(None, [args_str, kwargs_str]))
    logger.debug(f"Calling {func_name}({params})")

def log_error(error: Exception, context: str = ""):
    """记录错误信息"""
    context_str = f" in {context}" if context else ""
    logger.error(f"Error{context_str}: {type(error).__name__}: {str(error)}", exc_info=True)

def log_performance(func_name: str, duration: float, success: bool = True):
    """记录性能信息"""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Performance - {func_name}: {duration:.3f}s [{status}]")

# 装饰器：自动记录函数调用和性能
def log_calls(logger_name: str = None):
    """装饰器：自动记录函数调用和执行时间"""
    import functools
    import time
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_logger = get_logger(logger_name) if logger_name else logger
            start_time = time.time()
            
            try:
                func_logger.debug(f"Calling {func.__name__}")
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                func_logger.debug(f"{func.__name__} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                func_logger.error(
                    f"{func.__name__} failed after {duration:.3f}s: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator

# 异步版本的装饰器
def log_async_calls(logger_name: str = None):
    """装饰器：自动记录异步函数调用和执行时间"""
    import functools
    import time
    import asyncio
    import inspect
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_logger = get_logger(logger_name) if logger_name else logger
            
            # 检查函数是否是异步生成器
            if inspect.isasyncgenfunction(func):
                # 对于异步生成器，直接返回生成器对象
                func_logger.debug(f"Calling async generator {func.__name__}")
                return func(*args, **kwargs)
            else:
                # 对于普通异步函数，使用原来的逻辑
                async def async_wrapper():
                    start_time = time.time()
                    try:
                        func_logger.debug(f"Calling async {func.__name__}")
                        result = await func(*args, **kwargs)
                        duration = time.time() - start_time
                        func_logger.debug(f"Async {func.__name__} completed in {duration:.3f}s")
                        return result
                    except Exception as e:
                        duration = time.time() - start_time
                        func_logger.error(
                            f"Async {func.__name__} failed after {duration:.3f}s: {str(e)}",
                            exc_info=True
                        )
                        raise
                return async_wrapper()
        
        return wrapper
    return decorator