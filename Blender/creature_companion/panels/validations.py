import bpy

from .. import resources
from .common import Ct_Panel
from .. import registration
from ..operators import validations


@registration.register_class
class CREATURETIME_UL_Validations(bpy.types.UIList):
    """Display validation."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        layout.prop(item, "validate", text='')
        layout.label(text=item.name)

    def invoke(self, context, event):
        pass


@registration.register_class
class CREATURETIME_UL_Errors(bpy.types.UIList):
    """Display errors."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        layout.label(text=item.name, icon_value=item.icon_value)

    def invoke(self, context, event):
        pass


@registration.register_class
class VIEW3D_PT_Validator(Ct_Panel):
    """Validations panel."""

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Validator'
    bl_category = 'CreatureTime'

    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout

        # Display validations.
        layout_validations = self._create_section(layout, text='Validation', icon_value=resources.get('validate_x16').icon_id)

        row = layout_validations.row()
        row.template_list(CREATURETIME_UL_Validations.__name__,
                          'validation_validations',
                          scene, 'validations',
                          scene, 'validation_index',
                          rows=5)

        col = row.column(align=True)
        col.operator(validations.CREATURETIME_OT_ValidateAllActions.bl_idname,
                     text="",
                     icon_value=resources.get('validate_x16').icon_id)
        col.operator(validations.CREATURETIME_OT_ValidateActions.bl_idname,
                     text="",
                     icon_value=resources.get('validate_x16').icon_id)

        # Display results.
        layout_results = self._create_section(layout, text='Results', icon_value=resources.get('repair_x16').icon_id)
        row = layout_results.row()
        row.template_list(CREATURETIME_UL_Errors.__name__,
                          'validation_errors',
                          scene, 'errors',
                          scene, 'error_index',
                          rows=5)

        col = row.column(align=True)
        col.operator(validations.CREATURETIME_OT_RepairAllActions.bl_idname,
                     text="",
                     icon_value=resources.get('repair_x16').icon_id)
        col.operator(validations.CREATURETIME_OT_RepairActions.bl_idname,
                     text="",
                     icon_value=resources.get('repair_x16').icon_id)


class VIEW3D_PT_VrcAvatarContext(Ct_Panel):
    """Vrc Avatar Context panel."""

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Vrc Avatars'
    bl_category = 'CreatureTime'
    bl_order = 100
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout

        # Display avatar settings.
        layout_validation_context = self._create_section(layout, text='Vrc Avatars',
                                                         icon_value=resources.get('default_white_x16').icon_id)

        row = layout_validation_context.row()
        row.prop(scene.vrc_avatar_context, 'is_avatar_release')

        if scene.vrc_avatar_context.is_avatar_release:
            row = layout_validation_context.row()
            row.prop(scene.vrc_avatar_context, 'avatar_name', placeholder='Avatar name...')

            row = layout_validation_context.row(align=True)
            row.alignment = 'EXPAND'
            row.label(text='Version')
            row = row.row()
            row.alignment = 'RIGHT'
            row.prop(scene.vrc_avatar_context, 'version_major', text='')
            row.label(text='.')
            row.prop(scene.vrc_avatar_context, 'version_minor', text='')
            row.label(text='.')
            row.prop(scene.vrc_avatar_context, 'version_patch', text='')