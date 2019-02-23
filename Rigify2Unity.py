bl_info = {
    "name": "Rigify to Unity - V2",
    "category": "Rigging",
    "description": "Change Rigify rig into Mecanim-ready rig for Unity",
    "location": "At the bottom of Rigify rig data/armature tab",
    "blender":(2,80,0)
}

import bpy
import re


class UnityMecanim_Panel(bpy.types.Panel):
    bl_label = "Rigify to Unity converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.object.type == 'ARMATURE' and "DEF-upper_arm.L.001" in bpy.context.object.data.bones
    
    def draw(self, context):
        self.layout.operator("rig4mec.convert2unity")
        
        
class UnityMecanim_Convert2Unity(bpy.types.Operator):
    bl_idname = "rig4mec.convert2unity"
    bl_label = "Prepare Rig for Unity"
    
    def execute(self, context):
        
        # REMOVE FIRST WIDGETS
        bpy.data.collections.remove(bpy.data.collections['Widgets'])
        
        ob = bpy.context.object
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        try: 
            ob.data.bones['DEF-breast.L'].use_deform = False
            ob.data.bones['DEF-breast.R'].use_deform = False
        except: 
            pass

        ob.data.bones['DEF-pelvis.L'].use_deform = False
        ob.data.bones['DEF-pelvis.R'].use_deform = False

        bpy.ops.object.mode_set(mode='EDIT')
        
        ob.data.edit_bones['DEF-shoulder.L'].parent = ob.data.edit_bones['DEF-spine.003']
        ob.data.edit_bones['DEF-shoulder.R'].parent = ob.data.edit_bones['DEF-spine.003']
        
        ob.data.edit_bones['DEF-upper_arm.L'].parent = ob.data.edit_bones['DEF-shoulder.L']
        ob.data.edit_bones['DEF-upper_arm.R'].parent = ob.data.edit_bones['DEF-shoulder.R']
        
        ob.data.edit_bones['DEF-thigh.L'].parent = ob.data.edit_bones['DEF-spine']
        ob.data.edit_bones['DEF-thigh.R'].parent = ob.data.edit_bones['DEF-spine']

        ob.data.edit_bones['DEF-upper_arm.L'].tail = ob.data.edit_bones['DEF-upper_arm.L.001'].tail
        ob.data.edit_bones['DEF-forearm.L'].tail = ob.data.edit_bones['DEF-forearm.L.001'].tail
        ob.data.edit_bones['DEF-forearm.L'].parent = ob.data.edit_bones['DEF-upper_arm.L.001'].parent
        ob.data.edit_bones['DEF-hand.L'].parent = ob.data.edit_bones['DEF-forearm.L.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-upper_arm.L.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-forearm.L.001'])

        ob.data.edit_bones['DEF-upper_arm.R'].tail = ob.data.edit_bones['DEF-upper_arm.R.001'].tail
        ob.data.edit_bones['DEF-forearm.R'].tail = ob.data.edit_bones['DEF-forearm.R.001'].tail
        ob.data.edit_bones['DEF-forearm.R'].parent = ob.data.edit_bones['DEF-upper_arm.R.001'].parent
        ob.data.edit_bones['DEF-hand.R'].parent = ob.data.edit_bones['DEF-forearm.R.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-upper_arm.R.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-forearm.R.001'])

        ob.data.edit_bones['DEF-thigh.L'].tail = ob.data.edit_bones['DEF-thigh.L.001'].tail
        ob.data.edit_bones['DEF-shin.L'].tail = ob.data.edit_bones['DEF-shin.L.001'].tail
        ob.data.edit_bones['DEF-shin.L'].parent = ob.data.edit_bones['DEF-thigh.L.001'].parent
        ob.data.edit_bones['DEF-foot.L'].parent = ob.data.edit_bones['DEF-shin.L.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-thigh.L.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-shin.L.001'])

        ob.data.edit_bones['DEF-thigh.R'].tail = ob.data.edit_bones['DEF-thigh.R.001'].tail
        ob.data.edit_bones['DEF-shin.R'].tail = ob.data.edit_bones['DEF-shin.R.001'].tail
        ob.data.edit_bones['DEF-shin.R'].parent = ob.data.edit_bones['DEF-thigh.R.001'].parent
        ob.data.edit_bones['DEF-foot.R'].parent = ob.data.edit_bones['DEF-shin.R.001'].parent
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-thigh.R.001'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-shin.R.001'])

        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.L'])
        ob.data.edit_bones.remove(ob.data.edit_bones['DEF-pelvis.R'])

        try: 
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.L'])
            ob.data.edit_bones.remove(ob.data.edit_bones['DEF-breast.R'])
        except: 
            pass
        
        bpy.ops.object.mode_set(mode='OBJECT')

        namelist = [("DEF-spine.006", "DEF-head"),("DEF-spine.005","DEF-neck")]
        
        
        # FOR UNITY HIERARCHY
        
        ob.data.edit_bones['ORG-shoulder.L'].parent = ob.data.edit_bones['DEF-spine.003']
        ob.data.edit_bones['ORG-shoulder.R'].parent = ob.data.edit_bones['DEF-spine.003']
        ob.data.edit_bones['DEF-spine'].parent = ob.data.edit_bones['torso']
        
        
        for name, newname in namelist:
            # get the pose bone with name
            pb = ob.pose.bones.get(name)
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = newname

        self.report({'INFO'}, 'Unity ready rig!')                

        return{'FINISHED'}

def register():
    #classes     
    bpy.utils.register_class(UnityMecanim_Panel)
    bpy.utils.register_class(UnityMecanim_Convert2Unity)
    
    
def unregister():
    #classes
    bpy.utils.unregister_class(UnityMecanim_Panel)
    bpy.utils.unregister_class(UnityMecanim_Convert2Unity)