import bpy

from .. import resources
from ..operators import vertex_groups


def apply_operators(self, _):
    layout = self.layout
    layout.operator(vertex_groups.RemoveUnusedVertexGroups.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.separator()


def register():
    bpy.types.MESH_MT_vertex_group_context_menu.prepend(apply_operators)


def unregister():
    bpy.types.MESH_MT_vertex_group_context_menu.remove(apply_operators)