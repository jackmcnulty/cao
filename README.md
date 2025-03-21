# CAO — Convert Anything Offline

CAO is a modular, offline-first command-line tool that lets you convert files between hundreds of formats — including images, text, geospatial and (soon) more. It's designed to be clean, extensible, and completely offline with full plugin support.

---

## Features

- Offline support — no internet required, ever
- Image conversions (e.g., `png → jpg`, `webp → png`, etc.)
- Geospatial data conversions (e.g., `shp → geojson`, etc.)
- Text export from images or plain text
- Plugin system for adding your own converters
- Auto-discovery of sources and targets
- ZIP plugin bundling and importing

---

## Installation

```bash
git clone https://github.com/your-username/cao.git
cd cao
pip install -e .
```

You must be using Python 3.8+ and have `pip`, `click`, and `Pillow` installed.

---

## Usage Overview

### Convert a file

```bash
cao convert input.png output.jpg
cao convert input.png output.txt
```

### See what you can convert from a file type

```bash
cao from png
```

Example output:

```
You can convert 'png' into:
- bmp
- ico
- jpeg
- jpg
- png
- tiff
- txt
- webp
```

---

## Plugin System

CAO supports a powerful offline plugin system.

### Plugin Commands

| Command                            | Description                              |
|------------------------------------|------------------------------------------|
| `cao plugin list`                 | List all installed plugins               |
| `cao plugin install <path>`       | Install a plugin from `.py` or `.zip`    |
| `cao plugin remove <name>`        | Uninstall a plugin by name               |
| `cao plugin reload`               | Reload all plugins without restarting    |
| `cao plugin bundle [file]`        | Create a `.zip` of all installed plugins |

### Installing a Plugin

```bash
cao plugin install ./plugins/my_plugin.py
```

Or install a bundle of plugins:

```bash
cao plugin install ./cao_plugins_bundle.zip
```

### Listing Installed Plugins

```bash
cao plugin list
```

### Removing a Plugin

```bash
cao plugin remove my_plugin
```

### Reloading Plugins

```bash
cao plugin reload
```

### Bundling Plugins

```bash
cao plugin bundle my_bundle.zip
```

---

## Creating Your Own Plugin

### 1. Create a Python file like this:

```python
from cao.registry import ConverterRegistry

class MySource:
    def extract(self, path):
        return {"type": "text", "data": "Hello from plugin!"}

ConverterRegistry.register_source("my", MySource)

class MyTarget:
    @staticmethod
    def accepts_type(data_type):
        return data_type == "text"

    def write(self, data, path):
        with open(path, "w") as f:
            f.write(f"Plugin says: {data['data']}")

ConverterRegistry.register_target("cool", lambda ext: MyTarget())
```

### 2. Install it

```bash
cao plugin install ./my_plugin.py
```

### 3. Use it

```bash
cao convert input.my output.cool
```

---

## Project Structure (Simplified)

```
cao/
├── cli.py                  ← CLI entry point
├── registry.py             ← Converter & plugin manager
├── engine.py               ← Core conversion logic
├── sources/                ← Organized by type (image/, text/, etc.)
├── targets/                ← Organized by type (image/, text/, etc.)
├── plugins/                ← User-added plugin folder
├── setup.py
├── pyproject.toml
```

---

## Contributing

- All sources should inherit from `BaseSource`
- All targets should inherit from `BaseTarget`
- Register converters using `ConverterRegistry.register_source()` or `register_target()`

We welcome contributions and plugin creators.

---

## Coming Soon

- PDF support
- DOCX/Text document pipelines
- Audio conversion family
- Web UI for plugin browsing

---

## Credits

Built with inspiration from tools like ImageMagick, ffmpeg, and Pandoc — but offline, modular, and Pythonic.

---

## License

MIT License. Use it, hack it, ship it.
