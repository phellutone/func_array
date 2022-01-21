
import bpy
from .properties import FuncArray, FuncArrayDummy, FuncArrayObject, FuncArrayIndex
from .operators import FUNCARRAY_OT_add, FUNCARRAY_OT_remove, FUNCARRAY_OT_activation
from .panels import OBJECT_UL_FuncArray, OBJECT_PT_FuncArray
from .handlers import deform_update



paths = {
    FuncArray.identifier: (
        bpy.types.Scene,
        bpy.props.CollectionProperty(
            name='Func Array',
            type=FuncArray
        )
    ),
    FuncArrayIndex.identifier: (
        bpy.types.Scene,
        bpy.props.IntProperty(
            name='Active Func Array Index'
        )
    ),
    FuncArrayDummy.identifier: (
        bpy.types.Object,
        bpy.props.BoolProperty(
            name='Is Func Array Dummy'
        )
    )
}

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

    for identifier in paths:
        base, prop = paths[identifier]
        setattr(base, identifier, prop)

    if not deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(deform_update)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for identifier in paths:
        base, prop = paths[identifier]
        delattr(base, identifier)

    if deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(deform_update)
