"""
错误查看器对话框

显示应用程序的错误历史,支持:
1. 查看错误详情
2. 复制错误信息
3. 导出错误日志
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QTextEdit, QLabel, QSplitter,
    QListWidgetItem, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from datetime import datetime

from gui.error_handler import ErrorHandler


class ErrorViewerDialog(QDialog):
    """错误查看器对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("错误历史")
        self.resize(800, 600)
        
        self._init_ui()
        self._load_errors()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 顶部信息
        info_layout = QHBoxLayout()
        self.count_label = QLabel("错误数量: 0")
        info_layout.addWidget(self.count_label)
        info_layout.addStretch()
        
        # 按钮组
        btn_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self._load_errors)
        btn_layout.addWidget(self.refresh_btn)
        
        self.export_btn = QPushButton("导出日志")
        self.export_btn.clicked.connect(self._export_log)
        btn_layout.addWidget(self.export_btn)
        
        self.clear_btn = QPushButton("清空历史")
        self.clear_btn.clicked.connect(self._clear_history)
        btn_layout.addWidget(self.clear_btn)
        
        info_layout.addLayout(btn_layout)
        layout.addLayout(info_layout)
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧: 错误列表
        self.error_list = QListWidget()
        self.error_list.currentItemChanged.connect(self._on_error_selected)
        splitter.addWidget(self.error_list)
        
        # 右侧: 错误详情
        detail_widget = QVBoxLayout()
        detail_label = QLabel("错误详情:")
        detail_widget.addWidget(detail_label)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setPlaceholderText("选择左侧错误查看详细信息")
        detail_widget.addWidget(self.detail_text)
        
        # 复制按钮
        copy_btn = QPushButton("复制详情")
        copy_btn.clicked.connect(self._copy_detail)
        detail_widget.addWidget(copy_btn)
        
        # 创建右侧容器
        from PyQt6.QtWidgets import QWidget
        right_widget = QWidget()
        right_widget.setLayout(detail_widget)
        splitter.addWidget(right_widget)
        
        splitter.setSizes([300, 500])
        layout.addWidget(splitter)
        
        # 底部按钮
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        bottom_layout.addWidget(close_btn)
        
        layout.addLayout(bottom_layout)
    
    def _load_errors(self):
        """加载错误历史"""
        self.error_list.clear()
        self.detail_text.clear()
        
        errors = ErrorHandler.get_error_history()
        self.count_label.setText(f"错误数量: {len(errors)}")
        
        if not errors:
            self.detail_text.setPlaceholderText("暂无错误记录")
            return
        
        # 倒序显示 (最新的在前)
        for error in reversed(errors):
            timestamp = error['timestamp'].strftime("%H:%M:%S")
            error_type = error['type']
            message = error['message'][:50]  # 截断显示
            
            item_text = f"[{timestamp}] {error_type}: {message}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, error)
            self.error_list.addItem(item)
    
    def _on_error_selected(self, current, previous):
        """错误选中处理"""
        if not current:
            self.detail_text.clear()
            return
        
        error = current.data(Qt.ItemDataRole.UserRole)
        
        # 格式化显示
        detail = f"""时间: {error['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
类型: {error['type']}
消息: {error['message']}
"""
        
        if error.get('user_message'):
            detail += f"\n用户提示: {error['user_message']}\n"
        
        detail += f"\n详细堆栈:\n{'-' * 60}\n{error['stack_trace']}"
        
        self.detail_text.setPlainText(detail)
    
    def _copy_detail(self):
        """复制错误详情"""
        text = self.detail_text.toPlainText()
        if text:
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "成功", "错误详情已复制到剪贴板")
    
    def _export_log(self):
        """导出错误日志"""
        errors = ErrorHandler.get_error_history()
        if not errors:
            QMessageBox.information(self, "提示", "暂无错误记录可导出")
            return
        
        # 选择保存位置
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出错误日志",
            f"error_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
            "日志文件 (*.log);;所有文件 (*)"
        )
        
        if filename:
            try:
                output_path = ErrorHandler.export_error_log(filename)
                QMessageBox.information(
                    self,
                    "成功",
                    f"错误日志已导出到:\n{output_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "错误",
                    f"导出失败: {str(e)}"
                )
    
    def _clear_history(self):
        """清空错误历史"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有错误历史记录吗?\n\n此操作不可恢复!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            ErrorHandler.clear_history()
            self._load_errors()
            QMessageBox.information(self, "成功", "错误历史已清空")
