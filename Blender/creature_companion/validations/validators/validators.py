import re

import bpy

from ..validation import Validation
from .. import validation_registry


@validation_registry.register_validator
class ObjectNamesValidation(Validation):
    NAME = 'Object => Data Names'

    @staticmethod
    def repair_names(context):
        data, obj = context
        data.name = obj.name
        return True

    def validate(self, context, scene):
        for obj in bpy.data.objects:
            if not isinstance(obj.data, (bpy.types.Mesh, bpy.types.Armature)):
                continue

            mesh = obj.data
            if obj.name != mesh.name:
                self.error(
                    'Name (%s) did not match object name (%s)' % (mesh.name, obj.name),
                    ObjectNamesValidation.repair_names, (mesh, obj))


@validation_registry.register_validator
class BoneNamesValidation(Validation):
    NAME = 'Bone Names'

    @staticmethod
    def repair_names(context):
        bone = context[0]
        name = bone.name
        if ':' in name:
            name = name[name.rfind(':') + 1:]
        if 'Left' in name:
            name = name.replace('Left', '')
            name += '_L'
        if 'Right' in name:
            name = name.replace('Right', '')
            name += '_R'
        if ' ' in name:
            name = name.replace(' ', '')
        bone.name = name

        return True


    def validate(self, context, scene):
        error_msg = 'Bone name (%s) needs to have correct naming convention'

        for obj in bpy.data.objects:
            if not isinstance(obj.data, bpy.types.Armature):
                continue

            armature = obj.data
            for bone in armature.bones:
                if ':' in bone.name:
                    self.error(error_msg % bone.name, BoneNamesValidation.repair_names, bone)
                    continue

                if ' ' in bone.name:
                    self.error(error_msg % bone.name, BoneNamesValidation.repair_names, bone)
                    continue

                if 'Left' in bone.name:
                    self.error(error_msg % bone.name, BoneNamesValidation.repair_names, bone)
                    continue

                if 'Right' in bone.name:
                    self.error(error_msg % bone.name, BoneNamesValidation.repair_names, bone)
                    continue


@validation_registry.register_validator
class NamingConventionsValidation(Validation):
    NAME = 'Naming Conventions'

    def validate(self, context, scene):
        object_error_msg = 'Object name (%s) needs to have correct naming convention'
        data_error_msg = 'Data name (%s) needs to have correct naming convention'
        material_error_msg = 'Material name (%s) needs to have correct naming convention'
        # image_error_msg = 'Image name (%s) needs to have correct naming convention'

        object_names_regex = re.compile('^[a-zA-Z0-9]+(?:[_.][a-zA-Z0-9]+)*$')
        material_names_regex = re.compile('^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*$')
        image_names_regex = re.compile('^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*(?:.[0-1]{4})?.(?:png|tif)$')

        # Object names
        for obj in bpy.data.objects:
            obj.name = obj.name
            if not object_names_regex.match(obj.name):
                self.error(object_error_msg % obj.name)
            data = obj.data
            if not object_names_regex.match(data.name):
                self.error(data_error_msg % data.name)

        # Material names
        ignore_materials = (
            'Dots Stroke' # Blender stroke default
        )
        for material in bpy.data.materials:
            if material.name in ignore_materials:
                continue
            if not material_names_regex.match(material.name):
                self.error(material_error_msg % material.name)

        # TODO: Figure out how to handle naming conventions for packed images and files.
        # Image names
        # for image in bpy.data.images:
        #     if image.type == 'RENDER_RESULT':
        #         continue
        #     if not image_names_regex.match(image.name):
        #         self.error(image_error_msg % image.name)


@validation_registry.register_validator
class ImageValidation(Validation):
    NAME = 'Image Validation'

    def is_power_of_two(self, value):
        return (value != 0) and ((value & (value - 1)) == 0)

    def validate(self, context, scene):
        power_of_two_error_msg = 'Image (%s) size is not a power of two (%s, %s)'
        size_too_big_error_msg = 'Image (%s) size is too big (%s, %s)'

        # Image names
        for image in bpy.data.images:
            if image.type == 'RENDER_RESULT':
                continue

            size = image.size
            if not self.is_power_of_two(size[0]) or not self.is_power_of_two(size[1]):
                self.error(power_of_two_error_msg % (image.name, size[0], size[1]))

            # Detect if normal map to skip
            colorspace_settings = image.colorspace_settings
            is_normal = (image.depth == 96 and colorspace_settings.name == 'Non-Color' and
                         colorspace_settings.is_data and image.is_float and image.type == 'IMAGE' and
                         image.source == 'FILE')

            if not is_normal:
                if size[0] > 4096 or size[1] > 4096:
                    self.error(size_too_big_error_msg % (image.name, size[0], size[1]))


@validation_registry.register_validator
class HiddenGeometryValidation(Validation):
    NAME = 'Hidden Geometry'

    @staticmethod
    def unhideObject(context):
        data, obj = context
        data.name = obj.name

        # Unhide object
        obj.hide_set(False)

        # Also ensure viewport/render visibility is enabled
        obj.hide_viewport = False
        obj.hide_render = False

        return True

    @staticmethod
    def unhidePolygons(context):
        data, obj = context
        data.name = obj.name

        # Unhide polygons
        for poly in data.polygons:
            poly.hide = False

        data.update()

        return True

    def validate(self, context, scene):
        for obj in bpy.data.objects:
            if not isinstance(obj.data, bpy.types.Mesh):
                continue

            mesh = obj.data

            for poly in mesh.polygons:
                if poly.hide:
                    self.warning(f'Has hidden geometry ({obj.name}).', HiddenGeometryValidation.unhidePolygons, (mesh, obj))
                    break

            # Viewport hidden (eye icon)
            if obj.hide_get():
                self.warning(f'Is hidden in viewport ({obj.name}).', HiddenGeometryValidation.unhideObject, (mesh, obj))

            # Disabled in viewport (monitor icon)
            if obj.hide_viewport:
                self.warning(f'Viewport disabled ({obj.name}).', HiddenGeometryValidation.unhideObject, (mesh, obj))

            # Hidden in render (camera icon)
            if obj.hide_render:
                self.warning(f'Hidden in render ({obj.name}).', HiddenGeometryValidation.unhideObject, (mesh, obj))