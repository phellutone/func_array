
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

from . import func_array

def register():
    func_array.register()

def unregister():
    func_array.unregister()