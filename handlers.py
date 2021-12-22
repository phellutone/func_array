import bpy
import bmesh
from .properties import FuncArray, FuncArrayObject, _DG

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
            ob.is_func_array_dummy = True
            e.object = ob
            co.objects.link(ob)

def eval_dup(context: bpy.types.Context, block: FuncArray):
    eval_obj_init(block, block.count, block.trg_co)

    ob = block.target.copy()
    context.scene.collection.objects.link(ob)

    ctr = block.controller
    for i in range(block.count):
        eval_mesh = block.eval_targets[i].object.data
        bm = bmesh.new()
        bm.from_mesh(eval_mesh)
        bm.clear()

        if block.count == 1:
            block.controller = block.ctr_min
        else:
            block.controller = i/(block.count-1)*(block.ctr_max-block.ctr_min)+block.ctr_min
        depsgraph = context.evaluated_depsgraph_get()
        eval_obj = ob.evaluated_get(depsgraph)
        me = bpy.data.meshes.new_from_object(eval_obj)
        me.transform(eval_obj.matrix_world)
        bm.from_mesh(me)
        bpy.data.meshes.remove(me)

        bm.to_mesh(eval_mesh)
        bm.free()
    bpy.data.objects.remove(ob)
    block.controller = ctr

_FUNCARRAY_UPDATE_LOCK = False

@bpy.app.handlers.persistent
def deform_update(scene, depsgraph):
    global _FUNCARRAY_UPDATE_LOCK, _DG
    if _FUNCARRAY_UPDATE_LOCK:
        return
    
    farray: list[FuncArray] = scene.func_array
    index: int = scene.active_func_array_index
    if index < 0 or not farray:
        return

    _FUNCARRAY_UPDATE_LOCK = True

    for block in farray:
        if not block.is_activate:
            continue

        if block.mute:
            continue

        deg = [d for i, d in _DG if i == index]
        if not deg:
            continue
        deg = deg[0]

        if not deg.updates:
            continue

        eval_dup(bpy.context, block)
    
    _FUNCARRAY_UPDATE_LOCK = False
