'''
{'xMax': 0.8656285,
 'xMin': -0.8656085,
 'yMax': 0.4348336,
 'yMin': -1.3589503,
 'zMax': 0.15359592,
 'zMin': -0.1527159}
'''

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

# pe and pn:
#from utils import pe, pn # Aug 18, 2020
def pn(n=0):  print('\n'*n) # Aug 18, 2020
def pe(n=89): print('='*n) # Aug 18, 2020
#==============================================




#==================================================
def getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxLowerLegWidthInches_X, customerEstimatedMaxLowerLegDepthInches_Z, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):
  X,Y,Z=0,1,2

  leftUpperLegIdxes = leftUpperLegIndices(vertices)
  leftUpperLegVerts = deepcopy(vertices[leftUpperLegIdxes, : ] )

  # Center:
  #   (newUpperLegCentroid = (0,0,0)  )
  origUpperLegCentroid = leftUpperLegVerts.mean(axis=0)  # DOWN=0
  #====================================================================================
  # TODO: rename all these hellishly-long-variable names to simply "leftUpperLegVerts"  
  #====================================================================================
  leftUpperLegVertsCenteredOnOrigin = leftUpperLegVerts - origUpperLegCentroid

  # Scale down:
  #   Normalize UpperLegLen to 1:
  #     NOTE:  (UpperLegLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of UpperLeg;   **doesn't lose information**    -nxb; August 14, 2020
  currHeightX = leftUpperLegVertsCenteredOnOrigin[:,X].max() - leftUpperLegVertsCenteredOnOrigin[:,X].min()
  currHeightY = leftUpperLegVertsCenteredOnOrigin[:,Y].max() - leftUpperLegVertsCenteredOnOrigin[:,Y].min()
  currHeightZ = leftUpperLegVertsCenteredOnOrigin[:,Z].max() - leftUpperLegVertsCenteredOnOrigin[:,Z].min()
  leftUpperLegVertsCenteredOnOrigin[:,X] /= currHeightX
  leftUpperLegVertsCenteredOnOrigin[:,Y] /= currHeightY
  leftUpperLegVertsCenteredOnOrigin[:,Z] /= currHeightZ
  #========================================================================================
  # Here the UpperLeg (AKA thigh) is weird-and-FAT-looking b/c its width is 1 while its height is also 1.
  #                         -nxb, August 17, 2020
  #========================================================================================

  # Scale up again:
  leftUpperLegVertsCenteredOnOrigin[:,X] *=customerEstimatedMaxUpperLegWidthInches_X
  leftUpperLegVertsCenteredOnOrigin[:,Y] *=customerEstimatedUpperLegLenInches
  leftUpperLegVertsCenteredOnOrigin[:,Z] *=customerEstimatedMaxUpperLegDepthInches_Z
  #=======================================================================================================================================================
  # Here the upperLeg is normally proportioned again because we're using the customer's **__ACTUAL__**   Depth, Width, and Height.     
  #   -nxb, August 17, 2020
  #=======================================================================================================================================================

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftUpperLegVertsTranslatedBack = leftUpperLegVertsCenteredOnOrigin + origUpperLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftUpperLegVertsTranslatedBack[:,Y] -= finalResizedLeftUpperLegVertsTranslatedBack[:,Y].min()

  return finalResizedLeftUpperLegVertsTranslatedBack, leftUpperLegIdxes, {} # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "makeLeftLeg(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):     ==================================================

#==================================================





