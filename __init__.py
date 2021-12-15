
bl_info = {
    'name': 'func array',
    'author': 'phellutone',
    'version': (0, 0, 1),
    'blender': (2, 93, 0),
    'location': 'View3D > Sidebar > Tool Tab',
    'description': 'functionally object array tool',
    'support': 'TESTING',
    'tracker_url': 'https://github.com/phellutone/func_array/issues',
    'category': 'Object'
}


if 'bpy' in locals():
    import imp
    imp.reload(func_array)
    imp.reload(func_array_variable)
else:
    from .func_array import FuncArray, FUNCARRAY_OT_add, FUNCARRAY_OT_remove, FUNCARRAY_OT_activate, OBJECT_UL_FuncArray, OBJECT_PT_FuncArray
    from .func_array_variable import FuncArrayVariable, FUNCARRAY_OT_variable_add, FUNCARRAY_OT_variable_remove, OBJECT_UL_FuncArrayVariable, OBJECT_PT_FuncArrayVariable

import bpy

classes = (
    FuncArrayVariable,
    FuncArray,
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    FUNCARRAY_OT_activate,
    FUNCARRAY_OT_variable_add,
    FUNCARRAY_OT_variable_remove,
    OBJECT_UL_FuncArray,
    OBJECT_UL_FuncArrayVariable,
    OBJECT_PT_FuncArray,
    OBJECT_PT_FuncArrayVariable
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.func_array = bpy.props.CollectionProperty(type=FuncArray)
    bpy.types.Scene.active_func_array_index = bpy.props.IntProperty()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.func_array
    del bpy.types.Scene.active_func_array_index