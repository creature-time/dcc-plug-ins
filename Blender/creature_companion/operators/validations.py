import bpy

from .. import constants
from .. import registration
from .. import resources
from ..validations import validation_registry


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


@registration.register_class
class CREATURETIME_OT_ValidateAllActions(bpy.types.Operator):
    """Performs validation on all validation"""

    bl_idname = constants.generate_id('validation_validate_all')
    bl_label = "Validate All"
    bl_description = "Run all validations"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        for item in scene.validations:
            if item.validate:
                return True
        return False

    def invoke(self, context, event):
        scene = bpy.context.scene

        # Clear out previous errors
        scene.errors.clear()

        for idx, item in enumerate(scene.validations):
            if not item.validate:
                continue
            validation = validation_registry.VALIDATIONS[idx]
            validate_item(context, scene, item, validation)

        return {"FINISHED"}


@registration.register_class
class CREATURETIME_OT_ValidateActions(bpy.types.Operator):
    """Performs validation on selected validation"""

    bl_idname = constants.generate_id('validation_validate')
    bl_label = "Validate"
    bl_description = "Run selected validation"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        try:
            scene.validations[scene.validation_index]
        except IndexError:
            return False
        else:
            return True

    def invoke(self, context, event):
        scene = bpy.context.scene

        try:
            item = scene.validations[scene.validation_index]
        except IndexError:
            pass
        else:
            # Clear out previous errors
            scene.errors.clear()

            # Run Validation
            validation = validation_registry.VALIDATIONS[item.id]
            validate_item(context, scene, item, validation)

        return {"FINISHED"}


@registration.register_class
class CREATURETIME_OT_RepairAllActions(bpy.types.Operator):
    """Performs repair on selected error"""

    bl_idname = constants.generate_id('validation_repair_all')
    bl_label = "Repair All"
    bl_description = "Repair all errors"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        for item in scene.errors:
            validation = validation_registry.VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                return True
        return False

    def invoke(self, context, event):
        scene = bpy.context.scene
        to_remove = []
        for index, item in enumerate(scene.errors):
            validation = validation_registry.VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                if validation.repair(item.error_id):
                    to_remove.insert(0, index)
                    continue
            index += 1

        for index in to_remove:
            scene.errors.remove(index)

        return {"FINISHED"}


@registration.register_class
class CREATURETIME_OT_RepairActions(bpy.types.Operator):
    """Performs repair on selected error"""

    bl_idname = constants.generate_id('validation_repair')
    bl_label = "Repair"
    bl_description = "Repair selected error"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = bpy.context.scene
        try:
            item = scene.errors[scene.error_index]
        except IndexError:
            return False
        else:
            validation = validation_registry.VALIDATIONS[item.validation_id]
            return validation.has_repair(item.error_id)

    def invoke(self, context, event):
        scene = bpy.context.scene
        try:
            item = scene.errors[scene.error_index]
        except IndexError:
            pass
        else:
            validation = validation_registry.VALIDATIONS[item.validation_id]
            if validation.has_repair(item.error_id):
                if validation.repair(item.error_id):
                    scene.errors.remove(scene.error_index)
                else:
                    raise Exception('Failed to repair - %s' % item.name)

        return {"FINISHED"}