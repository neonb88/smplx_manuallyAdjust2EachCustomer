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

#==============================================
# imports   added by nxb, August 13, 2020   :
import datetime # added by nxb, August 13, 2020
from copy import deepcopy # Aug 14, 2020
#==============================================

#==================================================
def getResizedLeftSMPLX_Tibia(vertices, customerEstimatedTibiaLenInches, customerEstimatedHeightInches):    # we don't have this customerEstimatedTibiaLenInches, 
  # TODO:  find the EXACT RIGHT VERTEX  in SMPL-X that will let us scale the tibia correctly
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  # TODO    TODO TODO TODO TODO
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE: NOTE: NOTE: NOTE: NOTE:  slight assumption that causes a problem:  I can't really scale  the tibia directly to yHeight==1, because the SMPL-X tibia we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the tibia correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the tibia correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the tibia correctly 
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # TODO TODO  TODO TODO TODO
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  X,Y,Z=0,1,2

  leftTibiaIdxes = leftTibiaIndices(vertices)
  print(" "* 9)
  print("="*99)
  print("leftTibiaIndices: ")
  print(leftTibiaIdxes)
  print("leftTibiaIdxes.shape: ")
  print(leftTibiaIdxes.shape)
  print("="*99)
  print(" "* 9)
  leftTibiaVerts = deepcopy(vertices[leftTibiaIdxes, : ] )      # TODO:   do translation and scaling on this shit.   -nxb, August 14, 2020

  # Center:
  #   (newTibiaCentroid = (0,0,0)  )
  origTibiaCentroid = leftTibiaVerts.mean(axis=0)  # DOWN=0
  #====================================================================================
  # TODO: rename all these hellishly-long-variable names to simply "leftTibiaVerts"  
  #====================================================================================
  leftTibiaVertsCenteredOnOrigin = leftTibiaVerts - origTibiaCentroid

  # Scale down:
  #   Normalize tibiaLen to 1:
  #     NOTE:  (tibiaLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of tibia;   **doesn't lose information**    -nxb; August 14, 2020
  currHeightY = leftTibiaVertsCenteredOnOrigin[:,Y].max() - leftTibiaVertsCenteredOnOrigin[:,Y].min()
  leftTibiaVertsCenteredOnOrigin /= currHeightY
  #====================================================================================================================
  # NOTE
  # NOTE
  # NOTE:  slight assumption that causes a problem:  I can't really scale  the tibia directly to yHeight==1, because the SMPL-X tibia we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  # NOTE
  # NOTE
  #====================================================================================================================
  #   In code, "T-Pose" translates to      ("` theta==np.zeros( 127*3 )`")
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the tibia correctly 

  # Scale up again:
  leftTibiaVertsCenteredOnOrigin *=customerEstimatedTibiaLenInches
  #leftTibiaVertsCenteredOnOriginScaledToRealTibiaLenInches = leftTibiaVertsCenteredOnOriginNormalizedTo1 * customerEstimatedTibiaLenInches
  #leftTibiaVertsCenteredOnOrigin *= customerEstimatedTibiaLenInches
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the tibia correctly 

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftTibiaVerts = leftTibiaVertsCenteredOnOrigin + origTibiaCentroid

  return finalResizedLeftTibiaVerts, leftTibiaIdxes




  resizedVerts = deepcopy(vertices)
  print(" "* 9)
  print("="*99)
  print("resizedVerts.shape: ")
  print(resizedVerts.shape)
  print("="*99)
  print(" "* 9)
  resizedVerts[leftTibiaIdxes,: ] *= 2 # this line should do some weird geometry to the SMPL-X model's left tibia    -nxb, August 14, 2020
  #vertices[:, leftTibiaIdxes] *= 2 # this line should do some weird geometry to the SMPL-X model's left tibia    -nxb, August 14, 2020
  return resizedVerts
  raise Exception( "fucking finish your code, Bendich.")
#==================================================

