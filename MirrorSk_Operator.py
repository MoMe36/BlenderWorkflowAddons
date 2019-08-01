import bpy 
import math 
import mathutils as m 


class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Mirror Shape Keys using Vertex Groups ?"

    
    target_ob = bpy.props.StringProperty(name ="Target Object:", default = "Head")
    target_mesh = bpy.props.StringProperty(name= "Target Mesh:", default = "Plane.000")
     
    def execute(self, context):
        
        try: 
            self.do_mirror()
            msg = 'Perfect run'
        except: 
            msg = 'Something is wrong'
        
        self.report({'INFO'}, msg)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def do_mirror(self):
        
        obj = bpy.data.collections['Collection'].all_objects[self.target_ob]
        mesh = bpy.data.meshes[self.target_mesh]
        
        vg_keys = obj.vertex_groups.keys() 
        # Get shape keys 
        sk_keys = mesh.shape_keys.key_blocks.keys()
        
        for sk in sk_keys: 
            if sk == "Basis": 
                pass 
            else: 
                print("Processing: {} ".format(sk))
                # Deform mesh using SK
                mesh.shape_keys.key_blocks[sk].value = 1. 
                
                # Duplicates 
                left_duplicate = obj.shape_key_add(name = '{}.l'.format(sk), from_mix = True)
                right_duplicate = obj.shape_key_add(name = '{}.r'.format(sk), from_mix = True)
                mid_duplicate = obj.shape_key_add(name = '{}.m'.format(sk), from_mix = True)
                
                # Assigning vertex groups 
                left_duplicate.vertex_group = "Left"
                right_duplicate.vertex_group = "Right"
                mid_duplicate.vertex_group = "Mid"
                
                # Return to initial state 
                mesh.shape_keys.key_blocks[sk].value = 0. 

        
        

    

bpy.utils.register_class(DialogOperator)

# test call
bpy.ops.object.dialog_operator('INVOKE_DEFAULT')

