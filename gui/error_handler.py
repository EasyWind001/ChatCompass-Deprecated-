"""
错误处理与日志管理模块

统一管理GUI错误,提供:
1. 错误弹窗显示
2. 详细日志记录
3. 错误历史追踪
4. 用户友好提示
"""
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QMessageBox, QWidget

# 配置日志
logger = logging.getLogger(__name__)


class ErrorHandler:
    """统一错误处理器"""
    
    # 错误历史记录 (内存缓存最近100条)
    _error_history = []
    _max_history = 100
    
    @classmethod
    def handle_error(
        cls,
        error: Exception,
        parent: Optional[QWidget] = None,
        title: str = "错误",
        user_message: Optional[str] = None,
        show_dialog: bool = True,
        log_level: str = "error"
    ):
        """
        统一错误处理入口
        
        Args:
            error: 异常对象
            parent: 父窗口 (用于对话框)
            title: 对话框标题
            user_message: 用户友好的错误描述 (可选)
            show_dialog: 是否显示错误对话框
            log_level: 日志级别 (debug/info/warning/error/critical)
        """
        # 1. 记录详细日志 (含完整堆栈)
        error_msg = str(error)
        stack_trace = traceback.format_exc()
        
        log_func = getattr(logger, log_level, logger.error)
        log_func(
            f"错误发生: {user_message or error_msg}\n"
            f"异常类型: {type(error).__name__}\n"
            f"详细信息: {error_msg}\n"
            f"堆栈跟踪:\n{stack_trace}"
        )
        
        # 2. 保存到错误历史
        cls._add_to_history({
            'timestamp': datetime.now(),
            'type': type(error).__name__,
            'message': error_msg,
            'user_message': user_message,
            'stack_trace': stack_trace
        })
        
        # 3. 显示用户友好的错误对话框
        if show_dialog:
            cls._show_error_dialog(
                parent=parent,
                title=title,
                error=error,
                user_message=user_message,
                stack_trace=stack_trace
            )
    
    @classmethod
    def _show_error_dialog(
        cls,
        parent: Optional[QWidget],
        title: str,
        error: Exception,
        user_message: Optional[str],
        stack_trace: str
    ):
        """显示错误对话框"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        # 构建显示内容
        if user_message:
            main_text = user_message
            detailed_text = (
                f"异常类型: {error_type}\n"
                f"错误信息: {error_msg}\n\n"
                f"详细堆栈:\n{stack_trace}"
            )
        else:
            main_text = f"{error_type}: {error_msg}"
            detailed_text = f"详细堆栈:\n{stack_trace}"
        
        # 创建对话框
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(main_text)
        msg_box.setDetailedText(detailed_text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
    
    @classmethod
    def _add_to_history(cls, error_record: dict):
        """添加到错误历史"""
        cls._error_history.append(error_record)
        
        # 保持历史记录大小
        if len(cls._error_history) > cls._max_history:
            cls._error_history = cls._error_history[-cls._max_history:]
    
    @classmethod
    def get_error_history(cls, limit: Optional[int] = None):
        """获取错误历史"""
        if limit:
            return cls._error_history[-limit:]
        return cls._error_history.copy()
    
    @classmethod
    def clear_history(cls):
        """清空错误历史"""
        cls._error_history.clear()
        logger.info("错误历史已清空")
    
    @classmethod
    def export_error_log(cls, output_path: Optional[Path] = None):
        """
        导出错误日志到文件
        
        Args:
            output_path: 输出文件路径 (默认: logs/error_history_YYYYMMDD_HHMMSS.log)
        """
        if not cls._error_history:
            logger.info("没有错误历史可导出")
            return
        
        # 确定输出路径
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path("logs") / f"error_history_{timestamp}.log"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ChatCompass 错误历史导出\n")
            f.write(f"导出时间: {datetime.now()}\n")
            f.write(f"错误数量: {len(cls._error_history)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, record in enumerate(cls._error_history, 1):
                f.write(f"[错误 #{i}]\n")
                f.write(f"时间: {record['timestamp']}\n")
                f.write(f"类型: {record['type']}\n")
                f.write(f"消息: {record['message']}\n")
                if record.get('user_message'):
                    f.write(f"用户提示: {record['user_message']}\n")
                f.write(f"\n堆栈跟踪:\n{record['stack_trace']}\n")
                f.write("-" * 80 + "\n\n")
        
        logger.info(f"错误历史已导出到: {output_path}")
        return output_path


# 便捷函数
def handle_error(
    error: Exception,
    parent: Optional[QWidget] = None,
    user_message: Optional[str] = None,
    show_dialog: bool = True
):
    """
    快捷错误处理函数
    
    使用示例:
    ```python
    try:
        # 可能出错的代码
        result = risky_operation()
    except Exception as e:
        handle_error(
            e,
            parent=self,
            user_message="执行操作失败,请检查输入参数"
        )
    ```
    """
    ErrorHandler.handle_error(
        error=error,
        parent=parent,
        user_message=user_message,
        show_dialog=show_dialog
    )


def handle_warning(
    message: str,
    parent: Optional[QWidget] = None,
    title: str = "警告"
):
    """
    显示警告对话框并记录日志
    
    Args:
        message: 警告消息
        parent: 父窗口
        title: 对话框标题
    """
    logger.warning(f"警告: {message}")
    
    if parent:
        QMessageBox.warning(parent, title, message)


def handle_info(
    message: str,
    parent: Optional[QWidget] = None,
    title: str = "提示",
    show_dialog: bool = False
):
    """
    显示信息提示并记录日志
    
    Args:
        message: 提示消息
        parent: 父窗口
        title: 对话框标题
        show_dialog: 是否显示对话框
    """
    logger.info(f"提示: {message}")
    
    if show_dialog and parent:
        QMessageBox.information(parent, title, message)
