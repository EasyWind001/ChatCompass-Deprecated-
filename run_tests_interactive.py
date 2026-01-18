"""
交互式测试快速启动脚本

用法:
1. 基础用法 (单元测试 + 集成测试):
   python run_tests_interactive.py

2. 测试特定模块:
   python run_tests_interactive.py tests/unit/test_db_manager.py

3. 测试特定目录:
   python run_tests_interactive.py tests/gui

4. 测试多个目标:
   python run_tests_interactive.py tests/unit tests/integration

5. 不停止模式 (一次运行完):
   python run_tests_interactive.py --no-stop

6. 快速模式 (只运行unit和integration):
   python run_tests_interactive.py --quick
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from tests.interactive_test_runner import main

if __name__ == "__main__":
    main()
