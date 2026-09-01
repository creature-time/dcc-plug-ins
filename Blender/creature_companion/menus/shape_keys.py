import bpy

from .. import resources
from ..operators import shape_keys


def apply_operators(self, _):
    layout = self.layout
    layout.operator(shape_keys.RemoveUnusedShapeKeys.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(shape_keys.ApplyShapeKeyAsBasis.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(shape_keys.SelectAffectedShapeKeyVertices.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.separator()


def register():
    bpy.types.MESH_MT_shape_key_context_menu.prepend(apply_operators)


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(apply_operators)