# AGENTS.md — Python / Agent 开发预提示词

> 本文件供 AI 编码助手（opencode、Claude Code、Cursor 等）自动读取，用于在协作前了解项目背景、环境与约定。**始终用简体中文交流与回复。**

---

## 1. 项目定位

这是一个 **Python 学习 + AI Agent 开发** 的个人项目，主要内容：

- `preSrc/`：Python 基础语法学习（已完成，作为参考）
- `src/python_study/modules/`：各类模块与库的实战 demo
- 逐步演进为基于 **LangChain** 的 Agent 应用开发项目

## 2. 作者背景与当前阶段

- 10 年 **前端** 开发经验（JavaScript / TypeScript），熟悉 Web 开发、HTTP、异步编程、SSE 流式处理。
- Python 基础语法已基本掌握（数据类型、控制流、函数、OOP、异常、模块等）。
- **当前阶段目标：使用 LangChain 进行 Agent 项目开发**，从搭建调用链开始，逐步实现具备工具调用（function calling）能力的 Agent。
- 学习节奏：基础与框架两手抓，遇到不熟悉的 Python 语法/内置模块时，先补基础再看框架用法。

## 3. 硬件与软件环境

### 硬件
- Intel Core i5-5257U @ 2.70GHz，4 核，8GB 内存（性能有限，避免在本地跑重型模型）
- macOS 12.7.6 (Monterey)，zsh

### 软件
- **Python 3.12**（`.python-version` 锁定 3.12，`.venv` 虚拟环境已存在）
- **uv 0.12.0** 作为唯一包管理工具（存在 `uv.lock`），**禁止直接使用 pip**
- 已安装依赖：`aiohttp`、`chardet`、`numpy`、`pillow`、`psutil`、`python-dotenv`、`requests`；dev 组：`watchdog`
- 已有 `demo.db`（SQLite 数据库，sqlite3 demo 产物）

### 网络
- 无全局代理，访问外网（GitHub、PyPI 之外的境外资源）需走本地代理 `http://127.0.0.1:7897`
- 阿里云百炼 DashScope 接口在国内，无需代理

### API 密钥
- `DASHSCOPE_API_KEY` 存于 `.env`（阿里云百炼，支持 Qwen 系列模型）
- 通过 `python-dotenv` 的 `load_dotenv()` 加载，**不要硬编码、不要提交具体密钥**

## 4. 项目结构导览

```
python-study/
├── preSrc/                          # 基础语法学习（已学完，可参考）
│   ├── data_types_demo.py
│   ├── control_flow_demo.py
│   ├── functions_demo.py
│   ├── oop_demo/                    # OOP 系列：继承/封装/魔术方法等
│   └── my_module/                   # 自定义模块示例
├── src/python_study/
│   ├── __init__.py                  # main() 入口，逐行取消注释可运行对应 demo
│   ├── dev.py                       # watchdog 热重载开发模式
│   ├── utils/                       # 路径辅助函数
│   │   └── getProjectPath() / getAssetsPath()
│   ├── assets/                      # demo 用图片等资源
│   └── modules/
│       ├── LLMDemos/                # LLM 相关
│       │   ├── SSEDemo.py           # SSE 流式接收 demo
│       │   └── qwenDemo.py          # DashScope Qwen 流式对话 demo
│       ├── bulitModuleDemos/        # Python 内建模块（asyncio/collections/process 等 11 个）
│       └── thirdModuleDemos/        # 第三方库（requests/psutil/sqlite3/pillow/chardet）
├── pyproject.toml                   # 依赖与项目配置（uv）
├── uv.lock                          # uv 锁文件
├── .python-version                  # Python 版本锁定
└── .env                             # API 密钥（不入库）
```

## 5. 命令速查

```bash
uv sync                 # 按 pyproject.toml 安装/同步依赖
uv add <pkg>            # 添加依赖并更新锁文件
uv remove <pkg>         # 移除依赖
uv run start            # 运行主入口（python_study:main）
uv run dev              # 热重载模式：监听 .py 变更自动重启 start
.venv/bin/python xxx.py # 直接用虚拟环境 Python 运行脚本
```

## 6. 工作约定

1. **依赖管理**：新增/升级依赖一律 `uv add`，不直接改 pyproject.toml 手写、不用 pip。
2. **密钥安全**：所有密钥只放 `.env`，通过 `load_dotenv()` + `os.getenv()` 读取，禁止硬编码、禁止写入任何会入库的文件。
3. **demo 组织**：新增示例沿用现有命名 `XxxDemo.py`，内含 `main()` 函数；在 `src/python_study/__init__.py` 中导入并预留调用注释。demo 文件与模块放在对应分类目录（built / third / LLM）下。
4. **代码风格**：与现有 demo 保持一致——使用 `typing.TypedDict`/类型标注、中文 print 输出便于阅读；导包顺序标准库 → 第三方 → 本地。
5. **热重载注意**：`uv run dev` 会监听 `src/` 下 `.py` 变更，调试时避免循环触发。
6. **测试**：当前为学习型项目，无自动化测试框架；新代码至少保证 `uv run start` 能正常编译运行。

## 7. 学习路线（当前：LangChain Agent 开发）

按顺序推进，每步产出可运行的 demo 并入库：

1. **LangChain 接入 Qwen**：使用 `langchain-openai`（DashScope 兼容 OpenAI 协议，`base_url` 指向 compatible-mode 接口）接入 `qwen-plus`，实现 ChatModel 基础对话与流式输出。
2. **Prompts & Output Parsers**：PromptTemplate、消息模板、结构化输出解析（Pydantic）。
3. **Chains & LCEL**：可组合链（Runnable），串联 Prompt → Model → Parser。
4. **Tools & Function Calling**：定义工具（注意 DashScope 需开启 `enable_thinking` / 工具参数），让模型调用本地函数（如时间、文件、数据库查询）。
5. **Agents & 循环**：AgentExecutor / ReAct 循环，实现多步工具编排。
6. **进阶方向**（视兴趣选择）：RAG（向量检索）、记忆（Memory）、多 Agent 协作。

> 模型与接口以现有 `qwenDemo.py` 为基准对接；新增 langchain 系列依赖按需 `uv add langchain langchain-openai`。

## 8. 前端背景迁移点（供参考）

| 前端概念 | Python 对应 |
|---------|------------|
| `async/await` | `asyncio` + `async def` / `await`，`asyncio.run()` 启动 |
| 事件循环 / EventEmitter | `asyncio` 事件循环、`aiohttp` 流式读取 |
| SSE / `EventSource` | 逐行解析 `data:` 前缀（见 `SSEDemo.py`） |
| `fetch` / `axios` | `aiohttp`（异步）/ `requests`（同步） |
| TS 类型 / interface | `typing.TypedDict`、`dataclass`、Pydantic（LangChain 中常用） |
| `npm` / `yarn` | `uv` |
| JSON 处理 | `json` 模块 |

---

*本文档随项目演进持续更新：环境变更、新阶段目标、约定调整都应及时同步到这里。*
