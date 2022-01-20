
import bpy
from .properties import FuncArray, FuncArrayDummy, FuncArrayObject, FuncArrayIndex
from .operators import FUNCARRAY_OT_VD_remove, FUNCARRAY_OT_add, FUNCARRAY_OT_remove, FUNCARRAY_OT_activation, FUNCARRAY_OT_VD_add
from .panels import OBJECT_UL_FuncArray, OBJECT_PT_FuncArray, OBJECT_PT_FuncArrayVD
from .handlers import deform_update, favd_access_context, favd_access_id
from .virtual_driver import virtual_driver



virtual_driver.VIRTUALDRIVER_OT_add.bl_idname = FUNCARRAY_OT_VD_add.bl_idname
virtual_driver.VIRTUALDRIVER_OT_remove.bl_idname = FUNCARRAY_OT_VD_remove.bl_idname


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
        FuncArray,
        FUNCARRAY_OT_VD_add,
        FUNCARRAY_OT_VD_remove
    ]+[cls for cls in virtual_driver.classes if not cls in (
        virtual_driver.OBJECT_PT_VirtualDriver,
        virtual_driver.VIRTUALDRIVER_OT_add,
        virtual_driver.VIRTUALDRIVER_OT_remove
    )]
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
