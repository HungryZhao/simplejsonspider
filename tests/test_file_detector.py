# tests/test_file_detector.py

import unittest
from simplejsonspider.file_detector import FileTypeDetector


class TestFileTypeDetector(unittest.TestCase):
    
    def test_detect_json(self):
        """测试JSON格式检测"""
        json_content = '{"name": "test", "value": 123, "items": [1, 2, 3]}'
        self.assertEqual(FileTypeDetector.detect_content_type(json_content), 'json')
    
    def test_detect_yaml(self):
        """测试YAML格式检测"""
        yaml_content = """---
name: test
value: 123
items:
  - 1
  - 2
  - 3
"""
        self.assertEqual(FileTypeDetector.detect_content_type(yaml_content), 'yaml')
    
    def test_detect_vtt(self):
        """测试VTT格式检测"""
        vtt_content = """WEBVTT

00:00:01.000 --> 00:00:05.000
Hello World

00:00:06.000 --> 00:00:10.000
This is a test subtitle
"""
        self.assertEqual(FileTypeDetector.detect_content_type(vtt_content), 'vtt')
    
    def test_detect_xml(self):
        """测试XML格式检测"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<root>
    <item>test</item>
    <value>123</value>
</root>"""
        self.assertEqual(FileTypeDetector.detect_content_type(xml_content), 'xml')
    
    def test_detect_csv(self):
        """测试CSV格式检测"""
        csv_content = """name,age,city
John,25,NYC
Jane,30,LA
Bob,35,SF"""
        self.assertEqual(FileTypeDetector.detect_content_type(csv_content), 'csv')
    
    def test_detect_txt(self):
        """测试纯文本格式检测"""
        txt_content = "This is just plain text content without any special format."
        self.assertEqual(FileTypeDetector.detect_content_type(txt_content), 'txt')
    
    def test_get_file_extension(self):
        """测试文件扩展名获取"""
        self.assertEqual(FileTypeDetector.get_file_extension('json'), '.json')
        self.assertEqual(FileTypeDetector.get_file_extension('yaml'), '.yaml')
        self.assertEqual(FileTypeDetector.get_file_extension('vtt'), '.vtt')
        self.assertEqual(FileTypeDetector.get_file_extension('xml'), '.xml')
        self.assertEqual(FileTypeDetector.get_file_extension('csv'), '.csv')
        self.assertEqual(FileTypeDetector.get_file_extension('txt'), '.txt')
    
    def test_should_prettify(self):
        """测试是否需要格式化判断"""
        self.assertTrue(FileTypeDetector.should_prettify('json'))
        self.assertTrue(FileTypeDetector.should_prettify('yaml'))
        self.assertTrue(FileTypeDetector.should_prettify('xml'))
        self.assertFalse(FileTypeDetector.should_prettify('txt'))
        self.assertFalse(FileTypeDetector.should_prettify('vtt'))
    
    def test_prettify_json(self):
        """测试JSON格式化"""
        json_content = '{"name":"test","value":123}'
        expected = '{\n  "name": "test",\n  "value": 123\n}'
        result = FileTypeDetector.prettify_content(json_content, 'json')
        self.assertEqual(result, expected)
    
    def test_prettify_yaml(self):
        """测试YAML格式化"""
        yaml_content = "name: test\nvalue: 123"
        result = FileTypeDetector.prettify_content(yaml_content, 'yaml')
        self.assertIn('name: test', result)
        self.assertIn('value: 123', result)
    
    def test_edge_cases(self):
        """测试边缘情况"""
        # 空内容
        self.assertEqual(FileTypeDetector.detect_content_type(''), 'txt')
        
        # 只有空白字符
        self.assertEqual(FileTypeDetector.detect_content_type('   \n\t  '), 'txt')
        
        # 无效JSON
        self.assertEqual(FileTypeDetector.detect_content_type('{"invalid": json}'), 'txt')
        
        # 看起来像JSON但不是的内容
        self.assertEqual(FileTypeDetector.detect_content_type('{this is not json}'), 'txt')


if __name__ == '__main__':
    unittest.main()
