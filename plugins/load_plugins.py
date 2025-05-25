import importlib.util
import os
import sys
from typing import List, Type, TypeVar

PLUGIN_FOLDER = os.path.dirname(os.path.abspath(__file__))

T = TypeVar('T')

def load_plugins(plugin_base_class: Type[T]) -> List[T]:
    plugins = []
    for filename in os.listdir(PLUGIN_FOLDER):
        if filename.endswith(".plugin.py"):
            module_name = filename[:-3]
            module_path = os.path.join(PLUGIN_FOLDER, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")
                    continue
                # Find plugin classes in the module
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, plugin_base_class)
                        and attr is not plugin_base_class
                    ):
                        try:
                            plugin_instance = attr()
                            plugins.append(plugin_instance)
                        except Exception as e:
                            print(f"Failed to instantiate plugin {attr_name}: {e}")
    return plugins