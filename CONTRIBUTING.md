# Contributing to CAO

Thanks for your interest in contributing to CAO — **Convert Anything Offline**. Whether you're fixing a bug, adding a new converter, improving docs, or building a plugin, you're helping make CAO better for everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Creating Converters](#creating-converters)
  - [Sources](#sources)
  - [Targets](#targets)
- [Plugins](#plugins)
- [Testing Your Contribution](#testing-your-contribution)
- [Pull Requests](#pull-requests)

---

## Code of Conduct

We expect contributors to follow basic standards of professionalism, respect, and collaboration. Be kind, helpful, and constructive.

---

## Getting Started

1. **Fork the repo** and clone your fork.
2. Set up the dev environment:

```bash
git clone https://github.com/your-username/cao.git
cd cao
pip install -e .
```

> You must have Python 3.8+ installed. Dependencies include `click`, `Pillow`, and optionally others depending on your plugin.

---

## Project Structure

```
cao/
├── cli.py                  # CLI entry point
├── registry.py             # Core registry for sources/targets/plugins
├── engine.py               # File conversion logic
├── sources/                # Organized by category (e.g., image/, text/)
├── targets/                # Organized by category
├── plugins/                # User-installed plugins
├── tests/                  # (optional) Unit tests
├── setup.py
├── pyproject.toml
```

---

## Creating Converters

### Sources

Sources extract raw content from a specific file type (e.g. PNG, TXT, DOCX).

1. Create a file in `cao/sources/<category>/your_source.py`
2. Subclass `BaseSource`
3. Implement the `extract(path)` method
4. Register with `ConverterRegistry.register_source("ext", YourSource)`

Example:

```python
from cao.sources.base import BaseSource
from cao.registry import ConverterRegistry

class PNGSource(BaseSource):
    def extract(self, path):
        from PIL import Image
        img = Image.open(path)
        return {"type": "image", "data": img}

ConverterRegistry.register_source("png", PNGSource)
```

### Targets

Targets take extracted content and write it to a specific file format.

1. Create a file in `cao/targets/<category>/your_target.py`
2. Subclass `BaseTarget`
3. Implement:
   - `write(data, path)`
   - `accepts_type(data_type)`
4. Register with `ConverterRegistry.register_target("ext", lambda ext: YourTarget(ext))`

Example:

```python
from cao.targets.base import BaseTarget
from cao.registry import ConverterRegistry

class JPGTarget(BaseTarget):
    def __init__(self, format):
        self.format = format

    def write(self, data, path):
        data["data"].save(path, format="JPEG")

    @staticmethod
    def accepts_type(data_type):
        return data_type == "image"

ConverterRegistry.register_target("jpg", lambda ext: JPGTarget(ext))
```

---

## Plugins

You can build a plugin by creating a `.py` file that registers a new source or target using the `ConverterRegistry`.

To install:
```bash
cao plugin install ./your_plugin.py
```

To test:
```bash
cao convert input.yourformat output.target
```

To remove:
```bash
cao plugin remove your_plugin
```

To bundle:
```bash
cao plugin bundle my_plugins.zip
```

---

## Testing Your Contribution

Run basic conversion commands manually:

```bash
cao convert input.png output.jpg
cao from png
cao plugin list
```

For automated testing, you may place test files in a future `tests/` directory and use `pytest`.

---

## Pull Requests

1. Fork the repo and create a new branch.
2. Commit your changes with clear messages.
3. Submit a pull request describing:
   - What you added/changed
   - Why it’s useful
   - How to test it (if applicable)

We’ll review your PR and may request changes or merge it.

---

Thanks for contributing to CAO!
