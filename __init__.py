import bpy
import re


bl_info = {
    "name": "Cleanup Vertex Groups",
    "author": "12funkeys",
    "version": (0, 16),
    "blender": (2, 74, 0),
    "location": "Mesh > Vertex Groups",
    "description": "Remove 0 Weight Vertex Groups",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}


# menu
class CleanupVertexGroups(bpy.types.Operator):
    bl_idname = "mesh.cleanup_vertex_groups"
    bl_label = "Cleanup Vertex Groups"
    bl_description = "Remove 0 weight vertex groups"
    bl_options = {'REGISTER', 'UNDO'}


    # 
    def execute(self, context):

        self.report({'INFO'}, "START")

        ob = bpy.context.object
        me = bpy.context.object.data
        
        dict = {}


        for AVG in ob.vertex_groups:
            flag = 0
            index = AVG.index
            #self.report({'INFO'}, "*****"+ str(AVG.name) + ":" + str(index) + "***************")

            ###bpy.data.meshes[id].vertices[n]
            for mev in me.vertices:
                #self.report({'INFO'}, "    Mesh Vertex Index:" + str(mev.index))
 
                ###bpy.data.meshes[id].vertices[n].groups[n]
                for mevg in mev.groups:
                    #self.report({'INFO'}, "        flag:" + str(flag))
                    ###group index
                    ###bpy.data.meshes[id].vertices[n].groups[n].group
                    #self.report({'INFO'}, "        Element Index:" + str(mevg.group) + " Vertex Groups Index:" + str(index))
                    if mevg.group == index:
                        #self.report({'INFO'}, "        Element Weight:" + str(mevg.weight))
                        if mevg.weight > 0:
                            flag = 0
                            break
                        
                        else:
                            flag = 1                    
                    else:
                        flag = 1
                        
                if flag == 0:
                    break

            #self.report({'INFO'}, str(index) + ":" + str(flag))
            if AVG.name not in dict:
                dict[AVG.name] = flag

            #mirror_name
            if flag == 0:

                #search
                m = re.search("(^|_|\.|-|\s)(LEFT|RIGHT)(_+|$|\.+|\s+)|(^|_|\.|-|\s+)(L|R)(_+|$|\.+|\s+)", AVG.name, re.IGNORECASE)

                if m != None:
                    #self.report({'INFO'}, "m.group():" + str(m.group())) 

                    m2 = re.search("[A-Z]+", m.group(), re.IGNORECASE)
                    if m2 != None:
                        #self.report({'INFO'}, "m2.group():" + str(m2.group())) 

                        #split
                        #sp = AVG.name.split(m2.group())
                        #self.report({'INFO'}, "sp:" + str(sp)) 
                        
                        if m2.group() == "LEFT":
                            flip_word = m.group().replace("LEFT", "RIGHT")
                        elif m2.group() == "Left":
                            flip_word = m.group().replace("Left", "Right")
                        elif m2.group() == "left":
                            flip_word = m.group().replace("left", "right")
                        elif m2.group() == "L":
                            flip_word = m.group().replace("L", "R")
                        elif m2.group() == "l":
                            flip_word = m.group().replace("l", "r")
                        elif m2.group() == "RIGHT":
                            flip_word = m.group().replace("RIGHT", "LEFT")
                        elif m2.group() == "Right":
                            flip_word = m.group().replace("Right", "Left")
                        elif m2.group() == "right":
                            flip_word = m.group().replace("right", "left")
                        elif m2.group() == "R":
                            flip_word = m.group().replace("R", "L")
                        elif m2.group() == "r":
                            flip_word = m.group().replace("r", "l")

                        #self.report({'INFO'}, str(flip_word)) 
                            
                        search_name = re.sub("(^|_|\.|-|\s)(LEFT|RIGHT)(_+|$|\.+|\s+)|(^|_|\.|-|\s+)(L|R)(_+|$|\.+|\s+)", flip_word, AVG.name)

                        #self.report({'INFO'}, str(AVG.name))               
                        #self.report({'INFO'}, str(search_name)) 

                        if search_name in ob.vertex_groups:
                            #self.report({'INFO'}, "remove:" + str(search_name))
                            
                            if search_name not in dict:
                                dict[search_name] = 0

                        else:
                            #self.report({'INFO'}, "no search_name") 
                            pass

                    else:
                        #self.report({'INFO'}, "m2 not match") 
                        pass


                else:
                    #self.report({'INFO'}, "m not match") 
                    pass

        self.report({'INFO'}, "removed list:") 
        for key in dict.keys():
            #self.report({'INFO'}, str(key) + ":" + str(dict[key])) 
            if dict[key] == 1:
                vg = ob.vertex_groups.get(key)
                if vg is not None:
                    ob.vertex_groups.remove(vg)
                    self.report({'INFO'}, key) 


        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator("mesh.cleanup_vertex_groups", icon='X')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.MESH_MT_vertex_group_specials.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.MESH_MT_vertex_group_specials.remove(menu_func)

if __name__ == "__main__":
    register()
