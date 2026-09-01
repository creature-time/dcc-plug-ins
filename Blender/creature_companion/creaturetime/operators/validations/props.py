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


class CREATURETIME_VrcAvatarContext(bpy.types.PropertyGroup):
    """Validation context properties."""

    # name: StringProperty() -> Instantiated by default
    is_avatar_release: bpy.props.BoolProperty(name='Is Avatar Release', default=False)
    avatar_name: bpy.props.StringProperty(name='Avatar Name', default='')
    version_major: bpy.props.IntProperty(default=1)
    version_minor: bpy.props.IntProperty(default=0)
    version_patch: bpy.props.IntProperty(default=0)