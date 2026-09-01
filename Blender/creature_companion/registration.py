import bpy
import os


creaturetime_dir = os.path.dirname(__file__)
plugin_dir = os.path.dirname(creaturetime_dir)


# Context for plugin.
class _RegistrationContext:
    def __init__(self):
        self.registerable_objects = set()

_context = _RegistrationContext()

def register_class(cls):
    _context.registerable_objects.add(cls)
    return cls


def register():
    for cls in _context.registerable_objects:
        print(f'-- Registered class - {cls}')
        bpy.utils.register_class(cls)


def unregister():
    for cls in _context.registerable_objects:
        print(f'-- Unregistered class - {cls}')
        bpy.utils.unregister_class(cls)
    _context.registerable_objects.clear()