import bpy

FUNCARRAY_UPDATE_LOCK = False

@bpy.app.handlers.persistent
def deform_update(scene, depsgraph):
    global FUNCARRAY_UPDATE_LOCK
    if FUNCARRAY_UPDATE_LOCK:
        return

    ids = [u.id.original for u in depsgraph.updates if isinstance(u.id, bpy.types.Object)]
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

        if not block.is_evaluated:
            continue

        if block.lock:
            continue

        if not block.target in ids:
            continue

        block.is_evaluated = False

    FUNCARRAY_UPDATE_LOCK = False
