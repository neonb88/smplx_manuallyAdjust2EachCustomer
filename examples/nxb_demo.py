# -*- coding: utf-8 -*-

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: ps-license@tuebingen.mpg.de

import os.path as osp
import argparse

import numpy as np
import torch

import smplx

import datetime # added by nxb, August 13, 2020

def main(model_folder, model_type='smplx', ext='npz',
         gender='neutral', plot_joints=False,
         plotting_module='pyrender',
         use_face_contour=False):

    model = smplx.create(model_folder, model_type=model_type,
                         gender=gender, use_face_contour=use_face_contour,
                         ext=ext)
    print(model)

    output_dir_fname='/home/nathan_bendich/Documents/code/gitCloned/smplx/examples/out_meshes/'
    local_output_dir_fname='/home/nathan_bendich/Documents/code/gitCloned/smplx/examples/'
    #betas = torch.randn([1, 10], dtype=torch.float32)    originally random
    betas = torch.zeros([1, 10], dtype=torch.float32)    #originally random      -nxb, August 13, 2020
    #betas[0]=4     # NOTE: changing the betas actually changes the verts.    -nxb, August 13, 2020
    expression = torch.randn([1, 10], dtype=torch.float32)

    output = model(betas=betas, expression=expression,
                   return_verts=True)
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    '''
      maxesAndMins:
        {'xMax': 0.8656285,
         'xMin': -0.8656085,
         'yMax': 0.43483356,
         'yMin': -1.3589503,
         'zMax': 0.15359592,
         'zMin': -0.1527159}
    '''
    joints = output.joints.detach().cpu().numpy().squeeze()

    #print('betas =', betas)              # betas = tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    #print('betas.shape =', betas.shape)  # torch.Size([1,10])
    print('Vertices shape =', vertices.shape) # (10475,3)
    print('Vertices type =', type(vertices)  ) # "numpy.ndarray" ;   I'm like 90% sure)    
    timestamp= datetime.datetime.now().strftime('%Y_%m_%d____%H:%M_%p__')

    #================================================================================
    #                                   Save:
    #================================================================================
    # save done properly,  with timestamps:  
    np.save('{}smplxVerts_{}.npy'.format(output_dir_fname, timestamp), vertices    )
    # "local" save:
    np.save('{}currSmplxVerts.npy'.format(local_output_dir_fname), vertices    )

    print('Joints shape =', joints.shape)     # (127,  3)

    if plotting_module == 'pyrender':
        import pyrender
        import trimesh
        import trimesh.exchange.obj #  Added by nxb on   August 13, 2020
        vertex_colors = np.ones([vertices.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8]
        tri_mesh = trimesh.Trimesh(vertices, model.faces,
                                   vertex_colors=vertex_colors)

        #================================================================================
        #                                   Save:
        #================================================================================
        # Added by NXB, August 13, 2020 :
        export_obj = trimesh.exchange.obj.export_obj(tri_mesh, include_texture=True)
        print("="*99)
        print("about to write mesh as .obj file")

        # Save in backupdir with timestamps:
        with open('{}out.obj'.format(output_dir_fname), 'w') as fp:    trimesh.util.write_encoded(fp, export_obj)
        # "local" save:
        with open('out.obj'.format(output_dir_fname), 'w') as fp:    trimesh.util.write_encoded(fp, export_obj)

        mesh = pyrender.Mesh.from_trimesh(tri_mesh)

        scene = pyrender.Scene()
        scene.add(mesh)

        if plot_joints:
            sm = trimesh.creation.uv_sphere(radius=0.005)
            sm.visual.vertex_colors = [0.9, 0.1, 0.1, 1.0]
            tfs = np.tile(np.eye(4), (len(joints), 1, 1))
            tfs[:, :3, 3] = joints
            joints_pcl = pyrender.Mesh.from_trimesh(sm, poses=tfs)
            scene.add(joints_pcl)

        pyrender.Viewer(scene, use_raymond_lighting=True)
    elif plotting_module == 'matplotlib':
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        mesh = Poly3DCollection(vertices[model.faces], alpha=0.1)
        face_color = (1.0, 1.0, 0.9)
        edge_color = (0, 0, 0)
        mesh.set_edgecolor(edge_color)
        mesh.set_facecolor(face_color)
        ax.add_collection3d(mesh)
        ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], color='r')

        if plot_joints:
            ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2], alpha=0.1)
        plt.show()
    elif plotting_module == 'open3d':
        import open3d as o3d

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(
            vertices)
        mesh.triangles = o3d.utility.Vector3iVector(model.faces)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color([0.3, 0.3, 0.3])

        o3d.visualization.draw_geometries([mesh])
    else:
        raise ValueError('Unknown plotting_module: {}'.format(plotting_module))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SMPL-X Demo')

    parser.add_argument('--model-folder', required=True, type=str,
                        help='The path to the model folder')
    parser.add_argument('--model-type', default='smplx', type=str,
                        choices=['smpl', 'smplh', 'smplx'],
                        help='The type of model to load')
    parser.add_argument('--gender', type=str, default='neutral',
                        help='The gender of the model')
    parser.add_argument('--plotting-module', type=str, default='pyrender',
                        dest='plotting_module',
                        choices=['pyrender', 'matplotlib', 'open3d'],
                        help='The module to use for plotting the result')
    parser.add_argument('--ext', type=str, default='npz',
                        help='Which extension to use for loading')
    parser.add_argument('--plot-joints', default=False,
                        type=lambda arg: arg.lower() in ['true', '1'],
                        help='The path to the model folder')
    parser.add_argument('--use-face-contour', default=False,
                        type=lambda arg: arg.lower() in ['true', '1'],
                        help='Compute the contour of the face')

    args = parser.parse_args()

    model_folder = osp.expanduser(osp.expandvars(args.model_folder))
    model_type = args.model_type
    plot_joints = args.plot_joints
    use_face_contour = args.use_face_contour
    gender = args.gender
    ext = args.ext
    plotting_module = args.plotting_module

    main(model_folder, model_type, ext=ext,
         gender=gender, plot_joints=plot_joints,
         plotting_module=plotting_module,
         use_face_contour=use_face_contour)
