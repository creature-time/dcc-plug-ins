import bpy

from creaturetime.operators.avatar_tools import props


def register():
    object_type = bpy.types.Object
    object_type.ct_avatar_tools = bpy.props.PointerProperty(type=props.CtAvatarToolsProperties)

def unregister():
    object_type = bpy.types.Object
    del object_type.ct_avatar_tools
