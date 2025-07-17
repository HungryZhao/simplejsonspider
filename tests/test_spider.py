# tests/test_spider.py

import os
import shutil
import json
from simplejsonspider import SimpleJSONSpider

def test_run_and_save_json(tmp_path):
    # 使用jsonplaceholder测试，始终可用
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    filename_template = "{id}_{title}"
    storage_dir = tmp_path / "data"
    storage_dir_str = str(storage_dir)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir_str
    )
    spider.run()
    
    # 取回实际保存的文件名（和API返回字段有关）
    expected_filename = "1_delectus aut autem.json"
    file_path = os.path.join(storage_dir_str, expected_filename)
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert '"id": 1' in content

def test_custom_file_extension(monkeypatch, tmp_path):
    """测试自定义文件扩展名"""
    api_url = "http://example.com/test"
    filename_template = "test_file"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return '{"id": 1, "title": "test"}'
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        file_extension=".custom"
    )
    spider.run()
    
    # 检查文件是否以自定义扩展名保存
    file_path = os.path.join(storage_dir, "test_file.custom")
    assert os.path.exists(file_path)

def test_auto_detect_json(monkeypatch, tmp_path):
    """测试自动检测JSON格式"""
    api_url = "http://example.com/test"
    filename_template = "auto_detect"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return '{"id": 1, "title": "test"}'
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        auto_detect_type=True
    )
    spider.run()
    
    # 检查文件是否自动检测为JSON并保存
    file_path = os.path.join(storage_dir, "auto_detect.json")
    assert os.path.exists(file_path)

def test_auto_detect_yaml(monkeypatch, tmp_path):
    """测试自动检测YAML格式"""
    api_url = "http://example.com/test"
    filename_template = "auto_detect"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return 'name: test\nvalue: 123\nitems:\n  - 1\n  - 2\n  - 3'
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        auto_detect_type=True
    )
    spider.run()
    
    # 检查文件是否自动检测为YAML并保存
    file_path = os.path.join(storage_dir, "auto_detect.yaml")
    assert os.path.exists(file_path)

def test_auto_detect_vtt(monkeypatch, tmp_path):
    """测试自动检测VTT格式"""
    api_url = "http://example.com/test"
    filename_template = "auto_detect"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return 'WEBVTT\n\n00:00:01.000 --> 00:00:05.000\nHello World'
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        auto_detect_type=True
    )
    spider.run()
    
    # 检查文件是否自动检测为VTT并保存
    file_path = os.path.join(storage_dir, "auto_detect.vtt")
    assert os.path.exists(file_path)

def test_auto_detect_txt(monkeypatch, tmp_path):
    """测试自动检测纯文本格式"""
    api_url = "http://example.com/test"
    filename_template = "auto_detect"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return 'This is just plain text content.'
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        auto_detect_type=True
    )
    spider.run()
    
    # 检查文件是否自动检测为纯文本并保存
    file_path = os.path.join(storage_dir, "auto_detect.txt")
    assert os.path.exists(file_path)

def test_headers_and_cookies(monkeypatch, tmp_path):
    # 模拟请求，确保headers/cookies能被传递
    api_url = "http://example.com/test"
    filename_template = "dummy"
    storage_dir = str(tmp_path)
    headers = {"User-Agent": "pytest-agent"}
    cookies = {"testcookie": "123"}

    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return '{"id": 1, "title": "dummy"}'
    
    def dummy_get(url, headers=None, cookies=None):
        assert headers is not None
        assert cookies is not None
        assert headers["User-Agent"] == "pytest-agent"
        assert cookies["testcookie"] == "123"
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)

    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir,
        headers=headers,
        cookies=cookies,
    )
    spider.run()
    # 检查文件是否生成
    file_path = os.path.join(storage_dir, "dummy.json")
    assert os.path.exists(file_path)

def test_backward_compatibility(monkeypatch, tmp_path):
    """测试向后兼容性"""
    api_url = "http://example.com/test"
    filename_template = "{id}_{title}"
    storage_dir = str(tmp_path)
    
    class DummyResp:
        def raise_for_status(self): pass
        @property
        def text(self): return '{"id": 1, "title": "test"}'
        def json(self): return {"id": 1, "title": "test"}
    
    def dummy_get(url, headers=None, cookies=None):
        return DummyResp()
    
    monkeypatch.setattr("requests.get", dummy_get)
    
    spider = SimpleJSONSpider(
        api_url=api_url,
        filename_template=filename_template,
        storage_dir=storage_dir
    )
    
    # 测试旧的fetch_json方法
    json_data = spider.fetch_json()
    assert json_data["id"] == 1
    assert json_data["title"] == "test"
    
    # 测试旧的save_json方法
    spider.save_json(json_data)
    file_path = os.path.join(storage_dir, "1_test.json")
    assert os.path.exists(file_path)

