# import bpy
# import os
# import importlib.util
# import sys
#
# plugin_dir = os.path.dirname(__file__)
#
# def load_module(module_name, file_path):
#     submodule_search_locations = [plugin_dir]
#     print(f'-- Discovered {module_name} at {file_path} (submodule_search_locations={submodule_search_locations}).')
#     spec = importlib.util.spec_from_file_location(module_name, file_path, submodule_search_locations=submodule_search_locations)
#     module = importlib.util.module_from_spec(spec)
#     sys.modules[module_name] = module
#     spec.loader.exec_module(module)
#     return module