#==================================================
# TODO:  resurrect a general version of this (ie. all you have to do is tell it "lTibiaLen" or "lThighLen" and it spits out a properly resized   'numpy.ndarray' variable    "`SMPLX_Verts`"
"""
  # TODO:  resurrect a general version of this (ie. all you have to do is tell it "lTibiaLen" or "lThighLen" and it spits out a properly resized   'numpy.ndarray' variable    "`SMPLX_Verts`"
def filterVerts(vs):
  '''
    TODO:  generalize w/ a keyword arguments?      (ie. "lTibia" or "lThigh" or "lFoot" or whatever)
      -nxb; Aug 14, 2020
  '''
  return filterVertsLeftTibia(vs)
"""
#==================================================

#==================================================
def leftTibiaIndices(vs):
#def filterVertsLeftTibia(vs):
  L_KNEE_Y_HEIGHT  = -0.8582508 
  L_ANKLE_Y_HEIGHT = -1.2795366  
  MIDDLE_OF_BODY_X = 0      # **__ROUGHLY__** correct;   certainly correct enough to distinguish between the left and right tibias (in t-pose with legs "fairly widely" spread)
  X, Y, Z = 0,1,2

  belowKneeIdxs = np.where(   
    np.less(vs[:,Y],   
            L_KNEE_Y_HEIGHT))[0]
  aboveAnkleIdxs = np.where(   
    np.greater(vs[:,Y],   
            L_ANKLE_Y_HEIGHT))[0]
  leftSideOFBodyIdxs = np.where(
    np.greater(vs[:,X],
            MIDDLE_OF_BODY_X))[0]

  # belowKnees AND aboveAnkles:
  tibiasVertsIdxs     = np.intersect1d(  aboveAnkleIdxs,  belowKneeIdxs) 
  leftTibiasVertsIdxs = np.intersect1d(  tibiasVertsIdxs, leftSideOFBodyIdxs) 
  return leftTibiasVertsIdxs
  #leftTibia           = vs[leftTibiasVertsIdxs, :]
  #return leftTibia


#==================================================


