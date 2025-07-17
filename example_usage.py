# example_usage.py - 使用示例

from simplejsonspider import SimpleJSONSpider, FileTypeDetector

# 示例1: 自动检测文件类型（默认行为）
def example_auto_detect():
    """自动检测文件类型的示例"""
    spider = SimpleJSONSpider(
        api_url="https://api.example.com/data",
        filename_template="data_{id}",
        storage_dir="./downloads",
        auto_detect_type=True,  # 自动检测文件类型
        prettify_content=True   # 格式化内容
    )
    
    # 运行爬虫，会自动检测文件类型并添加相应扩展名
    spider.run()

# 示例2: 指定文件扩展名
def example_custom_extension():
    """指定文件扩展名的示例"""
    spider = SimpleJSONSpider(
        api_url="https://api.example.com/subtitle",
        filename_template="subtitle_{episode}",
        storage_dir="./downloads",
        file_extension=".vtt",  # 强制使用.vtt扩展名
        auto_detect_type=False  # 不自动检测类型
    )
    
    spider.run()

# 示例3: 手动使用文件类型检测器
def example_manual_detection():
    """手动使用文件类型检测器的示例"""
    
    # 测试不同类型的内容
    test_contents = [
        '{"name": "test", "value": 123}',  # JSON
        'name: test\nvalue: 123',           # YAML
        'WEBVTT\n\n00:00:01.000 --> 00:00:05.000\nHello World',  # VTT
        '<?xml version="1.0"?><root><item>test</item></root>',    # XML
        'name,age,city\nJohn,25,NYC\nJane,30,LA',                # CSV
        'This is just plain text content'  # TXT
    ]
    
    for content in test_contents:
        content_type = FileTypeDetector.detect_content_type(content)
        extension = FileTypeDetector.get_file_extension(content_type)
        should_prettify = FileTypeDetector.should_prettify(content_type)
        
        print(f"Content: {content[:30]}...")
        print(f"Detected type: {content_type}")
        print(f"Extension: {extension}")
        print(f"Should prettify: {should_prettify}")
        
        if should_prettify:
            prettified = FileTypeDetector.prettify_content(content, content_type)
            print(f"Prettified: {prettified[:50]}...")
        
        print("-" * 50)

# 示例4: 向后兼容性 - 旧的使用方式仍然有效
def example_backward_compatibility():
    """向后兼容性示例"""
    spider = SimpleJSONSpider(
        api_url="https://api.example.com/json",
        filename_template="old_style_{id}.json",
        storage_dir="./downloads"
    )
    
    # 旧的方式仍然可以工作
    try:
        json_data = spider.fetch_json()  # 只有当响应确实是JSON时才会成功
        spider.save_json(json_data)
    except ValueError as e:
        print(f"Not JSON content: {e}")
        # 可以回退到新的方式
        spider.run()

if __name__ == "__main__":
    print("=== 自动检测文件类型示例 ===")
    example_manual_detection()
    
    print("\n=== 文件类型检测器使用示例 ===")
    # 取消注释以下行来测试实际的API调用
    # example_auto_detect()
    # example_custom_extension()
    # example_backward_compatibility()
