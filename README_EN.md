# ChatCompass - AI Conversation Knowledge Base

<div align="center">

**One-stop management for your AI conversations**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-65%20Passed-brightgreen.svg)](tests/)
[![Version](https://img.shields.io/badge/Version-v1.2.7-orange.svg)](CHANGELOG.md)

[简体中文](README_CN.md) | English

</div>

## 📖 Introduction

ChatCompass is a local knowledge base system designed for managing AI conversations. Save conversations from ChatGPT, Claude, DeepSeek and more with one click.

### Why ChatCompass?

- 💡 **Conversations get lost** - Platform conversations may be deleted or expire
- 🔍 **Hard to search** - Difficult to find previous conversations
- 📝 **Knowledge leakage** - Valuable AI conversation content not archived
- 🔒 **Privacy concerns** - Conversations stored on third-party platforms

### What Can ChatCompass Do?

- ✅ **One-Click Import** - Paste share link, auto-extract conversation
- ✅ **Smart Search** - Full-text search + context positioning
- ✅ **Permanent Save** - Local database, full data control
- ✅ **AI Assistant** - Auto-generate summaries, categories and tags
- ✅ **Completely Free** - Open source, runs locally

## ✨ Key Features

### 🔍 Smart Search (Context Positioning)

```
🔍 Search: Python

  [1] 📄 Python Data Analysis Tutorial
      💬 Platform: chatgpt | 📁 Category: Programming
      📍 Found 2 matches:

         🤖 Assistant (Message 2/5)
         ...learn【Python】data analysis, start with Pandas and NumPy...

         🤖 Assistant (Message 4/5)
         ...【Python】is very popular in data science because...

      💡 Enter 'show 1' to view complete conversation
```

### 📦 Platform Support

| Platform | Status | URL Format |
|----------|--------|------------|
| ChatGPT | ✅ | `https://chatgpt.com/share/xxx` |
| Claude | ✅ | `https://claude.ai/share/xxx` |
| DeepSeek | ✅ | `https://chat.deepseek.com/share/xxx` |
| Gemini | 🚧 | Planned |

## 🚀 Quick Start

### Installation (3 Steps)

```bash
# 1. Clone project
git clone https://github.com/yourusername/ChatCompass.git
cd ChatCompass

# 2. One-click install
# Windows users
install.bat

# Mac/Linux users
bash install.sh

# 3. Start using
python main.py
```

### Basic Usage

```bash
# Add conversation
python main.py add "https://chatgpt.com/share/xxxxx"

# Search conversations
python main.py search "Python tutorial"

# View details
python main.py show 1

# Delete conversation
python main.py delete 1

# View statistics
python main.py stats
```

### Interactive Mode

```bash
$ python main.py

ChatCompass> add https://chatgpt.com/share/xxxxx
  ✅ Scraping successful: Python Basics

ChatCompass> search Python
  Found 1 result

ChatCompass> show 1
  (Display complete conversation)

ChatCompass> exit
```

## ⚙️ Configuration

### Basic Usage (No Configuration Required)

ChatCompass core features work **without any configuration**:
- ✅ Add conversations
- ✅ Search conversations
- ✅ View details
- ✅ Statistics

### AI Features (Optional)

For **auto-summaries** and **smart tags**:

#### Option 1: Local AI (Recommended, Free)

```bash
# 1. Install Ollama (https://ollama.ai)
ollama pull qwen2.5:7b

# 2. Configure .env
AI_MODE=local
OLLAMA_MODEL=qwen2.5:7b
```

**Pros**: Completely free, offline, privacy-protected  
**Cons**: Requires 8GB+ memory

#### Option 2: Online AI

```bash
# Use DeepSeek (Recommended, cost-effective)
AI_MODE=online
DEEPSEEK_API_KEY=your-api-key
```

**Pros**: Better results, no local computation  
**Cons**: Requires internet, has usage cost

## 📁 Project Structure

```
ChatCompass/
├── main.py                   # Main entry point
├── config.py                 # Configuration
│
├── database/                 # Database module
│   ├── sqlite_manager.py     # SQLite storage
│   └── es_manager.py         # Elasticsearch storage
│
├── scrapers/                 # Scraper module
│   ├── chatgpt_scraper.py    # ChatGPT scraper
│   ├── claude_scraper.py     # Claude scraper
│   ├── deepseek_scraper.py   # DeepSeek scraper
│   └── scraper_factory.py    # Scraper factory
│
├── ai/                       # AI module
│   ├── ollama_client.py      # Ollama client
│   └── openai_client.py      # OpenAI client
│
└── tests/                    # Test suite (66 tests)
```

## 🎯 Use Cases

### Case 1: Learning Notes Management
> Learned Python with ChatGPT, want to save valuable conversations

```bash
python main.py add https://chatgpt.com/share/xxxxx
python main.py search "Python lists"
```

### Case 2: Work Archive
> Used Claude to write documents, want to organize these conversations

```bash
python main.py add https://claude.ai/share/xxxxx
python main.py list --category writing
```

### Case 3: Knowledge Base Building
> Accumulated many AI conversations, want to build personal knowledge base

```bash
python main.py stats
python main.py search tag:Python
```

## 🧪 Testing

```bash
# Run tests
python run_all_tests.py

# Or use pytest
pytest tests/ -v
```

**Test Results:** 66 tests, 98.5% pass rate, 87% code coverage

## 📚 Documentation

- [Full README](README.md) - Detailed documentation
- [Quick Reference](QUICK_REFERENCE.md) - Command reference
- [Docker Guide](DOCKER_BUILD_GUIDE.md) - Docker deployment
- [Testing Guide](TESTING_GUIDE.md) - Testing instructions
- [Contributing](CONTRIBUTING.md) - Development guide
- [Documentation Index](DOCUMENTATION_INDEX.md) - All documents

## 🤝 Contributing

Welcome Issues and Pull Requests!

### Contributing Process

1. Fork this project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

See: [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

This project is licensed under [MIT License](LICENSE)

## ⚠️ Disclaimer

- This tool is for personal learning and research only
- When scraping third-party website content, please comply with relevant terms of service
- Users are responsible for legal liability of using this tool

## 💬 Contact

- 📮 [GitHub Issues](https://github.com/yourusername/ChatCompass/issues)
- 💬 [GitHub Discussions](https://github.com/yourusername/ChatCompass/discussions)

## 🙏 Acknowledgments

Thanks to: [Playwright](https://playwright.dev/) · [Ollama](https://ollama.ai/) · [SQLite](https://www.sqlite.org/) · [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

<div align="center">

**Turn AI conversations into permanent knowledge assets** 💎

Made with ❤️ by ChatCompass Team

[⬆ Back to Top](#chatcompass---ai-conversation-knowledge-base)

</div>
