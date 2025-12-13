import bpy


class CtAvatarToolsProperties(bpy.types.PropertyGroup):
    vrcft_vertex_groups_repeat: bpy.props.IntProperty(
        name="Repeat",
        description="Number of times to repeat for vertex group smoothing.",
        default=3)
    vrcft_vertex_group_left: bpy.props.StringProperty(
        name="Left",
        description="Left side vertex group used to generate from source vrcft shape keys.",
        default="vrcft.mask_left")
    vrcft_vertex_group_right: bpy.props.StringProperty(
        name="Right",
        description="Right side vertex group used to generate from source vrcft shape keys.",
        default="vrcft.mask_right")
    vrcft_selected_only: bpy.props.BoolProperty(
        name="Selected Only",
        description="Only perform generation on selected valid source vrcft shape key.",
        default=True)
