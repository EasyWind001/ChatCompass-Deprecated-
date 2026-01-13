# ChatCompass - AI对话知识库管理系统

<div align="center">

**一站式管理你的AI对话，让知识不再流失**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-52%20Passed-brightgreen.svg)](tests/)

[English](README_EN.md) | [功能特性](#-功能特性) | [快速开始](#-快速开始) | [文档](#-文档)

</div>

## 📖 项目简介

ChatCompass 是一款专为管理AI对话而设计的本地知识库系统。它能够：

- 🔗 **一键导入**：支持ChatGPT、Claude等主流AI平台的分享链接
- 🤖 **智能分析**：自动生成摘要、分类和标签（可选）
- 🔍 **强大搜索**：全文检索+上下文定位，快速找到想要的信息
- 📊 **知识管理**：本地SQLite存储，完全掌控你的数据

## ✨ 功能特性

### 🎯 核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| **多平台支持** | ChatGPT、Claude等 | ✅ 已完成 |
| **智能抓取** | 自动提取对话内容 | ✅ 已完成 |
| **全文搜索** | 基于SQLite FTS5 | ✅ 已完成 |
| **上下文定位** | 搜索结果显示前后文 | ✅ v1.2新增 |
| **对话详情** | 查看完整对话内容 | ✅ v1.1新增 |
| **AI分析** | 自动摘要和标签（可选） | ✅ 已完成 |
| **命令行界面** | 交互式CLI | ✅ 已完成 |
| **GUI界面** | 桌面应用 | 🚧 开发中 |

### 🔍 搜索增强功能（v1.2）

- **上下文显示**：搜索结果显示匹配片段的前后80字符
- **精确定位**：标注匹配位置（第几条消息）
- **关键词高亮**：用【】包裹关键词
- **角色区分**：区分用户👤和助手🤖的消息
- **多处匹配**：支持一个对话中的多处匹配展示

**搜索效果示例：**
```
🔍 搜索: Python

  [1] 📄 Python数据分析教程
      💬 平台: chatgpt | 📁 分类: 编程
      📍 找到 2 处匹配:

         🤖 助手 (第 2/5 条消息)
         ...学习【Python】数据分析，建议从Pandas和NumPy开始...

         🤖 助手 (第 4/5 条消息)
         ...【Python】在数据科学领域非常流行，因为...

      💡 输入 'show 1' 查看完整对话
```

### 📦 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| ChatGPT | ✅ | 支持分享链接 |
| Claude | ✅ | 支持分享链接 |
| Gemini | 🚧 | 计划支持 |
| DeepSeek | 🚧 | 计划支持 |

## 🚀 快速开始

### 前置要求

- Python 3.9 或更高版本
- Windows / macOS / Linux

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ChatCompass.git
cd ChatCompass
```

#### 2. 安装依赖

```bash
# 使用一键安装脚本（推荐）
# Windows
install.bat

# Linux/macOS
bash install.sh

# 或手动安装
pip install -r requirements.txt
playwright install chromium
```

#### 3. 配置（可选）

```bash
# 复制配置文件
cp .env.example .env

# 编辑.env，配置AI功能（可选）
# 不配置也能正常使用，只是没有自动摘要功能
```

### 基本使用

#### 命令行模式

```bash
# 交互模式
python main.py

# 直接添加对话
python main.py add "https://chatgpt.com/share/xxxxx"

# 搜索对话
python main.py search "Python教程"

# 查看对话详情
python main.py show 1

# 查看统计信息
python main.py stats
```

#### 交互模式

```
$ python main.py

ChatCompass> help         # 查看帮助
ChatCompass> list         # 列出所有对话
ChatCompass> search Python  # 搜索
ChatCompass> show 1       # 查看详情
ChatCompass> exit         # 退出
```

### 使用示例

```bash
# 1. 添加ChatGPT对话
python main.py add "https://chatgpt.com/share/6964e4ba-8264-8010-99ad-ab2399bb1dca"

# 2. 搜索相关对话
python main.py search "编程"

# 3. 查看详细内容
python main.py show 1

# 4. 查看统计
python main.py stats
```

## 📁 项目结构

```
ChatCompass/
├── README.md                 # 项目说明文档
├── CHANGELOG.md              # 版本更新日志
├── requirements.txt          # Python依赖列表
├── .env.example              # 配置文件示例
├── .gitignore                # Git忽略规则
│
├── main.py                   # 🎯 主程序入口
├── config.py                 # ⚙️ 配置管理
├── setup.py                  # 📦 安装脚本
│
├── install.bat               # Windows一键安装
├── install.sh                # Linux/macOS一键安装
├── run.bat                   # Windows快速启动
├── run.sh                    # Linux/macOS快速启动
├── run_tests.bat             # Windows测试脚本
├── run_tests.py              # 测试运行器
│
├── database/                 # 💾 数据库模块
│   ├── __init__.py
│   ├── db_manager.py         # 数据库管理器（核心）
│   └── schema.sql            # 数据库表结构定义
│
├── scrapers/                 # 🕷️ 网页爬虫模块
│   ├── __init__.py
│   ├── base_scraper.py       # 爬虫基类
│   ├── chatgpt_scraper.py    # ChatGPT爬虫实现
│   ├── claude_scraper.py     # Claude爬虫实现
│   └── scraper_factory.py    # 爬虫工厂（自动选择）
│
├── ai/                       # 🤖 AI分析模块
│   ├── __init__.py
│   ├── ollama_client.py      # Ollama本地模型客户端
│   └── openai_client.py      # OpenAI/DeepSeek API客户端
│
├── tests/                    # 🧪 测试套件
│   ├── __init__.py
│   ├── conftest.py           # Pytest配置
│   ├── README.md             # 测试说明
│   ├── unit/                 # 单元测试
│   │   ├── test_database.py
│   │   ├── test_scrapers.py
│   │   └── test_ai_clients.py
│   └── integration/          # 集成测试
│       └── test_full_workflow.py
│
└── docs/                     # 📚 文档目录
    ├── PROJECT_SUMMARY.md            # 项目总结
    ├── search_implementation.md      # 搜索实现文档
    ├── SEARCH_CONTEXT_FEATURE.md     # 搜索增强功能文档
    ├── SEARCH_ENHANCEMENT_SUMMARY.md # 搜索增强总结
    └── archive/                      # 开发过程文档归档
        └── ...
```

### 目录说明

#### 核心模块

- **`database/`** - 数据库管理模块
  - 使用SQLite3存储对话数据
  - 实现FTS5全文搜索
  - 提供完整的CRUD操作
  - 支持标签管理和统计

- **`scrapers/`** - 网页爬虫模块
  - 基于Playwright自动化抓取
  - 支持多平台适配
  - 实现多层回退机制
  - 自动处理页面结构变化

- **`ai/`** - AI分析模块（可选）
  - 支持本地模型（Ollama）
  - 支持在线API（OpenAI/DeepSeek）
  - 自动生成摘要和标签
  - 智能分类对话内容

#### 测试

- **52个测试用例**，覆盖核心功能
- **96.3%通过率**，确保代码质量
- **49%代码覆盖率**，持续改进中

运行测试：
```bash
# Windows
run_tests.bat

# Linux/macOS
python run_tests.py
```

#### 文档

- **`docs/`** - 详细技术文档
  - 功能说明文档
  - 实现细节文档
  - 开发过程归档

## 🔧 配置说明

### AI功能配置（可选）

ChatCompass的核心功能（添加、搜索、查看）**不需要配置AI**即可使用。

AI功能仅用于：
- 自动生成对话摘要
- 自动分类对话
- 自动提取标签

#### 本地模式（推荐，免费）

```env
# .env 文件
AI_MODE=local
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

**安装Ollama：**
1. 访问 https://ollama.ai 下载安装
2. 运行 `ollama pull qwen2.5:7b`
3. 启动服务 `ollama serve`

#### 在线模式

```env
AI_MODE=online

# 使用DeepSeek（推荐，性价比高）
DEEPSEEK_API_KEY=your-api-key
DEEPSEEK_MODEL=deepseek-chat

# 或使用OpenAI
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini
```

#### 禁用AI（默认）

```env
# 留空或不配置，程序会跳过AI分析
AI_MODE=
```

## 🎯 使用技巧

### 搜索技巧

```bash
# 单关键词
python main.py search "Python"

# 多关键词（空格分隔）
python main.py search "Python 数据分析"

# 精确短语（使用引号）
python main.py search "机器学习入门"
```

### 查看对话

```bash
# 通过ID查看
python main.py show 1

# 通过URL查看
python main.py show "https://chatgpt.com/share/xxxxx"

# 交互模式中查看
ChatCompass> show 1
```

### 批量管理

```bash
# 列出所有对话
ChatCompass> list

# 查看统计信息
ChatCompass> stats

# 按分类筛选
ChatCompass> list --category 编程
```

## 🧪 测试

项目包含完整的测试套件，确保代码质量。

### 运行测试

```bash
# Windows
run_tests.bat

# Linux/macOS  
python run_tests.py

# 或使用pytest
pytest tests/ -v
```

### 测试覆盖

- ✅ 数据库操作测试（13个）
- ✅ 爬虫功能测试（16个）
- ✅ AI客户端测试（19个）
- ✅ 完整流程测试（4个）

**总计：52个测试，96.3%通过率**

详见：[tests/README.md](tests/README.md)

## 📊 数据库设计

### 核心表结构

```sql
-- 对话表
conversations (
    id INTEGER PRIMARY KEY,
    source_url TEXT UNIQUE,      -- 原始链接
    platform TEXT,                -- 平台（chatgpt/claude）
    title TEXT,                   -- 对话标题
    raw_content TEXT,             -- 完整对话内容（JSON）
    summary TEXT,                 -- AI摘要
    category TEXT,                -- 分类
    word_count INTEGER,           -- 字数统计
    message_count INTEGER,        -- 消息数
    created_at DATETIME,          -- 创建时间
    updated_at DATETIME,          -- 更新时间
    is_favorite INTEGER,          -- 是否收藏
    notes TEXT                    -- 用户备注
)

-- 标签表
tags (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,             -- 标签名
    color TEXT,                   -- 颜色
    usage_count INTEGER           -- 使用次数
)

-- 关联表
conversation_tags (
    conversation_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (conversation_id, tag_id)
)

-- FTS5全文搜索表
conversations_fts (
    title, summary, raw_content
)
```

详见：[database/schema.sql](database/schema.sql)

## 📝 更新日志

### v1.2 (2026-01-13) - 搜索增强

- ✨ 新增：搜索结果显示上下文定位
- ✨ 新增：精确标注匹配位置
- ✨ 新增：关键词高亮显示
- ✨ 新增：支持多处匹配展示
- 🎨 优化：搜索结果显示格式

### v1.1 (2026-01-12) - Show功能

- ✨ 新增：show命令查看对话详情
- 🐛 修复：ChatGPT爬虫页面结构适配
- 🎨 优化：交互模式体验
- 🔧 改进：Windows控制台编码处理

### v1.0 (2026-01-12) - 初始版本

- ✅ 基础功能完成
- ✅ 52个测试通过
- ✅ ChatGPT和Claude平台支持

完整更新日志：[CHANGELOG.md](CHANGELOG.md)

## 🛠️ 技术栈

- **语言**: Python 3.9+
- **数据库**: SQLite3 + FTS5（全文搜索）
- **爬虫**: Playwright + BeautifulSoup4
- **AI**: Ollama (本地) / OpenAI API (在线)
- **测试**: Pytest
- **GUI**: PyQt6（计划中）

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 开发环境设置

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install pytest pytest-cov

# 运行测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

本工具仅供个人学习和研究使用。使用本工具抓取第三方网站内容时，请遵守相关网站的服务条款和robots.txt规则。用户需自行承担使用本工具的法律责任。

## 💬 支持与反馈

- 📮 提交Issue: [GitHub Issues](https://github.com/yourusername/ChatCompass/issues)
- 📧 邮箱: your.email@example.com
- 💬 讨论: [GitHub Discussions](https://github.com/yourusername/ChatCompass/discussions)

## 🙏 致谢

感谢以下开源项目：

- [Playwright](https://playwright.dev/) - 强大的浏览器自动化工具
- [Ollama](https://ollama.ai/) - 本地大模型运行平台
- [SQLite FTS5](https://www.sqlite.org/fts5.html) - 全文搜索引擎
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML解析库

## ⭐ Star历史

如果这个项目对你有帮助，请给个⭐️吧！

---

<div align="center">

Made with ❤️ by ChatCompass Team

[⬆ 返回顶部](#chatcompass---ai对话知识库管理系统)

</div>
