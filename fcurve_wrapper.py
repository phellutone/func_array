from typing import Literal, Union
import re
import bpy
from .utils import anim_index

class FCurveWrapper(bpy.types.PropertyGroup):
    id: bpy.props.PointerProperty(type=bpy.types.ID)
    data_path: bpy.props.StringProperty()
    array_index: bpy.props.IntProperty()

    def observe(self) -> Union[
                            tuple[Literal[True], int],
                            tuple[Literal[False], str]
                        ]:
        if self.id == None or self.data_path == '':
            return (False, 'INPUT')
        if not hasattr(self.id, 'animation_data'):
            return (False, 'ID')
        if not self.id.animation_data:
            return (False, 'ANIMATION_DATA')
        fixes = [i for i, f in enumerate(self.id.animation_data.drivers) if f.data_path == self.data_path]
        if not fixes:
            return (False, 'PATH')
        if len(fixes) > 1:
            return (False, 'DUPLICATE')
        return (True, fixes[0])
    
    def resolve(self) -> Union[bpy.types.FCurve, None]:
        res, dat = self.observe()
        if not res:
            if dat == 'INPUT':
                return
            if dat == 'ID':
                return
            if dat == 'ANIMATION_DATA':
                self.id.animation_data_create()
                dat = 'PATH'
            if dat == 'PATH':
                self.add_driver()
                _, dat = self.observe()
            if dat == 'DUPLICATE':
                return
        return self.id.animation_data.drivers[dat]
    
    # def variable_update(self, id: bpy.types.ID, path: str):
    #     res, dat = self.observe()
    #     if not res:
    #         return
    #     fcurve = self.id.animation_data.drivers[dat]
    #     driver = fcurve.driver
    #     v1 = [v for v in driver.variables if v.type == 'SINGLE_PROP']
    #     v2 = [v for v in v1 if v.targets[0].id == id]
    #     v3 = [v for v in v2 if v.targets[0].data_path == path]
    #     [v for v in driver.variables if v.targets[0].id == id and re.search('func_array\[\d+\].variables\[\d+\]', v.targets[0].data_path)]

    def init(self, id: bpy.types.ID, path: str):
        res, dat = anim_index(id, path)
        if not res:
            return

        idx = -1 if dat[-1][0] is None else 0
        self.id = id
        self.data_path = dat[-1+idx][1]
        self.array_index = dat[-1][3] if isinstance(dat[-1][3], int) else 0

        res, dat = self.observe()
        if not res:
            
