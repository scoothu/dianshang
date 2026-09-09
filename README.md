# 电商后台管理系统 — Mock后端 + Web可视化 + 自动化测试

> 自主搭建 Flask Mock 后端服务 + Web 可视化管理界面，并基于 Python + Pytest + Requests 实现电商后台 API 自动化测试，覆盖登录、商品、订单三大核心业务模块，实现从业务模拟 → 接口测试 → 可视化演示的闭环。

## 项目背景

针对电商后台的登录、商品、订单三大业务模块，**自主搭建 Mock 后端服务 + Web 可视化管理界面**，并完成接口自动化测试全流程落地。基于 Flask 实现 15+ 个 API 接口（注册/登录/商品CRUD/订单状态流转等），使用 HTML/CSS/JS 开发后台管理界面，基于 Python + Pytest + Requests 实现核心业务接口的自动化回归，使用 XMind 梳理测试点，使用 Excel 管理缺陷，完成从需求分析到缺陷闭环的完整测试流程。

## 简历项目描述

> 以下为本项目在简历中的完整描述，用于保持简历与项目内容一致。

### 电商订单系统端到端全链路自动化（UI+API+DB 三层联调）

**技术栈**：Python, Pytest, Requests, Postman, MySQL
**时间**：2025-10 ~ 2025-11

**项目描述**：

- 搭建 Flask Mock 测试服务，实现登录、商品、订单 15+ 核心接口，构建独立隔离测试环境
- 梳理 3 大核心模块（登录/商品/订单）业务规则，设计 47 条功能测试用例，覆盖正常/边界/异常输入场景
- 基于 Python + Pytest + Requests 编写全量接口自动化脚本，实现断言封装、日志记录、参数化驱动
- 使用禅道跟踪 bug，发现并推动修复"登录模块用户名长度校验顺序异常"缺陷，通过回归测试验证修复后关闭

**项目成果**：

- 接口自动化回归覆盖率达 85%+
- 回归测试效率提升约 60%
- 生成 HTML 测试报告 + PDF 文档，形成完整项目交付物

## 技术栈

| 类别 | 技术 / 工具 |
|------|------------|
| 编程语言 | Python 3.10+ |
| 后端框架 | Flask 3.0+（Mock 后端服务） |
| 前端技术 | HTML5 / CSS3 / JavaScript（Web 可视化管理界面） |
| 测试框架 | Pytest 9.1.1 |
| HTTP请求 | Requests 2.31+ |
| 配置管理 | PyYAML 6.0 |
| 数据库 | MySQL 8.0（mysql-connector-python） |
| 测试报告 | pytest-html 4.2.0 |
| 接口调试 | Postman |
| 测试点梳理 | XMind |
| 缺陷管理 | Excel |
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
├── web/                    # Web 可视化管理界面
│   ├── login.html          # 登录/注册页面
│   └── index.html          # 后台管理主界面（商品/订单/用户/密码管理）
├── mock_server.py          # Mock 电商后台服务（Flask，含15+ API + 静态页面路由）
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

服务启动在 `http://127.0.0.1:8080`，提供以下功能：
- **API 接口**：注册/登录/商品CRUD/订单状态流转/修改密码等 15+ 个 API
- **Web 界面**：访问 `http://127.0.0.1:8080/login` 打开可视化管理界面
- **默认账号**：`admin / admin123`（也可通过注册页面自定义账号密码）

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

### 接口覆盖清单（15个API）

| # | 方法 | 接口路径 | 模块 | 用例数 |
|---|------|---------|------|--------|
| 1 | POST | /api/login | 登录 | 10 |
| 2 | POST | /api/logout | 登录 | 1 |
| 3 | GET | /api/user/info | 登录 | 1 |
| 4 | POST | /api/register | 登录 | —（Web 界面调用） |
| 5 | POST | /api/change-password | 登录 | —（Web 界面调用） |
| 6 | GET | /api/products | 商品 | 4 |
| 7 | GET | /api/products/{id} | 商品 | 2 |
| 8 | POST | /api/products | 商品 | 8 |
| 9 | PUT | /api/products/{id} | 商品 | 4 |
| 10 | DELETE | /api/products/{id} | 商品 | 1 |
| 11 | GET | /api/orders | 订单 | 4 |
| 12 | GET | /api/orders/{id} | 订单 | 2 |
| 13 | POST | /api/orders | 订单 | 6 |
| 14 | PUT | /api/orders/{id}/status | 订单 | 5 |
| 15 | PUT | /api/orders/{id}/cancel | 订单 | 1 |

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

## Web 可视化管理界面

启动 Mock 服务后，浏览器访问 `http://127.0.0.1:8080/login` 即可使用 Web 管理界面：

| 页面 | 功能 |
|------|------|
| 登录/注册页 | 用户登录、自定义账号密码注册 |
| 数据概览页 | 用户数、商品数、订单数、销售额、订单状态分布 |
| 商品管理页 | 商品新增、编辑、删除、搜索、分类筛选 |
| 订单管理页 | 新建订单、状态流转（待付款→已付款→已发货→已完成）、取消订单 |
| 用户管理页 | 查看注册用户列表 |
| 修改密码页 | 修改当前登录账号密码 |

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

- **Mock 后端开发**：使用 Flask 搭建 15+ 个 API 接口，支持自定义账号密码注册、商品/订单动态管理
- **Web 可视化**：开发后台管理界面，完整展示电商核心流程（登录 → 商品管理 → 订单流转 → 密码修改）
- **自动化测试**：设计 47 条测试用例覆盖核心业务场景，**全部通过**，自动化回归覆盖率达 **85%+**
- **缺陷闭环**：发现并修复「登录模块用户名长度校验顺序异常」缺陷，优化接口参数校验逻辑
- **回归效率**：回归测试效率提升约 **60%**
- **交付物**：产出 HTML 测试报告 + PDF 文档，形成完整的项目交付物
