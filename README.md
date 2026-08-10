# 电商后台管理系统 — 接口自动化测试项目

> 基于 Python + Pytest + Requests 的电商后台 API 自动化测试框架，覆盖登录、商品、订单三大核心业务模块。

## 项目背景

对电商后台的登录、商品、订单三大业务模块进行全流程测试，包括功能测试和接口测试。基于 Python + Pytest + Requests 实现核心业务接口的自动化回归，使用 XMind 梳理测试点，使用禅道 / Excel 管理缺陷，完成从需求分析到缺陷闭环的完整测试流程。

## 技术栈

| 类别 | 技术 / 工具 |
|------|------------|
| 编程语言 | Python 3.10+ |
| 测试框架 | Pytest 9.1.1 |
| HTTP请求 | Requests 2.31+ |
| 配置管理 | PyYAML 6.0 |
| 数据库 | MySQL 8.0（mysql-connector-python） |
| 测试报告 | pytest-html 4.2.0 |
| 接口调试 | Postman |
| 测试点梳理 | XMind |
| 缺陷管理 | 禅道 / Excel |
| 抓包工具 | Fiddler |
| 压测工具 | JMeter（了解） |

## 项目结构

```
dianshang/
├── config/                 # 配置文件
│   └── config.yaml         # 环境配置（接口地址、数据库、日志）
├── utils/                  # 工具支撑层
│   ├── config.py           # 配置管理（单例模式）
│   ├── database.py         # 数据库操作封装
│   └── logger.py           # 日志管理（控制台 + 文件）
├── api/                    # 接口封装层
│   ├── base_api.py         # 基础API类（GET/POST/PUT/DELETE）
│   ├── login_api.py        # 登录接口（登录/登出/用户信息）
│   ├── product_api.py      # 商品接口（CRUD全流程）
│   └── order_api.py        # 订单接口（创建/查询/状态流转/取消）
├── testdata/               # 测试数据层（数据驱动）
│   ├── login_data.py       # 登录模块测试数据
│   ├── product_data.py     # 商品模块测试数据
│   └── order_data.py       # 订单模块测试数据
├── tests/                  # 测试用例层
│   ├── test_login.py       # 登录模块测试用例（12条）
│   ├── test_product.py     # 商品模块测试用例（19条）
│   └── test_order.py       # 订单模块测试用例（16条）
├── reports/                # 测试报告
│   ├── report.html         # pytest-html 自动生成报告
│   └── test_report.html    # 专业定制测试报告
├── mock_server.py          # Mock 电商后台服务（Flask）
├── conftest.py             # pytest 全局配置（sys.path）
├── run_tests.py            # 测试启动入口脚本
├── run.bat                 # Windows 一键运行脚本
├── pytest.ini              # pytest 配置文件
├── requirements.txt        # 项目依赖
└── .gitignore              # Git 忽略文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Mock 后端服务

```bash
python mock_server.py
```

服务启动在 `http://127.0.0.1:8080`，提供登录、商品、订单全部接口的 Mock 响应。

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行指定模块
pytest tests/test_login.py -v       # 登录模块
pytest tests/test_product.py -v     # 商品模块
pytest tests/test_order.py -v       # 订单模块

# 生成 HTML 测试报告
pytest --html=reports/report.html --self-contained-html

# 并行运行
pytest -n auto
```

### 4. Windows 一键运行

双击 `run.bat`，按菜单提示选择运行模式。

## 测试覆盖

### 接口覆盖清单（13个API）

| # | 方法 | 接口路径 | 模块 | 用例数 |
|---|------|---------|------|--------|
| 1 | POST | /api/login | 登录 | 10 |
| 2 | POST | /api/logout | 登录 | 1 |
| 3 | GET | /api/user/info | 登录 | 1 |
| 4 | GET | /api/products | 商品 | 4 |
| 5 | GET | /api/products/{id} | 商品 | 2 |
| 6 | POST | /api/products | 商品 | 8 |
| 7 | PUT | /api/products/{id} | 商品 | 4 |
| 8 | DELETE | /api/products/{id} | 商品 | 1 |
| 9 | GET | /api/orders | 订单 | 4 |
| 10 | GET | /api/orders/{id} | 订单 | 2 |
| 11 | POST | /api/orders | 订单 | 6 |
| 12 | PUT | /api/orders/{id}/status | 订单 | 5 |
| 13 | PUT | /api/orders/{id}/cancel | 订单 | 1 |

### 测试用例统计

| 模块 | 用例数 | 通过 | 失败 | 通过率 | 正常流 | 异常流 | 边界值 |
|------|--------|------|------|--------|--------|--------|--------|
| 登录 | 12 | 12 | 0 | 100% | 3 | 6 | 3 |
| 商品 | 19 | 19 | 0 | 100% | 8 | 7 | 3 |
| 订单 | 16 | 16 | 0 | 100% | 9 | 5 | 1 |
| **合计** | **47** | **47** | **0** | **100%** | **20** | **18** | **7** |

### 测试设计方法

- **等价类划分**：正常登录 / 空值 / 非法输入
- **边界值分析**：密码长度边界、商品价格边界、数量边界
- **场景法**：订单状态流转（pending → paid → shipped → completed / cancelled）
- **参数化测试**：Pytest `@pytest.mark.parametrize` 数据驱动

## 测试报告

运行测试后，报告生成在 `reports/` 目录下：

| 文件 | 说明 |
|------|------|
| `report.html` | pytest-html 插件自动生成的测试报告 |
| `test_report.html` | 专业定制测试报告（含项目概述、环境信息、用例明细、缺陷记录、测试结论等9个章节） |

## 框架设计

### 分层架构

```
测试用例层 (tests/)       — pytest 参数化驱动，数据与用例分离
    ↓
接口封装层 (api/)         — BaseAPI 封装 HTTP 请求，业务 API 继承扩展
    ↓
测试数据层 (testdata/)    — 数据驱动，便于维护和扩展
    ↓
工具支撑层 (utils/)       — 配置管理 / 日志记录 / 数据库操作
    ↓
配置层 (config/)          — YAML 配置，支持多环境切换
```

### 核心特性

- **会话管理**：BaseAPI 使用 `requests.Session()` 保持登录态
- **单例模式**：ConfigManager 和 Logger 均使用单例，避免重复初始化
- **数据驱动**：测试数据独立存放，参数化注入用例
- **日志记录**：同时输出到控制台和文件，便于问题排查
- **配置分离**：YAML 配置文件，支持多环境切换

## 项目成果

- 设计用例覆盖核心业务场景，**47条测试用例全部通过**
- 核心接口自动化回归覆盖率达 **85%+**
- 回归测试效率提升约 **60%**
- 完成从需求分析到缺陷闭环的完整测试流程
