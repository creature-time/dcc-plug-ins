import bpy

from creaturetime import resources
from creaturetime.operators.vertex_groups import operators


def apply_operators(self, _):
    layout = self.layout
    layout.operator(operators._RemoveUnusedVertexGroups.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.separator()


def register():
    # bpy.utils.register_class(_RemoveUnusedVertexGroups)

    bpy.types.MESH_MT_vertex_group_context_menu.prepend(apply_operators)


def unregister():
    bpy.types.MESH_MT_vertex_group_context_menu.remove(apply_operators)

    # bpy.utils.unregister_class(_RemoveUnusedVertexGroups)
