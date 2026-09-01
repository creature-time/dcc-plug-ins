import inspect
import os

import bpy

import creaturetime
from creaturetime.operators.validations import props
from creaturetime.operators.validations import operators
from creaturetime.operators.validations.validation import Validation


@bpy.app.handlers.persistent
def load_validations(*args, **kwargs):
    scene = bpy.context.scene
    scene.errors.clear()
    scene.validations.clear()
    for idx, val in enumerate(operators.VALIDATIONS):
        item = scene.validations.add()
        item.name = val.NAME
        item.id = idx
        item.validate = True


def _discover_validations():
    root = os.path.join(os.path.dirname(__file__), 'validators')

    files = os.listdir(root)
    if '__init__.py' in files:
        files.remove('__init__.py')

    for file in files:
        filepath = os.path.join(root, file)
        if not os.path.isfile(filepath):
            continue

        if not os.path.splitext(filepath)[1] == '.py':
            continue

        relpath = os.path.relpath(root, os.path.dirname(creaturetime.__file__)).replace(os.sep, '.')

        basename, _ = os.path.splitext(file)
        module_path = f'creaturetime.{relpath}.{basename}'
        file_path = os.path.join(root, file)

        validation_module = creaturetime.load_module(module_path, file_path)
        for name, obj in inspect.getmembers(validation_module, inspect.isclass):
            if issubclass(obj, Validation) and obj is not Validation:
                print(f'Discovered validation: {name}')
                operators.VALIDATIONS.append(obj())

    operators.VALIDATIONS.sort(key=lambda x: x.NAME)

def register():
    _discover_validations()

    # Set up validation properties
    scene = bpy.types.Scene
    scene.validations = bpy.props.CollectionProperty(type=props.CREATURETIME_Validation)
    scene.validation_index = bpy.props.IntProperty(name='Active Validation Index')
    scene.errors = bpy.props.CollectionProperty(type=props.CREATURETIME_Error)
    scene.error_index = bpy.props.IntProperty(name='Active Error Index')

    scene.vrc_avatar_context = bpy.props.PointerProperty(type=props.CREATURETIME_VrcAvatarContext)

    bpy.app.handlers.load_post.append(load_validations)


def unregister():
    bpy.app.handlers.load_post.remove(load_validations)

    # Tear down scene properties
    scene = bpy.types.Scene
    del scene.validations
    del scene.validation_index
    del scene.errors
    del scene.error_index
    del scene.vrc_avatar_context

    operators.VALIDATIONS.clear()