
import bpy




class FuncArrayObject(bpy.types.PropertyGroup):
    identifier = 'func_array_object'

    object: bpy.props.PointerProperty(
        name='Object',
        type=bpy.types.Object
    )

class FuncArray(bpy.types.PropertyGroup):
    identifier = 'func_array'

    def target_poll(self, object: bpy.types.Object) -> bool:
        return object.type == 'MESH' and not getattr(object, FuncArrayDummy.identifier)

    def controller_update(self, context: bpy.types.Context) -> None:
        if self.ctr_range < 0:
            return
        if self.ctr_max < self.controller:
            self.controller = self.ctr_max
        elif self.controller < self.ctr_min:
            self.controller = self.ctr_min

    def ctr_range_update(self, context: bpy.types.Context) -> None:
        if self.ctr_min <= self.ctr_max:
            self.ctr_range = self.ctr_max-self.ctr_min
        else:
            self.ctr_range = -1

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

    controller: bpy.props.FloatProperty(
        name='Controller',
        update=controller_update
    )

    ctr_min: bpy.props.FloatProperty(
        name='Min',
        default=0.0,
        update=ctr_range_update
    )
    ctr_max: bpy.props.FloatProperty(
        name='Max',
        default=1.0,
        update=ctr_range_update
    )
    ctr_range: bpy.props.FloatProperty(
        name='Control Range',
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
