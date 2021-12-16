import bpy
import bmesh
from .func_array_variable import FuncArrayVariable
from .func_array import FuncArray

FUNCARRAY_UPDATE_LOCK = False

def evaluate(depsgraph, obj, bm):
    eval_obj = obj.evaluated_get(depsgraph)
    me = bpy.data.meshes.new_from_object(eval_obj)
    me.transform(eval_obj.matrix_world)
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)

def dup(target: bpy.types.Object, count: int, eval_mesh: bpy.types.Mesh, variables: list[FuncArrayVariable]):
    obj = target.copy()
    bpy.context.scene.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(eval_mesh)
    bm.clear()

    for i in range(count):
        for v in variables:
            v.controller = i/(count-1)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        evaluate(depsgraph, obj, bm)
    
    bpy.data.objects.remove(obj)
    bm.to_mesh(eval_mesh)
    bm.free()

def update(scene, depsgraph):
    global FUNCARRAY_UPDATE_LOCK
    if FUNCARRAY_UPDATE_LOCK:
        return

    ids = [u.id for u in depsgraph.updates if isinstance(u.id, bpy.types.Object)]
    if not ids:
        return
    
    farray: list[FuncArray] = scene.func_array
    index: int = scene.active_func_array_index
    if not farray or index < 0:
        return
    
    FUNCARRAY_UPDATE_LOCK = True

    for block in farray:
        if not block.is_activate:
            continue

        if block.target is None or block.eval_target is None:
            continue
        eval_mesh = block.eval_target.data

        targets = [id for id in ids if id.original == block.target]
        if not targets:
            continue
        target = targets[0]

        varis: list[FuncArrayVariable] = block.variables
        varid: int = block.active_variable_index
        if not varis or varid < 0:
            continue

        dup(target, block.count, eval_mesh, block.variables)

    FUNCARRAY_UPDATE_LOCK = False
