from flask import Flask, render_template_string, request
from music_service import music_service
from logger_manager import system_logger

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    song_info = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword:
            result = music_service.search_song(keyword)
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

# 可扩展：日志查看、机器人控制等页面

def run_web():
    app.run(host='0.0.0.0', port=12000, debug=False) 