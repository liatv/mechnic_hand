# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
import os
import bpy
import io_mesh_stl.stl_utils
from bpy.props import (
        StringProperty,
        BoolProperty,
        CollectionProperty,
        EnumProperty,
        FloatProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        )
from bpy.types import (
        Operator,
        OperatorFileListElement,
        )
# from mathutils import Matrix
# from stl import mesh

class Import_STL_Mechanic_Operator(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "mechanic_bones.import_stl"
    bl_label = "Import STL"

    filename_ext = ".stl"

    filter_glob = StringProperty(
            default="*.stl",
            options={'HIDDEN'},
            )
    files = CollectionProperty(
            name="File Path",
            type=OperatorFileListElement,
            )
    directory = StringProperty(
            subtype='DIR_PATH',
            )

    global_scale = FloatProperty(
            name="Scale",
            soft_min=0.001, soft_max=1000.0,
            min=1e-6, max=1e6,
            default=1.0,
            )

    use_scene_unit = BoolProperty(
            name="Scene Unit",
            description="Apply current scene's unit (as defined by unit scale) to imported data",
            default=False,
            )

    use_facet_normal = BoolProperty(
            name="Facet Normals",
            description="Use (import) facet normals (note that this will still give flat shading)",
            default=False,
            )

    def createMesh(self, name, verts, edges, faces, context):
        add_mesh = bpy.data.meshes.new(name)     # Create mesh and object
        ob = bpy.data.objects.new(name, add_mesh)
        bpy.context.collection.objects.link(ob)
        add_mesh.from_pydata(verts, edges, faces)
        add_mesh.update(calc_edges=True)    # Update mesh with new data
        # add_mesh.transform(Matrix.Scale(0.1, 4, (1, 1, 1)))
        return ob

    def load_stl(self, file, name, context):
        # change to blender unit to match the stl file  
        # we can do that in a diffrent way 
        # like set it from the addon
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
        bpy.context.scene.unit_settings.scale_length = 0.001
        bpy.context.space_data.clip_end = 10000
        bpy.context.space_data.overlay.grid_scale = 0.001

        tris, tri_nors, pts = io_mesh_stl.stl_utils.read_stl(file)

        self.createMesh(name.split('.')[0], pts, [], tris, context)

    def execute(self, context):
        for file in self.files: 
            path = os.path.join(self.directory, file.name)
            self.load_stl(path, file.name, context)

        return {'FINISHED'}
