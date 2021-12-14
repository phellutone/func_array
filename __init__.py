bl_info = {
    "name": "func array",
    "author": "phellutone",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Tool Tab",
    "description": "functionally object array tool",
    "support": "TESTING",
    "tracker_url": "https://github.com/phellutone/func_array/issues",
    "category": "Object"
}


if "bpy" in locals():
    import imp
else:
    pass

import bpy
from .utils import anim_index

# def anim_index(id, path):
#     def path_disassembly(path):
#         tmp = ''
#         res = []
#         sid = -1
#         for i, s in enumerate(path):
#             if sid != -1 and sid != i:
#                 continue
#             sid = -1
#             if s == '[':
#                 res.append(('path', tmp))
#                 r, tmp = path_disassembly(path[i+1:])
#                 sid = r+i
#                 if len(tmp) > 1:
#                     res.append(('eval', tmp))
#                 else:
#                     res.append(tmp[0])
#                 tmp = ''
#             elif s == '.':
#                 if tmp:
#                     res.append(('path', tmp))
#                 tmp = ''
#             elif s == '"':
#                 idx = path.find('"', i+1)
#                 res.append(('str', path[i:idx+1]))
#                 sid = idx+1
#                 tmp = ''
#             elif s == ']':
#                 if tmp.isdigit():
#                     res.append(('int', int(tmp)))
#                 elif tmp:
#                     res.append(('path', tmp))
#                 return i+2, res
#             else:
#                 tmp += s
#         if tmp:
#             res.append(('path', tmp))
#         return res

#     def path_assembly(id, path, resolve=True):
#         res = [(id.bl_rna, '', id, '')]
#         tmp = id
#         stmp = ''
#         f = True
#         for i, p in enumerate(path):
#             if p[0] == 'path':
#                 e = p[1]
#                 ev = ('' if f else '.')+e
#                 f = False
#             elif p[0] in ('int', 'str'):
#                 e = p[1]
#                 ev = '['+str(e)+']'
#             else:
#                 e = eval(path_assembly(id, p[1], False)[-1][1])
#                 ev = '['+str(e)+']'
#             prop = None
#             if resolve:
#                 try:
#                     prop = tmp.bl_rna.properties[e]
#                 except Exception as _:
#                     prop = None
#                 tmp = id.path_resolve(stmp+ev)
#             stmp = stmp+ev
#             res.append((prop, stmp, tmp, e))
#         return res
    
#     try:
#         pd = path_disassembly(path)
#         pa = path_assembly(id, pd)
#     except Exception as _:
#         return None

#     # for p in pa:
#     #     print(p)

#     prop, stmp, tmp, e = pa[-1]
#     if prop is None:
#         prop, stmp, _, _ = pa[-2]
#     if isinstance(prop, bpy.types.Property):
#         if not prop.is_animatable:
#             return (False, 'invalid: the property is not animatable')
#         if prop.is_readonly:
#             return (False, 'invalid: the property is readonly')
#         if prop.type in ('BOOL', 'INT', 'FLOAT'):
#             if prop.is_array:
#                 if type(e) == int:
#                     return (True, pa)
#                 else:
#                     return (False, 'invalid: set the array index of the property')
#         return (True, pa)
#     return (False, 'invalid: the property is not support')

