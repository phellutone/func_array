import bpy
from .func_array_variable import FuncArrayVariable

class FuncArray(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty()

    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH'
    )
    eval_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH'
    )

    count: bpy.props.IntProperty(
        min=1,
        default=1,
        soft_max=25
    )

    variables: bpy.props.CollectionProperty(type=FuncArrayVariable)
    active_variable_index: bpy.props.IntProperty()

class FUNCARRAY_OT_add(bpy.types.Operator):
    bl_idname = 'func_array.add'
    bl_label = 'add'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        block: FuncArray = farray.add()

        block.name = 'Array '+str(len(farray))
        block.index = len(farray)-1
        context.scene.active_func_array_index = len(farray)-1

        bpy.ops.func_array.variable_add()
        return {'FINISHED'}

class FUNCARRAY_OT_remove(bpy.types.Operator):
    bl_idname = 'func_array.remove'
    bl_label = 'remove'
    bl_description = ''
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        farray: list[FuncArray] = context.scene.func_array
        index: int = context.scene.active_func_array_index
        if index < 0 or not farray:
            return {'CANCELLED'}

        block: FuncArray = farray[index]

        farray.remove(index)

        for b in farray:
            if b.index < index:
                continue
            b.index = b.index-1

        context.scene.active_func_array_index = min(max(0, index), len(farray)-1)
        return {'FINISHED'}

class OBJECT_UL_FuncArray(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(item, 'name', icon='ANIM', text='', emboss=False)
            row.prop(item, 'mute', icon='CHECKBOX_HLT' if not item.mute else 'CHECKBOX_DEHLT', text='', emboss=False)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text='', icon=icon)

class OBJECT_PT_FuncArray(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_idname = "VIEW3D_PT_func_array"
    bl_label = "Func Array"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.template_list("OBJECT_UL_FuncArray", "", scene, "func_array", scene, "active_func_array_index", rows=3)
        col = row.column(align=True)
        col.operator("func_array.add", icon="ADD", text="")
        col.operator("func_array.remove", icon="REMOVE", text="")

        if scene.func_array:
            index = scene.active_func_array_index
            block = scene.func_array[index]

            col = layout.column()
            col.prop(block, "target", text="Target")
            col.prop(block, "count", text="Count")


classes = (
    FuncArray,
    FUNCARRAY_OT_add,
    FUNCARRAY_OT_remove,
    OBJECT_UL_FuncArray,
    OBJECT_PT_FuncArray
)
