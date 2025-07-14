import os
from dotenv import load_dotenv

# 加载.env环境变量
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    GUILD_ID = os.getenv('GUILD_ID')
    VOICE_CHANNEL_ID = os.getenv('VOICE_CHANNEL_ID')
    TEXT_CHANNEL_ID = os.getenv('TEXT_CHANNEL_ID')
    ADMIN_ID = os.getenv('ADMIN_ID')
    API_URL = 'https://api.vkeys.cn/v2/music/netease'
    # 端口等可扩展
    WEB_PORT = int(os.getenv('WEB_PORT', 12000))
    LOG_DIR = os.getenv('LOG_DIR', 'logs')

    @classmethod
    def check_config(cls):
        if not cls.BOT_TOKEN:
            raise ValueError('请在.env中配置BOT_TOKEN')
        if not cls.GUILD_ID:
            raise ValueError('请在.env中配置GUILD_ID')

# 用于其他模块导入
config = Config 