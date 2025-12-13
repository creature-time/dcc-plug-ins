import bpy


from creaturetime import constants

class _RemoveUnusedVertexGroups(bpy.types.Operator):
    """
    Delete Vertex Groups with no assigned weight of active object
    Credit goes to CoDEmanX.
    """

    bl_label = "Remove Unused Vertex Groups"
    bl_idname = constants.generate_id('remove_unused_vertex_groups')
    bl_options = {'REGISTER', 'UNDO'}
    bl_region_type = 'UI'

    def execute(self, context):
        ob = context.object
        ob.update_from_editmode()

        used_vertex_groups = {i: False for i, k in enumerate(ob.vertex_groups)}

        for v in ob.data.vertices:
            for g in v.groups:
                if g.weight > 0.0:
                    used_vertex_groups[g.group] = True

        for i, used in sorted(used_vertex_groups.items(), reverse=True):
            if not used:
                ob.vertex_groups.remove(ob.vertex_groups[i])

        return {'FINISHED'}