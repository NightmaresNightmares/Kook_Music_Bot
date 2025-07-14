import threading
from web_interface import run_web
import bot
from logger_manager import system_logger

def main():
    # 启动Web服务
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    system_logger.info('Web控制面板已启动')
    # 启动机器人
    bot.main()

if __name__ == '__main__':
    main() 