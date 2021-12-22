import bpy

_FUNCARRAY_DEPSGRAPHS: list[tuple[int, bpy.types.Depsgraph]] = []

class FuncArrayObject(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    is_activate: bpy.props.BoolProperty()
    is_computing: bpy.props.BoolProperty()
    is_evaluated: bpy.props.BoolProperty()
    object: bpy.props.PointerProperty(type=bpy.types.Object)

class FuncArray(bpy.types.PropertyGroup):
    index: bpy.props.IntProperty()
    name: bpy.props.StringProperty()
    mute: bpy.props.BoolProperty(default=False)

    is_activate: bpy.props.BoolProperty()

    target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=lambda self, object: object.type == 'MESH' and not object.is_func_array_dummy
    )
    eval_targets: bpy.props.CollectionProperty(type=FuncArrayObject)

    count: bpy.props.IntProperty(
        min=1,
        default=1,
        soft_max=25
    )

    controller: bpy.props.FloatProperty(
        min=0.0,
        max=1.0
    )
    def ctr_update(self, context):
        self.__class__.controller = bpy.props.FloatProperty(
            min=self.ctr_min,
            max=self.ctr_max
        )
    ctr_min: bpy.props.FloatProperty(
        default=0.0,
        update=ctr_update
    )
    ctr_max: bpy.props.FloatProperty(
        default=1.0,
        update=ctr_update
    )

    trg_co: bpy.props.PointerProperty(type=bpy.types.Collection)
    trg_ob: bpy.props.PointerProperty(type=bpy.types.Object)
