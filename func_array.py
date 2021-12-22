import bpy
from .properties import FuncArray, FuncArrayObject
from .operators import FUNCARRAY_OT_add, FUNCARRAY_OT_remove, FUNCARRAY_OT_activation
from .panels import OBJECT_UL_FuncArray, OBJECT_PT_FuncArray
from .handlers import deform_update

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
    bpy.types.Object.is_func_array_dummy = bpy.props.BoolProperty()

    if not deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(deform_update)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.func_array
    del bpy.types.Scene.active_func_array_index
    del bpy.types.Object.is_func_array_dummy

    if deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(deform_update)
