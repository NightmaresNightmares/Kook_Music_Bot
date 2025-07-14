import logging
import os
from config import config

# 日志目录
if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)

# 系统日志
system_log_path = os.path.join(config.LOG_DIR, 'bot.log')
# 操作日志
operation_log_path = os.path.join(config.LOG_DIR, 'bot_operations.log')

# 系统日志logger
system_logger = logging.getLogger('MusicBot')
system_logger.setLevel(logging.INFO)
if not system_logger.handlers:
    fh = logging.FileHandler(system_log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    system_logger.addHandler(fh)

# 操作日志logger
operation_logger = logging.getLogger('MusicBotOperation')
operation_logger.setLevel(logging.INFO)
if not operation_logger.handlers:
    fh2 = logging.FileHandler(operation_log_path, encoding='utf-8')
    formatter2 = logging.Formatter('%(asctime)s - %(message)s')
    fh2.setFormatter(formatter2)
    operation_logger.addHandler(fh2)

# 便于其他模块导入
__all__ = ['system_logger', 'operation_logger'] 