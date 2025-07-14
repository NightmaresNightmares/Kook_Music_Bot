import requests
from logger_manager import system_logger, operation_logger
from config import config
from simple_kook_voice import VoiceClient
import asyncio

class MusicService:
    @staticmethod
    def search_song(keyword: str, choose: int = 1) -> dict:
        params = {'word': keyword, 'choose': choose}
        try:
            system_logger.info(f'发送API请求: {config.API_URL} {params}')
            response = requests.get(config.API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data['code'] == 200:
                # 兼容data为列表或单个对象
                result_data = data['data'][0] if isinstance(data['data'], list) and data['data'] else data['data']
                # 只返回url字段作为音频链接
                song_info = {
                    'song': result_data.get('song'),
                    'singer': result_data.get('singer'),
                    'album': result_data.get('album'),
                    'quality': result_data.get('quality'),
                    'size': result_data.get('size'),
                    'time': result_data.get('time'),
                    'url': result_data.get('url'),  # 只用url字段
                }
                operation_logger.info(f"搜索成功: {song_info['song']} - {song_info['singer']}")
                return {'success': True, 'data': song_info}
            else:
                system_logger.error(f'API请求失败: {data.get("message")}, 参数: {params}')
                return {'success': False, 'error': data.get('message', '未知错误')}
        except Exception as e:
            system_logger.error(f'搜索歌曲时发生错误: {str(e)}, 参数: {params}')
            return {'success': False, 'error': str(e)}

    @staticmethod
    def daily_recommend():
        # 示例：获取每日推荐歌单
        params = {'type': 'recommend'}
        try:
            response = requests.get(config.API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data['code'] == 200:
                return {'success': True, 'data': data['data']}
            else:
                return {'success': False, 'error': data.get('message', '未知错误')}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    async def play_song_to_voice_channel(bot, url, guild_id, channel_id):
        try:
            vc = VoiceClient(bot, guild_id, channel_id)
            await vc.join()
            await vc.play(url)
            operation_logger.info(f'推流播放: {url} 到频道 {channel_id}')
            # 可选：播放完自动退出
            # await vc.disconnect()
        except Exception as e:
            system_logger.error(f'推流播放失败: {str(e)}')

music_service = MusicService() 