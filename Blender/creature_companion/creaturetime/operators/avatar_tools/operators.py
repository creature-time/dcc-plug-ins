import bpy
from mathutils.geometry import distance_point_to_plane

from creaturetime import constants


def setup_default_shape_keys(mesh, shape_key_setup):
    DEFAULT_BASIS_NAME = 'Basis'

    shape_keys = mesh.data.shape_keys
    if not shape_keys:
        mesh.shape_key_add(name=DEFAULT_BASIS_NAME, from_mix=False)
        shape_keys = mesh.data.shape_keys

    #    print(f'Checking shape keys...')

    expected_shape_key_order = [DEFAULT_BASIS_NAME]
    for category in shape_key_setup:
        expected_shape_key_order.append(category)

        expected_shape_keys = shape_key_setup[category]
        expected_shape_key_order += expected_shape_keys

    # Need basis shape key for relative_key reference.
    basis_shape_key = None

    key_blocks = shape_keys.key_blocks

    # Get current key order.
    shape_key_order = []
    for shape_key in key_blocks:
        if shape_key.name == DEFAULT_BASIS_NAME:
            basis_shape_key = shape_key
        shape_key_order.append(shape_key.name)

    if not basis_shape_key:
        basis_shape_key = mesh.shape_key_add(name=DEFAULT_BASIS_NAME, from_mix=False)
        shape_key_order.append(DEFAULT_BASIS_NAME)

    wm = bpy.context.window_manager
    current_step = 0
    wm.progress_begin(current_step, len(expected_shape_key_order))

    for target, shape_key_name in enumerate(expected_shape_key_order):
        #        print(f'Validating shape key (shape_key={shape_key_name}).')

        index = -1
        if shape_key_name in shape_key_order:
            index = shape_key_order.index(shape_key_name)

        #        print(f'{shape_key_name} {index} {target}')
        if index == -1:
            shape_key = mesh.shape_key_add(name=shape_key_name, from_mix=False)

            index = len(shape_key_order)
            shape_key_order.append(shape_key_name)
        else:
            shape_key = key_blocks[index]

        if shape_key_name in shape_key_setup and not shape_key.lock_shape:
            shape_key.mute = True
            shape_key.lock_shape = True

        shape_key.relative_key = basis_shape_key

        if target == index:
            continue

        #        print(f'Fixing shape key index (shape_key={shape_key_name}, index={index}, target={target}).')
        mesh.active_shape_key_index = index

        if index > target:
            while index > target:
                bpy.ops.object.shape_key_move(type='UP')
                index -= 1

        else:
            while index < target:
                bpy.ops.object.shape_key_move(type='DOWN')
                index += 1

        shape_key_order.remove(shape_key_name)
        shape_key_order.insert(target, shape_key_name)

        current_step += 1
        wm.progress_update(current_step)

    mesh.active_shape_key_index = 0


def get_vrcft_default_shape_keys():
    return [
        'EyeClosed.Source',
        'EyeSquint.Source',
        'EyeClosedSquintCorrective.Source',
        'EyeWide.Source',
        'EyeDilation',
        'EyeConstrict',
        'BrowDown.Source',
        'EyeClosedBrowDownCorrective.Source',
        'BrowInnerUp',
        'EyeClosedBrowInnerUpCorrective.Source',
        'BrowOuterUp.Source',
        'EyeClosedBrowOuterUpCorrective.Source',
        'NoseSneer',
        'CheekSquint.Source',
        'CheekPuff.Source',
        'CheekSuck.Source',
        'JawOpen',
        'MouthClosed',
        'JawLeft',
        'JawRight',
        'JawForward',
        'LipSuckUpper',
        'LipSuckLower',
        'LipFunnel',
        'LipPucker',
        'MouthUpperUp.Source',
        'MouthLowerDown',
        'MouthLeft',
        'MouthRight',
        'MouthSmile.Source',
        'MouthFrown.Source',
        'MouthStretch.Source',
        'MouthDimple.Source',
        'MouthRaiserUpper',
        'MouthRaiserLower',
        'MouthPress',
        'MouthTightener.Source',
        'TongueOut',
        'TongueOutStep1',
        'TongueOutStep2',
        'TongueDown',
        'TongueUp',
        'TongueLeft',
        'TongueRight',
        'TongueUpLeftMorph',
        'TongueUpRightMorph',
        'TongueDownLeftMorph',
        'TongueDownRightMorph',
    ]


DEFAULT_VRCFT_SOURCE_SUFFIX = '.Source'
DEFAULT_VRCFT_SOURCE_SUFFIX_LEN = len(DEFAULT_VRCFT_SOURCE_SUFFIX)


