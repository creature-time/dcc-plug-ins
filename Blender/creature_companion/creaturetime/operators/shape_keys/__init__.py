import bpy

from creaturetime import resources
from creaturetime.operators.shape_keys import operators


def apply_operators(self, _):
    layout = self.layout
    layout.operator(operators._RemoveUnusedShapeKeys.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(operators._ApplyShapeKeyAsBasis.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(operators._SelectAffectedShapeKeyVertices.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.separator()


def register():
    bpy.types.MESH_MT_shape_key_context_menu.prepend(apply_operators)


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(apply_operators)
