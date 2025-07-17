#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终测试脚本 - 验证所有新功能
"""

from simplejsonspider import SimpleJSONSpider, FileTypeDetector
import tempfile
import os
import json

def test_all_features():
    """测试所有新功能"""
    print("🚀 SimpleJSONSpider v0.3.0 功能测试\n")
    
    # 1. 测试文件类型检测器
    print("1. 测试文件类型检测器:")
    test_contents = [
        ('{"name": "test"}', 'json'),
        ('name: test\nvalue: 123', 'yaml'),
        ('WEBVTT\n\n00:00:01.000 --> 00:00:05.000\nTest', 'vtt'),
        ('<?xml version="1.0"?><root></root>', 'xml'),
        ('name,age\nJohn,25\nJane,30', 'csv'),
        ('This is plain text', 'txt')
    ]
    
    for content, expected_type in test_contents:
        detected_type = FileTypeDetector.detect_content_type(content)
        status = "✅" if detected_type == expected_type else "❌"
        print(f"  {status} {expected_type}: {detected_type}")
    
    # 2. 测试自动检测功能
    print("\n2. 测试自动检测功能:")
    with tempfile.TemporaryDirectory() as temp_dir:
        spider = SimpleJSONSpider(
            api_url='https://jsonplaceholder.typicode.com/todos/1',
            filename_template='{id}_{title}',
            storage_dir=temp_dir,
            auto_detect_type=True
        )
        
        try:
            spider.run()
            files = os.listdir(temp_dir)
            if files and files[0].endswith('.json'):
                print("  ✅ 自动检测JSON格式成功")
            else:
                print("  ❌ 自动检测JSON格式失败")
        except Exception as e:
            print(f"  ❌ 自动检测测试失败: {e}")
    
    # 3. 测试自定义扩展名
    print("\n3. 测试自定义扩展名:")
    with tempfile.TemporaryDirectory() as temp_dir:
        spider = SimpleJSONSpider(
            api_url='https://jsonplaceholder.typicode.com/todos/1',
            filename_template='custom_file',
            storage_dir=temp_dir,
            file_extension='.custom'
        )
        
        try:
            spider.run()
            files = os.listdir(temp_dir)
            if files and files[0].endswith('.custom'):
                print("  ✅ 自定义扩展名功能成功")
            else:
                print("  ❌ 自定义扩展名功能失败")
        except Exception as e:
            print(f"  ❌ 自定义扩展名测试失败: {e}")
    
    # 4. 测试向后兼容性
    print("\n4. 测试向后兼容性:")
    with tempfile.TemporaryDirectory() as temp_dir:
        spider = SimpleJSONSpider(
            api_url='https://jsonplaceholder.typicode.com/todos/1',
            filename_template='{id}_{title}.json',
            storage_dir=temp_dir
        )
        
        try:
            # 测试旧方法
            json_data = spider.fetch_json()
            spider.save_json(json_data)
            files = os.listdir(temp_dir)
            if files and files[0].endswith('.json'):
                print("  ✅ 向后兼容性测试成功")
            else:
                print("  ❌ 向后兼容性测试失败")
        except Exception as e:
            print(f"  ❌ 向后兼容性测试失败: {e}")
    
    # 5. 测试格式化功能
    print("\n5. 测试格式化功能:")
    json_content = '{"name":"test","value":123}'
    yaml_content = 'name: test\nvalue: 123'
    
    try:
        # JSON格式化
        formatted_json = FileTypeDetector.prettify_content(json_content, 'json')
        if '"name": "test"' in formatted_json:
            print("  ✅ JSON格式化成功")
        else:
            print("  ❌ JSON格式化失败")
        
        # YAML格式化
        formatted_yaml = FileTypeDetector.prettify_content(yaml_content, 'yaml')
        if 'name: test' in formatted_yaml:
            print("  ✅ YAML格式化成功")
        else:
            print("  ❌ YAML格式化失败")
    except Exception as e:
        print(f"  ❌ 格式化测试失败: {e}")
    
    print("\n🎉 所有测试完成！")

if __name__ == "__main__":
    test_all_features()
