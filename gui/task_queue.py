"""
异步任务队列

功能:
1. 任务队列管理
2. 并发控制
3. 异步执行
4. 进度更新
5. 错误处理
"""

import asyncio
import logging
import uuid
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from enum import Enum

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = 'pending'       # 等待中
    RUNNING = 'running'       # 执行中
    COMPLETED = 'completed'   # 已完成
    FAILED = 'failed'         # 失败
    CANCELLED = 'cancelled'   # 已取消


class TaskQueue(QObject):
    """异步任务队列"""
    
    # 信号
    task_added = pyqtSignal(str)                    # 任务添加 (task_id)
    task_started = pyqtSignal(str)                  # 任务开始 (task_id)
    task_progress = pyqtSignal(str, int, str)       # 任务进度 (task_id, progress, message)
    task_completed = pyqtSignal(str, object)        # 任务完成 (task_id, result)
    task_failed = pyqtSignal(str, str)              # 任务失败 (task_id, error)
    task_cancelled = pyqtSignal(str)                # 任务取消 (task_id)
    
    def __init__(self, max_workers: int = 3):
        """
        初始化任务队列
        
        Args:
            max_workers: 最大并发数
        """
        super().__init__()
        self.max_workers = max_workers
        self.tasks: Dict[str, Dict] = {}
        self.is_running = False
        self.active_tasks = 0
        
        logger.info(f"任务队列初始化完成 (max_workers={max_workers})")
    
    def add_task(self, url: str, platform: str, **kwargs) -> str:
        """
        添加任务到队列
        
        Args:
            url: 对话URL
            platform: 平台名称
            **kwargs: 其他参数
            
        Returns:
            任务ID
        """
        task_id = str(uuid.uuid4())
        
        task = {
            'id': task_id,
            'url': url,
            'platform': platform,
            'status': TaskStatus.PENDING.value,
            'progress': 0,
            'message': '等待中...',
            'created_at': datetime.now(),
            'started_at': None,
            'completed_at': None,
            'result': None,
            'error': None,
            **kwargs
        }
        
        self.tasks[task_id] = task
        self.task_added.emit(task_id)
        
        logger.info(f"任务已添加: {task_id} - {url}")
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def get_task_status(self, task_id: str) -> Optional[str]:
        """获取任务状态"""
        task = self.tasks.get(task_id)
        return task['status'] if task else None
    
    def update_task_status(self, task_id: str, status: str):
        """更新任务状态"""
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = status
            
            if status == TaskStatus.RUNNING.value:
                self.tasks[task_id]['started_at'] = datetime.now()
                self.task_started.emit(task_id)
            elif status == TaskStatus.COMPLETED.value:
                self.tasks[task_id]['completed_at'] = datetime.now()
            elif status == TaskStatus.CANCELLED.value:
                self.task_cancelled.emit(task_id)
    
    def update_task_progress(self, task_id: str, progress: int, message: str = ""):
        """更新任务进度"""
        if task_id in self.tasks:
            self.tasks[task_id]['progress'] = progress
            self.tasks[task_id]['message'] = message
            self.task_progress.emit(task_id, progress, message)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        # 只能取消等待中或执行中的任务
        if task['status'] in [TaskStatus.PENDING.value, TaskStatus.RUNNING.value]:
            self.update_task_status(task_id, TaskStatus.CANCELLED.value)
            logger.info(f"任务已取消: {task_id}")
            return True
        
        return False
    
    def get_pending_tasks(self) -> List[Dict]:
        """获取所有等待中的任务"""
        return [
            task for task in self.tasks.values()
            if task['status'] == TaskStatus.PENDING.value
        ]
    
    def get_active_count(self) -> int:
        """获取活跃任务数"""
        return sum(
            1 for task in self.tasks.values()
            if task['status'] == TaskStatus.RUNNING.value
        )
    
    def clear_completed(self):
        """清除已完成的任务"""
        completed_ids = [
            tid for tid, task in self.tasks.items()
            if task['status'] in [
                TaskStatus.COMPLETED.value,
                TaskStatus.FAILED.value,
                TaskStatus.CANCELLED.value
            ]
        ]
        
        for task_id in completed_ids:
            del self.tasks[task_id]
        
        logger.info(f"已清除 {len(completed_ids)} 个已完成任务")
    
    def stop(self):
        """停止队列"""
        self.is_running = False
        logger.info("任务队列已停止")


class TaskWorker(QObject):
    """任务工作器"""
    
    def __init__(self, scraper=None):
        """
        初始化工作器
        
        Args:
            scraper: 爬虫实例
        """
        super().__init__()
        self.scraper = scraper
    
    async def execute_task(self, task: Dict) -> Optional[Dict]:
        """
        执行任务
        
        Args:
            task: 任务信息
            
        Returns:
            执行结果
        """
        try:
            logger.info(f"开始执行任务: {task['id']}")
            
            if not self.scraper:
                raise ValueError("爬虫实例未设置")
            
            # 调用爬虫
            result = await self.scraper.scrape(
                url=task['url'],
                platform=task['platform']
            )
            
            logger.info(f"任务执行成功: {task['id']}")
            return result
            
        except Exception as e:
            logger.error(f"任务执行失败: {task['id']} - {e}", exc_info=True)
            return None
