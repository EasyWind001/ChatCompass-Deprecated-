# ChatCompass GUI使用指南

> **版本**: v1.3.0  
> **更新日期**: 2026-01-17

---

## 📖 简介

ChatCompass GUI版本提供了完整的图形化界面,让AI对话管理更加直观和高效。

### 核心特性

- 🎨 **现代化界面** - 基于PyQt6的美观UI
- 🔍 **强大搜索** - 实时搜索和多维度过滤
- 📋 **剪贴板监控** - 自动识别复制的AI对话链接
- ⚡ **异步处理** - 后台任务队列,不阻塞UI
- 🔔 **系统托盘** - 最小化到托盘,后台监控

---

## 🚀 快速开始

### 启动GUI

```bash
# 方法1: 使用启动脚本(推荐)
python main_gui.py

# 方法2: 直接导入
python -c "from gui.main_window import MainWindow; from PyQt6.QtWidgets import QApplication; app = QApplication([]); window = MainWindow(); window.show(); app.exec()"
```

### 首次使用

1. **启动应用** - 双击运行或使用命令行
2. **添加对话** - 点击工具栏"添加"按钮或复制链接
3. **浏览对话** - 在列表中选择查看详情
4. **搜索过滤** - 使用搜索栏快速找到对话

---

## 💡 主要功能

### 1. 对话列表

**显示内容:**
- ID编号
- 对话标题
- AI平台(ChatGPT/Claude/DeepSeek等)
- 分类
- 创建时间
- 字数统计

**操作:**
- 单击选择对话
- 双击查看详情
- 右键打开菜单

### 2. 搜索和过滤

**搜索栏功能:**
- 关键词搜索(标题/摘要/内容)
- 平台过滤(All/ChatGPT/Claude/等)
- 实时搜索(输入2+字符自动搜索)

**使用技巧:**
```
# 单关键词搜索
Python

# 多关键词搜索
Python 教程

# 平台过滤
选择下拉框: ChatGPT
```

### 3. 添加对话

**方法1: 手动添加**
1. 点击工具栏"添加"按钮
2. 粘贴AI对话链接
3. 等待爬取完成

**方法2: 自动识别(推荐)**
1. 复制AI对话链接
2. 自动弹出确认对话框
3. 点击"添加"确认

**支持的链接格式:**
- `https://chatgpt.com/share/xxxx`
- `https://claude.ai/share/xxxx`
- `https://chat.deepseek.com/share/xxxx`

### 4. 查看详情

**详情面板显示:**
- 对话标题
- 原始链接
- AI平台
- 创建/更新时间
- 字数和消息数统计
- 完整对话内容

**操作按钮:**
- **复制链接** - 复制原始URL
- **导出** - 导出为Markdown/JSON
- **删除** - 删除对话(需确认)

### 5. 批量操作

**启用多选模式:**
1. 在对话列表右键菜单选择"启用多选"
2. 勾选要操作的对话
3. 右键选择批量操作

**支持的批量操作:**
- 删除多个对话
- 批量导出
- 全选/取消全选

### 6. 剪贴板监控

**功能说明:**
- 后台监听系统剪贴板
- 自动识别AI对话链接
- 弹窗提示是否添加
- 支持快捷键操作

**启用/禁用:**
```python
# 启动时禁用监控
python main_gui.py --no-monitor

# 或在设置中切换
菜单栏 -> 设置 -> 剪贴板监控
```

**性能:**
- CPU占用 < 1%
- 内存占用 < 10MB
- 检查间隔: 1秒

### 7. 异步任务队列

**功能特点:**
- 后台处理爬取任务
- 实时进度显示
- 支持并发(最多3个任务)
- 自动错误重试

**任务状态:**
- ⏳ **等待中** - 任务已添加到队列
- ⚙️ **处理中** - 正在爬取
- ✅ **已完成** - 成功添加
- ❌ **失败** - 爬取失败

**查看任务:**
- 状态栏显示队列大小
- 进度条显示当前任务
- 点击查看详细日志

