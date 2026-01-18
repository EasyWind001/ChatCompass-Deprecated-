# 错误处理与日志系统使用指南

## 📋 概述

ChatCompass v1.3.0 引入了完善的错误处理和日志管理系统,确保所有错误都能被记录和追踪。

## 🎯 核心功能

### 1. 自动日志记录
- **文件日志**: 所有日志自动保存到 `logs/chatcompass_YYYYMMDD.log`
- **按日分割**: 每天生成新的日志文件
- **完整堆栈**: 记录完整的异常堆栈信息
- **分级记录**: DEBUG/INFO/WARNING/ERROR/CRITICAL

### 2. 用户友好的错误弹窗
```python
from gui.error_handler import handle_error

try:
    # 可能出错的操作
    result = risky_operation()
except Exception as e:
    handle_error(
        e,
        parent=self,
        user_message="操作失败,请检查输入参数"
    )
```

**弹窗特性**:
- 显示用户友好的错误描述
- 可展开查看详细堆栈
- 自动记录到日志和历史

### 3. 错误历史追踪
- **内存缓存**: 保留最近100条错误记录
- **实时查看**: 通过"帮助→查看错误日志"菜单访问
- **详细信息**: 包含时间、类型、消息、堆栈

### 4. 错误日志导出
- 支持导出完整的错误历史
- 格式化输出,便于分析
- 可用于bug报告

## 📚 API 使用指南

### 错误处理

#### 1. 基本错误处理
```python
from gui.error_handler import handle_error

try:
    # 业务逻辑
    do_something()
except Exception as e:
    handle_error(e, parent=self, user_message="操作失败")
```

#### 2. 警告提示
```python
from gui.error_handler import handle_warning

if not is_valid_input(data):
    handle_warning("输入数据无效", parent=self)
    return
```

#### 3. 信息提示
```python
from gui.error_handler import handle_info

handle_info("任务已成功完成", parent=self, show_dialog=True)
```

### 高级用法

#### 自定义错误级别
```python
from gui.error_handler import ErrorHandler

ErrorHandler.handle_error(
    error=my_exception,
    parent=self,
    title="自定义标题",
    user_message="用户友好的错误描述",
    show_dialog=True,
    log_level="critical"  # debug/info/warning/error/critical
)
```

#### 获取错误历史
```python
from gui.error_handler import ErrorHandler

# 获取最近10条错误
recent_errors = ErrorHandler.get_error_history(limit=10)

for error in recent_errors:
    print(f"{error['timestamp']}: {error['message']}")
```

#### 导出错误日志
```python
from gui.error_handler import ErrorHandler
from pathlib import Path

# 导出到指定文件
output_path = Path("error_report.log")
ErrorHandler.export_error_log(output_path)
```

## 🔍 GUI错误查看器

### 访问方式
1. 主菜单: **帮助 → 查看错误日志**
2. 快捷键: (未设置,可自定义)

### 功能特性
- **错误列表**: 时间倒序显示所有错误
- **详细信息**: 点击查看完整堆栈
- **复制**: 一键复制错误详情
- **导出**: 导出错误日志到文件
- **清空**: 清空错误历史记录

### 使用场景
1. **调试问题**: 查看最近发生的错误
2. **Bug报告**: 导出错误日志附加到issue
3. **问题追踪**: 查看错误发生的时间和频率

## 📂 日志文件结构

```
ChatCompass/
├── logs/
│   ├── chatcompass_20260117.log    # 每日日志
│   ├── chatcompass_20260118.log
│   └── error_history_*.log          # 手动导出的错误日志
```

### 日志格式
```
2026-01-17 14:30:45,123 - gui.main_window - ERROR - 刷新对话列表失败
异常类型: sqlite3.OperationalError
详细信息: database is locked
堆栈跟踪:
Traceback (most recent call last):
  File "gui/main_window.py", line 285, in refresh_list
    conversations = self.db.list_conversations()
  ...
```

## 🛠️ 开发者指南

### 在新组件中集成错误处理

```python
from gui.error_handler import handle_error, handle_warning
import logging

logger = logging.getLogger(__name__)

class MyComponent(QWidget):
    def risky_operation(self):
        """可能出错的操作"""
        try:
            # 1. 先记录操作日志
            logger.info("开始执行风险操作")
            
            # 2. 执行业务逻辑
            result = self._do_something()
            
            # 3. 记录成功
            logger.info("操作成功完成")
            return result
            
        except ValueError as e:
            # 4. 处理预期的错误
            handle_warning(
                f"输入参数错误: {e}",
                parent=self
            )
        except Exception as e:
            # 5. 处理未预期的错误
            handle_error(
                e,
                parent=self,
                user_message="操作失败,请重试或联系支持"
            )
```

### 最佳实践

1. **始终捕获异常**: 不要让异常传播到Qt事件循环
2. **用户友好消息**: 提供清晰的错误描述,避免技术术语
3. **记录上下文**: 在日志中包含足够的上下文信息
4. **分级处理**: 
   - `DEBUG`: 详细的调试信息
   - `INFO`: 一般性操作日志
   - `WARNING`: 可恢复的问题
   - `ERROR`: 需要关注的错误
   - `CRITICAL`: 严重错误,影响系统运行

## 🧪 测试

### 测试错误处理
```python
def test_error_handling():
    """测试错误处理机制"""
    from gui.error_handler import ErrorHandler
    
    # 清空历史
    ErrorHandler.clear_history()
    
    # 触发错误
    try:
        raise ValueError("测试错误")
    except Exception as e:
        ErrorHandler.handle_error(
            e,
            user_message="测试错误处理",
            show_dialog=False  # 测试时不显示弹窗
        )
    
    # 验证记录
    history = ErrorHandler.get_error_history()
    assert len(history) == 1
    assert history[0]['type'] == 'ValueError'
```

## 📊 故障排查

### 常见问题

#### Q: 日志文件太大怎么办?
**A**: 日志按日分割,旧日志可以定期清理或归档。

#### Q: 错误历史占用内存?
**A**: 只保留最近100条,内存占用可控。可通过清空历史释放。

#### Q: 如何在生产环境隐藏详细堆栈?
**A**: 修改 `ErrorHandler._show_error_dialog()`,生产环境只显示用户消息。

#### Q: 如何集成到远程监控?
**A**: 可以扩展 `ErrorHandler.handle_error()`,添加远程上报逻辑。

## 🔄 版本历史

### v1.3.0 (2026-01-17)
- ✨ 新增统一错误处理机制
- ✨ 新增错误历史追踪
- ✨ 新增GUI错误查看器
- ✨ 新增日志导出功能
- 📝 完善日志配置

## 📞 技术支持

如果遇到问题:
1. 查看 `logs/` 目录下的日志文件
2. 使用"查看错误日志"功能检查错误历史
3. 导出错误日志附加到GitHub Issue
4. 提供复现步骤

---

**记住**: 良好的错误处理不仅能帮助开发者调试,更能提升用户体验! 🎯
