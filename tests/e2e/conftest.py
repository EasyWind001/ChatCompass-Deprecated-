"""E2E测试配置和fixtures"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from database.db_manager import DatabaseManager


@pytest.fixture(scope="function")
def temp_db():
    """创建临时测试数据库"""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_chat.db")
    
    db = DatabaseManager(db_path)
    # DatabaseManager在__init__中已自动初始化数据库
    
    yield db
    
    # 清理
    db.close()
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="function")
def qapp():
    """创建QApplication实例用于GUI测试"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # 不关闭app,因为可能被其他测试使用


@pytest.fixture
def mock_conversation():
    """Mock对话数据"""
    return {
        'id': 1,
        'title': 'Test Conversation',
        'source_url': 'https://chatgpt.com/share/test-123',
        'platform': 'chatgpt',
        'summary': 'This is a test conversation about Python',
        'category': 'Programming',
        'word_count': 150,
        'message_count': 5,
        'raw_content': {'messages': [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]},
        'created_at': '2026-01-17 10:00:00',
        'updated_at': '2026-01-17 10:00:00'
    }


@pytest.fixture
def sample_conversations():
    """多个测试对话数据"""
    return [
        {
            'source_url': f'https://chatgpt.com/share/test-{i}',
            'platform': 'chatgpt' if i % 2 == 0 else 'claude',
            'title': f'Conversation {i}',
            'summary': f'Summary {i}',
            'category': 'Programming' if i % 2 == 0 else 'Writing',
            'raw_content': f'[{{"role": "user", "content": "Test {i}"}}]',
            'word_count': 100 + i * 10,
            'message_count': 3 + i
        }
        for i in range(1, 6)
    ]


def wait_for_condition(condition, timeout=5000, interval=100):
    """
    等待条件满足
    
    Args:
        condition: 返回bool的函数
        timeout: 超时时间(ms)
        interval: 检查间隔(ms)
    
    Returns:
        bool: 条件是否满足
    """
    import time
    elapsed = 0
    while elapsed < timeout:
        if condition():
            return True
        QApplication.processEvents()
        time.sleep(interval / 1000)
        elapsed += interval
    return False
