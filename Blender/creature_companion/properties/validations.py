import bpy

from .. import registration


@registration.register_class
class CREATURETIME_Validation(bpy.types.PropertyGroup):
    """Validation properties."""

    # name: StringProperty() -> Instantiated by default
    id: bpy.props.IntProperty(default=-1)
    validate: bpy.props.BoolProperty()


@registration.register_class
class CREATURETIME_Error(bpy.types.PropertyGroup):
    """Validation error properties."""

    # name: StringProperty() -> Instantiated by default
    validation_id: bpy.props.IntProperty(default=-1)
    error_id: bpy.props.IntProperty(default=-1)
    icon_value: bpy.props.IntProperty(default=-1)


@registration.register_class
class CREATURETIME_VrcAvatarContext(bpy.types.PropertyGroup):
    """Validation context properties."""

    # name: StringProperty() -> Instantiated by default
    is_avatar_release: bpy.props.BoolProperty(name='Is Avatar Release', default=False)
    avatar_name: bpy.props.StringProperty(name='Avatar Name', default='')
    version_major: bpy.props.IntProperty(default=1)
    version_minor: bpy.props.IntProperty(default=0)
    version_patch: bpy.props.IntProperty(default=0)


def register():
    # Set up validation properties
    scene = bpy.types.Scene
    scene.validations = bpy.props.CollectionProperty(type=CREATURETIME_Validation)
    scene.validation_index = bpy.props.IntProperty(name='Active Validation Index')
    scene.errors = bpy.props.CollectionProperty(type=CREATURETIME_Error)
    scene.error_index = bpy.props.IntProperty(name='Active Error Index')

    scene.vrc_avatar_context = bpy.props.PointerProperty(type=CREATURETIME_VrcAvatarContext)


def unregister():
    # Tear down scene properties
    scene = bpy.types.Scene
    del scene.validations
    del scene.validation_index
    del scene.errors
    del scene.error_index
    del scene.vrc_avatar_context