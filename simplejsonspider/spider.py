# simplejsonspider/spider.py

import os
import requests
import json
from typing import Dict, Any, Optional, Tuple
from .file_detector import FileTypeDetector

class SimpleJSONSpider:
    def __init__(
        self,
        api_url: str,
        filename_template: str,
        storage_dir: str,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        file_extension: Optional[str] = None,
        auto_detect_type: bool = True,
        prettify_content: bool = True,
    ):
        self.api_url = api_url
        self.filename_template = filename_template
        self.storage_dir = storage_dir
        self.file_extension = file_extension
        self.auto_detect_type = auto_detect_type
        self.prettify_content = prettify_content
        self.headers = headers or {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.bilibili.com/",
        }
        self.cookies = cookies or {}
        os.makedirs(self.storage_dir, exist_ok=True)

    def fetch_content(self) -> Tuple[str, str]:
        """
        获取API响应内容并检测文件类型
        
        Returns:
            tuple: (content, content_type)
        """
        resp = requests.get(self.api_url, headers=self.headers, cookies=self.cookies)
        resp.raise_for_status()
        
        # 获取响应内容
        content = resp.text
        
        # 如果指定了文件扩展名，则使用指定的扩展名
        if self.file_extension:
            # 移除开头的点号（如果有）
            ext = self.file_extension.lstrip('.')
            content_type = ext
        elif self.auto_detect_type:
            # 自动检测文件类型
            content_type = FileTypeDetector.detect_content_type(content)
        else:
            # 默认尝试解析为JSON
            try:
                json.loads(content)
                content_type = 'json'
            except (json.JSONDecodeError, ValueError):
                content_type = 'txt'
        
        return content, content_type

    def fetch_json(self) -> Dict[str, Any]:
        """保持向后兼容性的方法"""
        content, content_type = self.fetch_content()
        if content_type == 'json':
            return json.loads(content)
        else:
            raise ValueError(f"Expected JSON content but got {content_type}")

    def get_filename(self, content: str, content_type: str) -> str:
        """
        根据内容获取文件名
        
        Args:
            content: 文件内容
            content_type: 内容类型
            
        Returns:
            完整的文件名（包含扩展名）
        """
        # 尝试解析为JSON以获取模板参数
        try:
            if content_type == 'json':
                json_obj = json.loads(content)
            else:
                # 对于非JSON内容，尝试解析为JSON获取模板参数
                try:
                    json_obj = json.loads(content)
                except (json.JSONDecodeError, ValueError):
                    # 如果无法解析为JSON，则使用空字典
                    json_obj = {}
            
            filename = self.filename_template.format(**json_obj)
        except KeyError as e:
            raise ValueError(f"Key '{e.args[0]}' not found in content for filename template.")
        except Exception:
            # 如果模板格式化失败，使用默认文件名
            filename = "downloaded_file"
        
        # 添加文件扩展名
        if self.file_extension:
            # 如果用户指定了扩展名，使用用户指定的
            ext = self.file_extension
            if not ext.startswith('.'):
                ext = '.' + ext
        else:
            # 否则根据检测的内容类型添加扩展名
            ext = FileTypeDetector.get_file_extension(content_type)
        
        # 如果文件名已经有扩展名，则不重复添加
        if not filename.endswith(ext):
            filename += ext
        
        return filename

    def save_content(self, content: str, content_type: str):
        """
        保存内容到文件
        
        Args:
            content: 要保存的内容
            content_type: 内容类型
        """
        filename = self.get_filename(content, content_type)
        filepath = os.path.join(self.storage_dir, filename)
        
        # 如果需要格式化内容
        if self.prettify_content and FileTypeDetector.should_prettify(content_type):
            content = FileTypeDetector.prettify_content(content, content_type)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"文件已保存: {filepath} (类型: {content_type})")

    def save_json(self, json_obj: Dict[str, Any]):
        """保持向后兼容性的方法"""
        content = json.dumps(json_obj, ensure_ascii=False, indent=2)
        self.save_content(content, 'json')

    def run(self):
        """运行爬虫"""
        content, content_type = self.fetch_content()
        self.save_content(content, content_type)
