# simplejsonspider/__init__.py

from .spider import SimpleJSONSpider
from .file_detector import FileTypeDetector

try:
    from ._version import __version__
except ImportError:
    # fallback for development
    __version__ = "0.0.0.dev0"

__all__ = ['SimpleJSONSpider', 'FileTypeDetector']
