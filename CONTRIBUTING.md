# Contributing to CAO

Thank you for your interest in contributing to CAO (Convert Anything Offline)! This project is designed to be clean, extensible, and offline-first. Contributions are welcome in the form of new converters, plugin tools, bug fixes, documentation, and feature ideas.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Creating a Source](#creating-a-source)
- [Creating a Target](#creating-a-target)
- [Plugin-Based Converters](#plugin-based-converters)
- [Code Style](#code-style)
- [Opening a Pull Request](#opening-a-pull-request)

---

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/cao.git
   cd cao
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -e .
   ```

4. Test that it works:

   ```bash
   cao --help
   ```

---

## Project Structure

```
cao/
├── sources/
│   ├── image/
│   ├── geospatial/
│   └── text/
├── targets/
│   ├── image/
│   ├── geospatial/
│   └── text/
├── plugins/
├── engine.py
├── registry.py
├── cli.py
```

Each format (or format group) has its own source and target implementation.

---

## Creating a Source

To create a new source (a file reader), subclass `BaseSource`:

```python
from cao.sources.base import BaseSource
from cao.registry import ConverterRegistry

class MyCustomSource(BaseSource):
    def extract(self, path):
        return {"type": "text", "data": open(path).read()}

    @classmethod
    def supported_extensions(cls):
        return ["xyz"]

    @classmethod
    def data_type(cls):
        return "text"
```

- `supported_extensions()` returns a list of file extensions this source supports.
- `data_type()` is required for CLI introspection and compatibility checks. It must return a string that matches the data types your targets will accept.

Register it:

```python
ConverterRegistry.register_source("xyz", MyCustomSource)
```

---

## Creating a Target

To create a new target (a file writer), subclass `BaseTarget`:

```python
from cao.targets.base import BaseTarget
from cao.registry import ConverterRegistry

class MyCustomTarget(BaseTarget):
    def write(self, data, path):
        with open(path, "w") as f:
            f.write(data["data"].upper())

    @staticmethod
    def accepts_type(data_type):
        return data_type == "text"
```

Register it:

```python
ConverterRegistry.register_target("abc", lambda ext: MyCustomTarget(ext))
```

---

## Plugin-Based Converters

You can build sources and targets as standalone `.py` files or bundles and load them using:

```bash
cao plugin install ./my_converter.py
```

All plugin converters must follow the same interface as above and use `ConverterRegistry.register_source` or `register_target`.

You can also remove or reload plugins:

```bash
cao plugin remove my_converter
cao plugin reload
```

---

## Code Style

- Follow PEP8 for Python formatting.
- One class per file is strongly encouraged.
- Group related converters into folders (e.g., `geospatial`, `image`, `text`).
- Keep debug or logging output behind a flag if needed.
- Keep source and target logic cleanly separated.

---

## Opening a Pull Request

1. Fork the repository.
2. Create a new branch for your contribution.
3. Make your changes and write a clear commit message.
4. Ensure the project still installs and `cao --help` works.
5. Open a pull request with a description of what you added and why.

We appreciate all clean, thoughtful contributions that improve CAO’s capabilities or architecture.

---

Thanks for contributing!
