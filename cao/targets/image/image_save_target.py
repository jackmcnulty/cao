from cao.targets.base import BaseTarget
from cao.registry import ConverterRegistry

class ImageSaveTarget(BaseTarget):
    supported_formats = ["jpg", "jpeg", "png", "webp", "bmp", "ico", "tiff"]

    def __init__(self, format):
        self.format = format.lower()

    def write(self, data, path, options=None):
        options = options or {}
        if options:
            raise ValueError(f"Image does not accept any options at this moment. Submit a PR to add support for options.")
        data["data"].save(path, format=self.format.upper())

    @staticmethod
    def accepts_type(data_type):
        return data_type == "image"

for ext in ImageSaveTarget.supported_formats:
    ConverterRegistry.register_target(ext, lambda ext=ext: ImageSaveTarget(ext))
