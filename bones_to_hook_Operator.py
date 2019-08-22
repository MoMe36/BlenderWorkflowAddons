import bpy 
import math 
import mathutils as m 

def get_pos(lattice): 
    return [lattice.matrix_world @ p.co for p in lattice.data.points]


class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Mirror Shape Keys using Vertex Groups ?"

    lattice_name = bpy.props.StringProperty(name= "Deform Lattice:", default = "Lattice")
    arm_name = bpy.props.StringProperty(name= "Control Armature:", default = "Armature")
     
    def execute(self, context):
        
        msg = self.pair_lattice_armature() 
        
        self.report({'INFO'}, msg)

        return {'FINISHED'}

    def pair_lattice_armature(self): 
        
        armature = bpy.data.objects[self.arm_name]
        lattice = bpy.data.objects[self.lattice_name]
        
        bones = armature.data.bones
        all_pos = get_pos(lattice)
        scene = bpy.context.view_layer
        
        for b_idx, b in enumerate(bones): 
            current_bone_pos = b.center.xyz 
            lattice_points = lattice.data.points
            closest_point_idx = 0
            
            # Selecting current bone's closest lattice point 
            for i, p in enumerate(all_pos): 
                
                dist = (all_pos[i] - current_bone_pos).length 
                if i == 0: 
                    current_dist = dist 
                else: 
                    if dist < current_dist: 
                        current_dist = dist 
                        closest_point_idx = i 
            

            # Creating the hook 
            scene.objects.active = lattice
            bpy.ops.object.modifier_add(type = 'HOOK') 
            
            hook_name = 'Hook' if b_idx == 0 else 'Hook.{:03d}'.format(b_idx) 

            # setting hook target

            bpy.context.object.modifiers[hook_name].object = armature 
            bpy.context.object.modifiers[hook_name].subtarget = b.name

            # assigning hook point
            
            bpy.ops.object.mode_set(mode = 'EDIT')
            for p in lattice.data.points: 
                p.select = False 
            lattice.data.points[closest_point_idx].select = True
            bpy.ops.object.hook_assign(modifier=hook_name)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            print('Affected {} to vertice {}'.format(b, closest_point_idx))
            
        return 'Perfect'

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    

        
        

    

bpy.utils.register_class(DialogOperator)

# test call
bpy.ops.object.dialog_operator('INVOKE_DEFAULT')

