import bpy

from creaturetime import constants
from creaturetime import resources


# Store all validations (populated during registration)
VALIDATIONS = []

def validate_item(context, wm, item, validation):
    validation.reset()
    validation.validate(context, wm)

    # Populate errors/warnings
    if validation.has_errors():
        error_icon_id = resources.get('error_x16').icon_id
        warning_icon_id = resources.get('warning_x16').icon_id
        for (error_id, error_type, message, repair) in validation.iter_errors():
            error_item = wm.errors.add()
            error_item.name = message
            error_item.icon_value = error_icon_id if error_type else warning_icon_id
            error_item.validation_id = item.id
            error_item.error_id = error_id


class CREATURETIME_OT_ValidateAllActions(bpy.types.Operator):
    """Performs validation on all validation"""

    bl_idname = constants.generate_id('validation_validate_all')
    bl_label = "Validate All"
    bl_description = "Run all validations"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        wm = bpy.context.window_manager
        for item in wm.validations:
            if item.validate:
                return True
        return False

    def invoke(self, context, event):
        wm = bpy.context.window_manager

        # Clear out previous errors
        wm.errors.clear()

        for idx, item in enumerate(wm.validations):
            if not item.validate:
                continue
            validation = VALIDATIONS[idx]
            validate_item(context, wm, item, validation)

        return {"FINISHED"}


class CREATURETIME_OT_ValidateActions(bpy.types.Operator):
    """Performs validation on selected validation"""

    bl_idname = constants.generate_id('validation_validate')
    bl_label = "Validate"
    bl_description = "Run selected validation"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        wm = bpy.context.window_manager
        try:
            wm.validations[wm.validation_index]
        except IndexError:
            return False
        else:
            return True

    def invoke(self, context, event):
        wm = bpy.context.window_manager

        try:
            item = wm.validations[wm.validation_index]
        except IndexError:
            pass
        else:
            # Clear out previous errors
            wm.errors.clear()

            # Run Validation
            validation = VALIDATIONS[item.id]
            validate_item(context, wm, item, validation)

        return {"FINISHED"}


class CREATURETIME_OT_RepairAllActions(bpy.types.Operator):
    """Performs repair on selected error"""

    bl_idname = constants.generate_id('validation_repair_all')
    bl_label = "Repair All"
    bl_description = "Repair all errors"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = bpy.context.window_manager
        for item in wm.errors:
            validation = VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                return True
        return False

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        to_remove = []
        for index, item in enumerate(wm.errors):
            validation = VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                if validation.repair(item.error_id):
                    to_remove.insert(0, index)
                    continue
            index += 1

        for index in to_remove:
            wm.errors.remove(index)

        return {"FINISHED"}


class CREATURETIME_OT_RepairActions(bpy.types.Operator):
    """Performs repair on selected error"""

    bl_idname = constants.generate_id('validation_repair')
    bl_label = "Repair"
    bl_description = "Repair selected error"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        wm = bpy.context.window_manager
        try:
            item = wm.errors[wm.error_index]
        except IndexError:
            return False
        else:
            validation = VALIDATIONS[item.validation_id]
            return validation.has_repair(item.error_id)

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        try:
            item = wm.errors[wm.error_index]
        except IndexError:
            pass
        else:
            validation = VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                if validation.repair(item.error_id):
                    wm.errors.remove(wm.error_index)
                else:
                    raise Exception('Failed to repair - %s' % item.name)

        return {"FINISHED"}
