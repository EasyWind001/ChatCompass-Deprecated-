"""
任务管理器

功能:
1. 管理任务队列和工作器
2. 协调爬虫和存储
3. 处理任务生命周期
4. 发送进度更新
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from concurrent.futures import ThreadPoolExecutor

from gui.task_queue import TaskQueue, TaskWorker, TaskStatus
from scrapers.scraper_factory import ScraperFactory

logger = logging.getLogger(__name__)


class TaskManagerThread(QThread):
    """任务管理器线程"""
    
    # 信号
    task_completed = pyqtSignal(str, dict)  # 任务完成 (task_id, result)
    task_failed = pyqtSignal(str, str)      # 任务失败 (task_id, error)
    task_progress = pyqtSignal(str, int, str)  # 进度更新 (task_id, progress, message)
    
    def __init__(self, task_queue: TaskQueue, storage):
        """
        初始化管理器线程
        
        Args:
            task_queue: 任务队列
            storage: 存储实例
        """
        super().__init__()
        self.task_queue = task_queue
        self.storage = storage
        self.is_running = False
        self.executor = ThreadPoolExecutor(max_workers=task_queue.max_workers)
        
        logger.info("任务管理器线程初始化完成")
    
    def run(self):
        """运行线程"""
        self.is_running = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.process_tasks())
        except Exception as e:
            logger.error(f"任务管理器线程错误: {e}", exc_info=True)
        finally:
            loop.close()
    
    async def process_tasks(self):
        """处理任务队列"""
        while self.is_running:
            try:
                # 获取待处理任务
                pending_tasks = self.task_queue.get_pending_tasks()
                active_count = self.task_queue.get_active_count()
                
                # 检查是否可以启动新任务
                if pending_tasks and active_count < self.task_queue.max_workers:
                    task = pending_tasks[0]
                    await self.execute_task(task)
                
                # 等待一小段时间再检查
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"处理任务时出错: {e}", exc_info=True)
    
    async def execute_task(self, task: Dict):
        """执行单个任务"""
        task_id = task['id']
        
        try:
            # 更新状态为执行中
            self.task_queue.update_task_status(task_id, TaskStatus.RUNNING.value)
            self.task_progress.emit(task_id, 10, "正在初始化...")
            
            # 创建爬虫
            scraper = ScraperFactory.create_scraper(task['platform'])
            if not scraper:
                raise ValueError(f"不支持的平台: {task['platform']}")
            
            self.task_progress.emit(task_id, 30, "正在爬取数据...")
            
            # 执行爬取
            result = await scraper.scrape_async(task['url'])
            
            if not result:
                raise Exception("爬取失败,未返回数据")
            
            self.task_progress.emit(task_id, 70, "正在保存到数据库...")
            
            # 保存到数据库 (使用正确的API)
            conversation_id = self.storage.add_conversation(
                source_url=task['url'],
                platform=task['platform'],
                title=result.get('title', '未知标题'),
                raw_content=result  # 传递完整的result作为raw_content
            )
            
            # 消息已经包含在raw_content中,不需要单独保存
            message_count = len(result.get('messages', []))
            
            self.task_progress.emit(task_id, 100, "✅ 完成")
            
            # 更新任务状态
            self.task_queue.update_task_status(task_id, TaskStatus.COMPLETED.value)
            self.task_queue.tasks[task_id]['result'] = {
                'conversation_id': conversation_id,
                'message_count': message_count
            }
            
            # 发送完成信号
            self.task_completed.emit(task_id, result)
            
            logger.info(f"任务执行成功: {task_id}")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"任务执行失败: {task_id} - {error_msg}", exc_info=True)
            
            # 更新任务状态
            self.task_queue.update_task_status(task_id, TaskStatus.FAILED.value)
            self.task_queue.tasks[task_id]['error'] = error_msg
            
            # 发送失败信号
            self.task_failed.emit(task_id, error_msg)
            self.task_progress.emit(task_id, 0, f"❌ 失败: {error_msg}")
    
    def stop(self):
        """停止线程"""
        self.is_running = False
        self.executor.shutdown(wait=False)
        logger.info("任务管理器线程已停止")


class TaskManager(QObject):
    """任务管理器"""
    
    # 信号
    task_added = pyqtSignal(str, str)           # 任务添加 (task_id, url)
    task_started = pyqtSignal(str)              # 任务开始 (task_id)
    task_progress = pyqtSignal(str, int, str)   # 进度更新 (task_id, progress, message)
    task_completed = pyqtSignal(str, dict)      # 任务完成 (task_id, result)
    task_failed = pyqtSignal(str, str)          # 任务失败 (task_id, error)
    
    def __init__(self, storage, max_workers: int = 3):
        """
        初始化任务管理器
        
        Args:
            storage: 存储实例
            max_workers: 最大并发数
        """
        super().__init__()
        self.storage = storage
        self.task_queue = TaskQueue(max_workers=max_workers)
        self.manager_thread: Optional[TaskManagerThread] = None
        
        # 连接队列信号
        self.task_queue.task_added.connect(
            lambda tid: self.task_added.emit(tid, self.task_queue.tasks[tid]['url'])
        )
        self.task_queue.task_started.connect(self.task_started.emit)
        
        logger.info(f"任务管理器初始化完成 (max_workers={max_workers})")
    
    def start(self):
        """启动管理器"""
        if self.manager_thread and self.manager_thread.isRunning():
            logger.warning("管理器已在运行")
            return
        
        self.manager_thread = TaskManagerThread(self.task_queue, self.storage)
        
        # 连接线程信号
        self.manager_thread.task_completed.connect(self.task_completed.emit)
        self.manager_thread.task_failed.connect(self.task_failed.emit)
        self.manager_thread.task_progress.connect(self.task_progress.emit)
        
        self.manager_thread.start()
        logger.info("任务管理器已启动")
    
    def stop(self):
        """停止管理器"""
        if self.manager_thread:
            self.manager_thread.stop()
            self.manager_thread.wait()
            self.manager_thread = None
        
        self.task_queue.stop()
        logger.info("任务管理器已停止")
    
    def add_task(self, url: str, platform: str) -> str:
        """添加任务"""
        return self.task_queue.add_task(url, platform)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        return self.task_queue.cancel_task(task_id)
    
    def get_task_status(self, task_id: str) -> Optional[str]:
        """获取任务状态"""
        return self.task_queue.get_task_status(task_id)
    
    def clear_completed(self):
        """清除已完成任务"""
        self.task_queue.clear_completed()