class FuncArrayVariable(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty()

    def to_update(self, context):
        self.to_id = None
        self.to_path = ""
        c = eval("bpy.types."+self.to_type)
        self.__class__.to_id = bpy.props.PointerProperty(type=c)
    to_type: bpy.props.EnumProperty(items=[
        ('Action',              "Action",           "", 'ACTION',               0),
        ('Armature',            "Armature",         "", 'ARMATURE_DATA',        1),
        ('Brush',               "Brush",            "", 'BRUSH_DATA',           2),
        ('Camera',              "Camera",           "", 'CAMERA_DATA',          3),
        ('CacheFile',           "Cache File",       "", 'FILE',                 4),
        ('Curve',               "Curve",            "", 'CURVE_DATA',           5),
        ('VectorFont',          "Font",             "", 'FONT_DATA',            6),
        ('GreasePencil',        "Grease Pencil",    "", 'GREASEPENCIL',         7),
        ('Collection',          "Collection",       "", 'OUTLINER_COLLECTION',  8),
        ('Image',               "Image",            "", 'IMAGE_DATA',           9),
        ('Key',                 "Key",              "", 'SHAPEKEY_DATA',        10),
        ('Light',               "Light",            "", 'LIGHT_DATA',           11),
        ('Library',             "Library",          "", 'LIBRARY_DATA_DIRECT',  12),
        ('FreestyleLineStyle',  "Line Style",       "", 'LINE_DATA',            13),
        ('Lattice',             "Lattice",          "", 'LATTICE_DATA',         14),
        ('Mask',                "Mask",             "", 'MOD_MASK',             15),
        ('Material',            "Material",         "", 'MATERIAL_DATA',        16),
        ('MetaBall',            "Metaball",         "", 'META_DATA',            17),
        ('Mesh',                "Mesh",             "", 'MESH_DATA',            18),
        ('MovieClip',           "Movie Clip",       "", 'TRACKER',              19),
        ('NodeTree',            "Node Tree",        "", 'NODETREE',             20),
        ('Object',              "Object",           "", 'OBJECT_DATA',          21),
        ('PaintCurve',          "Paint Curve",      "", 'CURVE_BEZCURVE',       22),
        ('Palette',             "Palette",          "", 'COLOR',                23),
        ('ParticleSettings',    "Particle",         "", 'PARTICLE_DATA',        24),
        ('LightProbe',          "Light Probe",      "", 'LIGHTPROBE_CUBEMAP',   25),
        ('Scene',               "Scene",            "", 'SCENE_DATA',           26),
        ('ID',                  "Simulation",       "", 'PHYSICS',              27),
        ('Sound',               "Sound",            "", 'SOUND',                28),
        ('Speaker',             "Speaker",          "", 'SPEAKER',              29),
        ('Text',                "Text",             "", 'TEXT',                 30),
        ('Texture',             "Texture",          "", 'TEXTURE',              31),
        ('ID',                  "Hair",             "", 'HAIR_DATA',            32),
        ('ID',                  "Point Cloud",      "", 'POINTCLOUD_DATA',      33),
        ('Volume',              "Volume",           "", 'VOLUME_DATA',          34),
        ('WindowManager',       "Window Manager",   "", 'WINDOW',               35),
        ('World',               "World",            "", 'WORLD_DATA',           36),
        ('WorkSpace',           "Workspace",        "", 'WORKSPACE',            37)
    ], default=21, update=to_update)

    to_id: bpy.props.PointerProperty(type=bpy.types.Object)
    to_path: bpy.props.StringProperty()

    def from_update(self, context):
        pass
    from_type: bpy.props.EnumProperty(items=[
        ('INDEX', 'Index', 'Array index', 'LINENUMBERS_ON', 0),
        ('CONST', 'Const', 'Float value', 'DOT',            1)
    ], default=0, update=from_update)

    fid: bpy.props.PointerProperty(type=bpy.types.ID)
    fpath: bpy.props.StringProperty()
    fidx: bpy.props.IntProperty()

    controller: bpy.props.FloatProperty()

class FuncArray(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty()

    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH'
    )
    eval_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH'
    )

    count: bpy.props.IntProperty(
        min=1,
        default=1,
        soft_max=25
    )

    variables: bpy.props.CollectionProperty(type=FuncArrayVariable)
    active_variables_index: bpy.props.IntProperty()

class FUNCARRAY_OT_add(bpy.types.Operator):
    bl_idname = "func_array.add"
    bl_label = "add"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray = context.scene.func_array
        block = farray.add()
        block.name = "Array "+str(len(farray))
        context.scene.active_func_array_index = len(farray)-1

        bpy.ops.func_array.variable_add()
        return {'FINISHED'}

