import bpy

from creaturetime import resources
from creaturetime.operators.common import Ct_Panel


class CREATURETIME_UL_Validations(bpy.types.UIList):
    """Display validation."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        layout.prop(item, "validate", text='')
        layout.label(text=item.name)

    def invoke(self, context, event):
        pass


class CREATURETIME_UL_Errors(bpy.types.UIList):
    """Display errors."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index):
        layout.label(text=item.name, icon_value=item.icon_value)

    def invoke(self, context, event):
        pass

class VIEW3D_PT_Validator(Ct_Panel):
    """Validations panel."""

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Validator'
    bl_category = 'CreatureTime'

    def draw(self, context):
        wm = bpy.context.window_manager
        layout = self.layout

        # Display validations.
        layout_validations = self._create_section(layout, text='Validation', icon_value=resources.get('validate_x16').icon_id)

        row = layout_validations.row()
        row.template_list(CREATURETIME_UL_Validations.__name__,
                          'validation_validations',
                          wm, 'validations',
                          wm, 'validation_index',
                          rows=5)

        from creaturetime.operators.validations import operators
        col = row.column(align=True)
        col.operator(operators.CREATURETIME_OT_ValidateAllActions.bl_idname,
                     text="",
                     icon_value=resources.get('validate_x16').icon_id)
        col.operator(operators.CREATURETIME_OT_ValidateActions.bl_idname,
                     text="",
                     icon_value=resources.get('validate_x16').icon_id)

        # Display results.
        layout_results = self._create_section(layout, text='Results', icon_value=resources.get('repair_x16').icon_id)
        row = layout_results.row()
        row.template_list(CREATURETIME_UL_Errors.__name__,
                          'validation_errors',
                          wm, 'errors',
                          wm, 'error_index',
                          rows=5)

        col = row.column(align=True)
        col.operator(operators.CREATURETIME_OT_RepairAllActions.bl_idname,
                     text="",
                     icon_value=resources.get('repair_x16').icon_id)
        col.operator(operators.CREATURETIME_OT_RepairActions.bl_idname,
                     text="",
                     icon_value=resources.get('repair_x16').icon_id)