#==================================================
# generalized version:      
#     def getResizedLeftSMPLX_LowerLeg(
#         vertices,
#         customerEstimatedLowerLegLenInches,
#         customerEstimatedHeightInches, 
#         prevBodyPartsXStretchingSlashScaling,  
#         prevBodyPartsZStretchingSlashScaling,  
#         currBodyPartsXStretchingSlashScaling,  
#         currBodyPartsZStretchingSlashScaling): 
#       # we don't have this variable "`customerEstimatedLowerLegLenInches`"  , 
#==================================================
def getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):
  '''
    This lowerLeg function SHOULD do the following:                  (August 18, 2020)
      (This docstring was written on August 18, 2020)

      """
        Expected, desired, non-buggy behavior:
          1.  Returns vertices **__MOSTLY__** centered on (0,0,0),   except the yMin is now 0.   

          2.  The truth is a little more detailed:
            a.  Basically, the SMPL-X base model I'm using has the center of the chest at (0,0,0).  
              (ie. The sternum is at the right xy position.  The anatomical location of z==0 is about as "deep" in the human body as the armpit(s))
            b.  Therefore, the output mesh should have the "bottom of the lowerLeg" at y==0 for easier matching

          This is only the way it should be for bodyParts like the upperLeg-lowerLeg boundary where the translation-before-smoothing is all along the **__Y__** axis.  For instance, for the foreArm-upperArm boundary in T-pose, the boundary should be along the **__X__** axis **__INSTEAD__**
      """
  '''

  #raise Exception( "fucking finish your code, Bendich.")

  # Idea:   have this spit out all the body parts with centroids at (0,0,0) ?    Then it's a different function's job to "put Humpty-Dumpty back together again"      -NXB, August 15, 2020

  # NOTE:    generalize this to be "getResizedLeftSMPLX_BodyPartNameHere(..., otherParams, ...)"  ?
  #   -nxb, August 15, 2020
  '''
    This function can be generalized to each body part?
    Code reuse would prevent some headaches, make it so changing error-catching in just the general function would fix the error(s) for all the body parts rather than just the one, 

    August 15, 2020
  '''


  # TODO:  find the EXACT RIGHT VERTEX  in SMPL-X that will let us scale the lowerLeg correctly
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  # TODO    TODO TODO TODO TODO
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE: NOTE: NOTE: NOTE: NOTE:  slight assumption that causes a problem:  I can't really scale  the lowerLeg directly to yHeight==1, because the SMPL-X lowerLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # TODO TODO  TODO TODO TODO
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================

    #===================================================================================================
    #   As of August 15, at 8:31 P.M.  EDT,   the function header was entitled:
    #===================================================================================================
    # function header " getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches): "
    #===================================================================================================
  X,Y,Z=0,1,2

  leftLowerLegIdxes = leftLowerLegIndices(vertices)
  leftLowerLegVerts = deepcopy(vertices[leftLowerLegIdxes, : ] )      # TODO:   do translation and scaling on this shit.   -nxb, August 14, 2020

  # Center:
  #   (newLowerLegCentroid = (0,0,0)  )
  origLowerLegCentroid = leftLowerLegVerts.mean(axis=0)  # DOWN=0
  #====================================================================================
  # TODO: rename all these hellishly-long-variable names to simply "leftLowerLegVerts"  
  #====================================================================================
  leftLowerLegVertsCenteredOnOrigin = leftLowerLegVerts - origLowerLegCentroid

  # Scale down:
  #   Normalize lowerLegLen to 1:
  #     NOTE:  (lowerLegLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of lowerLeg;   **doesn't lose information**    -nxb; August 14, 2020
  currHeightX = leftLowerLegVertsCenteredOnOrigin[:,X].max() - leftLowerLegVertsCenteredOnOrigin[:,X].min()
  currHeightY = leftLowerLegVertsCenteredOnOrigin[:,Y].max() - leftLowerLegVertsCenteredOnOrigin[:,Y].min()
  currHeightZ = leftLowerLegVertsCenteredOnOrigin[:,Z].max() - leftLowerLegVertsCenteredOnOrigin[:,Z].min()
  leftLowerLegVertsCenteredOnOrigin[:,X] /= currHeightX
  leftLowerLegVertsCenteredOnOrigin[:,Y] /= currHeightY
  leftLowerLegVertsCenteredOnOrigin[:,Z] /= currHeightZ
  #========================================================================================
  # Here the lowerLeg is weird-and-FAT-looking b/c its width is 1 while its height is also 1.
  #                         -nxb, August 17, 2020
  #========================================================================================

  #====================================================================================================================
  # NOTE
  # NOTE:  slight assumption that causes a problem:  I can't really scale  the lowerLeg directly to yHeight==1, because the SMPL-X lowerLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  # NOTE
  #====================================================================================================================
  #   In code, "T-Pose" translates to      ("` theta==np.zeros( 127*3 )`")
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 

  # Scale up again:
  leftLowerLegVertsCenteredOnOrigin[:,X] *= customerEstimatedMaxLowerLegWidthInches_X
  leftLowerLegVertsCenteredOnOrigin[:,Y] *= customerEstimatedLowerLegLenInches
  leftLowerLegVertsCenteredOnOrigin[:,Z] *= customerEstimatedMaxLowerLegDepthInches_Z
  #=======================================================================================================================================================
  # Here the lowerLeg is normally proportioned again because we're using the customer's **__ACTUAL__**   Depth, Width, and Height.     
  #   -nxb, August 17, 2020
  #=======================================================================================================================================================
  #leftLowerLegVertsCenteredOnOriginScaledToRealLowerLegLenInches = leftLowerLegVertsCenteredOnOriginNormalizedTo1 * customerEstimatedLowerLegLenInches
  #leftLowerLegVertsCenteredOnOrigin *= customerEstimatedLowerLegLenInches
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftLowerLegVertsTranslatedBack = leftLowerLegVertsCenteredOnOrigin + origLowerLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftLowerLegVertsTranslatedBack[:,Y] -=  finalResizedLeftLowerLegVertsTranslatedBack[:,Y].min()

  return finalResizedLeftLowerLegVertsTranslatedBack, leftLowerLegIdxes, {} # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "makeLeftLeg(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):    # we don't have this customerEstimatedLowerLegLenInches, ==================================================





