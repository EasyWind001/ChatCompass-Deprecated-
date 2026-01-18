"""
SearchBar - 搜索栏组件

提供搜索和过滤功能
"""
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QComboBox,
    QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon


class SearchBar(QWidget):
    """搜索栏组件"""
    
    # 信号
    search_requested = pyqtSignal(str)  # 搜索关键词
    platform_filter_changed = pyqtSignal(str)  # 平台过滤
    clear_search = pyqtSignal()  # 清除搜索
    
    def __init__(self, parent=None):
        """
        初始化搜索栏
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 搜索标签
        search_label = QLabel("搜索:")
        layout.addWidget(search_label)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入标题关键词...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.returnPressed.connect(self._on_search)
        self.search_input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.search_input, 3)
        
        # 平台过滤
        platform_label = QLabel("平台:")
        layout.addWidget(platform_label)
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "全部",
            "ChatGPT",
            "Claude",
            "DeepSeek",
            "Kimi",
            "Gemini",
            "Tongyi",
            "Poe"
        ])
        self.platform_combo.currentTextChanged.connect(self._on_platform_changed)
        layout.addWidget(self.platform_combo, 1)
        
        # 搜索按钮
        self.search_btn = QPushButton("搜索")
        self.search_btn.clicked.connect(self._on_search)
        layout.addWidget(self.search_btn)
        
        # 清除按钮
        self.clear_btn = QPushButton("清除")
        self.clear_btn.clicked.connect(self._on_clear)
        layout.addWidget(self.clear_btn)
        
    def _on_search(self):
        """执行搜索"""
        keyword = self.search_input.text().strip()
        self.search_requested.emit(keyword)
        
    def _on_text_changed(self, text: str):
        """文本变化(实时搜索)"""
        if len(text) == 0:
            # 清空时自动搜索
            self.search_requested.emit("")
        elif len(text) >= 2:
            # 至少2个字符才触发实时搜索
            self.search_requested.emit(text)
            
    def _on_platform_changed(self, platform: str):
        """平台过滤变化"""
        if platform == "全部":
            platform = ""
        self.platform_filter_changed.emit(platform.lower())
        
    def _on_clear(self):
        """清除搜索"""
        self.search_input.clear()
        self.platform_combo.setCurrentIndex(0)
        self.clear_search.emit()
        
    def get_search_keyword(self) -> str:
        """获取搜索关键词"""
        return self.search_input.text().strip()
    
    def get_selected_platform(self) -> str:
        """获取选中的平台"""
        platform = self.platform_combo.currentText()
        if platform == "全部":
            return ""
        return platform.lower()
    
    def set_platform(self, platform: str):
        """
        设置平台过滤
        
        Args:
            platform: 平台名称
        """
        # 查找并设置
        for i in range(self.platform_combo.count()):
            if self.platform_combo.itemText(i).lower() == platform.lower():
                self.platform_combo.setCurrentIndex(i)
                break