class FUNCARRAY_OT_remove(bpy.types.Operator):
    bl_idname = "func_array.remove"
    bl_label = "remove"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray = context.scene.func_array
        index = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}
        
        # for i in range(len(farray)):
        #     context.scene.active_func_array_index = i
        #     varid = farray[i].active_variables_index
        #     for j in range(len(farray[i].variables)):
        #         farray[i].active_variables_index = j
        #         bpy.ops.func_array.variable_update()
        #     farray[i].active_variables_index = varid
        # context.scene.active_func_array_index = index

        block = farray[index]
        farray.remove(index)
        context.scene.active_func_array_index = min(max(0, index), len(farray)-1)
        return {'FINISHED'}

class FUNCARRAY_OT_variable_add(bpy.types.Operator):
    bl_idname = "func_array.variable_add"
    bl_label = "add"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray = context.scene.func_array
        index = context.scene.active_func_array_index
        block = farray[index]

        varbk = block.variables.add()
        varbk.name = "Variable "+str(len(block.variables))
        block.active_variables_index = len(block.variables)-1
        return {'FINISHED'}

class FUNCARRAY_OT_variable_remove(bpy.types.Operator):
    bl_idname = "func_array.variable_remove"
    bl_label = "remove"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray = context.scene.func_array
        index = context.scene.active_func_array_index
        block = farray[index]
        varid = block.active_variables_index

        if block.active_variables_index < 0 or not block.variables:
            return {'CANCELLED'}
        
        # for i in range(len(block.variables)):
        #     block.active_variables_index = i
        #     bpy.ops.func_array.variable_update()
        # block.active_variables_index = varid

        varbk = block.variables[block.active_variables_index]
        varbk.to_id = None

        block.variables.remove(block.active_variables_index)
        block.active_variables_index = min(max(0, block.active_variables_index), len(block.variables)-1)
        return {'FINISHED'}

class FUNCARRAY_OT_variable_update(bpy.types.Operator):
    bl_idname = "func_array.variable_update"
    bl_label = "update"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray = context.scene.func_array
        index = context.scene.active_func_array_index
        block = farray[index]

        if block.active_variables_index < 0 or not block.variables:
            return {'CANCELLED'}
        
        varbk: FuncArrayVariable = block.variables[block.active_variables_index]

        # if varbk.fid == varbk.to_id and varbk.fpath == varbk.to_path:
        #     return {'FINISHED'}

        if varbk.fid is None or varbk.fpath == "":
            pass
        else:
            if varbk.fid.animation_data:
                fcurve = varbk.fid.animation_data.drivers.find(varbk.fpath, index=varbk.fidx)
                if fcurve:
                    varbk.fid.animation_data.drivers.remove(fcurve)

        try:
            varbk.to_id.path_resolve(varbk.to_path)
            res, dat = anim_index(varbk.to_id, varbk.to_path)
            if res:
                idx = -1 if dat[-1][0] is None else 0
                varbk.fid = varbk.to_id
                varbk.fpath = dat[-1+idx][1]
                varbk.fidx = dat[-1][3] if str(dat[-1][3]).isdigit() else 0

                if not varbk.fid.animation_data:
                    varbk.fid.animation_data_create()
                fcurve = varbk.fid.animation_data.drivers.new(varbk.fpath, index=varbk.fidx)
                driver = fcurve.driver
                driver.type = 'SCRIPTED'
                v = driver.variables.new()
                v.name = "var"
                v.targets[0].id_type = 'SCENE'
                v.targets[0].id = varbk.id_data
                v.targets[0].data_path = varbk.path_from_id("controller")
                driver.expression = "var"
        except Exception as _:
            pass

        return {'FINISHED'}

