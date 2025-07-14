import os
import logging
import threading
from dotenv import load_dotenv
import khl
from music_service import music_service
from logger_manager import system_logger, operation_logger
from config import config

# 加载环境变量（已在config.py中处理）
# load_dotenv()

# 初始化Kook机器人
bot = khl.Bot(token=config.BOT_TOKEN)

# 歌曲搜索命令
@bot.command(name='点歌')
async def music_command(msg: khl.Message, *, keyword: str):
    try:
        result = music_service.search_song(keyword)
        if result['success']:
            song_info = result['data']
            response = f"🎵 找到歌曲: {song_info['song']} - {song_info['singer']}\n"
            response += f"📀 专辑: {song_info['album']}\n"
            response += f"🎧 音质: {song_info['quality']}\n"
            response += f"🔗 正在语音频道播放..."
            await msg.reply(response)
            # 自动推流到语音频道
            guild_id = config.GUILD_ID
            channel_id = config.VOICE_CHANNEL_ID
            if guild_id and channel_id and song_info['url']:
                await music_service.play_song_to_voice_channel(bot, song_info['url'], guild_id, channel_id)
            else:
                await msg.reply("❌ 配置缺失或音频链接无效，无法推流播放")
        else:
            await msg.reply(f"❌ 搜索失败: {result['error']}")
    except Exception as e:
        system_logger.error(f'命令处理错误: {str(e)}')
        await msg.reply(f"处理命令时发生错误，请查看日志")

# 推荐命令
@bot.command(name='推荐')
async def recommend_command(msg: khl.Message):
    result = music_service.daily_recommend()
    if result['success']:
        songs = result['data']
        reply = '🎵 今日推荐：\n'
        for s in songs[:5]:
            reply += f"{s.get('song')} - {s.get('singer')}\n"
        await msg.reply(reply)
    else:
        await msg.reply(f"❌ 获取推荐失败: {result['error']}")

# 其他命令可按需扩展

def main():
    system_logger.info('Kook机器人启动')
    bot.run()

if __name__ == '__main__':
    main()