import bpy


class CREATURETIME_Validation(bpy.types.PropertyGroup):
    """Validation properties."""

    # name: StringProperty() -> Instantiated by default
    id: bpy.props.IntProperty(default=-1)
    validate: bpy.props.BoolProperty()


class CREATURETIME_Error(bpy.types.PropertyGroup):
    """Validation error properties."""

    # name: StringProperty() -> Instantiated by default
    validation_id: bpy.props.IntProperty(default=-1)
    error_id: bpy.props.IntProperty(default=-1)
    icon_value: bpy.props.IntProperty(default=-1)