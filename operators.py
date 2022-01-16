
import bpy
from .properties import FuncArray, FuncArrayIndex, _FUNCARRAY_DEPSGRAPHS
from .handlers import eval_dup, eval_obj_init



class FUNCARRAY_OT_add(bpy.types.Operator):
    bl_idname = 'func_array.add'
    bl_label = 'add'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        farray: list[FuncArray] = getattr(scene, FuncArray.identifier)
        block: FuncArray = farray.add()

        block.name = 'Array '+str(len(farray))
        block.index = len(farray)-1

        setattr(scene, FuncArrayIndex.identifier, len(farray)-1)
        return {'FINISHED'}

class FUNCARRAY_OT_remove(bpy.types.Operator):
    bl_idname = 'func_array.remove'
    bl_label = 'remove'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context: bpy.types.Context) -> set[str]:
        scene = context.scene
        farray: list[FuncArray] = getattr(scene, FuncArray.identifier)
        index: int = getattr(scene, FuncArrayIndex.identifier)
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]
        if block.is_activate:
            bpy.ops.func_array.activation()
        farray.remove(index)

        for b in farray:
            if b.index < index:
                continue
            b.index = b.index-1

        setattr(scene, FuncArrayIndex.identifier, min(max(0, index), len(farray)-1))
        return {'FINISHED'}

class FUNCARRAY_OT_activation(bpy.types.Operator):
    bl_idname = 'func_array.activation'
    bl_label = 'activation'
    bl_description = ''
    bl_options = {'REGISTER'}

    def execute(self, context: bpy.types.Context) -> set[str]:
        global _FUNCARRAY_DEPSGRAPHS

        scene = context.scene
        farray: list[FuncArray] = getattr(scene, FuncArray.identifier)
        index: int = getattr(scene, FuncArrayIndex.identifier)
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]

        if block.is_activate:
            ob = block.trg_ob
            bpy.data.objects.remove(ob)

            co = block.trg_co
            eval_obj_init(block, 0, co)
            bpy.data.collections.remove(co)

            _FUNCARRAY_DEPSGRAPHS = [(i, d) for i, d in _FUNCARRAY_DEPSGRAPHS if i != index]

            block.is_activate = False
            return {'FINISHED'}
        else:
            if block.target is None:
                return {'CANCELLED'}

            target: bpy.types.Object = block.target

            co = bpy.data.collections.new('FuncArrayDummy.'+target.name)
            block.trg_co = co

            eval_obj_init(block, block.count, co)

            obj = bpy.data.objects.new('FuncArray.'+target.name, None)
            obj.instance_type = 'COLLECTION'
            obj.instance_collection = co
            block.trg_ob = obj
            context.scene.collection.objects.link(obj)

            _FUNCARRAY_DEPSGRAPHS.append((index, context.evaluated_depsgraph_get()))

            block.is_activate = True
            eval_dup(context, block)
            return {'FINISHED'}
