"""
ChatCompass GUI Launcher

图形界面启动器
"""
import sys
import os
import logging
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


def setup_logging():
    """配置日志系统"""
    # 确保logs目录存在
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志文件名 (按日期分割)
    log_file = log_dir / f"chatcompass_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # 文件处理器 - 记录所有级别
            logging.FileHandler(log_file, encoding='utf-8'),
            # 控制台处理器 - 只显示WARNING及以上
            logging.StreamHandler()
        ]
    )
    
    # 设置控制台处理器的级别
    logging.getLogger().handlers[1].setLevel(logging.WARNING)
    
    logging.info("=" * 60)
    logging.info("ChatCompass GUI 启动")
    logging.info(f"日志文件: {log_file}")
    logging.info("=" * 60)


def main():
    """主函数"""
    # 配置日志
    setup_logging()
    
    try:
        # 启用高DPI缩放
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        # 创建应用
        app = QApplication(sys.argv)
        app.setApplicationName("ChatCompass")
        app.setOrganizationName("ChatCompass Team")
        
        # 导入主窗口 (延迟导入,避免日志配置前导入)
        from gui.main_window import MainWindow
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        logging.info("主窗口已显示")
        
        # 运行应用
        sys.exit(app.exec())
        
    except Exception as e:
        logging.critical(f"应用启动失败: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
