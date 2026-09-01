import bpy

from .. import resources
from ..operators import shape_keys
from ..validations import validation_registry


@bpy.app.handlers.persistent
def load_validations(*args, **kwargs):
    scene = bpy.context.scene
    scene.errors.clear()
    scene.validations.clear()
    for idx, val in enumerate(validation_registry.VALIDATIONS):
        item = scene.validations.add()
        item.name = val.NAME
        item.id = idx
        item.validate = True


def apply_operators(self, _):
    layout = self.layout
    layout.operator(shape_keys.RemoveUnusedShapeKeys.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(shape_keys.ApplyShapeKeyAsBasis.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.operator(shape_keys.SelectAffectedShapeKeyVertices.bl_idname, icon_value=resources.get('default_white_x16').icon_id)
    layout.separator()


def register():
    bpy.app.handlers.load_post.append(load_validations)


def unregister():
    bpy.app.handlers.load_post.remove(load_validations)