from cao.sources.base import BaseSource
from cao.registry import ConverterRegistry
from PIL import Image

class ImageOpenSource(BaseSource):
    def extract(self, path, options=None):
        options = options or {}
        if options:
            raise ValueError(f"Image does not accept any options at this moment. Submit a PR to add support for options.")
        img = Image.open(path)
        return {"type": "image", "data": img}

    @classmethod
    def supported_extensions(cls):
        return ["png", "jpg", "jpeg", "bmp", "webp", "tiff", "ico"]
    
    @classmethod
    def data_type(cls):
        return "image"

# Register all supported formats
for ext in ImageOpenSource.supported_extensions():
    ConverterRegistry.register_source(ext, ImageOpenSource)
