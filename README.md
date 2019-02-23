# BlenderWorkflowAddons

Simple blender scripts to enhance speed when needed 


## Rigify2Unity 

Most of the work is from [this very useful implementation](https://github.com/AlexLemminG/RigifyToUnity, "old"). Something in the hierarchy didn't quite fit with Mecanim and this is an ugly fix for it. Here are the changes: 

* `ORG-shoulder` left and right are now parented to `DEF-spine.003`
* `DEF-spine` is now a `torso` child 

Let me know if this works for you ! (It is possible to install it as an addon, however, if an error is returned, try launching it as a script.)
