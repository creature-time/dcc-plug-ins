from .common import Ct_Panel
from .. import registration
from ..operators.avatar_tools import (CREATURETIME_OT_AvatarGenerateVrcftVertexGroups,
                                      CREATURETIME_OT_AvatarShapeKeys,
                                      CREATURETIME_OT_AvatarGenerateVrcftShapeKeys)


@registration.register_class
class MESH_PT_CT_AvatarTools(Ct_Panel):
    """Avatar tools panel."""

    bl_label = '[CreatureTime] Avatar Tools'
    bl_idname = 'MESH_PT_CT_AvatarTools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'MESH'

    def draw(self, context):
        active = context.active_object
        ct_avatar_tools = context.object.ct_avatar_tools

        layout = self.layout

        vertex_groups_layout = self._create_section(layout, text='Vertex Groups')

        vertex_groups_layout.prop(ct_avatar_tools, 'vrcft_vertex_groups_repeat')
        vertex_groups_layout.operator(CREATURETIME_OT_AvatarGenerateVrcftVertexGroups.bl_idname,
                                      text=CREATURETIME_OT_AvatarGenerateVrcftVertexGroups.bl_label,
                                      icon='GROUP_VERTEX')

        shape_keys_layout = self._create_section(layout, text='Shape Keys')

        shape_keys_layout.operator(CREATURETIME_OT_AvatarShapeKeys.bl_idname,
                                   text=CREATURETIME_OT_AvatarShapeKeys.bl_label,
                                   icon='SHAPEKEY_DATA')

        vrcft_vertex_groups_row = shape_keys_layout.row(align=True)
        vrcft_vertex_groups_row.prop_search(ct_avatar_tools, 'vrcft_vertex_group_left', active, 'vertex_groups',
                                            text='Masks', icon='TRIA_LEFT')
        vrcft_vertex_groups_row.prop_search(ct_avatar_tools, 'vrcft_vertex_group_right', active, 'vertex_groups',
                                            text='', icon='TRIA_RIGHT')

        shape_keys_layout.prop(ct_avatar_tools, 'vrcft_selected_only', text='Only Selected')
        shape_keys_layout.operator(CREATURETIME_OT_AvatarGenerateVrcftShapeKeys.bl_idname,
                                   text=CREATURETIME_OT_AvatarGenerateVrcftShapeKeys.bl_label,
                                   icon='SHAPEKEY_DATA')