#==================================================
def main(model_folder, model_type='smplx', ext='npz',
         gender='neutral', plot_joints=False,
         plotting_module='pyrender',
         use_face_contour=False):

    model = smplx.create(model_folder, model_type=model_type,
                         gender=gender, use_face_contour=use_face_contour,
                         ext=ext)
    # nxb added the following lines (Aug 18, 2020)
    X,Y,Z=0,1,2

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
    #TIM_ESTIMATED_LOWER_LEG_LENGTH_INCHES = ...  # TODO: automate estimating customer's lowerLeg length from video(s) and OpenPose.  -nxb, August 14, 2020
    # NOTE: 
    '''       -nxb, August 14, 2020
      For both:
        1.    TIM_PIXEL_HEIGHT_INCHES  and
          (and)
        2.    TIM_LEFT_LOWER_LEG_PIXEL_LEN_INCHES
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
        b) for TIM_LEFT_LOWER_LEG_PIXEL_LEN_INCHES  
          I measured between 
            1. the "inside" of Tim's knee on the screen and the    
            2. the  inside of Tim's left ankle on the screen
    # end comment:  }   (})

       -nxb, August 14, 2020
    '''
    # end NOTE:
    TIM_PIXEL_HEIGHT_INCHES = 5.6875
    TIM_LEFT_LOWER_LEG_PIXEL_LEN_INCHES = 1.375
    TIM_SELF_REPORTED_HEIGHT_INCHES = 74     #   Tim's probably exaggerating how tall he is.
    # "Tim's probably shorter than he says he is" comment continued:    "but I guess I'll cut him some slack for a fucking sec.  Of course, when it comes to literally getting him ideal jeans, we should use camera parameters to estimate his body measurements better."   -nxb, August 14, 2020   
    TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN = \
      TIM_LEFT_LOWER_LEG_PIXEL_LEN_INCHES *\
      (TIM_SELF_REPORTED_HEIGHT_INCHES / TIM_PIXEL_HEIGHT_INCHES) # how many "real" inches are in 1 pixel inch   
      #(on my laptop in `feh`, when I hit "down" 3 times, with Tim's Photo
    # The CALF and
    #   lowerLeg"height"  are more important than the rest of the lowerLeg.       -nxb, August 17, 2020

      # FIXME NOTE TODO:               nxb got these measurements "TIM_LOWER_LEG_WIDTH_AKA_X_INCHES  and TIM_LOWER_LEG_DEPTH_AKA_Z_INCHES"  just by measuring ('eyeballing," technically) his own leg (lowerLeg, shin, etc.)    -nxb, August 17, 2020





    #================================================================================
    #=============================== Make these Tim's ===============================
    #================================================================================
    #=========================== Right now they're NXB's ============================
    #================================================================================
    # FIXME NOTE TODO:  These lowerLeg measurements are Nathan's, not Tim's.  I've got to put Tim's measurements in.  -nxb, August 17, 2020
    NXB_LOWER_LEG_WIDTH_AKA_X_INCHES  = 4  #  This is the widest  LowerLegWidth.   Obviously a lowerLeg and a calf is a complicated thing.  The maxWidth ends up being of the calf.      (x is AKA    "fingertip-to-fingertip in T-pose" )
    NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES  = 5  #  This is the deepest LowerLegDepth.   Obviously the lower leg's skin has a complicated mesh that can't be captured with 2 or 3 lengths.  The maxDepth ends up being near the shin.      (z is AKA    "bellyButton-To-Spine," AKA "Dorsal-to-ventral")
    #================================================================================
    #================================================================================
    #================================================================================

    TIM_ANKLE_WIDTH_AKA_X_INCHES  = 3.25 
    TIM_ANKLE_DEPTH_AKA_Z_INCHES  = 3.75

    # """
    # NXB's lowerLeg (measured with a real measuring tape) is roughly 
    #   18 inches, 
    #     and my calculation says 
    #   17.89 inches for Tim Schrader's lowerLeg.  
    # So my calculation is is probably MOSTLY correct.    
    # """
    #    -nxb;   on August 14, 2020      (more technically, 8:19 P.M. EDT    on August 14, 2020)

    #================================================================================
    #================================================================================
    #================================================================================
    #  Major Line:                                                                 
    #                  (" ` resizeLeftSMPLX_LowerLeg(...) ` "  contains a LOT of code)
    #================================================================================
    #================================================================================
    #================================================================================
    resizedLeftLowerLegVerts, leftLowerLegIdxes, leftLowerLegParams = getResizedLeftSMPLX_LowerLeg(vertices, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, TIM_ANKLE_WIDTH_AKA_X_INCHES, TIM_ANKLE_DEPTH_AKA_Z_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)
                                             #getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches,                                customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, TIM_LOWER_LEG_WIDTH_AKA_X_INCHES, TIM_LOWER_LEG_DEPTH_AKA_Z_INCHES):    # we don't have this customerEstimatedLowerLegLenInches, 
    vertsWithResizedLeftLowerLeg = deepcopy(vertices)
    vertsWithResizedLeftLowerLeg[leftLowerLegIdxes] = resizedLeftLowerLegVerts
    #================================================================================

    # TODO:     leftUpperLegParams  for merging UpperLegs with lowerLegs        (in "`getResizedLeftSMPLX_UpperLeg(... , ... , ... )`")
    resizedLeftUpperLegVerts, leftUpperLegIdxes, leftUpperLegParams = getResizedLeftSMPLX_UpperLeg(vertices, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, TIM_ANKLE_WIDTH_AKA_X_INCHES, TIM_ANKLE_DEPTH_AKA_Z_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)
    #getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches,                                customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, TIM_UpperLeg_WIDTH_AKA_X_INCHES, TIM_UpperLeg_DEPTH_AKA_Z_INCHES):    # we don't have this customerEstimatedUpperLegLenInches, 
    vertsWithResizedLeftUpperLeg = deepcopy(vertices)
    vertsWithResizedLeftUpperLeg[leftUpperLegIdxes] = resizedLeftUpperLegVerts
 


    #====================================================================
    # TODO:  put this code into func "makeLeftLeg(... , ... , ... , ...)"
    #====================================================================
    #                            start
    #====================================================================

    #=========================================================
    #   def makeLeftLeg(... , ... ,    ... (moreParams)   ):
    #=========================================================


    #====================================================
    # Move the    lowerLeg back and forth and     
    #                      left and right until it's directly 
    #   under the upperLeg
    #
    #   -nxb, August 18, 2020
    #====================================================
    # (I begun a more technical way of saying it, 
    #   but I figure the code is the technically arcane, hard-to-understand version anyway.  
    # In case you want to see my "failures," here's the more "arcane" diction-style comment:    
    #   "Calculate the "lateral" shift to align the vertices:"      -nxb, August 18, 2020
    #====================================================


    lowerLegEndsY = resizedLeftLowerLegVerts[:,Y].max()    # I fixed this bug at 3:00 P.M. EDT on Aug 18, 2020      -nxb    ( "`min()`" ==>  "`max()`"  )         
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)


    lowerLegHeightMagnitude = resizedLeftLowerLegVerts[:,Y].max() - resizedLeftLowerLegVerts[:,Y].min()
    upperLegHeightMagnitude = resizedLeftUpperLegVerts[:,Y].max() - resizedLeftUpperLegVerts[:,Y].min()    # TODO:  remove the "min()" call (min() should always be 0)        -nxb;   August, 18, 2020
    LOWER_LEG_____BOUNDARY_SKIN_END_CONST = lowerLegHeightMagnitude / 10  # TODO: fiddle with this LOWER_...CONST.
    UPPER_LEG_____BOUNDARY_SKIN_END_CONST = upperLegHeightMagnitude / 10  # TODO: fiddle with this UPPER_...CONST.
    lowersTopBoundarySkinIdxs = np.where(
      np.greater(
        resizedLeftLowerLegVerts[:,Y],
        lowerLegEndsY - LOWER_LEG_____BOUNDARY_SKIN_END_CONST #     (I have to do math in this line    because this is pre-translation-up-and-down)      -nxb, August 18, 2020
      ))[0]    # TODO:    rename this awkwardly named "LOWER_LEG_____BOUNDARY_SKIN_END_CONST"        -nxb; August 18, 2020
    pn(2)
    print('='*99) # comment written     August 18, 2020
    print("lowersTopBoundarySkinIdxs: ") # comment written     August 18, 2020
    print(lowersTopBoundarySkinIdxs) # comment written     August 18, 2020
    print('='*99) # comment written     August 18, 2020
    pn(2)
    uppersBottomBoundarySkinIdxs = np.where(
      np.less(
        resizedLeftUpperLegVerts[:,Y],
        UPPER_LEG_____BOUNDARY_SKIN_END_CONST))[0]    # TODO:    rename this awkwardly named "UPPER_LEG_____BOUNDARY_SKIN_END_CONST"        -nxb; August 18, 2020
    pn(2)
    print('='*99) # comment written     August 18, 2020
    print("uppersBottomBoundarySkinIdxs: ")# comment written     August 18, 2020
    print(uppersBottomBoundarySkinIdxs)# comment written     August 18, 2020
    print('='*99)# comment written     August 18, 2020
    pn(2)

    pe(77)
    print("resizedLeftLowerLegVerts.shape :")# comment written     August 18, 2020
    print(resizedLeftLowerLegVerts.shape)# comment written     August 18, 2020
    print("resizedLeftUpperLegVerts.shape :")# comment written     August 18, 2020
    print(resizedLeftUpperLegVerts.shape)# comment written     August 18, 2020
    pe(77)
    lowersTopBoundarySkin     = resizedLeftLowerLegVerts[lowersTopBoundarySkinIdxs    ]     
    uppersBottomBoundarySkin  = resizedLeftUpperLegVerts[uppersBottomBoundarySkinIdxs ]   
    # OR,  more technically, resizedLeftUpperLegVerts[uppersBottomBoundarySkinIdxs, : ]     -August 18, 2020
    pn(2)
    pe(77)
    print(lowersTopBoundarySkin.shape)# comment written     August 18, 2020
    print(uppersBottomBoundarySkin.shape)# comment written     August 18, 2020
    pe(77)
    pn(2)
    lowersCentroid = lowersTopBoundarySkin.mean(axis=0)
    uppersCentroid = uppersBottomBoundarySkin.mean(axis=0)
    desiredX_Translation  = uppersCentroid
    desiredZ_Translation  = uppersCentroid
    pn(2)
    pe(77)
    print(lowersCentroid)         # NOTE NOTE     are these centroids FINE?       -Aug 18, 2020 at 8:05 P.M.
    print(uppersCentroid)         # NOTE NOTE     are these centroids FINE?       -Aug 18, 2020 at 8:05 P.M.
    print(lowersCentroid.shape)# comment written     August 18, 2020
    print(uppersCentroid.shape)# comment written     August 18, 2020
    pe(77)
    pn(2)

    # "Move the thigh above the calves"  :
    #   Using more math jargon,   "Translate the upperLeg s.t. the 'leftLeg is whole'  "  
    translationUpperToLowerX  = lowersCentroid[X] - uppersCentroid[X]
    translationUpperToLowerY  = lowerLegEndsY
    translationUpperToLowerZ  = lowersCentroid[Z] - uppersCentroid[Z]

    resizedLeftUpperLegVerts[:,X] += translationUpperToLowerX
    resizedLeftUpperLegVerts[:,Y] += translationUpperToLowerY
    resizedLeftUpperLegVerts[:,Z] += translationUpperToLowerZ

    vertsWithResizedLeftUpperLeg[leftUpperLegIdxes] = resizedLeftUpperLegVerts
    vertsWithResizedLeftLeg = deepcopy(vertsWithResizedLeftUpperLeg)
    vertsWithResizedLeftLeg[leftLowerLegIdxes] = resizedLeftLowerLegVerts
    vertsWithResizedLeftLeg[leftUpperLegIdxes] = resizedLeftUpperLegVerts
    #====================================================================
    #                                End
    #====================================================================
    # TODO:  put this code into func "makeLeftLeg(... , ... , ... , ...)"
    #====================================================================

    TODO_TODO_TODO_params={}
    makeLeftLeg(TODO_TODO_TODO_params)


    # This stub/function header was written on August 17, 2020:       -nxb
    """
    leftLegVerts = makeLeftLeg(  
      resizedLeftUpperLegVerts, 
      resizedLeftLowerLegVerts,  
      mergingParams={"leftUpperLegParams":leftUpperLegParams, "leftLowerLegParams":leftLowerLegParams}
    )
    vs  = ...
    """



    """         DON'T DELETE!             this information is always always always pretty useful.
                DON'T DELETE!             this information is always always always pretty useful.
                DON'T DELETE!             this information is always always always pretty useful.
                DON'T DELETE!             this information is always always always pretty useful.
                DON'T DELETE!             this information is always always always pretty useful.
      maxesAndMins:           NOTE: was this from "`verts`" or from "`joints`" ?   -nxb, August 14, 2020
        {'xMax': 0.8656285,
         'xMin': -0.8656085,
         'yMax': 0.43483356,
         'yMin': -1.3589503,
         'zMax': 0.15359592,
         'zMin': -0.1527159}
    """
    joints = output.joints.detach().cpu().numpy().squeeze()

    #print('betas =', betas)              # betas = tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    #print('betas.shape =', betas.shape)  # torch.Size([1,10])
    print('Vertices shape =', vertices.shape) # (10475,3)
    #print('Vertices type =', type(vertices)  ) # "numpy.ndarray" ;   I'm like 90% sure)    
    timestamp= datetime.datetime.now().strftime('%Y_%m_%d____%H:%M_%p__')

    #===================================================================================================
    # Saves:
    #===================================================================================================
    #   Save done properly,  with timestamps:  
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
        # Lower:
        """
        resizedTrimesh =  trimesh.Trimesh(vertsWithResizedLeftLowerLeg, model.faces,
                                   vertex_colors=vertex_colors) # nxb, Aug 13, 2020
        """
        # Upper:
        """
        resizedTrimesh =  trimesh.Trimesh(vertsWithResizedLeftUpperLeg, model.faces,
                                   vertex_colors=vertex_colors) # nxb, Aug 13, 2020
        """
        resizedTrimesh =  trimesh.Trimesh(vertsWithResizedLeftLeg, model.faces,
                                   vertex_colors=vertex_colors) # nxb, Aug 13, 2020
        mesh = pyrender.Mesh.from_trimesh(resizedTrimesh)

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
        pn(3)
        print("="*99)
        print("about to write mesh as .obj file")
        pe(99)
        pn(3)

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



































































































#============================================ BLANK LINES =============================================