def get_vrcft_shape_keys(obj):
    vrcft_shape_keys = get_vrcft_default_shape_keys()

    unused_shape_keys = []

    shape_keys = obj.data.shape_keys
    if not shape_keys:
        return vrcft_shape_keys, unused_shape_keys

    existing_shape_keys = {shape_key.name: shape_key for shape_key in shape_keys.key_blocks}

    expected_vrcft_shape_keys = []
    for shape_key in vrcft_shape_keys:
        if f'_{shape_key}' in existing_shape_keys:
            expected_vrcft_shape_keys.append(f'_{shape_key}')
            existing_shape_keys[f'_{shape_key}'].mute = True

            if shape_key.endswith(DEFAULT_VRCFT_SOURCE_SUFFIX):
                source_shape_key = shape_key[:-DEFAULT_VRCFT_SOURCE_SUFFIX_LEN]
                for shape_key in [f'{source_shape_key}Left', f'{source_shape_key}Right', f'_{source_shape_key}Left',
                                  f'_{source_shape_key}Right']:
                    if shape_key in existing_shape_keys:
                        unused_shape_keys.append(shape_key)
                        existing_shape_keys[shape_key].mute = True

        else:
            expected_vrcft_shape_keys.append(shape_key)

            if shape_key.endswith(DEFAULT_VRCFT_SOURCE_SUFFIX):
                source_shape_key = shape_key[:-DEFAULT_VRCFT_SOURCE_SUFFIX_LEN]
                for shape_key in [f'{source_shape_key}Left', f'{source_shape_key}Right']:
                    if shape_key in existing_shape_keys:
                        expected_vrcft_shape_keys.append(shape_key)

                for shape_key in [f'_{source_shape_key}Left', f'_{source_shape_key}Right']:
                    if shape_key in existing_shape_keys:
                        unused_shape_keys.append(shape_key)
                        existing_shape_keys[shape_key].mute = True

    return expected_vrcft_shape_keys, unused_shape_keys


class CREATURETIME_OT_AvatarShapeKeys(bpy.types.Operator):
    """Performs setup for avatar shape keys"""

    bl_idname = constants.generate_id('avatars_shape_keys')
    bl_label = "Setup Avatar Shape Keys"
    bl_description = "Run avatar shape key setup"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object
                and context.active_object.type == 'MESH'
                and context.mode == 'OBJECT')

    def invoke(self, context, event):
        setup_avatar_shape_keys = {
            '=== Visemes ===': [
                'vrc.v_sil',
                'vrc.v_pp',
                'vrc.v_ff',
                'vrc.v_th',
                'vrc.v_dd',
                'vrc.v_kk',
                'vrc.v_ch',
                'vrc.v_ss',
                'vrc.v_nn',
                'vrc.v_rr',
                'vrc.v_aa',
                'vrc.v_e',
                'vrc.v_ih',
                'vrc.v_oh',
                'vrc.v_ou'
            ],
            '=== Eye Look ===': [
                'Blink',
                'LookUp',
                'LookDown'
            ],
            '=== Vrcft ===': []
        }

        obj = context.active_object

        vrcft_shape_keys, unused_shape_keys = get_vrcft_shape_keys(obj)

        setup_avatar_shape_keys['=== Vrcft ==='] = vrcft_shape_keys
        if unused_shape_keys:
            setup_avatar_shape_keys['=== Unused ==='] = unused_shape_keys

        setup_default_shape_keys(obj, setup_avatar_shape_keys)

        return {"FINISHED"}


def generate_vrcft_shape_key(active, shape_key, vrcft_source_shape_keys, generate_vrcft_shape_keys):
    # print(f'Checking shape key '
    #       f'(index={index}, shape_key_name={shape_key_name}, '
    #       f'mute={mute}, lock_shape={lock_shape}).')
    if shape_key.mute or shape_key.lock_shape:
        return

    # print(f'Does the shape exist (shape_key_name={shape_key_name}, found={shape_key_name in vrcft_source_shape_keys})?')
    if shape_key.name not in vrcft_source_shape_keys:
        return

    source_shape_key = shape_key.name[:-DEFAULT_VRCFT_SOURCE_SUFFIX_LEN]
    shape_key.value = 1
    for suffix, vertex_group in generate_vrcft_shape_keys.items():
        gen_shape_key = f'{source_shape_key}{suffix}'
        if active.data.shape_keys.key_blocks.find(gen_shape_key) == -1:
            # print(f'Generating vrcft shape key (gen_shape_key={gen_shape_key}).')
            shape_key.vertex_group = vertex_group
            active.shape_key_add(name=gen_shape_key, from_mix=True)

    shape_key.vertex_group = str()
    shape_key.value = 0


