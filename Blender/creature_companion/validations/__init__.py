import bpy

from . import validation_registry
from . import validators


def register():
    validation_registry.register()


def unregister():
    validation_registry.unregister()