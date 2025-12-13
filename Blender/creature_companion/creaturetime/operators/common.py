import bpy
import textwrap

from creaturetime import constants
from creaturetime import resources

def _multiline(context, layout, text):
    chars = int(context.region.width / 7)  # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for index, text_line in enumerate(text_lines):
        layout.label(text=text_line)


class Ct_Note(bpy.types.Operator):
    bl_idname = constants.generate_id('messagebox')
    bl_label = ''
    bl_description = 'Click to see message.'

    message: bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )
    icon: bpy.props.StringProperty(
        name = "icon",
        description = "icon",
        default = 'NONE'
    )
    icon_value: bpy.props.IntProperty(
        name = "icon_value",
        description = "icon_value",
        default = 0
    )

    def execute(self, context):
        message = self.message
        def draw(popup, context):
            _multiline(context, popup.layout, message)
        context.window_manager.popup_menu(draw)
        return {'FINISHED'}


class Ct_Panel(bpy.types.Panel):
    def _create_section(self, layout, info=None, warning=None, critical=None, *args, **kwargs):
        kwargs['text'] = kwargs['text'].upper()

        section_layout = layout.box()

        section_layout_title = section_layout.row()

        col = section_layout_title.column()
        col.alignment = 'EXPAND'
        col.label(*args, **kwargs)

        col = None
        if info:
            if not col:
                col = section_layout_title.column()
            self.info(col, info)

        if warning:
            if not col:
                col = section_layout_title.column()
            self.warning(col, warning)

        if critical:
            if not col:
                col = section_layout_title.column()
            self.critical(col, critical)

        return section_layout

    def __msg(self, layout, msg_type, text, icon='NONE', icon_value=0):
        msg_box = layout.operator(Ct_Note.bl_idname, icon=icon, icon_value=icon_value)#, text=msg_type, emboss = False)
        msg_box.icon = icon
        msg_box.icon_value = icon_value
        msg_box.message = text

    def info(self, layout, text):
        self.__msg(layout, 'Info', text, icon='INFO')

    def warning(self, layout, text):
        self.__msg(layout, 'Warning', text, icon_value=resources.get('warning_x16').icon_id)

    def critical(self, layout, text):
        self.__msg(layout, 'Critical', text, icon_value=resources.get('error_x16').icon_id)


def hide(obj, val=True):
    obj.hide_set(val)

def select(obj, sel=True):
    if sel:
        hide(obj, False)
    obj.select_set(sel)

def get_active():
    return bpy.context.view_layer.objects.active

def set_active(obj, skip_sel=False):
    if not skip_sel:
        select(obj)
    bpy.context.view_layer.objects.active = obj

def switch(new_mode, check_mode=True):
    if check_mode and get_active() and get_active().mode == new_mode:
        return

    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode=new_mode, toggle=False)

def has_shape_keys(mesh):
    if not hasattr(mesh.data, 'shape_keys'):
        return False
    return hasattr(mesh.data.shape_keys, 'key_blocks')

def sort_shape_keys(mesh, shape_key_order=None):
    if not has_shape_keys(mesh):
        return
    set_active(mesh)

    if not shape_key_order:
        shape_key_order = []

    order = [
        'Basis',
        'vrc.blink_left',
        'vrc.blink_right',
        'vrc.lowerlid_left',
        'vrc.lowerlid_right',
        'vrc.v_aa',
        'vrc.v_ch',
        'vrc.v_dd',
        'vrc.v_e',
        'vrc.v_ff',
        'vrc.v_ih',
        'vrc.v_kk',
        'vrc.v_nn',
        'vrc.v_oh',
        'vrc.v_ou',
        'vrc.v_pp',
        'vrc.v_rr',
        'vrc.v_sil',
        'vrc.v_ss',
        'vrc.v_th',
        'Basis Original'
    ]

    for shape in shape_key_order:
        if shape not in order:
            order.append(shape)

    wm = bpy.context.window_manager
    current_step = 0
    wm.progress_begin(current_step, len(order))

    i = 0
    for name in order:
        if name == 'Basis' and 'Basis' not in mesh.data.shape_keys.key_blocks:
            i += 1
            current_step += 1
            wm.progress_update(current_step)
            continue

        for index, shape_key in enumerate(mesh.data.shape_keys.key_blocks):
            if shape_key.name == name:
                mesh.active_shape_key_index = index
                new_index = i
                index_diff = (index - new_index)

                if new_index >= len(mesh.data.shape_keys.key_blocks):
                    bpy.ops.object.shape_key_move(type='BOTTOM')
                    break

                position_correct = False
                if 0 <= index_diff <= (new_index - 1):
                    while position_correct is False:
                        if mesh.active_shape_key_index != new_index:
                            bpy.ops.object.shape_key_move(type='UP')
                        else:
                            position_correct = True
                else:
                    if mesh.active_shape_key_index > new_index:
                        bpy.ops.object.shape_key_move(type='TOP')

                    position_correct = False
                    while position_correct is False:
                        if mesh.active_shape_key_index != new_index:
                            bpy.ops.object.shape_key_move(type='DOWN')
                        else:
                            position_correct = True

                i += 1
                break

        current_step += 1
        wm.progress_update(current_step)

    mesh.active_shape_key_index = 0

    wm.progress_end()