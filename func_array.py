import bpy
from .handler import deform_update



class FuncArrayObject(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    is_activate: bpy.props.BoolProperty()
    is_computing: bpy.props.BoolProperty()
    is_evaluated: bpy.props.BoolProperty()
    object: bpy.props.PointerProperty(type=bpy.types.Object)

class FuncArray(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty(default=False)

    is_activate: bpy.props.BoolProperty()
    is_evaluated: bpy.props.BoolProperty()

    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH'
    )
    eval_targets: bpy.props.CollectionProperty(type=FuncArrayObject)

    count: bpy.props.IntProperty(
        min=1,
        default=1,
        soft_max=25
    )

    controller: bpy.props.FloatProperty()
    ctr_max: bpy.props.FloatProperty(default=1.0)
    ctr_min: bpy.props.FloatProperty(default=0.0)

    trg_co: bpy.props.PointerProperty(type=bpy.types.Collection)
    trg_ob: bpy.props.PointerProperty(type=bpy.types.Object)

def eval_obj_init(block: FuncArray, count: int, co: bpy.types.Collection):
    if len(block.eval_targets) > count:
        for i in reversed(range(count, len(block.eval_targets))):
            e = block.eval_targets[i]
            ob = e.object
            me = e.object.data
            bpy.data.objects.remove(ob)
            bpy.data.meshes.remove(me)
            block.eval_targets.remove(i)
    elif len(block.eval_targets) < count:
        for i in range(count-len(block.eval_targets)):
            e: FuncArrayObject = block.eval_targets.add()
            me = bpy.data.meshes.new('FuncArrayDummy.'+block.target.name+'.'+str(i))
            ob = bpy.data.objects.new('FuncArrayDummy.'+block.target.name+'.'+str(i), me)
            e.object = ob
            co.objects.link(ob)

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

class FUNCARRAY_OT_activation(bpy.types.Operator):
    bl_idname = 'func_array.activation'
    bl_label = 'activation'
    bl_description = ''
    bl_options = {'REGISTER'}

    _timer = None

    def modal(self, context, event):
        """
        is_evaluated: False -> True
        """
        
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'PASS_THROUGH'}
        
        for block in farray:
            if not block.is_activate:
                continue

            if block.is_evaluated:
                continue

            if block.mute:
                continue

            print('execution')
            block.is_evaluated = True

        return {'PASS_THROUGH'}

    def execute(self, context):
        """
        is_activate: toggle
        """

        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]

        if block.is_activate:
            ob = block.trg_ob
            bpy.data.objects.remove(ob)

            co = block.trg_co
            eval_obj_init(block, 0, co)
            bpy.data.collections.remove(co)

            if self._timer is not None:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                self._timer = None

            block.is_activate = False
            return {'FINISHED'}
        else:
            if block.target is None:
                return {'CANCELLED'}
            
            co = bpy.data.collections.new('FuncArrayDummy.'+block.target.name)
            block.trg_co = co

            eval_obj_init(block, block.count, co)

            obj = bpy.data.objects.new('FuncArray.'+block.target.name, None)
            obj.instance_type = 'COLLECTION'
            obj.instance_collection = co
            block.trg_ob = obj
            context.scene.collection.objects.link(obj)

            if self._timer is None:
                wm = context.window_manager
                self._timer = wm.event_timer_add(0.05, window=context.window)
                wm.modal_handler_add(self)

            block.is_activate = True
            return {'RUNNING_MODAL'}

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
            index: int = scene.active_func_array_index
            block: FuncArray = scene.func_array[index]

            col = layout.column()

            row = col.row()
            if block.is_activate:
                row.operator('func_array.activation', text='deactivate', icon='PAUSE')
            else:
                row.operator('func_array.activation', text='activate', icon='PLAY')

            box = col.box().column()
            box.enabled = not block.is_activate
            box.prop(block, 'target', text='Target')
            box.prop(block, 'count', text='Count')

            row = box.row(align=True)
            row.prop(block, 'ctr_max', text='max')
            row.prop(block, 'ctr_min', text='min')
            box.prop(block, 'controller')


classes = (
    FuncArrayObject,
    FuncArray,
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    FUNCARRAY_OT_activation,
    OBJECT_UL_FuncArray,
    OBJECT_PT_FuncArray,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.func_array = bpy.props.CollectionProperty(type=FuncArray)
    bpy.types.Scene.active_func_array_index = bpy.props.IntProperty()
    if not deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(deform_update)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.func_array
    del bpy.types.Scene.active_func_array_index
    if deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(deform_update)
