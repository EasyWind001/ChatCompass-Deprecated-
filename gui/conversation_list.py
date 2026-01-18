"""
ConversationList - 对话列表组件

显示对话列表的表格视图,支持搜索、过滤、排序和批量操作
"""
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QAction
from datetime import datetime


class ConversationList(QWidget):
    """对话列表组件"""
    
    # Signals
    conversation_selected = pyqtSignal(int)  # 对话选择信号 (conversation_id)
    
    def __init__(self, db, parent=None):
        """
        初始化对话列表
        
        Args:
            db: 数据库连接
            parent: 父窗口
        """
        super().__init__(parent)
        self.db = db
        self.conversations = []
        self._all_conversations = []  # 保存完整列表用于过滤
        
        self._init_ui()
        
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "标题", "平台", "时间"])
        
        # 表格设置
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)  # 启用排序
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # 右键菜单
        
        # 列宽设置
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # 连接信号
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        
        layout.addWidget(self.table)
        
    def load_conversations(self, conversations: List[Dict[str, Any]]):
        """
        加载对话列表
        
        Args:
            conversations: 对话列表
        """
        self.conversations = conversations
        self._all_conversations = conversations  # 保存完整列表
        self._display_conversations(conversations)
    
    def _display_conversations(self, conversations: List[Dict[str, Any]]):
        """
        显示对话列表
        
        Args:
            conversations: 要显示的对话列表
        """
        self.table.setSortingEnabled(False)  # 临时禁用排序
        self.table.setRowCount(len(conversations))
        
        for row, conv in enumerate(conversations):
            # ID
            id_item = QTableWidgetItem(str(conv.get('id', '')))
            id_item.setData(Qt.ItemDataRole.UserRole, conv.get('id'))
            self.table.setItem(row, 0, id_item)
            
            # 标题
            title = conv.get('title', 'Untitled')
            title_item = QTableWidgetItem(title)
            title_item.setToolTip(title)
            self.table.setItem(row, 1, title_item)
            
            # 平台
            platform = conv.get('platform', 'unknown')
            platform_item = QTableWidgetItem(platform)
            
            # 平台颜色标识
            if platform == 'chatgpt':
                platform_item.setForeground(QColor('#10a37f'))
            elif platform == 'claude':
                platform_item.setForeground(QColor('#7c3aed'))
            elif platform == 'deepseek':
                platform_item.setForeground(QColor('#0066cc'))
                
            self.table.setItem(row, 2, platform_item)
            
            # 时间
            created_at = conv.get('created_at', '')
            if created_at:
                # 格式化时间
                if 'T' in str(created_at):
                    created_at = str(created_at).split('T')[0]
                elif ' ' in str(created_at):
                    created_at = str(created_at).split(' ')[0]
                    
            time_item = QTableWidgetItem(str(created_at))
            self.table.setItem(row, 3, time_item)
            
        self.table.setSortingEnabled(True)  # 重新启用排序
            
    def _on_selection_changed(self):
        """选择变化处理"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            if 0 <= row < len(self.conversations):
                conv_id = self.conversations[row].get('id')
                if conv_id:
                    self.conversation_selected.emit(conv_id)
                    
    def get_selected_conversation(self) -> Optional[Dict[str, Any]]:
        """
        获取选中的对话
        
        Returns:
            选中的对话数据,如果没有选中则返回None
        """
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            if 0 <= row < len(self.conversations):
                return self.conversations[row]
        return None
        
    def clear(self):
        """清空列表"""
        self.conversations = []
        self._all_conversations = []
        self.table.setRowCount(0)
    
    # ========== 搜索和过滤功能 ==========
    
    def filter_by_title(self, keyword: str) -> List[Dict[str, Any]]:
        """
        按标题搜索
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的对话列表
        """
        if not keyword:
            self._display_conversations(self._all_conversations)
            return self._all_conversations
        
        keyword_lower = keyword.lower()
        filtered = [
            conv for conv in self._all_conversations
            if keyword_lower in conv.get('title', '').lower()
        ]
        
        self._display_conversations(filtered)
        return filtered
    
    def filter_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """
        按平台过滤
        
        Args:
            platform: 平台名称
            
        Returns:
            匹配的对话列表
        """
        if not platform or platform.lower() == 'all':
            self._display_conversations(self._all_conversations)
            return self._all_conversations
        
        filtered = [
            conv for conv in self._all_conversations
            if conv.get('platform', '').lower() == platform.lower()
        ]
        
        self._display_conversations(filtered)
        return filtered
    
    def filter_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        按日期范围过滤
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            匹配的对话列表
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            filtered = []
            for conv in self._all_conversations:
                created_at = conv.get('created_at', '')
                if created_at:
                    # 提取日期部分
                    date_str = str(created_at).split(' ')[0]
                    conv_date = datetime.strptime(date_str, "%Y-%m-%d")
                    
                    if start <= conv_date <= end:
                        filtered.append(conv)
            
            self._display_conversations(filtered)
            return filtered
            
        except Exception:
            return self._all_conversations
    
    # ========== 批量操作功能 ==========
    
    def enable_multi_selection(self, enabled: bool = True):
        """
        启用/禁用多选模式
        
        Args:
            enabled: 是否启用
        """
        if enabled:
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        else:
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    
    def get_selected_ids(self) -> List[int]:
        """
        获取选中的对话ID列表
        
        Returns:
            对话ID列表
        """
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        ids = []
        for row in selected_rows:
            id_item = self.table.item(row, 0)
            if id_item:
                conv_id = id_item.data(Qt.ItemDataRole.UserRole)
                if conv_id:
                    ids.append(conv_id)
        
        return ids
    
    def select_all(self):
        """全选"""
        self.table.selectAll()
    
    def clear_selection(self):
        """清除选择"""
        self.table.clearSelection()
    
    # ========== 排序功能 ==========
    
    def sort_by_column(self, column: int, order: Qt.SortOrder):
        """
        按列排序
        
        Args:
            column: 列索引
            order: 排序顺序
        """
        self.table.sortItems(column, order)
    
    # ========== 右键菜单 ==========
    
    def create_context_menu(self) -> QMenu:
        """
        创建右键菜单
        
        Returns:
            菜单对象
        """
        menu = QMenu(self)
        
        # 查看详情
        view_action = QAction("查看详情", self)
        menu.addAction(view_action)
        
        # 复制链接
        copy_action = QAction("复制链接", self)
        menu.addAction(copy_action)
        
        menu.addSeparator()
        
        # 导出
        export_action = QAction("导出", self)
        menu.addAction(export_action)
        
        # 删除
        delete_action = QAction("删除", self)
        menu.addAction(delete_action)
        
        return menu
    
    def _show_context_menu(self, position):
        """显示右键菜单"""
        # 如果有选中项才显示菜单
        if self.table.selectedItems():
            menu = self.create_context_menu()
            menu.exec(self.table.viewport().mapToGlobal(position))
