import bpy

class PathResolver:
    #   id.data_path.prop_path[index]
    # [  bpy_struct].[           str] layout
    # [ID].[              str][  int] fcurve
    # 
    # id.path_resolve(data_path), prop_path+'['+index+']'
    # id, data_path+'.'+prop_path, index

    def __init__(self, id: bpy.types.ID, path: str):
        if isinstance(id, bpy.types.ID) and not path == '':
            try:
                id.path_resolve(path)
                pd = self.path_disassembly(path)
                pa = self.path_assembly(id, pd)

                self.graph = pa
                self.state = True
                return
            except Exception as _:
                pass
        self.state = False
        return
    
    def id_path_index(self):
        if not self.state:
            return None
        
        prop, _, _, e, t = self.graph[-1]
        if t == 'int':
            (self.graph[0][2], self.graph[-3][1], self.graph[-2][3], e)
        elif t == 'path':
            (self.graph[0][2], self.graph[-2][1], self.graph[-1][3], 0)
        # if prop is None:
        #     prop = self.graph[-2][0]
        # if isinstance(prop, bpy.types.Property):
        #     # if not prop.is_animatable:
        #     #     return None
        #     # if prop.is_readonly:
        #     #     return None
        #     if prop.type in ('BOOL', 'INT', 'FLOAT'):
        #         if prop.is_array and type(e) is int:
        #             if self.graph[-1][0] is None:
        #                 return self.graph
        #             else:
        #                 return None
        #     return self.graph
        # return None

    def path_disassembly(self, path: str):
        tmp = ''
        res = []
        sid = -1
        for i, s in enumerate(path):
            if sid != -1 and sid != i:
                continue
            sid = -1
            if s == '[':
                res.append(('path', tmp))
                r, tmp = self.path_disassembly(path[i+1:])
                sid = r+i
                if len(tmp) > 1:
                    res.append(('eval', tmp))
                else:
                    res.append(tmp[0])
                tmp = ''
            elif s == '.':
                if tmp:
                    res.append(('path', tmp))
                tmp = ''
            elif s == '"':
                idx = path.find('"', i+1)
                res.append(('str', path[i:idx+1]))
                sid = idx+1
                tmp = ''
            elif s == ']':
                if tmp.isdigit():
                    res.append(('int', int(tmp)))
                elif tmp:
                    res.append(('path', tmp))
                return i+2, res
            else:
                tmp += s
        if tmp:
            res.append(('path', tmp))
        return res

    def path_assembly(self, id: bpy.types.ID, path: list, resolve=True):
        res = [(None, '', id, '', '')]
        tmp = id
        stmp = ''
        f = True
        for i, p in enumerate(path):
            if p[0] == 'path':
                e = p[1]
                ev = ('' if f else '.')+e
                f = False
            elif p[0] in ('int', 'str'):
                e = p[1]
                ev = '['+str(e)+']'
            else:
                e = eval(self.path_assembly(id, p[1], False)[-1][1])
                ev = '['+str(e)+']'
            prop = None
            stmp = stmp+ev
            if resolve:
                try:
                    prop = tmp.bl_rna.properties[e]
                except Exception as _:
                    prop = None
                tmp = id.path_resolve(stmp)
            res.append((prop, stmp, tmp, e, p[0]))
        return res

def anim_index(id: bpy.types.ID, path: str):
    pr = PathResolver(id, path)
    if not pr.state:
        return (False, 'invalid: could\'nt resolve the path')
    
    graph = pr.graph
    # for p in graph:
    #     print(p)

    prop, stmp, tmp, e, _ = graph[-1]
    if prop is None:
        prop, stmp, _, _, _ = graph[-2]
    if isinstance(prop, bpy.types.Property):
        if not prop.is_animatable:
            return (False, 'invalid: the property is not animatable')
        if prop.is_readonly:
            return (False, 'invalid: the property is readonly')
        if prop.type in ('BOOL', 'INT', 'FLOAT'):
            if prop.is_array:
                if type(e) == int:
                    return (True, graph)
                else:
                    return (False, 'invalid: set the array index of the property')
        return (True, graph)
    return (False, 'invalid: the property is not support')
