@echo off
chcp 65001 >nul
echo ============================================
echo   电商后台管理系统测试项目 - 运行脚本
echo ============================================
echo.

cd /d "%~dp0"

set PYTHONPATH=%~dp0;%~dp0lib

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)
echo Python环境 OK
echo.

echo [2/3] 检查依赖...
python -c "import sys; sys.path.insert(0, r'%~dp0lib'); import pytest; import requests; import yaml; print('所有依赖已安装 OK')"
if errorlevel 1 (
    echo 正在安装依赖到lib目录...
    pip install --target "%~dp0lib" pytest requests PyYAML pytest-html pytest-metadata pytest-xdist faker mysql-connector-python
)
echo.

echo [3/3] 运行测试用例...
echo.
echo 选择运行模式:
echo   1 - 运行登录模块测试
echo   2 - 运行商品模块测试
echo   3 - 运行订单模块测试
echo   4 - 运行所有测试
echo   5 - 仅收集测试用例（不执行）
echo   6 - 运行所有测试并生成HTML报告
echo.
set /p choice="请输入选项 (1-6): "

if "%choice%"=="1" (
    python "%~dp0run_tests.py" "%~dp0tests\test_login.py" -v
) else if "%choice%"=="2" (
    python "%~dp0run_tests.py" "%~dp0tests\test_product.py" -v
) else if "%choice%"=="3" (
    python "%~dp0run_tests.py" "%~dp0tests\test_order.py" -v
) else if "%choice%"=="4" (
    python "%~dp0run_tests.py" "%~dp0tests" -v
) else if "%choice%"=="5" (
    python "%~dp0run_tests.py" "%~dp0tests" -v --collect-only
) else if "%choice%"=="6" (
    if not exist "%~dp0reports" mkdir "%~dp0reports"
    python "%~dp0run_tests.py" "%~dp0tests" -v --html="%~dp0reports\report.html" --self-contained-html
) else (
    echo 无效选项
)

echo.
echo 测试运行完成！按任意键退出...
pause >nul
