
import bpy



_FUNCARRAY_DEPSGRAPHS: list[tuple[int, bpy.types.Depsgraph]] = []


class FuncArrayObject(bpy.types.PropertyGroup):
    identifier = 'func_array_object'

    object: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object
    )

class FuncArray(bpy.types.PropertyGroup):
    identifier = 'func_array'

    index: bpy.props.IntProperty(
        name='Index'
    )
    name: bpy.props.StringProperty(
        name='Name'
    )
    mute: bpy.props.BoolProperty(
        name='Mute',
        default=False
    )

    is_activate: bpy.props.BoolProperty(
        name='Is Activate'
    )

    def target_poll(self, object: bpy.types.Object) -> bool:
        return object.type == 'MESH' and not object.is_func_array_dummy
    target: bpy.props.PointerProperty(
        name='Target',
        type=bpy.types.Object,
        poll=target_poll
    )
    eval_targets: bpy.props.CollectionProperty(
        name='Evaluate Targets',
        type=FuncArrayObject
    )

    count: bpy.props.IntProperty(
        name='Count',
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
        name='Controller',
        update=controller_update
    )
    ctr_min: bpy.props.FloatProperty(
        name='Min',
        default=0.0
    )
    ctr_max: bpy.props.FloatProperty(
        name='Max',
        default=1.0
    )

    trg_co: bpy.props.PointerProperty(
        name='Collection',
        type=bpy.types.Collection
    )
    trg_ob: bpy.props.PointerProperty(
        name='Instance Object',
        type=bpy.types.Object
    )

class FuncArrayIndex:
    identifier = 'active_func_array_index'

class FuncArrayDummy:
    identifier = 'is_func_array_dummy'
