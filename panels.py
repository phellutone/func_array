
import bpy
from .operators import FUNCARRAY_OT_activation, FUNCARRAY_OT_add, FUNCARRAY_OT_remove
from .properties import FuncArray, FuncArrayIndex



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
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_idname = 'VIEW3D_PT_func_array'
    bl_label = 'Func Array'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context: bpy.types.Context) -> None:
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.template_list(
            OBJECT_UL_FuncArray.__name__,
            '',
            scene,
            FuncArray.identifier,
            scene,
            FuncArrayIndex.identifier,
            rows=3
        )
        col = row.column(align=True)
        col.operator(FUNCARRAY_OT_add.bl_idname, icon='ADD', text='')
        col.operator(FUNCARRAY_OT_remove.bl_idname, icon='REMOVE', text='')

        farray: list[FuncArray] = getattr(scene, FuncArray.identifier)
        if farray:
            index: int = getattr(scene, FuncArrayIndex.identifier)
            block = farray[index]

            col = layout.column()

            row = col.row()
            if block.is_activate:
                row.operator(FUNCARRAY_OT_activation.bl_idname, text='Deactivate', icon='PAUSE')
            else:
                row.operator(FUNCARRAY_OT_activation.bl_idname, text='Activate', icon='PLAY')

            box = col.box().column()
            boc = box.column()
            box.prop(block, 'target', text='Target')
            box.prop(block, 'count', text='Count')

            row = box.row(align=True)
            row.prop(block, 'ctr_min', text='Min')
            row.prop(block, 'ctr_max', text='Max')

            box.prop(block, 'controller')