### 8. 系统托盘

**托盘功能:**
- 最小化到托盘
- 托盘图标显示
- 右键快捷菜单

**托盘菜单:**
- 显示/隐藏主窗口
- 添加对话
- 查看统计
- 退出应用

**快捷操作:**
- 双击托盘图标: 显示/隐藏窗口
- 关闭窗口: 最小化到托盘(不退出)

---

## ⚙️ 配置选项

### GUI配置

在`config.py`中可以配置:

```python
# GUI设置
GUI_THEME = "light"  # light/dark
GUI_FONT_SIZE = 12
GUI_LANGUAGE = "zh_CN"  # zh_CN/en_US

# 剪贴板监控
CLIPBOARD_MONITOR_ENABLED = True
CLIPBOARD_CHECK_INTERVAL = 1000  # 毫秒

# 异步队列
ASYNC_QUEUE_ENABLED = True
MAX_CONCURRENT_TASKS = 3
TASK_TIMEOUT = 60  # 秒

# 系统托盘
SYSTEM_TRAY_ENABLED = True
MINIMIZE_TO_TRAY = True
```

### 数据库配置

```python
# 数据库路径
DATABASE_PATH = "chatcompass.db"

# 自动备份
AUTO_BACKUP = True
BACKUP_INTERVAL = 24  # 小时
```

---

## 🔧 故障排除

### 常见问题

**Q1: GUI启动失败**
```bash
# 检查PyQt6安装
pip install PyQt6 PyQt6-Qt6 PyQt6-sip

# 检查依赖
pip install -r requirements-gui.txt
```

**Q2: 剪贴板监控不工作**
```bash
# 检查pyperclip安装
pip install pyperclip

# Linux需要额外依赖
sudo apt-get install xclip  # 或 xsel
```

**Q3: 爬虫超时**
```python
# 增加超时时间
TASK_TIMEOUT = 120  # 改为120秒
```

**Q4: 内存占用过高**
```python
# 减少并发任务数
MAX_CONCURRENT_TASKS = 1
```

### 日志查看

```bash
# 查看日志文件
# Windows
type logs\chatcompass.log

# Linux/macOS
cat logs/chatcompass.log
```

### 重置配置

```bash
# 删除配置文件
rm config.py

# 重新启动会生成默认配置
python main_gui.py
```

---

## 📊 性能优化

### 推荐配置

**低配置系统:**
```python
MAX_CONCURRENT_TASKS = 1
CLIPBOARD_CHECK_INTERVAL = 2000
MINIMIZE_TO_TRAY = True
```

**高配置系统:**
```python
MAX_CONCURRENT_TASKS = 5
CLIPBOARD_CHECK_INTERVAL = 500
```

### 优化建议

1. **大量对话管理**
   - 使用搜索和过滤
   - 定期归档旧对话
   - 避免一次加载全部

2. **提升搜索性能**
   - 数据库定期VACUUM
   - 使用具体关键词
   - 利用平台过滤

3. **减少资源占用**
   - 禁用不需要的功能
   - 关闭系统托盘(不常用)
   - 减少并发任务数

---

## 🎯 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+N` | 添加对话 |
| `Ctrl+F` | 聚焦搜索框 |
| `Ctrl+R` | 刷新列表 |
| `Ctrl+W` | 关闭窗口 |
| `Ctrl+Q` | 退出应用 |
| `Delete` | 删除选中对话 |
| `Ctrl+A` | 全选 |
| `Esc` | 清除搜索 |

---

## 🔗 相关文档

- [项目主页](../README.md)
- [更新日志](../CHANGELOG.md)
- [开发计划](V1.3.0_PLAN.md)
- [测试指南](TESTING_GUIDE.md)

---

## 💬 反馈与支持

遇到问题或有建议? 欢迎:
- 提交Issue: [GitHub Issues](https://github.com/yourusername/ChatCompass/issues)
- 查看文档: [docs/](.)
- 联系作者: your.email@example.com

---

**享受使用ChatCompass GUI! 🎉**
