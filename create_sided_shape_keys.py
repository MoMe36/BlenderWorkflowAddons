import bpy 

target_mesh = 'Plane.000'
target_obj = 'Head' 


obj = bpy.data.collections['Collection'].all_objects[target_obj]
mesh = bpy.data.meshes[target_mesh]

# Get vertex groups 
vg_keys = obj.vertex_groups.keys() 

# Get shape keys 
sk_keys = mesh.shape_keys.key_blocks.keys()

# for each shape key except basis
# I. duplicate 3 times
# II. Rename current to name.full 
# III. Rename duplicates: name.l, name.r, name.m
# IV. for each duplicate, assign corresponding vertex group 

for sk in sk_keys: 
    
    if sk == "Basis": 
        pass 
    else: 
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