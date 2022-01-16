import bpy
import bmesh
from .properties import FuncArray, FuncArrayObject, _FUNCARRAY_DEPSGRAPHS

_FUNCARRAY_UPDATE_LOCK = False

def eval_obj_init(block: FuncArray, count: int, co: bpy.types.Collection) -> None:
    if len(block.eval_targets) > count:
        for i in reversed(range(count, len(block.eval_targets))):
            e = block.eval_targets[i]
            ob: bpy.types.Object = e.object
            me = ob.data
            bpy.data.objects.remove(ob)
            bpy.data.meshes.remove(me)
            block.eval_targets.remove(i)
    elif len(block.eval_targets) < count:
        for i in range(count-len(block.eval_targets)):
            e: FuncArrayObject = block.eval_targets.add()
            target: bpy.types.Object = block.target
            me = bpy.data.meshes.new('FuncArrayDummy.'+target.name+'.'+str(i))
            ob = bpy.data.objects.new('FuncArrayDummy.'+target.name+'.'+str(i), me)
            ob.is_func_array_dummy = True
            e.object = ob
            co.objects.link(ob)

def eval_dup(context: bpy.types.Context, block: FuncArray) -> None:
    global _FUNCARRAY_UPDATE_LOCK
    _FUNCARRAY_UPDATE_LOCK = True

    eval_obj_init(block, block.count, block.trg_co)

    target: bpy.types.Object = block.target
    ob = target.copy()
    context.scene.collection.objects.link(ob)

    ctr: float = block.controller
    for i in range(block.count):
        eval_target: FuncArrayObject = block.eval_targets[i]
        eval_obj: bpy.types.Object = eval_target.object
        eval_mesh = eval_obj.data
        bm = bmesh.new()
        bm.from_mesh(eval_mesh)
        bm.clear()

        if block.count == 1:
            block.controller = block.ctr_min
        else:
            block.controller = i/(block.count-1)*(block.ctr_max-block.ctr_min)+block.ctr_min
        depsgraph = context.evaluated_depsgraph_get()
        e_ob: bpy.types.Object = ob.evaluated_get(depsgraph)

        eval_obj.matrix_world = e_ob.matrix_world
        e_me = bpy.data.meshes.new_from_object(e_ob)
        bm.from_mesh(e_me)
        bm.to_mesh(eval_mesh)

        bpy.data.meshes.remove(e_me)
        bm.free()
    bpy.data.objects.remove(ob)
    block.controller = ctr

    _FUNCARRAY_UPDATE_LOCK = False

@bpy.app.handlers.persistent
def deform_update(scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph) -> None:
    global _FUNCARRAY_UPDATE_LOCK, _FUNCARRAY_DEPSGRAPHS
    if _FUNCARRAY_UPDATE_LOCK:
        return

    farray: list[FuncArray] = scene.func_array
    index: int = scene.active_func_array_index
    if index < 0 or not farray:
        return

    for block in farray:
        if not block.is_activate:
            continue

        if block.mute:
            continue

        deg = [d for i, d in _FUNCARRAY_DEPSGRAPHS if i == index]
        if not deg:
            continue
        deg = deg[0]

        if not deg.updates:
            continue

        eval_dup(bpy.context, block)
