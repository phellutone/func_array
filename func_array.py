import bpy
# from .func_array_variable import *
# from .handler import deform_update

class FuncArray(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty()
    is_activate: bpy.props.BoolProperty()

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

    # variables: bpy.props.CollectionProperty(type=FuncArrayVariable)
    # active_variable_index: bpy.props.IntProperty()

    controller: bpy.props.FloatProperty()
    ctr_max: bpy.props.FloatProperty(default=0.0)
    ctr_min: bpy.props.FloatProperty(default=1.0)

    trg_co: bpy.props.PointerProperty(type=bpy.types.Collection)
    trg_ob: bpy.props.PointerProperty(type=bpy.types.Object)

class FUNCARRAY_OT_add(bpy.types.Operator):
    bl_idname = 'func_array.add'
    bl_label = 'add'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        block: FuncArray = farray.add()

        block.name = 'Array '+str(len(farray))
        block.index = len(farray)-1
        context.scene.active_func_array_index = len(farray)-1

        # bpy.ops.func_array.variable_add()
        return {'FINISHED'}

class FUNCARRAY_OT_remove(bpy.types.Operator):
    bl_idname = 'func_array.remove'
    bl_label = 'remove'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]

        farray.remove(index)

        for b in farray:
            if b.index < index:
                continue
            b.index = b.index-1

        context.scene.active_func_array_index = min(max(0, index), len(farray)-1)
        return {'FINISHED'}

class FUNCARRAY_OT_activate(bpy.types.Operator):
    bl_idname = 'func_array.activate'
    bl_label = 'activate'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]
        if block.is_activate:
            return {'CANCELLED'}
        if block.target is None:
            return {'CANCELLED'}
        
        me = bpy.data.meshes.new('FuncArrayDummy.'+block.target.name)
        ob = bpy.data.objects.new('FuncArrayDummy.'+block.target.name, me)
        block.eval_target = ob

        co = bpy.data.collections.new('FuncArrayDummy.'+block.target.name)
        block.trg_co = co
        co.objects.link(ob)

        obj = bpy.data.objects.new('FuncArray.'+block.target.name, None)
        obj.instance_type = 'COLLECTION'
        obj.instance_collection = co
        block.trg_ob = obj
        context.scene.collection.objects.link(obj)
        # context.scene.collection.objects.link(ob)

        block.is_activate = True
        return {'FINISHED'}

class FUNCARRAY_OT_deactivate(bpy.types.Operator):
    bl_idname = 'func_array.deactivate'
    bl_label = 'deactivate'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]
        if not block.is_activate:
            return {'CANCELLED'}
        if block.target is None:
            return {'CANCELLED'}

        ob = block.eval_target
        me = block.eval_target.data
        bpy.data.objects.remove(ob)
        bpy.data.meshes.remove(me)

        ob = block.trg_ob
        bpy.data.objects.remove(ob)

        co = block.trg_co
        bpy.data.collections.remove(co)

        block.is_activate = False
        return {'FINISHED'}

class OBJECT_UL_FuncArray(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, 'name', icon='ANIM', text='', emboss=False)
            row.prop(item, 'mute', icon='CHECKBOX_HLT' if not item.mute else 'CHECKBOX_DEHLT', text='', emboss=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text='', icon=icon)

class OBJECT_PT_FuncArray(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_idname = 'VIEW3D_PT_func_array'
    bl_label = 'Func Array'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.template_list('OBJECT_UL_FuncArray', '', scene, 'func_array', scene, 'active_func_array_index', rows=3)
        col = row.column(align=True)
        col.operator('func_array.add', icon='ADD', text='')
        col.operator('func_array.remove', icon='REMOVE', text='')

        if scene.func_array:
            index = scene.active_func_array_index
            block = scene.func_array[index]

            col = layout.column()

            row = col.row()
            row.operator('func_array.activate')
            row.operator('func_array.deactivate')

            col.prop(block, 'target', text='Target')
            col.prop(block, 'count', text='Count')

            box = col.box().column()
            row = box.row(align=True)
            row.prop(block, 'ctr_max', text='max')
            row.prop(block, 'ctr_min', text='min')
            box.prop(block, 'controller')


classes = (
    # FuncArrayVariable,
    FuncArray,
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    FUNCARRAY_OT_activate,
    FUNCARRAY_OT_deactivate,
    # FUNCARRAY_OT_variable_add,
    # FUNCARRAY_OT_variable_remove,
    OBJECT_UL_FuncArray,
    # OBJECT_UL_FuncArrayVariable,
    OBJECT_PT_FuncArray,
    # OBJECT_PT_FuncArrayVariable
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.func_array = bpy.props.CollectionProperty(type=FuncArray)
    bpy.types.Scene.active_func_array_index = bpy.props.IntProperty()
    # if not deform_update in bpy.app.handlers.depsgraph_update_post:
    #     bpy.app.handlers.depsgraph_update_post.append(deform_update)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.func_array
    del bpy.types.Scene.active_func_array_index
    # if deform_update in bpy.app.handlers.depsgraph_update_post:
    #     bpy.app.handlers.depsgraph_update_post.remove(deform_update)
