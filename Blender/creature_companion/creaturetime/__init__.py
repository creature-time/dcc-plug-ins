import bpy
import os
import importlib.util
import sys
import inspect

# Setup plugin.
creaturetime_dir = os.path.dirname(__file__)
plugin_dir = os.path.dirname(creaturetime_dir)
discovery_dir = os.path.join(creaturetime_dir, 'operators')
root_module_path = 'creaturetime'

from creaturetime import resources

def load_module(module_name, file_path):
    submodule_search_locations = [plugin_dir]
    print(f'-- Discovered {module_name} at {file_path} (submodule_search_locations={submodule_search_locations}).')
    spec = importlib.util.spec_from_file_location(module_name, file_path, submodule_search_locations=submodule_search_locations)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _register_classes(module_name, file_path):
    module = load_module(module_name, file_path)

    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, _ALLOWED_CLASSES) and hasattr(obj, 'bl_label') and obj not in _ALLOWED_CLASSES:
            print(f'---- Discovered class: {name}')
            _context.registerable_objects.add(obj)
        elif issubclass(obj, _ALLOWED_STRUCTURES) and obj not in _ALLOWED_STRUCTURES:
            print(f'---- Discovered structure: {name}')
            _context.registerable_objects.add(obj)

# Context for plugin.
class _PluginContext:
    def __init__(self):
        self.registerable_objects = set()
        self.inits = []

_context = _PluginContext()

_ALLOWED_STRUCTURES = (
    bpy.types.PropertyGroup,
    bpy.types.UIList
)

_ALLOWED_CLASSES = (
    bpy.types.Panel,
    bpy.types.Operator,
)

def register():
    sys.path.append(plugin_dir)

    resources.load_resources()

    inits = []
    for root, dirs, files in os.walk(discovery_dir):
        if '__pycache__' in root:
            continue

        relpath = os.path.relpath(root, creaturetime_dir).replace(os.sep, '.')

        if '__init__.py' in files:
            module_path = f'{root_module_path}.{relpath}'
            file_path = os.path.join(root, '__init__.py')
            inits.append((module_path, file_path))
            files.remove('__init__.py')

        for file in files:
            basename, _ = os.path.splitext(file)
            module_path = f'{root_module_path}.{relpath}.{basename}'
            file_path = os.path.join(root, file)
            _register_classes(module_path, file_path)


    for cls in _context.registerable_objects:
        bpy.utils.register_class(cls)

    for module_name, filepath in inits:
        module = load_module(module_name, filepath)
        if not hasattr(module, 'register') or not hasattr(module, 'unregister'):
            del module
            continue
        _context.inits.append(module)
        getattr(module, 'register')()

def unregister():
    for module in _context.inits:
        getattr(module, 'unregister')()
    _context.inits.clear()

    for cls in _context.registerable_objects:
        bpy.utils.unregister_class(cls)
    _context.registerable_objects.clear()

    resources.unload_resources()