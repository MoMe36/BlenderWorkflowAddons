import bpy 


# get object 
head = bpy.collections['Collection'].all_objects['Head']
# Get vertex groups from object 
vg_keys = head.vertex_groups.keys() 


# get mesh 
head_mesh = bpy.data.meshes['Plane.000'] 
# get Shape Keys from mesh 

sk_keys = head_mesh.shape_keys.key_blocks.keys()