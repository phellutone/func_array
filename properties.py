
import bpy



_FUNCARRAY_DEPSGRAPHS: list[tuple[int, bpy.types.Depsgraph]] = []


class FuncArrayObject(bpy.types.PropertyGroup):
    identifier = 'func_array_object'

    index: bpy.props.IntProperty()
    is_activate: bpy.props.BoolProperty()
    is_computing: bpy.props.BoolProperty()
    is_evaluated: bpy.props.BoolProperty()
    object: bpy.props.PointerProperty(type=bpy.types.Object)

class FuncArray(bpy.types.PropertyGroup):
    identifier = 'func_array'

    index: bpy.props.IntProperty()
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty(default=False)

    is_activate: bpy.props.BoolProperty()

    def target_poll(self, object: bpy.types.Object) -> bool:
        return object.type == 'MESH' and not object.is_func_array_dummy
    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=target_poll
    )
    eval_targets: bpy.props.CollectionProperty(type=FuncArrayObject)

    count: bpy.props.IntProperty(
        min=1,
        default=1,
        soft_max=25
    )

    def controller_update(self, context: bpy.types.Context) -> None:
        if self.ctr_min < self.controller and self.ctr_max < self.controller:
            self.controller = self.ctr_max
        if self.controller < self.ctr_min and self.controller < self.ctr_max:
            self.controller = self.ctr_min
    controller: bpy.props.FloatProperty(
        update=controller_update
    )
    ctr_min: bpy.props.FloatProperty(
        default=0.0
    )
    ctr_max: bpy.props.FloatProperty(
        default=1.0
    )

    trg_co: bpy.props.PointerProperty(type=bpy.types.Collection)
    trg_ob: bpy.props.PointerProperty(type=bpy.types.Object)

class FuncArrayIndex:
    identifier = 'active_func_array_index'

class FuncArrayDummy:
    identifier = 'is_func_array_dummy'
