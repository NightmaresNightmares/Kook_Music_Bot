import os
import logging
import threading
from dotenv import load_dotenv
import khl
import requests
from flask import Flask, render_template_string, request

# 加载环境变量
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
LANGUAGE_CHANNEL_ID = os.getenv('LANGUAGE_CHANNEL_ID')
ADMIN_ID = os.getenv('ADMIN_ID')
API_URL = 'https://api.vkeys.cn/v2/music/netease'

# 配置日志
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('MusicBot')

# 初始化Kook机器人
bot = khl.Bot(token=BOT_TOKEN)

# 初始化Flask应用
app = Flask(__name__)

# 歌曲搜索函数
def search_song(keyword: str, choose: int = 1) -> dict:
    try:
        # 移除quality参数，仅保留choose=1
        params = {'word': keyword, 'choose': 1}
        # 记录完整请求URL
        full_url = f'{API_URL}?{"&".join([f"{k}={v}" for k, v in params.items()])}'
        logger.info(f'发送API请求: {full_url}')
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 200:
            # 检查返回数据是否为列表，如果是则取第一个元素
            # 确保即使返回列表也能正确获取首个结果
            result_data = data['data'][0] if isinstance(data['data'], list) and data['data'] else data['data']
            logger.info(f'API请求成功: {response.url}')
            return {'success': True, 'data': result_data}
        else:
            logger.error(f'API请求失败: {data["message"]}, URL: {response.url}, 参数: {params}')
            return {'success': False, 'error': data['message']}
    except Exception as e:
        logger.error(f'搜索歌曲时发生错误: {str(e)}, URL: {API_URL}, 参数: {params}')
        return {'success': False, 'error': str(e)}

# Kook机器人命令: 点歌
@bot.command(name='点歌')
async def music_command(msg: khl.Message, keyword: str):
    try:
        result = search_song(keyword)
        if result['success']:
            song_info = result['data']
            response = f"🎵 找到歌曲: {song_info['song']} - {song_info['singer']}\n"
            response += f"📀 专辑: {song_info['album']}\n"
            response += f"🎧 音质: {song_info['quality']}\n"
            response += f"🔗 链接: {song_info['link']}"
            await msg.reply(response)
            # 这里可以添加播放逻辑
        else:
            await msg.reply(f"❌ 搜索失败: {result['error']}")
    except Exception as e:
        logger.error(f'命令处理错误: {str(e)}')
        await msg.reply(f"处理命令时发生错误，请查看日志")

# Flask网页路由
@app.route('/', methods=['GET', 'POST'])
def index():
    song_info = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword:
            result = search_song(keyword)
            song_info = result
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>音乐点歌系统</title>
        <style>
            body { max-width: 800px; margin: 0 auto; padding: 2rem; font-family: sans-serif; }
            .search-box { margin-bottom: 2rem; }
            input[type='text'] { width: 70%; padding: 0.5rem; }
            button { padding: 0.5rem 1rem; background: #007bff; color: white; border: none; cursor: pointer; }
            .song-info { border: 1px solid #ddd; padding: 1rem; border-radius: 4px; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>音乐点歌系统</h1>
        <div class='search-box'>
            <form method='POST'>
                <input type='text' name='keyword' placeholder='输入歌曲名...' required>
                <button type='submit'>搜索</button>
            </form>
        </div>
        {% if song_info %}
            {% if song_info.success %}
                <div class='song-info'>
                    <h2>{{ song_info.data.song }} - {{ song_info.data.singer }}</h2>
                    <p>专辑: {{ song_info.data.album }}</p>
                    <p>发布时间: {{ song_info.data.time }}</p>
                    <p>音质: {{ song_info.data.quality }}</p>
                    <p>大小: {{ song_info.data.size }}</p>
                    <audio controls>
                        <source src='{{ song_info.data.url }}' type='audio/mpeg'>
                        您的浏览器不支持音频播放
                    </audio>
                </div>
            {% else %}
                <div class='error'>错误: {{ song_info.error }}</div>
            {% endif %}
        {% endif %}
    </body>
    </html>
    ''', song_info=song_info)

# 启动Flask服务器的函数
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

# 主函数
if __name__ == '__main__':
    # 在后台线程启动Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info('Flask服务器已启动')
    # 启动机器人
    bot.run()