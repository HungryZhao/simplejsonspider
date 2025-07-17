# simplejsonspider/file_detector.py

import json
import yaml
import re
from typing import Optional, Dict, Any


class FileTypeDetector:
    """文件类型检测器，用于识别不同格式的文件"""
    
    @staticmethod
    def detect_content_type(content: str) -> str:
        """
        检测文件内容的类型
        
        Args:
            content: 文件内容字符串
            
        Returns:
            文件类型：'json', 'yaml', 'yml', 'vtt', 'txt'
        """
        # 去除首尾空白字符
        content = content.strip()
        
        # 检测 VTT 格式 (需要在YAML之前检测，因为VTT可能被误识别为YAML)
        if FileTypeDetector._is_vtt(content):
            return 'vtt'
        
        # 检测 JSON 格式
        if FileTypeDetector._is_json(content):
            return 'json'
        
        # 检测 YAML 格式
        if FileTypeDetector._is_yaml(content):
            return 'yaml'
        
        # 检测 XML 格式
        if FileTypeDetector._is_xml(content):
            return 'xml'
        
        # 检测 CSV 格式
        if FileTypeDetector._is_csv(content):
            return 'csv'
        
        # 默认为纯文本
        return 'txt'
    
    @staticmethod
    def _is_json(content: str) -> bool:
        """检查是否为JSON格式"""
        try:
            json.loads(content)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    @staticmethod
    def _is_yaml(content: str) -> bool:
        """检查是否为YAML格式"""
        try:
            yaml.safe_load(content)
            # 额外检查YAML特征
            if any(line.strip().startswith(('---', '...')) for line in content.split('\n')):
                return True
            # 检查是否有YAML键值对格式
            if ':' in content and not content.strip().startswith(('{', '[')):
                return True
            return False
        except yaml.YAMLError:
            return False
        except Exception:
            return False
    
    @staticmethod
    def _is_vtt(content: str) -> bool:
        """检查是否为VTT字幕格式"""
        lines = content.strip().split('\n')
        if len(lines) < 2:
            return False
        
        # VTT文件通常以WEBVTT开头
        if lines[0].strip().startswith('WEBVTT'):
            return True
        
        # 检查是否包含时间戳格式 (00:00:00.000 --> 00:00:00.000)
        timestamp_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}'
        if re.search(timestamp_pattern, content):
            return True
        
        return False
    
    @staticmethod
    def _is_xml(content: str) -> bool:
        """检查是否为XML格式"""
        content = content.strip()
        return (content.startswith('<?xml') or 
                (content.startswith('<') and content.endswith('>')))
    
    @staticmethod
    def _is_csv(content: str) -> bool:
        """检查是否为CSV格式"""
        lines = content.strip().split('\n')
        if len(lines) < 2:
            return False
        
        # 检查前几行是否有一致的分隔符
        first_line = lines[0]
        separators = [',', ';', '\t']
        
        for sep in separators:
            if sep in first_line:
                first_count = first_line.count(sep)
                if first_count > 0:
                    # 检查后续行是否有相同数量的分隔符
                    consistent = True
                    for line in lines[1:3]:  # 检查前几行
                        if line.count(sep) != first_count:
                            consistent = False
                            break
                    if consistent:
                        return True
        
        return False
    
    @staticmethod
    def get_file_extension(content_type: str) -> str:
        """
        根据内容类型获取建议的文件扩展名
        
        Args:
            content_type: 文件内容类型
            
        Returns:
            文件扩展名（包含点号）
        """
        extension_map = {
            'json': '.json',
            'yaml': '.yaml',
            'yml': '.yml',
            'vtt': '.vtt',
            'xml': '.xml',
            'csv': '.csv',
            'txt': '.txt'
        }
        
        return extension_map.get(content_type, '.txt')
    
    @staticmethod
    def should_prettify(content_type: str) -> bool:
        """
        判断是否需要格式化内容
        
        Args:
            content_type: 文件内容类型
            
        Returns:
            是否需要格式化
        """
        return content_type in ['json', 'yaml', 'yml', 'xml']
    
    @staticmethod
    def prettify_content(content: str, content_type: str) -> str:
        """
        格式化内容
        
        Args:
            content: 原始内容
            content_type: 内容类型
            
        Returns:
            格式化后的内容
        """
        try:
            if content_type == 'json':
                data = json.loads(content)
                return json.dumps(data, ensure_ascii=False, indent=2)
            elif content_type in ['yaml', 'yml']:
                data = yaml.safe_load(content)
                return yaml.dump(data, default_flow_style=False, allow_unicode=True)
            elif content_type == 'xml':
                # 简单的XML格式化（可以考虑使用xml.etree.ElementTree）
                return content
            else:
                return content
        except Exception:
            # 格式化失败时返回原内容
            return content
