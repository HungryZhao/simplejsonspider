#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试新功能的实际使用示例
"""

from simplejsonspider import SimpleJSONSpider
import tempfile
import os

def test_real_json_api():
    """测试实际的JSON API"""
    print("=== 测试实际JSON API ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        spider = SimpleJSONSpider(
            api_url='https://jsonplaceholder.typicode.com/todos/1',
            filename_template='{id}_{title}',
            storage_dir=temp_dir,
            auto_detect_type=True,
            prettify_content=True
        )
        
        spider.run()
        
        # 检查生成的文件
        files = os.listdir(temp_dir)
        print(f"生成的文件: {files}")
        
        if files:
            file_path = os.path.join(temp_dir, files[0])
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"文件内容:\n{content[:200]}...")

def test_with_custom_extension():
    """测试自定义扩展名"""
    print("\n=== 测试自定义扩展名 ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        spider = SimpleJSONSpider(
            api_url='https://jsonplaceholder.typicode.com/todos/1',
            filename_template='custom_file',
            storage_dir=temp_dir,
            file_extension='.custom',
            auto_detect_type=False
        )
        
        spider.run()
        
        # 检查生成的文件
        files = os.listdir(temp_dir)
        print(f"生成的文件: {files}")
        
        if files:
            file_path = os.path.join(temp_dir, files[0])
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"文件内容:\n{content[:200]}...")

if __name__ == "__main__":
    test_real_json_api()
    test_with_custom_extension()
