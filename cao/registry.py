import os
import sys
import shutil
import zipfile
import importlib.util

class ConverterRegistry:
    sources = {}
    targets = {}

    @classmethod
    def register_source(cls, ext, klass):
        cls.sources[ext.lower()] = klass

    @classmethod
    def register_target(cls, ext, factory_fn):
        cls.targets[ext.lower()] = factory_fn

    @classmethod
    def get_source(cls, ext):
        return cls.sources.get(ext.lower())

    @classmethod
    def get_target(cls, ext):
        factory = cls.targets.get(ext.lower())
        return factory(ext) if factory else None

    @classmethod
    def list_possible_targets(cls, ext):
        source = cls.get_source(ext)
        if not source:
            return []

        try:
            dummy_data = source().extract("dummy.fake")
        except:
            return []

        data_type = dummy_data["type"]
        compatible = []
        for ext, factory in cls.targets.items():
            try:
                target = factory(ext)
                if target.accepts_type(data_type):
                    compatible.append(ext)
            except:
                continue

        return compatible

    @classmethod
    def _plugin_dir(cls):
        return os.path.join(os.path.dirname(__file__), "plugins")

    @classmethod
    def load_plugins(cls):
        """Dynamically loads all plugins from the 'plugins' folder."""
        plugin_dir = cls._plugin_dir()

        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)

        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"cao.plugins.{filename[:-3]}"
                module_path = os.path.join(plugin_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"[WARN] Failed to load plugin {module_name}: {e}")

    @classmethod
    def list_plugins(cls):
        plugin_dir = cls._plugin_dir()
        if not os.path.exists(plugin_dir):
            return []
        return [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    @classmethod
    def install_plugin(cls, plugin_path):
        plugin_dir = cls._plugin_dir()

        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)

        if plugin_path.endswith(".py"):
            dest_path = os.path.join(plugin_dir, os.path.basename(plugin_path))
            shutil.copy(plugin_path, dest_path)
            return f"Plugin '{os.path.basename(plugin_path)}' installed successfully!"

        elif plugin_path.endswith(".zip"):
            with zipfile.ZipFile(plugin_path, 'r') as zip_ref:
                zip_ref.extractall(plugin_dir)
            return f"Plugin package '{os.path.basename(plugin_path)}' installed successfully!"

        else:
            return "Invalid plugin format. Please provide a .py or .zip file."

    @classmethod
    def remove_plugin(cls, plugin_name):
        plugin_path = os.path.join(cls._plugin_dir(), f"{plugin_name}.py")

        if not os.path.exists(plugin_path):
            return f"Plugin '{plugin_name}' not found."

        try:
            os.remove(plugin_path)
            return f"Plugin '{plugin_name}' removed successfully."
        except Exception as e:
            return f"Failed to remove plugin '{plugin_name}': {e}"

    @classmethod
    def bundle_plugins(cls, output_zip_path="cao_plugins_bundle.zip"):
        plugin_dir = cls._plugin_dir()
        if not os.path.exists(plugin_dir):
            return "No plugins to bundle."

        with zipfile.ZipFile(output_zip_path, "w") as zipf:
            for filename in os.listdir(plugin_dir):
                if filename.endswith(".py") and filename != "__init__.py":
                    zipf.write(os.path.join(plugin_dir, filename), filename)
        return f"Plugins bundled into '{output_zip_path}'."

# 🔍 Auto-load all core sources/targets
def _load_all_converters_from(folder_name):
    base_dir = os.path.dirname(__file__)
    target_dir = os.path.join(base_dir, folder_name)

    for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith(".py") and filename not in ["__init__.py", "base.py"]:
                module_path = os.path.join(root, filename)

                # Convert path to Python import path
                rel_path = os.path.relpath(module_path, base_dir)
                import_path = rel_path.replace(os.sep, ".")[:-3]  # Strip .py

                try:
                    spec = importlib.util.spec_from_file_location(import_path, module_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[import_path] = module
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"[WARN] Failed to auto-load converter {import_path}: {e}")

def load_core_converters():
    _load_all_converters_from("sources")
    _load_all_converters_from("targets")
