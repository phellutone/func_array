import bpy
from .func_array import FuncArray
from .utils import anim_index

class FuncArrayVariable(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty()

    def to_update(self, context):
        self.to_id = None
        self.to_path = ''
        c = eval('bpy.types.'+self.to_type)
        self.__class__.to_id = bpy.props.PointerProperty(type=c)
    to_type: bpy.props.EnumProperty(items=[
        ('Action',              'Action',           '', 'ACTION',               0),
        ('Armature',            'Armature',         '', 'ARMATURE_DATA',        1),
        ('Brush',               'Brush',            '', 'BRUSH_DATA',           2),
        ('Camera',              'Camera',           '', 'CAMERA_DATA',          3),
        ('CacheFile',           'Cache File',       '', 'FILE',                 4),
        ('Curve',               'Curve',            '', 'CURVE_DATA',           5),
        ('VectorFont',          'Font',             '', 'FONT_DATA',            6),
        ('GreasePencil',        'Grease Pencil',    '', 'GREASEPENCIL',         7),
        ('Collection',          'Collection',       '', 'OUTLINER_COLLECTION',  8),
        ('Image',               'Image',            '', 'IMAGE_DATA',           9),
        ('Key',                 'Key',              '', 'SHAPEKEY_DATA',        10),
        ('Light',               'Light',            '', 'LIGHT_DATA',           11),
        ('Library',             'Library',          '', 'LIBRARY_DATA_DIRECT',  12),
        ('FreestyleLineStyle',  'Line Style',       '', 'LINE_DATA',            13),
        ('Lattice',             'Lattice',          '', 'LATTICE_DATA',         14),
        ('Mask',                'Mask',             '', 'MOD_MASK',             15),
        ('Material',            'Material',         '', 'MATERIAL_DATA',        16),
        ('MetaBall',            'Metaball',         '', 'META_DATA',            17),
        ('Mesh',                'Mesh',             '', 'MESH_DATA',            18),
        ('MovieClip',           'Movie Clip',       '', 'TRACKER',              19),
        ('NodeTree',            'Node Tree',        '', 'NODETREE',             20),
        ('Object',              'Object',           '', 'OBJECT_DATA',          21),
        ('PaintCurve',          'Paint Curve',      '', 'CURVE_BEZCURVE',       22),
        ('Palette',             'Palette',          '', 'COLOR',                23),
        ('ParticleSettings',    'Particle',         '', 'PARTICLE_DATA',        24),
        ('LightProbe',          'Light Probe',      '', 'LIGHTPROBE_CUBEMAP',   25),
        ('Scene',               'Scene',            '', 'SCENE_DATA',           26),
        ('ID',                  'Simulation',       '', 'PHYSICS',              27),
        ('Sound',               'Sound',            '', 'SOUND',                28),
        ('Speaker',             'Speaker',          '', 'SPEAKER',              29),
        ('Text',                'Text',             '', 'TEXT',                 30),
        ('Texture',             'Texture',          '', 'TEXTURE',              31),
        ('ID',                  'Hair',             '', 'HAIR_DATA',            32),
        ('ID',                  'Point Cloud',      '', 'POINTCLOUD_DATA',      33),
        ('Volume',              'Volume',           '', 'VOLUME_DATA',          34),
        ('WindowManager',       'Window Manager',   '', 'WINDOW',               35),
        ('World',               'World',            '', 'WORLD_DATA',           36),
        ('WorkSpace',           'Workspace',        '', 'WORKSPACE',            37)
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

class FUNCARRAY_OT_variable_add(bpy.types.Operator):
    bl_idname = 'func_array.variable_add'
    bl_label = 'add'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        block: FuncArray = farray[index]

        varbk: FuncArrayVariable = block.variables.add()
        varbk.name = 'Variable '+str(len(block.variables))
        block.active_variable_index = len(block.variables)-1
        return {'FINISHED'}

class FUNCARRAY_OT_variable_remove(bpy.types.Operator):
    bl_idname = 'func_array.variable_remove'
    bl_label = 'remove'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        block: FuncArray = farray[index]
        varid: int = block.active_variable_index

        if block.active_variable_index < 0 or not block.variables:
            return {'CANCELLED'}

        varbk: FuncArrayVariable = block.variables[block.active_variable_index]
        varbk.to_id = None

        block.variables.remove(block.active_variable_index)
        block.active_variable_index = min(max(0, block.active_variable_index), len(block.variables)-1)
        return {'FINISHED'}

class OBJECT_UL_FuncArrayVariable(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, 'name', icon='RNA', text='', emboss=False)
            row.prop(item, 'mute', icon='CHECKBOX_HLT' if not item.mute else 'CHECKBOX_DEHLT', text='', emboss=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text='', icon=icon)