class OBJECT_UL_FuncArrayVariable(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", icon="RNA", text="", emboss=False)
            row.prop(item, "mute", icon="CHECKBOX_HLT" if not item.mute else "CHECKBOX_DEHLT", text="", emboss=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=icon)

class OBJECT_UL_FuncArray(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, "name", icon="ANIM", text="", emboss=False)
            row.prop(item, "mute", icon="CHECKBOX_HLT" if not item.mute else "CHECKBOX_DEHLT", text="", emboss=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=icon)

class OBJECT_PT_FuncArray(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_idname = "VIEW3D_PT_fcurve_wrapper"
    bl_label = "Func Array"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.template_list("OBJECT_UL_FuncArray", "", scene, "func_array", scene, "active_func_array_index", rows=3)
        col = row.column(align=True)
        col.operator("func_array.add", icon="ADD", text="")
        col.operator("func_array.remove", icon="REMOVE", text="")

        if scene.func_array:
            index = scene.active_func_array_index
            block = scene.func_array[index]

            col = layout.column()
            col.prop(block, "target", text="Target")
            col.prop(block, "count", text="Count")
            # blank = col.row()
            # blank.enabled = False
            # blank.prop(block, "eval_target")

            row = layout.row()
            row.template_list("OBJECT_UL_FuncArrayVariable", "", block, "variables", block, "active_variables_index", rows=3)
            col = row.column(align=True)
            col.operator("func_array.variable_add", icon="ADD", text="")
            col.operator("func_array.variable_remove", icon="REMOVE", text="")

            if block.variables:
                varid = block.active_variables_index
                varbk = block.variables[varid]

                col = layout.column()
                col.operator("func_array.variable_update", text="update")

                box = col.box().column()
                box.label(text="Variable Input")
                box.use_property_split = True
                box.use_property_decorate = True
                box.prop(varbk, "from_type", text="Type", expand=True)
                box.prop(varbk, "controller", text="Controller")

                box = col.box().column()
                box.label(text="Variable Output")
                box.template_any_ID(varbk, "to_id", "to_type", text="Prop:")
                box.template_path_builder(varbk, "to_path", varbk.to_id, text="Path")
                try:
                    val = varbk.to_id.path_resolve(varbk.to_path)
                    res, dat = anim_index(varbk.to_id, varbk.to_path)
                    if not res:
                        bbx = box.box().split(factor=1.0).column()
                        bbx.alignment = 'RIGHT'
                        bbx.label(text=str(val))
                        box.label(text=dat)
                    else:
                        col = box.column()
                        col.enabled = False
                        col.active = False
                        idx = -1 if dat[-1][0] is None else 0
                        col.prop(dat[-2+idx][2], dat[-1+idx][3])
                except Exception as e:
                    box.label(text="invalid value")

        # col.prop(scene, "tTarget")
        # col.prop(scene, "tEvalTarget")
        # col.template_any_ID(scene, "tFWid", "tFWtype")
        # col.template_path_builder(scene, "tFWpath", scene.tFWid, text="Data Path")
        # box = col.box().split(factor=1.00).row()
        # box.alignment = 'RIGHT'
        # try:
        #     box.label(text=str(scene.tFWid.path_resolve(scene.tFWpath)))
        # except Exception as e:
        #     box.label(text="")

        # if scene.tFWid:
        #     col.template_list("FCurveWrapper_UL_FW", "", scene.tFWid.animation_data, "drivers", scene, "tFWindex", rows=3)





classes = (
    FuncArrayVariable,
    FuncArray,
    OBJECT_UL_FuncArrayVariable,
    OBJECT_UL_FuncArray,
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    FUNCARRAY_OT_variable_add,
    FUNCARRAY_OT_variable_remove,
    FUNCARRAY_OT_variable_update,
    OBJECT_PT_FuncArray
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.func_array = bpy.props.CollectionProperty(type=FuncArray)
    bpy.types.Scene.active_func_array_index = bpy.props.IntProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.func_array
    del bpy.types.Scene.active_func_array_index

if __name__ == "__main__":
    register()
