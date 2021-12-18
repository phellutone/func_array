import bpy
import bmesh

FUNCARRAY_UPDATE_LOCK = False

def evaluate(depsgraph, obj, bm):
    eval_obj = obj.evaluated_get(depsgraph)
    me = bpy.data.meshes.new_from_object(eval_obj)
    me.transform(eval_obj.matrix_world)
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)

def dup(scene, target, count, eval_mesh, variables):
    obj = target.copy()
    bpy.context.scene.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(eval_mesh)
    bm.clear()

    for i in range(count):
        for v in variables:
            v.controller = i/(count-1)
        depsgraph = scene.view_layers[0].depsgraph
        depsgraph.update()
        evaluate(depsgraph, obj, bm)
    
    bpy.data.objects.remove(obj)
    bm.to_mesh(eval_mesh)
    bm.free()

@bpy.app.handlers.persistent
def deform_update(scene, depsgraph):
    global FUNCARRAY_UPDATE_LOCK
    if FUNCARRAY_UPDATE_LOCK:
        return

    ids = [u.id for u in depsgraph.updates if isinstance(u.id, bpy.types.Object)]
    if not ids:
        return
    
    farray = scene.func_array
    index = scene.active_func_array_index
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

        varis = block.variables
        varid = block.active_variable_index
        if not varis or varid < 0:
            continue

        dup(scene, target, block.count, eval_mesh, block.variables)

    FUNCARRAY_UPDATE_LOCK = False