#==================================================
def main(model_folder, model_type='smplx', ext='npz',
         gender='neutral', plot_joints=False,
         plotting_module='pyrender',
         use_face_contour=False):

    model = smplx.create(model_folder, model_type=model_type,
                         gender=gender, use_face_contour=use_face_contour,
                         ext=ext)
    print(model)

    #output_dir_fname='/home/nathan_bendich/Documents/code/gitCloned/smplx/examples/out_meshes/'  # in DropBox now.     -nxb;   August 14, 2020.
    output_dir_fname='/home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/smplx_manuallyAdjust2EachCustomer/examples/out_meshes/'
    local_output_dir_fname='/home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/smplx_manuallyAdjust2EachCustomer/examples/'
    #local_output_dir_fname='/home/nathan_bendich/Documents/code/gitCloned/smplx/examples/'  # in DropBox now.     -nxb;   August 14, 2020.
    #betas = torch.randn([1, 10], dtype=torch.float32)    originally random
    betas = torch.zeros([1, 10], dtype=torch.float32)    #originally random      -nxb, August 13, 2020
    #betas[0]=4     # NOTE: changing the betas actually changes the verts.    -nxb, August 13, 2020
    expression = torch.randn([1, 10], dtype=torch.float32)

    output = model(betas=betas, expression=expression,
                   return_verts=True)
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    #TIM_ESTIMATED_TIBIA_LENGTH_INCHES = ...  # TODO: automate estimating customer's tibia length from video(s) and OpenPose.  -nxb, August 14, 2020
    # NOTE: 
    '''       -nxb, August 14, 2020
      For both:
        1.    TIM_PIXEL_HEIGHT_INCHES  and
          (and)
        2.    TIM_LEFT_TIBIA_PIXEL_LEN_INCHES
      I (NXB) measured Tim's height in inches using a video of him, viewed on my laptop screen, and then held up a ruler to measure it.
      The pic of him can be found in NXB's Dropbox (Dropbox/vr_mal.../IMPOR.../Tim_Schrader_8_frames.../*)     
      (The filepath on NXB's HP laptop is "` /home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/Tim_Schrader_8_Frames_____June_30_2020/0_degrees_____facing_camera.jpg `")

      Algorithm for what I did to get these measurements:
      1) open the image with "`feh`" :
        (`feh /home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/Tim_Schrader_8_Frames_____June_30_2020/0_degrees_____facing_camera.jpg `)
        and then
      2) hit the "down" arrow key 3 times to "zoom out." and then    
      3) measured between 2 "pixel points" I visually estimated on my laptop screen   with the ruler    TODO: reformat this comment in a 
        a) for TIM_PIXEL_HEIGHT_INCHES,
          I measured between 
            1. the top of    Tim's head on the screen and   
            2. the bottom of Tim's feet on the screen
        b) for TIM_LEFT_TIBIA_PIXEL_LEN_INCHES  
          I measured between 
            1. the "inside" of Tim's knee on the screen and the    
            2. the  inside of Tim's left ankle on the screen
    # end comment:  }   (})

       -nxb, August 14, 2020
    '''
    # end NOTE:
    TIM_PIXEL_HEIGHT_INCHES = 5.6875
    TIM_LEFT_TIBIA_PIXEL_LEN_INCHES = 1.375
    TIM_SELF_REPORTED_HEIGHT_INCHES = 74     #   Tim's probably exaggerating how tall he is.
    # "Tim's probably shorter than he says he is" comment continued:    "but I guess I'll cut him some slack for a fucking sec.  Of course, when it comes to literally getting him ideal jeans, we should use camera parameters to estimate his body measurements better."   -nxb, August 14, 2020   
    TIM_TIBIA_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN = \
      TIM_LEFT_TIBIA_PIXEL_LEN_INCHES *\
      (TIM_SELF_REPORTED_HEIGHT_INCHES / TIM_PIXEL_HEIGHT_INCHES) # how many "real" inches are in 1 pixel inch   
      #(on my laptop in `feh`, when I hit "down" 3 times, with Tim's Photo
    print("====================================================================")
    print("  TIM_TIBIA_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN :")  
    print( TIM_TIBIA_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN )
    print("====================================================================")

    # """
    # NXB's tibia (measured with a real measuring tape) is roughly 
    #   18 inches, 
    #     and my calculation says 
    #   17.89 inches for Tim Schrader's tibia.  
    # So my calculation is is probably MOSTLY correct.    
    # """
    #    -nxb;   on August 14, 2020      (more technically, 8:19 P.M. EDT    on August 14, 2020)

    #  Major Line:              (" ` resizeLeftSMPLX_Tibia(...) ` "  contains a LOT of code)
    reshapedLeftTibiaVerts, leftTibiaIdxes = getResizedLeftSMPLX_Tibia(vertices, TIM_TIBIA_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES)
    vertsWithReshapedLeftTibia = deepcopy(vertices)
    vertsWithReshapedLeftTibia[leftTibiaIdxes] = reshapedLeftTibiaVerts
 
    '''
      maxesAndMins:             NOTE: was this from "`verts`" or from "`joints`" ?   -nxb, August 14, 2020
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
    print('Vertices.shape =', vertices.shape) # (10475,3)
    print('Vertices type =', type(vertices)  ) # "numpy.ndarray" ;   
    
    '''
      maxesAndMins:             NOTE: was this from "`verts`" or from "`joints`" ?   -nxb, August 14, 2020
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
    # "local" save (joints:)
    np.save('{}currSmplxJoints.npy'.format(local_output_dir_fname), joints    )

    if plotting_module == 'pyrender':
        import pyrender
        import trimesh
        import trimesh.exchange.obj #  Added by nxb on   August 13, 2020
        vertex_colors = np.ones([vertices.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8]
        '''
          =============================================================================
          =============================================================================
            "DEV-mode"   "showMeTheCurrModel()"    code for showing the current mesh:
          =============================================================================
          =============================================================================
        '''
        reshapedTrimesh =  trimesh.Trimesh(vertsWithReshapedLeftTibia, model.faces,
                                   vertex_colors=vertex_colors) # nxb, Aug 13, 2020
        mesh = pyrender.Mesh.from_trimesh(reshapedTrimesh)

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

        #==============================================================================
        # After this line, it's (mostly) just the   
        #    original SMPL-X code from the original GitHub repo 
        #    (https://github.com/vchoutas/smplx):     
        #
        # -nxb, Aug 14, 2020
        #==============================================================================
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
        with open('{}out_{}.obj'.format(output_dir_fname, timestamp), 'w') as fp:     trimesh.util.write_encoded(fp, export_obj)
        # "local" save:
        with open('{}out.obj'.format(local_output_dir_fname), 'w') as fp:             trimesh.util.write_encoded(fp, export_obj)

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
