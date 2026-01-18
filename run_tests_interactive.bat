@echo off
REM ChatCompass 交互式测试运行器 - Windows批处理脚本
REM
REM 用法示例:
REM   run_tests_interactive.bat                    - 运行默认测试
REM   run_tests_interactive.bat --quick            - 快速模式
REM   run_tests_interactive.bat tests/unit         - 测试特定目录
REM   run_tests_interactive.bat --no-stop          - 不暂停模式

echo.
echo ========================================
echo ChatCompass 交互式测试运行器
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    echo 请先安装Python 3.9+
    pause
    exit /b 1
)

REM 运行测试
python run_tests_interactive.py %*

REM 暂停以便查看结果
if not "%1"=="--no-pause" (
    echo.
    pause
)
