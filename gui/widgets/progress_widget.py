"""
任务进度显示组件

功能:
1. 显示任务列表
2. 实时进度更新
3. 任务状态显示
4. 操作按钮(取消/清除)
"""

from typing import Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QProgressBar, QPushButton,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import logging

logger = logging.getLogger(__name__)


class TaskItem(QFrame):
    """单个任务项"""
    
    # 信号
    cancel_clicked = pyqtSignal(str)  # 取消按钮点击 (task_id)
    
    def __init__(self, task_id: str, url: str, parent=None):
        """
        初始化任务项
        
        Args:
            task_id: 任务ID
            url: URL
            parent: 父组件
        """
        super().__init__(parent)
        self.task_id = task_id
        self.url = url
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # 第一行: URL和取消按钮
        row1 = QHBoxLayout()
        
        self.url_label = QLabel(self.url)
        self.url_label.setWordWrap(True)
        self.url_label.setStyleSheet("color: #3498db; font-size: 10pt;")
        row1.addWidget(self.url_label, 1)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setFixedWidth(60)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_btn.clicked.connect(lambda: self.cancel_clicked.emit(self.task_id))
        row1.addWidget(self.cancel_btn)
        
        layout.addLayout(row1)
        
        # 第二行: 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 第三行: 状态信息
        self.status_label = QLabel("等待中...")
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 9pt;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def update_progress(self, progress: int, message: str = ""):
        """更新进度"""
        self.progress_bar.setValue(progress)
        if message:
            self.status_label.setText(message)
    
    def set_completed(self, success: bool = True):
        """设置完成状态"""
        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("✅ 完成")
            self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            self.cancel_btn.setEnabled(False)
        else:
            self.status_label.setText("❌ 失败")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.cancel_btn.setText("移除")
    
    def set_cancelled(self):
        """设置取消状态"""
        self.status_label.setText("⏸️ 已取消")
        self.status_label.setStyleSheet("color: #95a5a6; font-weight: bold;")
        self.cancel_btn.setText("移除")


class ProgressWidget(QWidget):
    """进度显示组件"""
    
    # 信号
    cancel_task = pyqtSignal(str)  # 取消任务 (task_id)
    clear_all = pyqtSignal()       # 清除所有
    
    def __init__(self, parent=None):
        """
        初始化进度组件
        
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.task_items: Dict[str, TaskItem] = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题栏
        header = QHBoxLayout()
        
        title_label = QLabel("任务队列")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header.addWidget(title_label)
        
        header.addStretch()
        
        # 清除按钮
        self.clear_btn = QPushButton("清除已完成")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_all.emit)
        header.addWidget(self.clear_btn)
        
        layout.addLayout(header)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 任务容器
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.task_container.setLayout(self.task_layout)
        
        scroll.setWidget(self.task_container)
        layout.addWidget(scroll)
        
        # 空状态提示
        self.empty_label = QLabel("暂无任务")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: #95a5a6; font-size: 11pt; padding: 20px;")
        self.task_layout.addWidget(self.empty_label)
        
        self.setLayout(layout)
    
    def add_task(self, task_id: str, url: str):
        """添加任务"""
        if task_id in self.task_items:
            return
        
        # 隐藏空状态
        self.empty_label.hide()
        
        # 创建任务项
        item = TaskItem(task_id, url)
        item.cancel_clicked.connect(self.cancel_task.emit)
        
        self.task_items[task_id] = item
        self.task_layout.addWidget(item)
        
        logger.info(f"添加任务到进度组件: {task_id}")
    
    def update_progress(self, task_id: str, progress: int, message: str = ""):
        """更新任务进度"""
        item = self.task_items.get(task_id)
        if item:
            item.update_progress(progress, message)
    
    def complete_task(self, task_id: str, success: bool = True):
        """完成任务"""
        item = self.task_items.get(task_id)
        if item:
            item.set_completed(success)
    
    def cancel_task_display(self, task_id: str):
        """取消任务显示"""
        item = self.task_items.get(task_id)
        if item:
            item.set_cancelled()
    
    def remove_task(self, task_id: str):
        """移除任务"""
        item = self.task_items.get(task_id)
        if item:
            self.task_layout.removeWidget(item)
            item.deleteLater()
            del self.task_items[task_id]
            
            # 如果没有任务了,显示空状态
            if not self.task_items:
                self.empty_label.show()
            
            logger.info(f"从进度组件移除任务: {task_id}")
    
    def clear_completed_tasks(self):
        """清除已完成的任务"""
        to_remove = []
        for task_id, item in self.task_items.items():
            if "完成" in item.status_label.text() or "失败" in item.status_label.text():
                to_remove.append(task_id)
        
        for task_id in to_remove:
            self.remove_task(task_id)
