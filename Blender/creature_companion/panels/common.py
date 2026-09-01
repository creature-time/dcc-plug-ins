import bpy
import textwrap


from .. import constants
from .. import resources


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