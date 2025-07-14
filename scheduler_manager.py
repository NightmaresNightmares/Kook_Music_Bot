import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from logger_manager import system_logger, operation_logger

class SchedulerManager:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        system_logger.info('定时任务调度器已启动')

    def add_job(self, func, trigger, **kwargs):
        job = self.scheduler.add_job(func, trigger, **kwargs)
        operation_logger.info(f'添加定时任务: {job}')
        return job

    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)
        operation_logger.info(f'删除定时任务: {job_id}')

    def list_jobs(self):
        return self.scheduler.get_jobs()

    def shutdown(self):
        self.scheduler.shutdown()
        system_logger.info('定时任务调度器已关闭')

scheduler_manager = SchedulerManager() 