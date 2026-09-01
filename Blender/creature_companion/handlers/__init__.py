import bpy

from . import validations


def register():
    validations.register()


def unregister():
    validations.unregister()