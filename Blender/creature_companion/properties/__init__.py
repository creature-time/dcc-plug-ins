import bpy


from . import validations
from . import avatar_tools


def register():
    validations.register()
    avatar_tools.register()


def unregister():
    validations.unregister()
    avatar_tools.unregister()