import bpy 
import math 
import mathutils as m 


class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Remove actions ?"

    to_remove_actions = bpy.props.StringProperty(name= "Actions to remove")
    remove_all = bpy.props.BoolProperty(name ="Remove all ?") 
    # path_to_anim += "/home/mehdi/Blender/Scripts/"

    def execute(self, context):

        if self.remove_all: 
            self.remove_all_actions()
            message = "Removed everything"

        else:
            removed, not_removed = self.remove_actions()
            message = 'Finished removing {} '.format(removed)
            if not_removed != []: 
                message += "Not removed: {}".format(not_removed)
            
        self.report({'INFO'}, message)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def remove_all_actions(self): 

        all_actions = bpy.data.actions 
        for aa in all_actions:
            bpy.data.actions.remove(aa)

        print('Removed all') 

    def remove_actions(self): 

        actions = self.to_remove_actions.split(',')
        removed = []
        not_removed = []
        
       
        for ac in actions: 
            if(ac.startswith(' ')):
                ac = ac[1:]
            
            if(ac.endswith(' ')):
                ac = ac[:-1]

            try: 
                bpy.data.actions.remove(bpy.data.actions[ac])
                removed.append(ac)
            except KeyError: 
                not_removed.append(ac)

        return removed, not_removed

    

bpy.utils.register_class(DialogOperator)

# test call
bpy.ops.object.dialog_operator('INVOKE_DEFAULT')

