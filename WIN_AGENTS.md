# AGENT.md

> 本文件用于为 AI 编程代理（opencode 等）提供本仓库的工作上下文。进入本仓库工作时，请先阅读本文件。

## 项目定位

这是一个**个人学习仓库**，目标是从 Python 基础出发，最终转向 **AI Agent 开发**。
它不是生产项目，但代码应保持干净、规范、可运行，因为每一行都是学习记录。

- 包名：`python_study`（pyproject 中 name 为 `python-study`）
- Python：3.12（`requires-python = ">=3.12"`），由 **uv** 管理（存在 `uv.lock`、`.python-version`）
- 构建后端：`uv_build`（src layout）

## 硬件与软件环境

- 操作系统：Windows 10 Pro 22H2（19045）
- 终端：**Git Bash**（位于 `D:\Program Files\Git\bin\bash.exe`）——**所有命令请给 Bash/POSIX 写法**，不是 PowerShell
- CPU：Intel i5-14600KF（14C20T）；内存：32GB；C 盘剩余约 91GB
- GPU：NVIDIA GeForce RTX 5060 Ti **16GB 显存**，CUDA 13.3（可本地跑中小模型）
- 已安装：Git 2.55（`D:\Program Files\Git`）、uv 0.12.3
- Python：3.12.13，由 uv 管理，`python` 与 `python3.12` 命令均可用

## 常用命令

在仓库根目录执行：

```bash
uv run start            # 运行主入口（python_study:main，在 src/python_study/__init__.py）
uv run dev              # 开发模式：watchdog 监听 src 下 *.py 变化并自动重启
uv run python xxx.py    # 运行任意脚本
uv add <package>        # 添加依赖
uv run python -m pip ... # 如确需 pip（一般不需要）
```

> 注意：`.venv` 是 uv 创建的虚拟环境，勿手改；依赖变更请走 `uv add`，勿直接编辑 `uv.lock`。

## 项目结构

```
python-study/
├── pyproject.toml          # 依赖与脚本入口（start / dev）
├── uv.lock / .python-version
├── src/python_study/       # 主包（src layout）
│   ├── __init__.py         # 入口 main()，各 demo 按需注释启用
│   ├── dev.py              # 热重载开发脚本
│   ├── assets/             # 图片、markdown 素材
│   ├── utils/              # 工具模块（目前为空）
│   └── modules/
│       ├── built_module_demos/   # 标准库 demo：asyncio/base64/collections/contextlib/datetime/hash/itertools/process/reg/serialize/urllib
│       ├── third_module_demos/   # 第三方库 demo：chardet/pillow/psutil/requests/sqlite3
│       └── llm_demos/           # LLM demo：qwen_demo（DashScope 兼容接口 + SSE 流式）、sse_demo
└── preSrc/                 # 学习练习区（廖雪峰教程风格，可随意改）
    ├── index.py            # 练习主脚本
    ├── data_types_demo.py / operators_demo.py / control_flow_demo.py / functions_demo.py / exception_demo.py / data_structures_demo.py
    ├── my_module/          # 自定义模块练习
    └── oop_demo/           # 面向对象练习
```

## 代码约定

- **demo 文件命名**：`xxx_demo.py`，内部统一提供 `main() -> None` 入口，靠 `python_study/__init__.py` 中注释启停。
- 类型标注：尽量使用现代语法，如 `list[int]`、`dict[str, int]`、`str | None`、`TypedDict`、`dataclass`、`ParamSpec`（见 `qwen_demo.py`、`dev.py` 与 `preSrc/index.py`）。
- 依赖已经内置类型支持时，优先用 `from collections.abc import ...`（如 `Iterable`）。
- 主包代码用绝对导入（`from python_study.modules.llm_demos import ...`）；`preSrc` 练习脚本可用相对导入。
- 异步使用 `asyncio` + `aiohttp`（见 `qwen_demo.py`）；不要无脑给所有 IO 加线程。
- `.env` 存密钥（已被 gitignore），通过 `python-dotenv` 的 `load_dotenv()` 加载（见 `qwen_demo.py` 的 `DASHSCOPE_API_KEY`）。
- 磁盘上有 `demo.db`，是 sqlite 练习产物，不属于版本管理重点。

## 使用者背景（重要，请据此调整教学/答疑方式）

- 10 年前端开发经验，熟悉 JS/TS、浏览器与全栈开发。
- 思维方式是"页面 + 接口"，对系统编程、进程/线程、底层原理较浅。
- **请用前端类比讲解 Python 概念**：
  - JS 对象字面量 ≈ `dict`，`Promise/async-await` ≈ `asyncio`，`npm/pnpm` ≈ `uv`，TS 类型 ≈ `typing`。
- 目标：Python 基础 → 工程化 → 并发/网络 → LLM 应用 → **AI Agent 开发**（工具调用、编排、可生产级）。

## 给 AI 的工作指引

1. 涉及命令一律给 **Bash（Git Bash）** 版本，适配 Windows（路径分隔符、编码、进程等坑要主动提醒）。
2. 讲解新概念先给"3 分钟能跑通的完整最小示例"，再讲原理与坑，并给前端类比。
3. 主动指出 Windows 下常见坑：`\` vs `/`、文件编码（GBK/UTF-8）、换行符、中文路径、进程信号。
4. 学习进度以仓库实际文件为准：`preSrc` 是基础练习区，`src/python_study/modules` 是进阶 demo 区。
5. 新增 demo 遵循现有约定：`xxx_demo.py` + `main()`，并在 `__init__.py` 的注释列表登记。
6. 本仓库目标是 Agent 开发，涉及 LLM 的代码（`llm_demos/`）是进阶方向，练习时优先复用现有 DashScope 调用模式。
