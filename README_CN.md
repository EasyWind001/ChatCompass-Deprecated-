# ChatCompass - AI对话知识库管理系统

<div align="center">

**🧭 一站式管理你的AI对话，让知识不再流失**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-65%20通过-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/Version-v1.2.7-orange.svg)](CHANGELOG.md)

[English](README_EN.md) | 简体中文

</div>

## 📖 项目简介

ChatCompass 是一款专为管理AI对话而设计的本地知识库系统。无论是ChatGPT、Claude还是DeepSeek的对话，一键保存，永久管理。

### 为什么需要ChatCompass？

- 💡 **AI对话易丢失**：平台对话可能被删除或过期
- 🔍 **难以检索**：想找之前的对话却找不到
- 📝 **价值流失**：宝贵的AI对话内容没有归档
- 🔒 **隐私担忧**：对话存储在第三方平台

### ChatCompass能做什么？

- ✅ **一键导入**：粘贴分享链接，自动抓取对话
- ✅ **智能搜索**：全文检索+上下文定位，秒找内容
- ✅ **永久保存**：本地数据库，完全掌控数据
- ✅ **AI辅助**：自动生成摘要、分类和标签
- ✅ **完全免费**：开源项目，本地运行

## ✨ 核心功能

### 🔍 智能搜索（上下文定位）

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

### 📦 多平台支持

| 平台 | 状态 | 链接格式 |
|------|------|----------|
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

# 2. 一键安装
# Windows用户
install.bat

# Mac/Linux用户  
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
  ✅ 抓取成功: Python编程基础

ChatCompass> search Python
  找到 1 条结果

ChatCompass> show 1
  （显示完整对话）

ChatCompass> exit
```

## ⚙️ 配置说明

### 基础使用（无需配置）

ChatCompass的核心功能**无需任何配置**即可使用：
- ✅ 添加对话
- ✅ 搜索对话  
- ✅ 查看详情
- ✅ 统计信息

### AI功能配置（可选）

如果想要**自动摘要**和**智能标签**：

#### 方式1：本地AI（推荐，免费）

```bash
# 1. 安装Ollama (https://ollama.ai)
ollama pull qwen2.5:7b

# 2. 配置.env
AI_MODE=local
OLLAMA_MODEL=qwen2.5:7b
```

**优点**：完全免费、完全离线、隐私保护  
**缺点**：需要8GB+内存

#### 方式2：在线AI

```bash
# 使用DeepSeek（推荐，性价比高）
AI_MODE=online
DEEPSEEK_API_KEY=your-api-key
```

**优点**：效果好、无需本地算力  
**缺点**：需要联网、有使用成本

## 📁 项目结构

```
ChatCompass/
├── main.py                   # 主程序入口
├── config.py                 # 配置管理
│
├── database/                 # 数据库模块
│   ├── sqlite_manager.py     # SQLite存储
│   └── es_manager.py         # Elasticsearch存储
│
├── scrapers/                 # 爬虫模块
│   ├── chatgpt_scraper.py    # ChatGPT爬虫
│   ├── claude_scraper.py     # Claude爬虫
│   ├── deepseek_scraper.py   # DeepSeek爬虫
│   └── scraper_factory.py    # 爬虫工厂
│
├── ai/                       # AI模块
│   ├── ollama_client.py      # Ollama客户端
│   └── openai_client.py      # OpenAI客户端
│
└── tests/                    # 测试套件（66个测试）
```

## 🎯 使用场景

### 场景1：学习笔记管理
> 和ChatGPT学习了Python，对话很有价值，想要保存下来

```bash
python main.py add https://chatgpt.com/share/xxxxx
python main.py search "Python列表"
```

### 场景2：工作资料归档
> 用Claude帮忙写文案，想整理归档这些对话

```bash
python main.py add https://claude.ai/share/xxxxx
python main.py list --category 写作
```

### 场景3：知识库建设
> 积累了大量AI对话，想建立个人知识库

```bash
python main.py stats
python main.py search tag:Python
```

## 🧪 测试

```bash
# 运行测试
python run_all_tests.py

# 或使用pytest
pytest tests/ -v
```

**测试结果：** 66个测试，98.5%通过率，87%代码覆盖率

## 📚 文档

- [完整README](README.md) - 详细文档
- [快速参考](QUICK_REFERENCE.md) - 命令速查
- [Docker指南](DOCKER_BUILD_GUIDE.md) - Docker部署
- [测试指南](TESTING_GUIDE.md) - 测试说明
- [贡献指南](CONTRIBUTING.md) - 参与开发
- [文档索引](DOCUMENTATION_INDEX.md) - 所有文档

## 🤝 参与贡献

欢迎提交Issue和Pull Request！

### 贡献流程

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

详见：[CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 许可证

本项目采用 [MIT许可证](LICENSE)

## ⚠️ 免责声明

- 本工具仅供个人学习和研究使用
- 使用本工具抓取第三方网站内容时，请遵守相关网站的服务条款
- 用户需自行承担使用本工具的法律责任

## 💬 联系方式

- 📮 [GitHub Issues](https://github.com/yourusername/ChatCompass/issues)
- 💬 [GitHub Discussions](https://github.com/yourusername/ChatCompass/discussions)

## 🙏 致谢

感谢以下开源项目：[Playwright](https://playwright.dev/) · [Ollama](https://ollama.ai/) · [SQLite](https://www.sqlite.org/) · [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

<div align="center">

**让AI对话成为永久的知识资产** 💎

Made with ❤️ by ChatCompass Team

[⬆ 返回顶部](#chatcompass---ai对话知识库管理系统)

</div>
