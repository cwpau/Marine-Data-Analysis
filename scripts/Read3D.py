import os
import bpy

# put the location to the folder where the objs are located here in this fashion
# this line will only work on windows ie C:\objects
path_to_fbx_dir = os.path.join('C:\\temp\\', 'fbx')

# get list of all files in directory
# file_list = sorted(os.listdir(path_to_obj_dir))

# get a list of files ending in 'obj'
# obj_list = [item for item in file_list if item.endswith('.fbx')]

# loop through the strings in obj_list and add the files to the scene
for root, dirs, files in os.walk(path_to_fbx_dir):
    files = [ fi for fi in files if fi.endswith(".fbx") ]
    for name in files:
        path_to_file = os.path.join(root, name)
        bpy.ops.import_scene.fbx(filepath = path_to_file)


# for item in obj_list:
#    path_to_file = os.path.join(path_to_obj_dir, item)
#    bpy.ops.import_scene.fbx(filepath = path_to_file)