class CREATURETIME_OT_AvatarGenerateVrcftVertexGroups(bpy.types.Operator):
    """Performs vrcft avatar shape key generation based on Source shape keys and left/right vertex groups."""

    bl_idname = constants.generate_id('avatars_vrcft_vertex_groups')
    bl_label = "Generate Vcrft Vertex Groups"
    bl_description = "Generate Vcrft Vertex Groups"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        active = context.object
        return active

    def invoke(self, context, event):
        obj = context.object
        ct_avatar_tools = obj.ct_avatar_tools

        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode="WEIGHT_PAINT")

        use_paint_mask = False
        use_paint_mask_vertex = False

        print(use_paint_mask, bpy.context.object.data.use_paint_mask)
        use_paint_mask, bpy.context.object.data.use_paint_mask = bpy.context.object.data.use_paint_mask, use_paint_mask
        print(use_paint_mask_vertex, bpy.context.object.data.use_paint_mask_vertex)
        use_paint_mask_vertex, bpy.context.object.data.use_paint_mask_vertex = bpy.context.object.data.use_paint_mask_vertex, use_paint_mask_vertex

        masks = {
            'vrcft.mask_left': ('vrcft_vertex_group_left', (1, 0, 0)),
            'vrcft.mask_right': ('vrcft_vertex_group_right', (-1, 0, 0))
        }

        plane_co = obj.location
        vertex_groups = obj.vertex_groups
        for vrcft_vertex_group_name, (prop, plane_no) in masks.items():
            setattr(ct_avatar_tools, prop, vrcft_vertex_group_name)
            if vertex_groups.find(vrcft_vertex_group_name) != -1:
                continue

            selected_vertices = [index for index, v in enumerate(obj.data.vertices) if distance_point_to_plane(v.co, plane_co, plane_no) >= 0]

            vertex_group = vertex_groups.new(name=vrcft_vertex_group_name)
            vertex_group.add(selected_vertices, 1.0, 'ADD')

            vertex_groups.active_index = vertex_groups.find(vrcft_vertex_group_name)
            bpy.ops.object.vertex_group_smooth(group_select_mode='ACTIVE', repeat=ct_avatar_tools.vrcft_vertex_groups_repeat)

        bpy.context.object.data.use_paint_mask = use_paint_mask
        bpy.context.object.data.use_paint_mask_vertex = use_paint_mask_vertex

        bpy.ops.object.mode_set(mode=current_mode)

        return {"FINISHED"}


class CREATURETIME_OT_AvatarGenerateVrcftShapeKeys(bpy.types.Operator):
    """Performs vrcft avatar shape key generation based on Source shape keys and left/right vertex groups."""

    bl_idname = constants.generate_id('avatars_vrcft_shape_keys')
    bl_label = "Generate Vrcft Shape Keys"
    bl_description = "Generate Vrcft Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        active = context.active_object
        return (active and context.mode == 'OBJECT')

    def invoke(self, context, event):
        active = context.active_object
        shape_keys = active.data.shape_keys
        if not shape_keys:
            return {'CANCELLED'}

        ct_avatar_tools = context.object.ct_avatar_tools

        validate_generate_shape_keys = {
            ct_avatar_tools.vrcft_vertex_group_left: 'Left',
            ct_avatar_tools.vrcft_vertex_group_right: 'Right'
        }

        generate_vrcft_shape_keys = {}
        for vertex_group, suffix in validate_generate_shape_keys.items():
            if vertex_group and active.vertex_groups.find(vertex_group) != -1:
                generate_vrcft_shape_keys[suffix] = vertex_group

        if not generate_vrcft_shape_keys:
            return {'CANCELLED'}

        shape_key_index = active.active_shape_key_index
        if shape_key_index == -1:
            return {'CANCELLED'}

        vrcft_shape_keys = get_vrcft_default_shape_keys()
        vrcft_source_shape_keys = set()
        for shape_key in vrcft_shape_keys:
            if shape_key.endswith(DEFAULT_VRCFT_SOURCE_SUFFIX):
                vrcft_source_shape_keys.add(shape_key)

        # Pre-operation setup.
        shape_key_values = {}
        for shape_key in shape_keys.key_blocks:
            shape_key_values[shape_key.name] = shape_key.value
            shape_key.value = 0

        # Perform task.
        if ct_avatar_tools.vrcft_selected_only:
            # Perform on selected shape keys.
            active_shape_key = shape_keys.key_blocks[active.active_shape_key_index]
            generate_vrcft_shape_key(active, active_shape_key, vrcft_source_shape_keys, generate_vrcft_shape_keys)
        else:
            # Perform on all shape keys.
            for index, shape_key in enumerate(shape_keys.key_blocks):
                generate_vrcft_shape_key(active, shape_key, vrcft_source_shape_keys, generate_vrcft_shape_keys)

        # Post-operation setup.
        for shape_key in shape_keys.key_blocks:
            if shape_key.name in shape_key_values:
                shape_key.value = shape_key_values[shape_key.name]

        return {"FINISHED"}