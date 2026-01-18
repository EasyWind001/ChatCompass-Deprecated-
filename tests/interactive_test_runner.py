"""
交互式测试运行器 - 带错误暂停和查看功能

特性:
1. 逐个运行测试用例
2. 发现错误立即暂停
3. 显示错误详情和历史
4. 等待用户确认修复后继续
5. 生成详细的测试报告
"""
import sys
import io
from pathlib import Path
from datetime import datetime
import pytest
import traceback
from typing import List, Dict, Any

# 设置UTF-8输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from gui.error_handler import ErrorHandler


class InteractiveTestRunner:
    """交互式测试运行器"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
        self.error_details = []
        self.start_time = None
        
    def print_header(self):
        """打印头部"""
        print("\n" + "=" * 80)
        print("🧪 ChatCompass 交互式测试运行器")
        print("=" * 80)
        print("\n📋 测试策略:")
        print("  1. 逐个运行测试用例")
        print("  2. 发现错误立即暂停")
        print("  3. 显示详细错误信息")
        print("  4. 等待确认后继续")
        print("\n" + "=" * 80 + "\n")
    
    def print_separator(self, char="-", length=80):
        """打印分隔线"""
        print(char * length)
    
    def display_error_details(self, test_name: str, error_info: Dict[str, Any]):
        """显示错误详细信息"""
        print("\n" + "🔴" * 40)
        print(f"\n❌ 测试失败: {test_name}\n")
        self.print_separator()
        
        # 错误类型和消息
        print(f"\n📛 错误类型: {error_info['type']}")
        print(f"💬 错误消息: {error_info['message']}\n")
        
        # 完整堆栈
        print("📚 完整堆栈跟踪:")
        self.print_separator()
        print(error_info['traceback'])
        self.print_separator()
        
        # 保存到错误历史
        self.error_details.append({
            'test_name': test_name,
            'timestamp': datetime.now(),
            'error_info': error_info
        })
        
        print("\n💡 建议:")
        print("  1. 复制上述错误信息")
        print("  2. 检查代码定位问题")
        print("  3. 修复错误")
        print("  4. 继续运行测试")
        print("\n" + "🔴" * 40 + "\n")
    
    def check_error_history(self):
        """检查错误处理器的历史"""
        history = ErrorHandler.get_error_history()
        if history:
            print(f"\n⚠️  发现 {len(history)} 个应用层错误:")
            for i, error in enumerate(history[-3:], 1):  # 只显示最近3个
                print(f"  {i}. [{error['timestamp'].strftime('%H:%M:%S')}] "
                      f"{error['type']}: {error['message'][:50]}")
            print("\n💡 提示: 使用 GUI 的 '帮助→查看错误日志' 查看完整历史\n")
    
    def wait_for_confirmation(self):
        """等待用户确认"""
        self.print_separator("=")
        print("\n⏸️  测试已暂停! 请选择:")
        print("  [c] 继续下一个测试")
        print("  [r] 重新运行当前测试")
        print("  [s] 跳过剩余测试")
        print("  [v] 查看错误历史")
        print("  [e] 导出错误日志")
        print("  [q] 退出测试")
        
        while True:
            choice = input("\n👉 请选择 [c/r/s/v/e/q]: ").strip().lower()
            
            if choice == 'c':
                print("\n✅ 继续下一个测试...\n")
                return 'continue'
            elif choice == 'r':
                print("\n🔄 重新运行当前测试...\n")
                return 'retry'
            elif choice == 's':
                print("\n⏭️  跳过剩余测试...\n")
                return 'skip'
            elif choice == 'v':
                self.show_error_summary()
            elif choice == 'e':
                self.export_error_log()
            elif choice == 'q':
                print("\n🛑 退出测试运行器\n")
                return 'quit'
            else:
                print("❌ 无效选择,请重新输入")
    
    def show_error_summary(self):
        """显示错误摘要"""
        if not self.error_details:
            print("\n✅ 暂无测试错误记录\n")
            return
        
        print("\n" + "=" * 80)
        print(f"📊 错误摘要 (共 {len(self.error_details)} 个)")
        print("=" * 80 + "\n")
        
        for i, error in enumerate(self.error_details, 1):
            print(f"[{i}] {error['test_name']}")
            print(f"    时间: {error['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    类型: {error['error_info']['type']}")
            print(f"    消息: {error['error_info']['message'][:60]}")
            print()
    
    def export_error_log(self):
        """导出测试错误日志"""
        if not self.error_details:
            print("\n✅ 暂无错误可导出\n")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Path("logs") / f"test_errors_{timestamp}.log"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ChatCompass 测试错误日志\n")
            f.write(f"生成时间: {datetime.now()}\n")
            f.write(f"错误数量: {len(self.error_details)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, error in enumerate(self.error_details, 1):
                f.write(f"[错误 #{i}]\n")
                f.write(f"测试用例: {error['test_name']}\n")
                f.write(f"时间: {error['timestamp']}\n")
                f.write(f"类型: {error['error_info']['type']}\n")
                f.write(f"消息: {error['error_info']['message']}\n")
                f.write(f"\n堆栈跟踪:\n{error['error_info']['traceback']}\n")
                f.write("-" * 80 + "\n\n")
        
        print(f"\n✅ 错误日志已导出到: {log_file}\n")
    
    def print_summary(self):
        """打印测试摘要"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print("\n" + "=" * 80)
        print("📊 测试完成总结")
        print("=" * 80)
        print(f"\n⏱️  耗时: {duration:.2f}秒")
        print(f"📝 总计: {self.total_tests} 个测试")
        print(f"✅ 通过: {self.passed_tests} 个")
        print(f"❌ 失败: {self.failed_tests} 个")
        print(f"⏭️  跳过: {self.skipped_tests} 个")
        
        if self.failed_tests > 0:
            print(f"\n❌ 失败率: {self.failed_tests/self.total_tests*100:.1f}%")
            print("\n🔍 失败的测试:")
            for error in self.error_details:
                print(f"  • {error['test_name']}")
        else:
            print("\n🎉 所有测试通过!")
        
        print("\n" + "=" * 80 + "\n")
    
    def run_test_file(self, test_file: Path, stop_on_first: bool = True):
        """
        运行单个测试文件
        
        Args:
            test_file: 测试文件路径
            stop_on_first: 遇到第一个错误就停止
        """
        print(f"\n🧪 测试文件: {test_file.name}")
        self.print_separator()
        
        # 清空错误历史
        ErrorHandler.clear_history()
        
        # 使用pytest运行测试
        class TestPlugin:
            def __init__(self, runner):
                self.runner = runner
                self.current_test = None
            
            def pytest_runtest_call(self, item):
                self.current_test = item.nodeid
            
            def pytest_runtest_logreport(self, report):
                if report.when == 'call':
                    self.runner.total_tests += 1
                    
                    if report.passed:
                        self.runner.passed_tests += 1
                        print(f"  ✅ {report.nodeid.split('::')[-1]}")
                    
                    elif report.failed:
                        self.runner.failed_tests += 1
                        test_name = report.nodeid.split('::')[-1]
                        
                        # 提取错误信息
                        error_info = {
                            'type': report.longrepr.reprcrash.message.split(':')[0] if hasattr(report.longrepr, 'reprcrash') else 'AssertionError',
                            'message': str(report.longrepr.reprcrash.message) if hasattr(report.longrepr, 'reprcrash') else str(report.longrepr),
                            'traceback': str(report.longrepr)
                        }
                        
                        # 显示错误详情
                        self.runner.display_error_details(test_name, error_info)
                        
                        # 检查应用层错误
                        self.runner.check_error_history()
                        
                        # 等待用户确认
                        if stop_on_first:
                            action = self.runner.wait_for_confirmation()
                            
                            if action == 'quit':
                                pytest.exit("用户退出测试")
                            elif action == 'skip':
                                pytest.exit("用户跳过剩余测试")
                            elif action == 'retry':
                                # TODO: 实现重试逻辑
                                print("⚠️  重试功能待实现,继续下一个测试")
                    
                    elif report.skipped:
                        self.runner.skipped_tests += 1
                        print(f"  ⏭️  {report.nodeid.split('::')[-1]} (已跳过)")
        
        plugin = TestPlugin(self)
        pytest.main([str(test_file), '-v', '--tb=short'], plugins=[plugin])
    
    def run(self, test_paths: List[str] = None, stop_on_first: bool = True):
        """
        运行测试套件
        
        Args:
            test_paths: 测试路径列表 (文件或目录)
            stop_on_first: 遇到第一个错误就停止
        """
        self.start_time = datetime.now()
        self.print_header()
        
        # 默认测试路径
        if not test_paths:
            test_paths = [
                'tests/unit',           # 单元测试
                'tests/integration',    # 集成测试
                'tests/gui',           # GUI测试
                'tests/e2e'            # E2E测试
            ]
        
        # 收集测试文件
        test_files = []
        for path_str in test_paths:
            path = Path(path_str)
            
            # 如果是pytest node格式 (如 tests/unit/test_db.py::TestClass::test_method)
            if '::' in path_str:
                # 提取文件路径部分
                file_path = Path(path_str.split('::')[0])
                if file_path.exists():
                    test_files.append(file_path)
                continue
            
            if path.is_file():
                test_files.append(path)
            elif path.is_dir():
                test_files.extend(sorted(path.glob('test_*.py')))
        
        if not test_files:
            print("❌ 未找到测试文件")
            return
        
        print(f"📁 找到 {len(test_files)} 个测试文件\n")
        
        # 逐个运行测试文件
        for i, test_file in enumerate(test_files, 1):
            print(f"\n{'='*80}")
            # 安全地显示相对路径
            try:
                rel_path = test_file.relative_to(Path.cwd())
            except ValueError:
                rel_path = test_file.name
            print(f"📦 [{i}/{len(test_files)}] 测试模块: {rel_path}")
            print(f"{'='*80}")
            
            try:
                self.run_test_file(test_file, stop_on_first)
            except pytest.ExitCode as e:
                if "用户退出" in str(e):
                    break
                elif "用户跳过" in str(e):
                    continue
        
        # 打印总结
        self.print_summary()
        
        # 如果有错误,询问是否导出
        if self.error_details:
            choice = input("\n💾 是否导出错误日志? [y/n]: ").strip().lower()
            if choice == 'y':
                self.export_error_log()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ChatCompass 交互式测试运行器')
    parser.add_argument(
        'paths',
        nargs='*',
        help='测试文件或目录路径 (默认: tests/unit tests/integration tests/gui)'
    )
    parser.add_argument(
        '--no-stop',
        action='store_true',
        help='不在错误时停止,运行所有测试'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速模式: 只运行单元测试和集成测试'
    )
    
    args = parser.parse_args()
    
    # 快速模式
    if args.quick:
        test_paths = ['tests/unit', 'tests/integration']
    else:
        test_paths = args.paths if args.paths else None
    
    # 运行测试
    runner = InteractiveTestRunner()
    runner.run(test_paths, stop_on_first=not args.no_stop)


if __name__ == "__main__":
    main()
