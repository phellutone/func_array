import bpy
from .properties import FuncArray, FuncArrayObject
from .handler import eval_dup, eval_obj_init

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
    _dg = None

    def modal(self, context, event):
        """
        is_evaluated: False -> True
        """
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'PASS_THROUGH'}
        
        depsgraph = FUNCARRAY_OT_activation._dg

        for block in farray:
            if not block.is_activate:
                continue

            if block.mute:
                continue
            
            if [u for u in depsgraph.updates]:
                eval_dup(context, block)

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

            wm = context.window_manager
            wm.event_timer_remove(FUNCARRAY_OT_activation._timer)
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

            FUNCARRAY_OT_activation._dg = context.evaluated_depsgraph_get()

            wm = context.window_manager
            FUNCARRAY_OT_activation._timer = wm.event_timer_add(0.02, window=context.window)
            wm.modal_handler_add(self)

            block.is_activate = True
            eval_dup(context, block)
            return {'RUNNING_MODAL'}
