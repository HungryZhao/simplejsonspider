# SimpleJSONSpider 使用指南

## 概述

SimpleJSONSpider v0.3.0 版本增加了多文件格式支持，现在可以自动识别并处理 JSON、YAML、VTT、XML、CSV 等多种文件格式。

## 新功能特性

### 1. 自动文件类型检测
- 自动识别下载内容的文件类型
- 根据内容类型选择合适的文件扩展名
- 支持 JSON、YAML、VTT、XML、CSV 等格式

### 2. 自定义文件扩展名
- 可以强制指定文件扩展名
- 忽略自动检测，使用用户指定的扩展名

### 3. 内容格式化
- 自动格式化结构化内容（JSON、YAML、XML）
- 可选择禁用格式化功能

### 4. 独立的文件类型检测器
- 可以单独使用 `FileTypeDetector` 类
- 提供内容类型检测、扩展名建议、格式化等功能

## 使用方法

### 基本用法（推荐）

```python
from simplejsonspider import SimpleJSONSpider

# 自动检测文件类型
spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='{id}_{title}',
    storage_dir='./downloads'
)
spider.run()
```

### 指定文件扩展名

```python
# 强制使用特定扩展名
spider = SimpleJSONSpider(
    api_url='https://api.example.com/subtitle',
    filename_template='subtitle_{episode}',
    storage_dir='./downloads',
    file_extension='.vtt'
)
spider.run()
```

### 禁用自动检测

```python
# 禁用自动检测，必须手动指定扩展名
spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='data_file',
    storage_dir='./downloads',
    auto_detect_type=False,
    file_extension='.txt'
)
spider.run()
```

### 控制格式化

```python
# 禁用内容格式化
spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='raw_data',
    storage_dir='./downloads',
    prettify_content=False
)
spider.run()
```

## 参数说明

### SimpleJSONSpider 构造函数参数

- `api_url`: API 接口地址
- `filename_template`: 文件名模板，支持占位符
- `storage_dir`: 存储目录
- `headers`: 自定义 HTTP 头部（可选）
- `cookies`: 自定义 cookies（可选）
- `file_extension`: 自定义文件扩展名（可选）
- `auto_detect_type`: 是否自动检测文件类型（默认: True）
- `prettify_content`: 是否格式化内容（默认: True）

## 支持的文件格式

| 格式 | 扩展名 | 自动检测 | 格式化支持 |
|------|--------|----------|------------|
| JSON | .json | ✅ | ✅ |
| YAML | .yaml | ✅ | ✅ |
| VTT | .vtt | ✅ | ❌ |
| XML | .xml | ✅ | ✅ |
| CSV | .csv | ✅ | ❌ |
| TXT | .txt | ✅ | ❌ |

## 文件类型检测器

```python
from simplejsonspider import FileTypeDetector

# 检测内容类型
content_type = FileTypeDetector.detect_content_type(content)

# 获取建议的扩展名
extension = FileTypeDetector.get_file_extension(content_type)

# 检查是否需要格式化
should_prettify = FileTypeDetector.should_prettify(content_type)

# 格式化内容
formatted = FileTypeDetector.prettify_content(content, content_type)
```

## 向后兼容性

旧版本的所有功能都保持兼容：

```python
# 0.2.x 版本的用法仍然有效
spider = SimpleJSONSpider(
    api_url='https://jsonplaceholder.typicode.com/todos/1',
    filename_template='{id}_{title}.json',
    storage_dir='./data'
)

# 可以继续使用旧的方法
json_data = spider.fetch_json()
spider.save_json(json_data)
```

## 错误处理

- 如果文件名模板中的占位符无法解析，将使用默认文件名
- 如果内容格式化失败，将保存原始内容
- 如果文件类型检测失败，将默认保存为 .txt 文件

## 最佳实践

1. 使用默认的自动检测功能，让工具自动选择合适的扩展名
2. 只在确实需要时才指定 `file_extension`
3. 对于结构化数据，启用 `prettify_content` 以获得更好的可读性
4. 使用有意义的文件名模板，便于后续管理

## 更新日志

### v0.3.0 (当前版本)
- 🆕 多文件格式支持
- 🆕 自动文件类型检测
- 🆕 自定义文件扩展名
- 🆕 内容格式化功能
- 🆕 独立的文件类型检测器
- 🔄 完全向后兼容

### v0.2.2
- 基础 JSON 支持
- 文件名模板
- 自定义 headers 和 cookies
