# ChatCompass - AI对话知识库管理系统

<div align="center">

**一站式管理你的AI对话，让知识不再流失**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-65%20Passed-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/Version-v1.2.7-orange.svg)](CHANGELOG.md)

[English](README_EN.md) | [快速开始](#-快速开始) | [文档](DOCUMENTATION_INDEX.md) | [更新日志](CHANGELOG.md)

</div>

## 📖 项目简介

ChatCompass 是一款专为管理AI对话而设计的本地知识库系统。

**核心能力：**
- 🔗 **一键导入**：支持ChatGPT、Claude、DeepSeek等主流AI平台
- 🔍 **智能搜索**：全文检索+上下文定位，快速找到想要的信息
- 🤖 **AI分析**：自动生成摘要、分类和标签（可选）
- 📊 **灵活存储**：SQLite/Elasticsearch双引擎
- 🐳 **Docker部署**：一键启动完整环境

## ✨ 功能特性

### 核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| **多平台支持** | ChatGPT、Claude、DeepSeek | ✅ 已完成 |
| **智能抓取** | 自动提取对话内容 | ✅ 已完成 |
| **全文搜索** | 上下文定位+高亮显示 | ✅ v1.2 |
| **对话管理** | 查看/删除/标签管理 | ✅ 已完成 |
| **AI分析** | 本地/在线AI支持 | ✅ v1.2.2 |
| **Docker部署** | 一键启动所有服务 | ✅ v1.2.2 |

### 支持的平台

| 平台 | 状态 | URL格式 |
|------|------|---------|
| ChatGPT | ✅ | `https://chatgpt.com/share/xxx` |
| Claude | ✅ | `https://claude.ai/share/xxx` |
| DeepSeek | ✅ | `https://chat.deepseek.com/share/xxx` |
| Gemini | 🚧 | 计划中 |

## 🚀 快速开始

### 安装（3步完成）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/ChatCompass.git
cd ChatCompass

# 2. 安装依赖（Windows用户使用install.bat）
bash install.sh

# 3. 开始使用
python main.py
```

### 基本使用

```bash
# 添加对话
python main.py add "https://chatgpt.com/share/xxxxx"

# 搜索对话
python main.py search "Python教程"

# 查看详情
python main.py show 1

# 删除对话
python main.py delete 1

# 查看统计
python main.py stats
```

### 交互模式

```bash
$ python main.py

ChatCompass> add https://chatgpt.com/share/xxxxx
ChatCompass> search Python
ChatCompass> show 1
ChatCompass> exit
```

### Docker部署（可选）

```bash
# 一键启动（推荐）
./docker-start.sh        # Linux/Mac
.\docker-start.bat       # Windows

# 或手动启动
docker-compose up -d
docker exec -it chatcompass-app python main.py
```

📖 详细说明：[Docker快速入门](docs/DOCKER_QUICKSTART.md)

## 📁 项目结构

```
ChatCompass/
├── main.py                   # 主程序入口
├── config.py                 # 配置管理
├── requirements.txt          # Python依赖
│
├── database/                 # 数据库模块
│   ├── sqlite_manager.py     # SQLite存储
│   ├── es_manager.py         # Elasticsearch存储
│   └── storage_adapter.py    # 存储适配器
│
├── scrapers/                 # 爬虫模块
│   ├── chatgpt_scraper.py    # ChatGPT爬虫
│   ├── claude_scraper.py     # Claude爬虫
│   ├── deepseek_scraper.py   # DeepSeek爬虫
│   └── scraper_factory.py    # 爬虫工厂
│
├── ai/                       # AI分析模块
│   ├── ollama_client.py      # Ollama客户端
│   └── openai_client.py      # OpenAI客户端
│
└── tests/                    # 测试套件（66个测试）
```

## 🔧 配置说明

ChatCompass的核心功能（添加、搜索、查看）**无需配置**即可使用。

### AI功能配置（可选）

#### 本地模式（推荐，免费）

```bash
# 1. 安装Ollama (https://ollama.ai)
ollama pull qwen2.5:7b

# 2. 配置.env
AI_MODE=local
OLLAMA_MODEL=qwen2.5:7b
```

#### 在线模式

```bash
# 使用DeepSeek（推荐）或OpenAI
AI_MODE=online
DEEPSEEK_API_KEY=your-api-key
```

#### 禁用AI（默认）

```bash
# 留空即可
AI_MODE=
```

## 🧪 测试

```bash
# 运行测试
python run_all_tests.py

# 或使用pytest
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

**测试覆盖：** 66个测试，98.5%通过率，87%代码覆盖率

详见：[测试指南](TESTING_GUIDE.md)

## 📚 文档索引

| 场景 | 推荐文档 |
|------|---------|
| 🚀 **快速开始** | [README.md](README.md) |
| 📖 **命令参考** | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 🐳 **Docker部署** | [DOCKER_BUILD_GUIDE.md](DOCKER_BUILD_GUIDE.md) |
| 🧪 **运行测试** | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| 🤝 **参与贡献** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 📝 **版本历史** | [CHANGELOG.md](CHANGELOG.md) |
| 🔍 **完整索引** | [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |

## 🛠️ 技术栈

- **语言**: Python 3.9+
- **数据库**: SQLite3 / Elasticsearch
- **爬虫**: Playwright + BeautifulSoup4
- **AI**: Ollama / OpenAI API
- **测试**: Pytest + pytest-cov
- **容器**: Docker + Docker Compose

## 🤝 贡献指南

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 快速流程

```bash
# 1. Fork并克隆
git clone https://github.com/YOUR_USERNAME/ChatCompass.git

# 2. 创建分支
git checkout -b feature/your-feature

# 3. 开发并测试
pytest tests/ -v

# 4. 提交PR
git commit -m "feat: your feature"
git push origin feature/your-feature
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 💬 支持与反馈

- 📮 [GitHub Issues](https://github.com/yourusername/ChatCompass/issues)
- 💬 [GitHub Discussions](https://github.com/yourusername/ChatCompass/discussions)

## 🙏 致谢

感谢以下开源项目：[Playwright](https://playwright.dev/) · [Ollama](https://ollama.ai/) · [SQLite](https://www.sqlite.org/) · [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

<div align="center">

Made with ❤️ by ChatCompass Team

[⬆ 返回顶部](#chatcompass---ai对话知识库管理系统)

</div>
