# **simplejsonspider** 

---

## 特点

- 🚀 **多格式支持**：自动识别 JSON、YAML、VTT、XML、CSV 等文件格式
- 🎯 **自定义扩展名**：支持强制指定文件扩展名
- ⚡️ **智能检测**：自动检测内容类型并选择合适的文件扩展名
- 🗂 **文件名模板**：支持如 `{id}_{title}` 的灵活文件名模板
- 🧰 **HTTP支持**：支持自定义 headers 和 cookies
- 🎨 **格式化输出**：自动格式化 JSON、YAML 等结构化内容
- 🔄 **向后兼容**：完全兼容旧版本的使用方式spider

**simplejsonspider** 一个超简单的 Python 工具包，用于请求指定的 API 并将返回内容自动保存为本地文件。支持 JSON、YAML、VTT、XML、CSV 等多种格式的自动识别和保存。只需要指定接口地址、文件名模板和存储路径，即可一键抓取、自动存储。用GPT 4.1 只花了15分钟写的，但是人工检查过代码，应该靠谱。


---

## 特点

- ⚡️ 支持自定义 HTTP headers 和 cookies
- 🗂 文件名模板自由拼接，支持如 `{id}_{title}.json`
- 🧰 用法极简，适合数据抓取、接口快照、API调试等场景

---

## 安装

```bash
pip install simplejsonspider
```

### 从 GitHub 安装最新版本

```bash
# 安装最新 release 版本
pip install https://github.com/HungryZhao/simplejsonspider/releases/latest/download/simplejsonspider-0.3.0-py3-none-any.whl

# 或者从源码安装
pip install git+https://github.com/HungryZhao/simplejsonspider.git
````

---

## 快速上手

### 基本用法（自动检测文件类型）

```python
from simplejsonspider import SimpleJSONSpider

# 自动检测文件类型并保存
spider = SimpleJSONSpider(
    api_url='https://jsonplaceholder.typicode.com/todos/1',
    filename_template='{id}_{title}',  # 不需要指定扩展名
    storage_dir='./data'
)
spider.run()
# 将自动保存为 1_delectus aut autem.json
```

### 指定文件扩展名

```python
# 强制使用指定的文件扩展名
spider = SimpleJSONSpider(
    api_url='https://api.example.com/subtitle',
    filename_template='subtitle_{episode}',
    storage_dir='./downloads',
    file_extension='.vtt'  # 强制使用 .vtt 扩展名
)
spider.run()
```

### 处理不同格式的内容

```python
# 下载 YAML 配置文件
spider = SimpleJSONSpider(
    api_url='https://api.example.com/config.yaml',
    filename_template='config_{version}',
    storage_dir='./config'
)
spider.run()  # 自动识别为 YAML 格式并保存为 .yaml 文件

# 下载 VTT 字幕文件
spider = SimpleJSONSpider(
    api_url='https://api.example.com/subtitle.vtt',
    filename_template='subtitle_{lang}',
    storage_dir='./subtitles'
)
spider.run()  # 自动识别为 VTT 格式并保存为 .vtt 文件
```

---

## 高级用法

### 自定义 headers 和 cookies

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.bilibili.com/"
}
cookies = {
    "SESSDATA": "your_cookie"
}

spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='{id}_{title}',
    storage_dir='./data',
    headers=headers,
    cookies=cookies
)
spider.run()
```

### 控制内容格式化

```python
# 禁用自动格式化（保持原始格式）
spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='raw_data',
    storage_dir='./data',
    prettify_content=False  # 禁用格式化
)
spider.run()
```

### 禁用自动类型检测

```python
# 禁用自动检测，必须手动指定扩展名
spider = SimpleJSONSpider(
    api_url='https://api.example.com/data',
    filename_template='data_file',
    storage_dir='./data',
    auto_detect_type=False,  # 禁用自动检测
    file_extension='.txt'    # 手动指定扩展名
)
spider.run()
```

## 文件类型检测器

你也可以单独使用文件类型检测器：

```python
from simplejsonspider import FileTypeDetector

# 检测内容类型
content = '{"name": "test", "value": 123}'
content_type = FileTypeDetector.detect_content_type(content)
print(content_type)  # 输出: json

# 获取建议的文件扩展名
extension = FileTypeDetector.get_file_extension(content_type)
print(extension)  # 输出: .json

# 格式化内容
formatted = FileTypeDetector.prettify_content(content, content_type)
print(formatted)  # 输出格式化后的JSON
```

## 支持的文件格式

| 格式 | 扩展名 | 检测特征 |
|------|--------|----------|
| JSON | .json | 标准JSON格式 |
| YAML | .yaml | YAML语法特征 |
| VTT | .vtt | WebVTT字幕格式 |
| XML | .xml | XML标记语言 |
| CSV | .csv | 逗号分隔值 |
| TXT | .txt | 纯文本（默认） |

## 向后兼容性

旧版本的使用方式仍然完全支持：

```python
# 0.2.x 版本的用法仍然有效
spider = SimpleJSONSpider(
    api_url='https://jsonplaceholder.typicode.com/todos/1',
    filename_template='{id}_{title}.json',
    storage_dir='./data'
)

# 使用旧的方法
json_data = spider.fetch_json()
spider.save_json(json_data)
```

---

## 文件名模板说明

* 支持 Python 的字符串格式化：`{id}_{title}`
* **注意**：模板里的字段必须是API响应内容中能够解析出的字段
* 对于 JSON 响应，字段必须是 JSON 顶层的键
* 对于非 JSON 响应，如果无法解析出字段，将使用默认文件名

---

## 更新日志

### v0.3.0
- 🆕 新增多文件格式支持（JSON、YAML、VTT、XML、CSV）
- 🆕 新增自动文件类型检测功能
- 🆕 新增自定义文件扩展名支持
- 🆕 新增内容格式化功能
- 🆕 新增独立的文件类型检测器模块
- 🔄 保持完全向后兼容性

### v0.2.2
- 基础 JSON API 抓取功能
- 支持自定义 headers 和 cookies
- 文件名模板功能

---

## 常见问题

* **遇到 412、403 等错误？**
  请添加正确的 User-Agent、Referer 或 Cookie（详见高级用法）。

* **如何处理非 JSON 格式的响应？**
  使用 `auto_detect_type=True`（默认）让工具自动检测文件类型，或使用 `file_extension` 参数指定扩展名。

* **如何保存多个API数据？**
  可在循环中多次创建 SimpleJSONSpider 实例，或自己扩展批量功能。

* **文件名模板解析失败怎么办？**
  如果 API 响应无法解析出模板字段，将使用默认文件名。建议检查 API 响应格式和模板字段是否匹配。

---

## License

Do what you want with it, but please keep the original author information,
or MIT License.

---

## 关于作者

Zeturn：[GitHub 主页](https://github.com/zeturn)

* 这个包发布在了小号上面 [HungryZhao](https://github.com/HungryZhao)

---

