import bpy

from . import shape_keys
from . import vertex_groups


def register():
    shape_keys.register()
    vertex_groups.register()


def unregister():
    shape_keys.unregister()
    vertex_groups.unregister()