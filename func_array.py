
from typing import Union
import bpy
from .properties import FuncArray, FuncArrayDummy, FuncArrayObject, FuncArrayIndex
from .operators import FUNCARRAY_OT_add, FUNCARRAY_OT_remove, FUNCARRAY_OT_activation
from .panels import OBJECT_UL_FuncArray, OBJECT_PT_FuncArray, OBJECT_PT_FuncArrayVD
from .handlers import deform_update
from .virtual_driver import virtual_driver



def favd_access_context(context: bpy.types.Context) -> bpy.types.bpy_struct:
    return favd_access_id(context.scene)

def favd_access_id(id: bpy.types.ID) -> bpy.types.bpy_struct:
    farray: Union[list[FuncArray], None] = getattr(id, FuncArray.identifier, None)
    if not farray:
        return
    index: Union[int, None] = getattr(id, FuncArrayIndex.identifier, None)
    if index is None:
        return
    return farray[index]

paths = {
    FuncArray.identifier: (bpy.types.Scene, bpy.props.CollectionProperty(type=FuncArray)),
    FuncArrayIndex.identifier: (bpy.types.Scene, bpy.props.IntProperty()),
    FuncArrayDummy.identifier: (bpy.types.Object, bpy.props.BoolProperty())
}

classes = (
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    FUNCARRAY_OT_activation,
    OBJECT_UL_FuncArray,
    OBJECT_PT_FuncArray,
    OBJECT_PT_FuncArrayVD,
)


def register():
    virtual_driver.preregister(
        bpy.types.Scene,
        FuncArray,
        favd_access_context,
        favd_access_id
    )
    vdclasses = [
        FuncArrayObject,
        FuncArray
    ]+[cls for cls in virtual_driver.classes if not cls is virtual_driver.OBJECT_PT_VirtualDriver]
    virtual_driver.classes = vdclasses
    virtual_driver.register()

    for cls in classes:
        bpy.utils.register_class(cls)

    for identifier in paths:
        base, prop = paths[identifier]
        setattr(base, identifier, prop)

    if not deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(deform_update)

def unregister():
    virtual_driver.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    for identifier in paths:
        base, prop = paths[identifier]
        delattr(base, identifier)

    if deform_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(deform_update)
