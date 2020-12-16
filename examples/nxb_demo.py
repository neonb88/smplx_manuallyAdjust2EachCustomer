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
import sys

debug=False
show=True

# pe and pn:
#from utils import pe, pn # Aug 18, 2020
def pn(n=0):  print('\n'*n) # Aug 18, 2020
def pe(n=89): print('='*n) # Aug 18, 2020

from smplx.utils import filterVertsBtwn, pPrintVarNXB
#==============================================


#==================================================
# generalized version:      
#     def resizedLeftSMPLX_KneeToButtBottom(
#         vertices,
#         customerEstimatedUpperLegLenInches,
#         customerEstimatedHeightInches, 
#         prevBodyPartsXStretchingSlashScaling,  
#         prevBodyPartsZStretchingSlashScaling,  
#         currBodyPartsXStretchingSlashScaling,  
#         currBodyPartsZStretchingSlashScaling): 
#       # we don't have this variable "`customerEstimatedUpperLegLenInches`"  , 
#==================================================
def resizedLeftSMPLX_KneeToButtBottom(vertices, joints, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):
  #========================================================================
  # TODO:  write in calf and thigh indices and real measurements in inches
  #     -nxb, August 31, 2020
  #========================================================================

  # NOTE:   even with "`pyrender.show()`" ,   this code is fairly performant.   (about 5 secs.   O(5 seconds)   )       At least while I'm only scaling the UpperLeg, most of the time is spent on file-IO rather than in this method.
  # TODO: update the docstring.
  '''

    @param vertices
    @param joints
    TODO: docstring
  '''

  #===================================================================================================
  #   As of August 31, 2020   the function header was entitled:
  #===================================================================================================
  # def resizedLeftSMPLX_KneeToButtBottom(vertices, joints, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):
  #===================================================================================================
  X,Y,Z=0,1,2

  leftUpperLegIdxes = leftUpperLegIndices(vertices)
  leftUpperLegVerts = deepcopy(vertices[leftUpperLegIdxes, : ] )      # TODO:   do translation and scaling on this shit.   -nxb, August 14, 2020
  yHeightButtBottom =  leftUpperLegVerts[:,Y].max()

  #====================================================================================
  # Center:
  #   (Center on the origin)
  #     (newUpperLegCentroid = (0,0,0)  )
  #====================================================================================
  origUpperLegCentroid = leftUpperLegVerts.mean(axis=0)  # DOWN=0
  # TODO: rename all these hellishly-long-variable names to simply "leftUpperLegVerts"  
  leftUpperLegVertsCenteredOnOrigin = leftUpperLegVerts - origUpperLegCentroid
  yHeightValueAtThighBeforeSMPLX_BodyIsNormalizedTo1 =  leftUpperLegVerts.max()
  jointsCenteredOnOrigin = joints - origUpperLegCentroid

  # Thigh height
  if   len(origUpperLegCentroid.shape)  == 2:
    centroidY = origUpperLegCentroid[:,Y]
  elif len(origUpperLegCentroid.shape)  == 1:
    centroidY = origUpperLegCentroid[Y]
  yHeightButtBottomCenteredOnOrigin = yHeightButtBottom - centroidY

  #====================================================================================
  # Scale down:
  #   Normalize UpperLegLen to 1:
  #     NOTE:  (UpperLegLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of UpperLeg;   **doesn't lose information**    -nxb; August 14, 2020
  #====================================================================================
  xWidthBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,X].max() - leftUpperLegVertsCenteredOnOrigin[:,X].min()
  yHeightBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,Y].max() - leftUpperLegVertsCenteredOnOrigin[:,Y].min()
  zDepthBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,Z].max() - leftUpperLegVertsCenteredOnOrigin[:,Z].min()
  leftUpperLegVertsCenteredOnOrigin[:,X] /= xWidthBeforeAnyScaling_atTheBeginningOfThisFunction
  leftUpperLegVertsCenteredOnOrigin[:,Y] /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  leftUpperLegVertsCenteredOnOrigin[:,Z] /= zDepthBeforeAnyScaling_atTheBeginningOfThisFunction

  # Just to derive ThighY:   -nxb, August 31, 2020
  yHeightButtBottomCenteredOnOrigin /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction

  jointsCenteredOnOrigin[:,X] /= xWidthBeforeAnyScaling_atTheBeginningOfThisFunction
  jointsCenteredOnOrigin[:,Y] /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  jointsCenteredOnOrigin[:,Z] /= zDepthBeforeAnyScaling_atTheBeginningOfThisFunction
  # Here the upperLeg is weird-and-FAT-looking b/c its width is 1 while its height is also 1.     (sanity check)
  #                         -nxb, August 17, 2020

  #====================================================================================================================
  # NOTE
  # NOTE:  slight assumption that causes a problem:  I can't really scale  the upperLeg directly to yHeight==1, because the SMPL-X upperLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  # NOTE
  #====================================================================================================================
  #   In code, "T-Pose" translates to      ("` theta==np.zeros( 127*3 )`")
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the upperLeg correctly 

  #====================================================================================
  # Scale up again:
  #====================================================================================
  #leftUpperLegVertsCenteredOnOrigin[:,X] *= customerEstimatedMaxUpperLegWidthInches_X    # old code as of 5 P.M. on August 24, 2020
  leftUpperLegVertsCenteredOnOrigin[:,Y] *= customerEstimatedUpperLegLenInches
  #leftUpperLegVertsCenteredOnOrigin[:,Z] *= customerEstimatedMaxUpperLegDepthInches_Z    # old code as of 5 P.M. on August 24, 2020
  # NOTE:   Both x and z are encapsulated (abstracted) away in the following function "scaleLegLinearlyWithYHeight" :
  #     THAT'S why I commented the "old code" out
  yHeightButtBottomCenteredOnOrigin *= customerEstimatedUpperLegLenInches

  # Also scale up 'joints' :
  jointsCenteredOnOrigin[:,X] *= customerEstimatedMaxUpperLegWidthInches_X
  jointsCenteredOnOrigin[:,Y] *= customerEstimatedUpperLegLenInches
  jointsCenteredOnOrigin[:,Z] *= customerEstimatedMaxUpperLegDepthInches_Z


  # FIXME:   these measurements are actually Nathan's; (I didn't measure Tim's yet)        -nxb; August 28, 2020
  NXBsRealThighXWidthInches = TimsRealThighXWidthInches = customersThighXWidthInches(customerImgFname="timsSideView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )
  NXBsRealThighZDepthInches = TimsRealThighZDepthInches = customersThighZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )
  NXBsRealKneeXWidthInches = TimsRealKneeXWidthInches = customersKneeXWidthInches(customerImgFname="timsSideView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )
  NXBsRealKneeZDepthInches = TimsRealKneeZDepthInches = customersKneeZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )

  LEFT_KNEE   = 4 # TODO: double-check this indexing?  (1-based vs. 0-based)
  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1   = jointsCenteredOnOrigin[LEFT_KNEE  , Y]    #  8.715
  yHeightValueAtButtBottomWithSMPLX_BodyNormalizedTo1  = yHeightButtBottomCenteredOnOrigin

  #===========================================================
  # Get indices of vertices between left Ankle and left Knee:
  #===========================================================
  idxsButtBottomToKnee, vertsButtBottomToKnee = filterVertsBtwn(
    leftUpperLegVertsCenteredOnOrigin,
    yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1,
    yHeightValueAtButtBottomWithSMPLX_BodyNormalizedTo1,
    axis='y')

  if debug:
    print('\n' +   '='*99+'\nwithin func {}'.format(sys._getframe().f_code.co_name) + '\n'+'='*99)
    pPrintVarNXB('TimsRealThighZDepthInches', TimsRealThighZDepthInches, nNewlines=1)

  # Scale vertices between ButtBottom and Knee :
  leftUpperLegVertsCenteredOnOrigin[idxsButtBottomToKnee]  = scaleLegLinearlyWithYHeight(
    vertsButtBottomToKnee, 
    yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1, 
    yHeightValueAtButtBottomWithSMPLX_BodyNormalizedTo1, 
    #4.125,     # KneeX
    TimsRealKneeXWidthInches,   # TODO:  write in calf and thigh indices and real measurements in inches
    TimsRealThighXWidthInches, 
    #4.75,      # KneeZ
    TimsRealKneeZDepthInches,   # TODO:  write in calf and thigh indices and real measurements in inches
    TimsRealThighZDepthInches)   # FIXME:     there's a lot of crap in here that should be changed.     -nxb on August 28, 2020      at 1:15 P.M. EDT

  #=========================================================================
  # TODO:  write in calf and thigh indices and real measurements in inches |
  #     -nxb, August 31, 2020                                              |
  #=========================================================================

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftUpperLegVertsTranslatedBack = leftUpperLegVertsCenteredOnOrigin + origUpperLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftUpperLegVertsTranslatedBack[:,Y] -=  finalResizedLeftUpperLegVertsTranslatedBack[:,Y].min()

  leftUpperLegXYZScaleParams = {  # TODO:  copy all this for UpperLeg.   (-nxb; August 19, 2020)
    'X' : customerEstimatedMaxUpperLegWidthInches_X / xWidthBeforeAnyScaling_atTheBeginningOfThisFunction,
    'Y' : customerEstimatedUpperLegLenInches        / yHeightBeforeAnyScaling_atTheBeginningOfThisFunction,
    'Z' : customerEstimatedMaxUpperLegDepthInches_Z / zDepthBeforeAnyScaling_atTheBeginningOfThisFunction,
  }

  #======================================================================================================
  #======================================================================================================
  #======================================================================================================
  #======================================================================================================


  return finalResizedLeftUpperLegVertsTranslatedBack, leftUpperLegIdxes, leftUpperLegXYZScaleParams # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "resizedLeftSMPLX_AnkleToKnee(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "resizedLeftSMPLX_AnkleToKnee(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):    # we don't have this customerEstimatedUpperLegLenInches, ==================================================


#==================================================
def getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxLowerLegWidthInches_X, customerEstimatedMaxLowerLegDepthInches_Z, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):
  '''
    This UpperLeg function SHOULD do the following:                  (August 18, 2020)
      (This docstring was written on August 18, 2020)

      """
        Expected, desired, non-buggy behavior:
          1.  Returns vertices **__MOSTLY__** centered on (0,0,0),   except the yMin is now 0.   

          2.  The truth is a little more detailed:
            a.  Basically, the SMPL-X base model I'm using has the center of the chest at (0,0,0).  
              (ie. The sternum is at the right xy position.  The anatomical location of z==0 is about as "deep" in the human body as the armpit(s))
            b.  Therefore, the output mesh should have the "bottom of the UpperLeg" at y==0 for easier matching

          This is only the way it should be for bodyParts like the UpperLeg-lowerLeg boundary where the translation-before-smoothing is all along the **__Y__** axis.  For instance, for the foreArm-upperArm boundary in T-pose, the boundary should be along the **__X__** axis **__INSTEAD__**
      """
  '''


  #===================================================================================================
  # TODO:  find the EXACT RIGHT VERTICES  in SMPL-X that will let us scale the UpperLeg correctly
  #===================================================================================================
  # NOTE: NOTE: NOTE: NOTE: NOTE:  This code isn't perfect.  Ideally, every damn vertex in SMPL-X would be exactly where the customers' vertices are at that time.       
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  # NOTE NOTE NOTE NOTE NOTE
  #===================================================================================================

  X,Y,Z=0,1,2

  leftUpperLegIdxes = leftUpperLegIndices(vertices)
  leftUpperLegVerts = deepcopy(vertices[leftUpperLegIdxes, : ] )      # TODO:   do translation and scaling on this shit.   -nxb, August 14, 2020

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
  xWidthBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,X].max() - leftUpperLegVertsCenteredOnOrigin[:,X].min()
  yHeightBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,Y].max() - leftUpperLegVertsCenteredOnOrigin[:,Y].min()
  zDepthBeforeAnyScaling_atTheBeginningOfThisFunction = leftUpperLegVertsCenteredOnOrigin[:,Z].max() - leftUpperLegVertsCenteredOnOrigin[:,Z].min()
  leftUpperLegVertsCenteredOnOrigin[:,X] /= xWidthBeforeAnyScaling_atTheBeginningOfThisFunction
  leftUpperLegVertsCenteredOnOrigin[:,Y] /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  leftUpperLegVertsCenteredOnOrigin[:,Z] /= zDepthBeforeAnyScaling_atTheBeginningOfThisFunction
  #========================================================================================
  # Here the UpperLeg (AKA thigh) is weird-and-FAT-looking b/c its width is 1 while its height is also 1.
  #                         -nxb, August 17, 2020
  #========================================================================================

  #   In code, "T-Pose" translates to      ("` theta==np.zeros( 127*3 )`")
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the upperLeg correctly 

  # Scale up again:
  leftUpperLegVertsCenteredOnOrigin[:,X] *=customerEstimatedMaxUpperLegWidthInches_X
  leftUpperLegVertsCenteredOnOrigin[:,Y] *=customerEstimatedUpperLegLenInches
  leftUpperLegVertsCenteredOnOrigin[:,Z] *=customerEstimatedMaxUpperLegDepthInches_Z
  #=======================================================================================================================================================
  # Here the upperLeg is normally proportioned again because we're using the customer's **__ACTUAL__**   Depth, Width, and Height.     
  #   -nxb, August 17, 2020
  #=======================================================================================================================================================
  #leftUpperLegVertsCenteredOnOriginScaledToRealUpperLegLenInches = leftUpperLegVertsCenteredOnOriginNormalizedTo1 * customerEstimatedUpperLegLenInches
  #leftUpperLegVertsCenteredOnOrigin *= customerEstimatedUpperLegLenInches
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the upperLeg correctly 

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftUpperLegVertsTranslatedBack = leftUpperLegVertsCenteredOnOrigin + origUpperLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftUpperLegVertsTranslatedBack[:,Y] -= finalResizedLeftUpperLegVertsTranslatedBack[:,Y].min()

  return finalResizedLeftUpperLegVertsTranslatedBack, leftUpperLegIdxes, {} # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "resizedLeftSMPLX_AnkleToKnee(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):     ==================================================

#==================================================









#==================================================
def scaleLegLinearlyWithYHeight(verts, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches):
  '''
    @Explanation:

    This function assumes a body part like the lower leg
      scales (roughly) in both the width (x) and depth (z) directions   LINEARLY with height
      (as of August 24, 2020)

    A simple example should illustrate better than my long, overly academic, awkward words:
      1.  Say we resize Nathan's human thigh to fit precisely in a cube of 10, 10, 10 units.
        Nathan's thigh is "verts"
      2.  Say Nathan's thigh's real "width" is 15 inches right near the bottom of the butt.  and
      2a.   His thigh is 18 inches "deep."
        (I've made Nathan quite thicc in this example.  Approaching the size of "The Hulk")
      3.  Say Nathan's leg's real "width" is only 4 inches at the "height" of his knees, in this example      (xWidthAtBotYHeight_RealCustomerInches and yBot)
      3a.   and his leg's real "depth" is 5 inches at the "height" of his knees.                              (zDepthAtBotYHeight_RealCustomerInches and yBot)

      4.  The **__OUTPUT__** return value halfway between the top of the thigh and the "bottom of the thigh" (beginning of the knee)     should be 
        a.   9.5 inches wide    (15+4)/2
        b.  11.5 inches deep    (18+5)/2
        c.  In other words, a point (circumference) HALFway between knee and bottom-of-butt HEIGHT-wise    should have HALF the WIDTH and HALF the DEPTH.
    Let me repeat that last point again so you actually think about it.  Please go back and reread so you understand.
    "In summation, a point (circumference) HALFway between knee and bottom-of-butt HEIGHT-wise    should have HALF the WIDTH and HALF the DEPTH."

      (as of August 24, 2020)

    @param verts  np.ndarray of shape (N, 3)
    @param yTop   value using CURRENT SCALE'S max and min of the variable 'verts'       (`verts_[:,Y].max()`)
    @param yBot   value using CURRENT SCALE'S min and min of the variable 'verts'       (`verts_[:,Y].min()`)
    @param xWidthAtTopYHeight_RealCustomerInches    real customers' measurements in inches
    @param xWidthAtBotYHeight_RealCustomerInches    real customers' measurements in inches
    @param zDepthAtTopYHeight_RealCustomerInches    real customers' measurements in inches
    @param zDepthAtBotYHeight_RealCustomerInches    real customers' measurements in inches

    @author: Nathan X Bendich (nxb)
    @precondition:     verts y ranges between yTop and yBot.
    @precondition:     the leg parts are already y-scaled to the correct height.  
      I think the y-scaling is easier than the x and z scaling for legs?      -nxb at     4:32 P.M. on    August 24, 2020

    Error-checking:   (assert verts[:,Y].max() == yTop       and    verts[:,Y].min() == yBot)
  '''


# August 31, 2020:   header for this function is
#   "def of func scaleLegLinearlyWithYHeight(verts, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches): "
  X,Y,Z=0,1,2
  verts_ = deepcopy(verts) 
  """ In other words, side effects and state are BAD;
    Using "deepcopy" is more "functional" than mutating the original numpy.ndarray, which is    GOOD.
    -nxb, August 24, 2020  """

  # Iterate up the height of the leg:
  #=======================================
  for i,yVal in enumerate(verts_[:,Y]):
  #=======================================
    # NOTE:
    """   It's kind of hard to understand this "x (width) scaling" and "z (depth) scaling" code.  
         See reasons in extended documentation below   
         (search for "DOCUMENTATION for this code" as of August 28, 2020) """
    #========================
    #   x (width) scaling:   
    #========================
    m = slope = (xWidthAtTopYHeight_RealCustomerInches - xWidthAtBotYHeight_RealCustomerInches) / (yTop - yBot)
    b = yInterceptOnTheGraph = xWidthAtTopYHeight_RealCustomerInches - (m*yTop)
    xScaling = m*yVal + b
    verts_[i,X] *= xScaling

    #========================
    #   z (depth) scaling:   
    #========================
    m = slope = (zDepthAtTopYHeight_RealCustomerInches - zDepthAtBotYHeight_RealCustomerInches) / (yTop - yBot)  # it's kind of hard to understand this code.  See reasons in extended documentation below
    b = yInterceptOnTheGraph = zDepthAtTopYHeight_RealCustomerInches - (m*yTop)
    zScaling = m*yVal + b # again, not quite y = m*x+b.  See thorougher documentation after the function for reasoning -August 24, 2020. 
    verts_[i,Z] *= zScaling
    # why are both xScaling and zScaling== 5.0?     -nxb, August 28, at 1:53 P.M.
  #============================================
  #end "for i, yVal in enumerate(verts_[:,Y]):"
  #============================================

  # NOTE: For now, I'm assuming that this function "scaleLegLinearlyWithYHeight" isn't the problem.  I think the problem is, instead, in some of the intermediate variables that are used to scale the leg.  If this assumption turns out to be wrong later, welp, GoodGameWellPlayed     -nxb, 8:43 P.M. on Dec. 15, 2020
  return verts_

    #==========================================================================================
    #==========================================================================================
    #==========================================================================================
    #==========================================================================================
    #==========================================================================================

    #==============================
    # DOCUMENTATION for this code:
    #==============================

    #========================
    #   x (width) scaling:   
    #========================
    # I drew out the "y = m*x + b"     that we learned in   algebra in   middle / high school and got the following:
    #   -nxb, August 24, 2020

    # "It's kind of hard to understand this code because when I drew it on paper, I put "y" from the human body on the "x" axis on the page and "x" from the human body on the "y" axis on the page.  There's probably a simpler formulation of the problem that's easier to read and understand for the particular leg(s) scaling we're doing at 2:29 P.M. on August 24, 2020.  But as long as the code works, maybe it's just better to not edit (and subsequently break) anything.   -nxb, August 24, 2020
  """ it's kind of hard to understand this code because when I drew it on paper, I put "y" from the human body on the "x" axis on the page and "x" from the human body on the "y" axis on the page.  There's probably a simpler formulation of the problem that's easier to read and understand for the particular leg(s) scaling we're doing at 2:29 P.M. on August 24, 2020.  But as long as the code works, maybe it's just better to not edit (and subsequently break) anything.   -nxb, August 24, 2020"""

    #========================
    #   z (depth) scaling:   
    #========================
    # I drew out the "y = m*x + b"     that we learned in   algebra in   middle / high school and got the following:
    #   -nxb, August 24, 2020

    #  It's kind of hard to understand this code because when I drew it on paper, I put "y" from the human body on the "x" axis on the page and "z" from the human body on the "y" axis on the page.  There's probably a simpler formulation of the problem that's easier to read and understand for the particular leg(s) scaling we're doing at 2:29 P.M. on August 24, 2020.  But as long as the code works, maybe it's just better to not edit (and subsequently break) anything.   -nxb, August 24, 2020

    #zScaling = m*yVal + b    # the comment after <== this line was/is      '''
    #backwards for the reasons    : " it's kind of hard to understand this code because when I drew it on paper, I put 'y' from the human body on the 'x' axis on the page and 'z' from the human body on the 'y' axis on the page.  There's probably a simpler formulation of the problem that's easier to read and understand for the particular leg(s) scaling we're doing at 2:29 P.M. on August 24, 2020.  But as long as the code works, maybe it's just better to not edit (and subsequently break) anything.   -nxb, August 24, 2020" 
    #  '''
  """ it's kind of hard to understand this code because when I drew it on paper, I put "y" from the human body on the "x" axis on the page and "z" from the human body on the "y" axis on the page.  There's probably a simpler formulation of the problem that's easier to read and understand for the particular leg(s) scaling we're doing at 2:29 P.M. on August 24, 2020.  But as long as the code works, maybe it's just better to not edit (and subsequently break) anything.   -nxb, August 24, 2020"""
#==================================================
























#===================================================================================================
def customersKneeZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # KNEE KNEE KNEE         not Knee right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  NXBs_REAL_KNEE_Z_DEPTH_IN_INCHES  = 4.75
  return NXBs_REAL_KNEE_Z_DEPTH_IN_INCHES
  # KNEE KNEE KNEE         not Knee right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)    Calf => knee
  # FIXME: rename(s)
  # FIXME: rename(s)
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

# FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
#===================================================================================================




#===================================================================================================
def customersAnkleXWidthInches(customerImgFname="timsSideView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  NXBs_REAL_ANKLE_X_WIDTH_IN_INCHES = 2.5 #19.5 #2.5     #NOTE: 2.5 is the real value
  return NXBs_REAL_ANKLE_X_WIDTH_IN_INCHES
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
#===================================================================================================





#======================================================================================================
# FIXME: ======================================================================================= FIXME
#TimsRealAnkleXWidthInches  =  5  # FIXME:     calculate Tim's from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
# FIXME: ======================================================================================= FIXME
#======================================================================================================




#===================================================================================================
def customersKneeXWidthInches(customerImgFname="timsFrontView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  # TODO:  "Calf" ==> "Knee"      -nxb, 2:34 P.M. EDT on August 28, 2020                  

  NXBs_REAL_KNEE_X_WIDTH_IN_INCHES = 4.125 # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # KNEE KNEE KNEE         not CALF right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)    Calf => knee
  # FIXME: rename(s)
  # FIXME: rename(s)
  return NXBs_REAL_KNEE_X_WIDTH_IN_INCHES
  #return CONST
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #TimsRealCalfXWidthInches  =  5  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #===================================================================================================






#===================================================================================================
def customersThighXWidthInches(customerImgFname="timsFrontView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
 
  NXBs_REAL_THIGH_X_WIDTH_IN_INCHES = 6.5   # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: improve the precision of the measurement.  -nxb; August 27, 2020
  # KNEE KNEE KNEE         not CALF right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  return NXBs_REAL_THIGH_X_WIDTH_IN_INCHES
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #TimsRealCalfXWidthInches  =  5  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #===================================================================================================



#===================================================================================================
def customersThighZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  
  # FIXME: rename(s)
  NXBs_REAL_THIGH_Z_DEPTH_IN_INCHES  = 6.875      # TODO:   I'm just making this up; I should measure it.  -Written by NXB on August 31, 2020 at 7:27 P.M.
  return NXBs_REAL_THIGH_Z_DEPTH_IN_INCHES
  # FIXME: rename(s)
  # FIXME: rename(s)
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

#===================================================================================================

# FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
#===================================================================================================










#======================================================================================================
# FIXME: ======================================================================================= FIXME
#TimsRealAnkleZDepthInches  =  5  # FIXME:     calculate Tim's from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
# FIXME: ======================================================================================= FIXME
#======================================================================================================



  # FIXME:   these measurements are actually Nathan's; (I didn't measure Tim's yet)        -nxb; August 28, 2020

#===================================================================================================
def customersCalfZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)
  # KNEE KNEE KNEE         not CALF right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  NXBs_REAL_KNEE_Z_DEPTH_IN_INCHES  = 4.75
  return NXBs_REAL_KNEE_Z_DEPTH_IN_INCHES
  # KNEE KNEE KNEE         not CALF right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)    Calf => knee
  # FIXME: rename(s)
  # FIXME: rename(s)
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

# FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
#===================================================================================================




#===================================================================================================
def customersAnkleZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  NXBs_REAL_ANKLE_Z_DEPTH_IN_INCHES = 3.5
  return NXBs_REAL_ANKLE_Z_DEPTH_IN_INCHES


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
#===================================================================================================

#======================================================================================================
# FIXME: ======================================================================================= FIXME
#TimsRealAnkleXWidthInches  =  5  # FIXME:     calculate Tim's from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
# FIXME: ======================================================================================= FIXME
#======================================================================================================




#===================================================================================================
def customersCalfXWidthInches(customerImgFname="timsFrontView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
  # TODO:  "Calf" ==> "Knee"      -nxb, 2:34 P.M. EDT on August 28, 2020                  

  
  # KNEE KNEE KNEE         not CALF right now.  -nxb; Aug 28 at 2:43 P.M. EDT
  # FIXME: rename(s)
  # FIXME: rename(s)
  # FIXME: rename(s)    Calf => knee
  # FIXME: rename(s)
  # FIXME: rename(s)

  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  NXBs_REAL_KNEE_X_WIDTH_IN_INCHES = 4.125
  return NXBs_REAL_KNEE_X_WIDTH_IN_INCHES


  #return CONST
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
  # TODO: fill in with image-based first-principles-calculations.  -nxb; August 27, 2020
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
#===================================================================================================

  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #TimsRealCalfXWidthInches  =  5  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #===================================================================================================


#==================================================
def leftCalfIdx(modelType='SMPLX', ):
  # TODO TODO TOOD:    finish this function.
  if modelType.upper() == 'SMPLX' or  modelType.upper() == 'SMPL-X' :
    raise Exception ("Please fill in this code, Nathan.  And more cmd line arguments.  \n HINT: use np.where() and np.greater() and np.less().  ")
  return 
  # (dumbshit)
#==================================================


#==================================================
def topOfLeftLowerLegIdx(modelType='SMPLX', ):
  # TODO TODO TOOD:    finish this function.
  if modelType.upper() == 'SMPLX' or  modelType.upper() == 'SMPL-X' :
    raise Exception ("Please fill in this code, Nathan.  And more cmd line arguments.  \n HINT: use np.where() and np.greater() and np.less().  ")
  return 
  # (dumbshit)
#==================================================


#==================================================
def bottomOfLeftLowerLegIdx(modelType='SMPLX', ):
  # TODO TODO TOOD:    finish this function.
  if modelType.upper() == 'SMPLX' or  modelType.upper() == 'SMPL-X' :
    raise Exception ("Please fill in this code, Nathan.  And more cmd line arguments.    \n HINT: use np.where() and np.greater() and np.less().  ")
  return 
  # (dumbshit)
#==================================================















































#====================================================================================================
def resizedLeftSMPLX_foot(vertices, xAnkleScaling, yAnkleScaling, zAnkleScaling):  # TODO: confirm this is correct (test)
  '''
    Resizes (scales) the foot in a simple way

    This method is so short because it uses the ankle scaling factors from "resizedLeftSMPLX_AnkleToKnee"

    @author nxb
    @since Dec. 13, 2020

    @param vertices
    @param joints
  '''
  # Indices:
  leftFootIdxes = leftFootIndices(vertices)
  leftFootVerts = deepcopy(vertices[leftFootIdxes, : ] )
  # Scale:
  X,Y,Z=0,1,2
  leftFootVerts[:,X] *= xAnkleScaling
  leftFootVerts[:,Y] *= yAnkleScaling
  leftFootVerts[:,Z] *= zAnkleScaling
  return leftFootVerts, leftFootIdxes
#========= end function def of   "resizedLeftSMPLX_foot(vertices, joints, xAnkleScaling, zAnkleScaling): ==========
















































#==================================================
# generalized version:      
#     def resizedLeftSMPLX_AnkleToKnee(
#         vertices,
#         customerEstimatedLowerLegLenInches,
#         customerEstimatedHeightInches, 
#         prevBodyPartsXStretchingSlashScaling,  
#         prevBodyPartsZStretchingSlashScaling,  
#         currBodyPartsXStretchingSlashScaling,  
#         currBodyPartsZStretchingSlashScaling): 
#       # we don't have this variable "`customerEstimatedLowerLegLenInches`"  , 
#==================================================
def resizedLeftSMPLX_AnkleToKnee(vertices, joints, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxLowerLegWidthInches_X, customerEstimatedMaxLowerLegDepthInches_Z):
  # NOTE: docstring is a few lines down.    -nxb, Dec. 11, 2020

  #========================================================================
  # TODO:  write in calf and thigh indices and real measurements in inches
  #     -nxb, August 31, 2020
  #========================================================================

  # NOTE:   even with "`pyrender.show()`" ,   this code is fairly performant.   (about 5 secs.   O(5 seconds)   )       At least while I'm only scaling the LowerLeg, most of the time is spent on file-IO rather than in this method.
  # TODO: update the docstring.
  '''
    @author nxb
    @since Dec. 11, 2020

    @param vertices
    @param joints

    The parameters passed into the function (like "customerEstimatedLowerLegLenInches", "customerEstimatedMaxLowerLegWidthInches_X", "customerEstimatedMaxLowerLegDepthInches_Z", and "customerEstimatedHeightInches") are not consistently used throughout this function; there are other parameters from "global function stores" that are used for parts of the function instead.

    As of Dec. 11, 2020, this method ("resizedLeftSMPLX_AnkleToKnee") does NOT stretch according to realCalfX and realCalfZ.
      Doesn't do calves

    Summary of this method:
      (as of Dec. 11, 2020)
      ("this method" was called "resizedLeftSMPLX_AnkleToKnee" as of Dec. 11, 2020)

      1.  Pick the indices of "leftLowerLeg" out of the bigger variable "vertices" which contains the whole SMPL-X body's vertices
        a.  Func is called "leftLowerLegIndices()"
        b.
      2.  Center the lowerLeg's centroid on (0,0,0)
      3.  Scale down all dimensions (x, y, and z) to magnitude 1
      4.  Scale up to customer's real leftLowerLeg dimensions
        a.
      5.  Do everything required to scale the joints and constantly have the joints in the right place, so we can split the leg(s) around
        a.  Center on origin
        b.  Scale down to 1
        c.  Scale up again to "real" positions
        d.
        e.
      6.  Get indices between left ankle and left knee
      7.  "scaleLegLinearlyWithYHeight" for the ankle-to-calf and
      8.  "scaleLegLinearlyWithYHeight" for the calf-to-knee section of the "lowerLeg" AKA tibia
      9.  translate to the ORIGINAL centroid of the leftLowerLeg   (ie. x and z locs too)
      10.   translate to yMin  ==  0
      11.   return how much we stretched the leg in x, y, and z?  Not 100% sure what's going on with the return value; maybe I had some clear idea for what that was supposed to do when I wrote it longer than 1 month ago, but now idk
      12.
      13.
  '''

  #===================================================================================================
  #   As of August 31, 2020   the function header was entitled:
  #===================================================================================================
  #   def resizedLeftSMPLX_AnkleToKnee(vertices, joints, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):
  #===================================================================================================
  X,Y,Z=0,1,2

  leftLowerLegIdxes = leftLowerLegIndices(vertices)
  leftLowerLegVerts = deepcopy(vertices[leftLowerLegIdxes, : ] )      # TODO:   do translation and scaling on this shit.   -nxb, August 14, 2020

  #====================================================================================
  # Center:
  #   (Center on the origin)
  #     (newLowerLegCentroid = (0,0,0)  )
  #====================================================================================
  origLowerLegCentroid = leftLowerLegVerts.mean(axis=0)  # DOWN=0
  # TODO: rename all these hellishly-long-variable names to simply "leftLowerLegVerts"  
  leftLowerLegVertsCenteredOnOrigin = leftLowerLegVerts - origLowerLegCentroid
  jointsCenteredOnOrigin = joints - origLowerLegCentroid

  #====================================================================================
  # Scale down:
  #   Normalize lowerLegLen to 1:
  #     NOTE:  (lowerLegLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of lowerLeg;   **doesn't lose information**    -nxb; August 14, 2020
  #====================================================================================
  xWidthBeforeAnyScaling_atTheBeginningOfThisFunction = leftLowerLegVertsCenteredOnOrigin[:,X].max() - leftLowerLegVertsCenteredOnOrigin[:,X].min()
  yHeightBeforeAnyScaling_atTheBeginningOfThisFunction = leftLowerLegVertsCenteredOnOrigin[:,Y].max() - leftLowerLegVertsCenteredOnOrigin[:,Y].min()
  zDepthBeforeAnyScaling_atTheBeginningOfThisFunction = leftLowerLegVertsCenteredOnOrigin[:,Z].max() - leftLowerLegVertsCenteredOnOrigin[:,Z].min()


  #=============
  #   Ankles:
  #=============
  # Get ankle verts:
  leftAnkleBotY = leftLowerLegVertsCenteredOnOrigin[:,Y].min()
  leftAnkleTopY = leftAnkleBotY + 0.1 * yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  leftAnkleIdxs, leftAnkleVertsCenteredOnOrigin = filterVertsBtwn(leftLowerLegVertsCenteredOnOrigin, leftAnkleBotY, leftAnkleTopY, axis='y')

  # Get xWidth of ankle:
  xWidthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction = leftAnkleVertsCenteredOnOrigin[:,X].max() - leftAnkleVertsCenteredOnOrigin[:,X].min()
  pPrintVarNXB("xWidthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction", xWidthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction, nNewlines=0)

  # Get zDepth of ankle:
  zDepthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction = leftAnkleVertsCenteredOnOrigin[:,Z].max() - leftAnkleVertsCenteredOnOrigin[:,Z].min()
  pPrintVarNXB("zDepthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction", zDepthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction, nNewlines=0)


  #============
  #   Knees: 
  #============
  # Get knee verts:
  kneeTopY = leftLowerLegVertsCenteredOnOrigin[:,Y].max()
  kneeBotY = kneeTopY - 0.1*yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  kneeIdxs, leftKneeVertsCenteredOnOrigin = filterVertsBtwn(leftLowerLegVertsCenteredOnOrigin, kneeBotY, kneeTopY, axis='y') # TODO: rename "idxs"    -nxb, Dec. 13, at 12:52 A.M.

  # Get xWidth of knee:
  xWidthKnee_BeforeAnyScaling_atTheBeginningOfThisFunction = leftKneeVertsCenteredOnOrigin[:,X].max() - leftKneeVertsCenteredOnOrigin[:,X].min()

  # Get zDepth of knee:
  zDepthKnee_BeforeAnyScaling_atTheBeginningOfThisFunction = leftKneeVertsCenteredOnOrigin[:,Z].max() - leftKneeVertsCenteredOnOrigin[:,Z].min()


  # Normalize to 1:
  leftLowerLegVertsCenteredOnOrigin[:,X] /= xWidthBeforeAnyScaling_atTheBeginningOfThisFunction
  leftLowerLegVertsCenteredOnOrigin[:,Y] /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  leftLowerLegVertsCenteredOnOrigin[:,Z] /= zDepthBeforeAnyScaling_atTheBeginningOfThisFunction

  jointsCenteredOnOrigin[:,X] /= xWidthBeforeAnyScaling_atTheBeginningOfThisFunction
  jointsCenteredOnOrigin[:,Y] /= yHeightBeforeAnyScaling_atTheBeginningOfThisFunction
  jointsCenteredOnOrigin[:,Z] /= zDepthBeforeAnyScaling_atTheBeginningOfThisFunction
  # Here the lowerLeg is weird-and-FAT-looking b/c its width is 1 while its height is also 1.     (sanity check)
  #                         -nxb, August 17, 2020

  #====================================================================================================================
  # NOTE
  # NOTE:  slight assumption that causes a problem:  I can't really scale  the lowerLeg directly to yHeight==1, because the SMPL-X lowerLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  # NOTE
  #====================================================================================================================
  #   In code, "T-Pose" translates to      ("` theta==np.zeros( 127*3 )`")
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 

  #====================================================================================
  # Scale up again:
  #====================================================================================
  #leftLowerLegVertsCenteredOnOrigin[:,X] *= customerEstimatedMaxLowerLegWidthInches_X    # old code as of 5 P.M. on August 24, 2020
  leftLowerLegVertsCenteredOnOrigin[:,Y] *= customerEstimatedLowerLegLenInches
  #leftLowerLegVertsCenteredOnOrigin[:,Z] *= customerEstimatedMaxLowerLegDepthInches_Z    # old code as of 5 P.M. on August 24, 2020
  # NOTE:   Both x and z are encapsulated (abstracted) away in the following function "scaleLegLinearlyWithYHeight" :
  #     THAT'S why I commented the "old code" out

  # Also scale up 'joints' :
  #      TODO: this should be updated s.t. wherever the joint is is scaled linearly between yBot and yTop, like in "scaleLegLinearlyWithYHeight"
  #      TODO: this should be updated s.t. wherever the joint is is scaled linearly between yBot and yTop, like in "scaleLegLinearlyWithYHeight"
  jointsCenteredOnOrigin[:,X] *= customerEstimatedMaxLowerLegWidthInches_X
  jointsCenteredOnOrigin[:,Y] *= customerEstimatedLowerLegLenInches
  jointsCenteredOnOrigin[:,Z] *= customerEstimatedMaxLowerLegDepthInches_Z
  #      TODO: this should be updated s.t. wherever the joint is is scaled linearly between yBot and yTop, like in "scaleLegLinearlyWithYHeight"

  # FIXME:   these measurements are actually Nathan's; (I didn't measure Tim's yet)        -nxb; August 28, 2020
  NXBsRealKneeXWidthInches  = TimsRealCalfXWidthInches  = customersCalfXWidthInches()
  NXBsRealKneeZDepthInches  = TimsRealCalfZDepthInches  = customersCalfZDepthInches()
  NXBsRealAnkleXWidthInches = TimsRealAnkleXWidthInches = customersAnkleXWidthInches()
  NXBsRealAnkleZDepthInches = TimsRealAnkleZDepthInches = customersAnkleZDepthInches()

  # TODO: change this from "calf" to "knee" ?   Briefly (ie. today)    requires less work.     -nxb; August 28, 2020
  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1   = -0.25     # where the Knee  is on the SMPL-X model      (y-dimension is foot to scalp)      (these were hard-coded before August 27, 2020 -nxb)
  yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1  = -0.3      # where the Ankle is on the SMPL-X model      (y-dimension is foot to scalp)      (these were hard-coded before August 27, 2020 -nxb)
  LEFT_KNEE   = 4 # TODO: double-check this indexing?  (1-based vs. 0-based)
  LEFT_ANKLE  = 7   # see   "`/home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/smplx_manuallyAdjust2EachCustomer/smplx/joint_names.py`"  for details.
  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1   = jointsCenteredOnOrigin[LEFT_KNEE  , Y]    #  8.715
  yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1  = jointsCenteredOnOrigin[LEFT_ANKLE , Y]    # -9.715

  #===========================================================
  # Get indices of vertices between left Ankle and left Knee:
  #===========================================================
  idxsAnkleToKnee, vertsAnkleToKnee = filterVertsBtwn(
    leftLowerLegVertsCenteredOnOrigin, 
    yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1,
    yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1, 
    axis='y')
  #  TODO Scale vertices between Ankle and Calf :
  # Scale vertices between Ankle and Calf :
  #  TODO Scale vertices between Ankle and Calf :
  # [insert code here]
  # [insert code here]

  # Scale vertices between Knee  and Calf :
  #  TODO Scale vertices between Knee and Calf :
  # [insert code here]
  # [insert code here]

  pPrintVarNXB("TimsRealAnkleXWidthInches", TimsRealAnkleXWidthInches, nNewlines=0)
  # Scale vertices between Ankle and Knee :
  leftLowerLegVertsCenteredOnOrigin[idxsAnkleToKnee]  = scaleLegLinearlyWithYHeight(
    vertsAnkleToKnee, 
    yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1, 
    yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1, 
    #4.125,   # KneeX
    NXBsRealKneeXWidthInches,   # TODO:  write in calf and thigh indices and real measurements in inches
    TimsRealAnkleXWidthInches,  #2.5
    #4.75,    # KneeZ
    NXBsRealKneeZDepthInches,   # TODO:  write in calf and thigh indices and real measurements in inches
    TimsRealAnkleZDepthInches)  #3.5 # FIXME:     there's a lot of crap in here that should be changed.     -nxb on August 28, 2020      at 1:15 P.M. EDT
  pPrintVarNXB("TimsRealAnkleZDepthInches", TimsRealAnkleZDepthInches, nNewlines=0)
  pPrintVarNXB("yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1", yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1, nNewlines=0)

  #========================================================================
  # TODO:  write in calf and thigh indices and real measurements in inches
  #     -nxb, August 31, 2020
  #========================================================================

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftLowerLegVertsTranslatedBack = leftLowerLegVertsCenteredOnOrigin + origLowerLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftLowerLegVertsTranslatedBack[:,Y] -=  finalResizedLeftLowerLegVertsTranslatedBack[:,Y].min()

  leftLowerLegXYZScaleParams = {  # TODO:  copy all this for UpperLeg.   (-nxb; August 19, 2020)
    'X' : customerEstimatedMaxLowerLegWidthInches_X / xWidthBeforeAnyScaling_atTheBeginningOfThisFunction,
    'Y' : customerEstimatedLowerLegLenInches        / yHeightBeforeAnyScaling_atTheBeginningOfThisFunction,
    'Z' : customerEstimatedMaxLowerLegDepthInches_Z / zDepthBeforeAnyScaling_atTheBeginningOfThisFunction,
    # Ankle:
    'xWidthAtAnkle':   customersAnkleXWidthInches()   / xWidthBeforeAnyScaling_atTheBeginningOfThisFunction,
    'yHeightAtAnkle':  customerEstimatedLowerLegLenInches/ yHeightBeforeAnyScaling_atTheBeginningOfThisFunction, # NOTE: scaled the same amount at the bottom of the leg as up at the knee
    'zDepthAtAnkle':   customersAnkleZDepthInches()   / zDepthBeforeAnyScaling_atTheBeginningOfThisFunction,
    # Knee:
    'xWidthAtKnee':   customersKneeXWidthInches()   /  xWidthBeforeAnyScaling_atTheBeginningOfThisFunction,
    'yHeightAtKnee':  customerEstimatedLowerLegLenInches/ yHeightBeforeAnyScaling_atTheBeginningOfThisFunction, # NOTE: scaled the same amount at the knee as down at the ankle
    'zDepthAtKnee':   customersKneeZDepthInches()   /  zDepthBeforeAnyScaling_atTheBeginningOfThisFunction,
    # TODO: proper "ankle-foot-boundary" resizing
    #'X_AtBot_Ankle': customersAnkleXWidthInches()   / xWidthAnkle_BeforeAnyScaling_atTheBeginningOfThisFunction, # TODO: proper "ankle-foot-boundary" resizing
    # TODO: proper "ankle-foot-boundary" resizing
  }

  return finalResizedLeftLowerLegVertsTranslatedBack, leftLowerLegIdxes, leftLowerLegXYZScaleParams # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "resizedLeftSMPLX_AnkleToKnee(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "resizedLeftSMPLX_AnkleToKnee(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):    # we don't have this customerEstimatedLowerLegLenInches, ==================================================




























































#==================================================
def leftUpperLegIndices(vs):
  L_KNEE_Y_HEIGHT         = -0.8582508 
  L_TOP_OF_UPPER_LEG_Y_HEIGHT = -0.58      # I "calculated" this value   "-0.58" in    Blender.  -nxb, Aug 14, 2020 
  # FIXME:   we're in debug mode:   use the "-0.58" value from above instead
  MIDDLE_OF_BODY_X = 0      # **__ROUGHLY__** correct;   certainly correct enough to distinguish between the left and right lowerLegs (in t-pose with legs "fairly widely" spread)

  #==============================
  #   Useful for debugging:
  #     -nxb, August 17, 2020
  #==============================
  #L_TOP_OF_UPPER_LEG_Y_HEIGHT = -0.46138254# from "smplx/joint_names.py"      (AKA from file "joints.npy")
  #MIDDLE_OF_BODY_X = -0.5 
  X,Y,Z = 0,1,2

  belowButtIdxs = np.where(   
    np.less(vs[:,Y],   
            L_TOP_OF_UPPER_LEG_Y_HEIGHT))[0]
  aboveKneeIdxs = np.where(   
    np.greater(vs[:,Y],   
            L_KNEE_Y_HEIGHT))[0]
  leftSideOfBodyIdxs = np.where(
    np.greater(vs[:,X],
            MIDDLE_OF_BODY_X))[0]

  # belowButt AND aboveKnees:
  upperLegsVertsIdxs     = np.intersect1d(  aboveKneeIdxs,   belowButtIdxs) 
  leftUpperLegsVertsIdxs = np.intersect1d(  upperLegsVertsIdxs, leftSideOfBodyIdxs) 
  return leftUpperLegsVertsIdxs
  #leftUpperLeg           = vs[leftUpperLegsVertsIdxs, :]
  #return leftUpperLeg
#==================================================


#==================================================
def leftFootIndices(vs):
  L_ANKLE_Y_HEIGHT = -1.2795366  
  MIDDLE_OF_BODY_X = 0      # **__ROUGHLY__** correct;   certainly correct enough to distinguish between the left and right lowerLegs (in t-pose with legs "fairly widely" spread)
  X,Y,Z = 0,1,2

  belowAnkleIdxs = np.where(   
    np.less(vs[:,Y],   
            L_ANKLE_Y_HEIGHT))[0]
  leftSideOfBodyIdxs = np.where(
    np.greater(vs[:,X],
            MIDDLE_OF_BODY_X))[0]

  # belowKnees AND aboveAnkles:
  leftFootIdxs            = np.intersect1d(  belowAnkleIdxs,  leftSideOfBodyIdxs)
  return leftFootIdxs
#==================================================



#==================================================
def leftLowerLegIndices(vs):
  L_KNEE_Y_HEIGHT  = -0.8582508 
  L_ANKLE_Y_HEIGHT = -1.2795366  
  MIDDLE_OF_BODY_X = 0      # **__ROUGHLY__** correct;   certainly correct enough to distinguish between the left and right lowerLegs (in t-pose with legs "fairly widely" spread)
  X,Y,Z = 0,1,2

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
  lowerLegsVertsIdxs     = np.intersect1d(  aboveAnkleIdxs,  belowKneeIdxs) 
  leftLowerLegsVertsIdxs = np.intersect1d(  lowerLegsVertsIdxs, leftSideOFBodyIdxs) 
  return leftLowerLegsVertsIdxs
  #leftLowerLeg           = vs[leftLowerLegsVertsIdxs, :]
  #return leftLowerLeg
#==================================================


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
    betas = torch.zeros([1, 10], dtype=torch.float32)    # -nxb, August 13, 2020
    #betas[0]=4     # NOTE: changing the betas actually changes the verts.    -nxb, August 13, 2020
    expression = torch.randn([1, 10], dtype=torch.float32)

    output = model(betas=betas, expression=expression,
                   return_verts=True)
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    joints = output.joints.detach().cpu().numpy().squeeze()



    #==============================================================================================
    #==============================================================================================

    #  TIM_ESTIMATED_LOWER_LEG_LENGTH_INCHES = ...
    #===============================================
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
    print("TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN:\n  {}".format(TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN) )

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

    TIM_ANKLE_WIDTH_AKA_X_INCHES  = 3.25 
    TIM_ANKLE_DEPTH_AKA_Z_INCHES  = 3.75

    #================================================================================
    #================================================================================
    #================================================================================
    #  Major Line:                                                                 
    #                  (" ` resizeLeftSMPLX_LowerLeg(...) ` "  contains a LOT of code)
    #================================================================================
    #================================================================================
    #================================================================================

    #======================
    # Lower leg :
    #   (ankle up to knee)
    #======================
    resizedLeftLowerLegVerts, leftLowerLegIdxes, leftLowerLegScaleParams = resizedLeftSMPLX_AnkleToKnee(vertices, joints, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)
    vertsWithResizedLeftLowerLeg = deepcopy(vertices)
    vertsWithResizedLeftLowerLeg[leftLowerLegIdxes] = resizedLeftLowerLegVerts

    # Scale the left foot to fit the lowerLeftLeg:
    resizedLeftFootVerts, leftFootIdxes = resizedLeftSMPLX_foot(vertices, leftLowerLegScaleParams['xWidthAtAnkle'],  leftLowerLegScaleParams['yHeightAtAnkle'],  leftLowerLegScaleParams['zDepthAtAnkle'])

    #==================================================================================================================
    # Get 2 ankle verts for translation :
    #   (1 right below ankle, the other 1 right above the ankle)  so we can re-translate :
    #==================================================================================================================

    #==================================================================================================================
    # Bottom of lower left leg:
    #   (AKA "left ankle")
    idxsLeftLowerLeg = leftLowerLegIndices(vertices)
    # This variable "yHeightBottomOfLeftLowerLeg" is the same as "yHeightOfLeftAnkle"
    yHeightBottomOfLeftLowerLeg = np.min  ( vertices[idxsLeftLowerLeg,Y] )
    idxOfBottomOfLeftLowerLeg   = np.where( np.equal( vertices[:,Y], yHeightBottomOfLeftLowerLeg ) )   [0]
    vertLeftSideBottomOfLowerLeg= vertices[ idxOfBottomOfLeftLowerLeg ]
    #==================================================================================================================

    #==================================================================================================================
    # Top of left foot:
    #   (AKA "left ankle")
    idxsLeftFoot = leftFootIndices(vertices)
    # This variable "yHeightTopOfLeftFoot" is the same as "yHeightOfLeftAnkle"
    yHeightTopOfLeftFoot      = np.max  ( vertices[idxsLeftFoot,Y])
    idxOfTopOfLeftFoot        = np.where( np.equal( vertices[:,Y], yHeightTopOfLeftFoot  ) )   [0]
    vertLeftSideTopOfLeftFoot = vertices[ idxOfTopOfLeftFoot]
    #==================================================================================================================




    '''
    # temporary debugging:
    pPrintVarNXB("idxOfBottomOfLeftLowerLeg", idxOfBottomOfLeftLowerLeg, nNewlines=1) # [5884]
    pPrintVarNXB("idxOfTopOfLeftFoot", idxOfTopOfLeftFoot, nNewlines=2)               # [5885]
    tmpDebuggingVerts = deepcopy(vertices)
    tmpDebuggingVerts[ idxOfBottomOfLeftLowerLeg , X ] +=   0.5
    tmpDebuggingVerts[ idxOfTopOfLeftFoot        , X ] -=   0.5

    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    # Basically a series of lines that functions equivalently to "pltshow(mesh)"
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    import pyrender
    import trimesh
    import trimesh.exchange.obj #  Added by nxb on   August 13, 2020
    vertex_colors = np.ones([tmpDebuggingVerts.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8] # gray
    resizedTrimesh =  trimesh.Trimesh(tmpDebuggingVerts, model.faces,
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

    pyrender.Viewer(scene, use_raymond_lighting=True)  # NOTE: this line turns on/off the mesh popping up visually AKA "pltshow"  -nxb; August 28, at 11:52 A.M.
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    # end 
    #   "Basically a series of lines that functions equivalently to "pltshow(mesh)"
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    #============================================================================
    '''





    # above - below => positiveY_Value
    origDisplacementLeftAnkle = vertLeftSideBottomOfLowerLeg - vertLeftSideTopOfLeftFoot
    print("\n"*3 +    "="*99)
    print("origDisplacementLeftAnkle: {}".format(origDisplacementLeftAnkle))
    #==================================================================================================================
    # end "Get 2 knee verts for translation"
    #   (1 right below knee, the other 1 right above the knee)  so we can re-translate :
    #==================================================================================================================

    # Scale "origDiff" in x, y, and z   to find the amount of "translationDelta" where the upperLeg SHOULD BE relative to the lowerLeg:
    #   upperLeg **__should__** be ABOVE the lowerLeg

    # Scale x:
    scaledDisplacementLeftAnkle  = deepcopy(origDisplacementLeftAnkle)
    print("\n"*3 +    "="*99)
    print("scaledDisplacementLeftAnkle: {}".format(scaledDisplacementLeftAnkle))
    scaledDisplacementLeftAnkle[:,X]*= leftLowerLegScaleParams['xWidthAtAnkle']
    scaledDisplacementLeftAnkle[:,Y]*= leftLowerLegScaleParams['yHeightAtAnkle']
    scaledDisplacementLeftAnkle[:,Z]*= leftLowerLegScaleParams['zDepthAtAnkle']
    print("scaledDisplacementLeftAnkle, (post-'scaling'): {}".format(scaledDisplacementLeftAnkle))

    #================================================================================
    # Translate foot under leftLowerLeg :
    #   First we need the correspondences between the indexing of "vertices" and the indexing of "resizedLeftFootVerts"
    #   1.  Get the index of bottomOfLeftLowerLeg within the indexing of "resizedLeftFootVerts"   then 
    #   2.  Get the index of topOfLeftFoot within the indexing of "resizedLeftFootVerts"   then 
    #   3.  bottomOfLeftLowerLeg - topOfLeftFoot
    idxOfBottomOfLeftLowerLegInResizedLeftLowerLegVerts = np.where(leftLowerLegIdxes == idxOfBottomOfLeftLowerLeg)[0] # 5884    =>  190
    currBottomOfResizedLeftLowerLeg = resizedLeftLowerLegVerts[ idxOfBottomOfLeftLowerLegInResizedLeftLowerLegVerts] # 5884   =>  190

    idxOfTopOfLeftFootInResizedLeftFootVerts = np.where(leftFootIdxes == idxOfTopOfLeftFoot)[0]#5885  =>  111
    currTopOfResizedLeftFoot = resizedLeftFootVerts [ idxOfTopOfLeftFootInResizedLeftFootVerts]#5885  =>  111
    currAnkleDisplacement = currBottomOfResizedLeftLowerLeg - currTopOfResizedLeftFoot

    pPrintVarNXB("idxOfBottomOfLeftLowerLegInResizedLeftLowerLegVerts", idxOfBottomOfLeftLowerLegInResizedLeftLowerLegVerts, nNewlines=0)
    pPrintVarNXB("currBottomOfResizedLeftLowerLeg", currBottomOfResizedLeftLowerLeg, nNewlines=0)
    pPrintVarNXB("idxOfTopOfLeftFootInResizedLeftFootVerts", idxOfTopOfLeftFootInResizedLeftFootVerts, nNewlines=0)
    pPrintVarNXB("currTopOfResizedLeftFoot", currTopOfResizedLeftFoot, nNewlines=0)
    # Move the leg to be above the foot:
    resizedLeftLowerLegVerts = resizedLeftLowerLegVerts - currBottomOfResizedLeftLowerLeg + currTopOfResizedLeftFoot + scaledDisplacementLeftAnkle

    # whatDisplacementIsCurrently =
    # whatDisplacementShouldBe =  Orig
    #resizedLeftFootVerts[] -


    #==================================================================================================================
    # Get 2 knee verts for translation :
    #   (1 right below knee, the other 1 right above the knee)  so we can re-translate :
    #==================================================================================================================
    L_KNEE_Y_HEIGHT  = -0.8582508
    # Lower left leg:
    idxsBelowKnee, vertsBelowKnee = filterVertsBtwn(vertices, -float('inf'),  L_KNEE_Y_HEIGHT,  axis='y')
    idxsLeftSide , vertsLeftSide  = filterVertsBtwn(vertices, 0,              float('inf'),     axis='x')
    idxsLeftSideBelowKnee = np.intersect1d(idxsBelowKnee, idxsLeftSide)
    #idxsLeftSideBelowKnee, vertsLeftSideBelowKnee = filterVertsBtwn(vertsBelowKnee, 0, float('inf'),  axis='x')
    # This variable "yHeightTopOfLeftLowerLeg" is the same as "yHeightOfLeftKnee"
    yHeightTopOfLeftLowerLeg  = np.max  ( vertices[idxsLeftSideBelowKnee,Y] )
    idxOfTopOfLeftLowerLeg    = np.where( np.equal( vertices[:,Y], yHeightTopOfLeftLowerLeg ) )   [0]
    vertLeftSideTopOfLowerLeg = vertices[ idxOfTopOfLeftLowerLeg ]

    # Upper left leg:
    #   NOTE: we're getting the upperLegVert that's CLOSEST to "L_KNEE_Y_HEIGHT" in ***Y*** rather than adjacent to this leftTibiaVert that we got.
    idxsAboveKnee, vertsAboveKnee = filterVertsBtwn(vertices, L_KNEE_Y_HEIGHT, float('inf'), axis='y')
    idxsLeftSideAboveKnee = np.intersect1d(idxsAboveKnee, idxsLeftSide)
    #idxsLeftSideAboveKnee, vertsLeftSideAboveKnee = filterVertsBtwn(vertsAboveKnee, 0, float('inf'),  axis='x')
    yHeightBottomOfLeftLowerLeg = np.min  ( vertices[idxsLeftSideAboveKnee,Y])
    idxOfBottomOfLeftUpperLeg   = np.where( np.equal( vertices[:,Y], yHeightBottomOfLeftLowerLeg  ) )   [0]
    vertLeftSideBottomOfUpperLeg= vertices[ idxOfBottomOfLeftUpperLeg ]

    # above - below => positiveY_Value
    origDisplacementLeftKnee = vertLeftSideBottomOfUpperLeg - vertLeftSideTopOfLowerLeg
    #==================================================================================================================
    # end "Get 2 knee verts for translation"
    #   (1 right below knee, the other 1 right above the knee)  so we can re-translate :
    #==================================================================================================================

    # Scale "origDiff" in x, y, and z   to find the amount of "translationDelta" where the upperLeg SHOULD BE relative to the lowerLeg:
    #   upperLeg **__should__** be ABOVE the lowerLeg

    # Scale x:
    scaledDisplacementLeftKnee  = deepcopy(origDisplacementLeftKnee)
    print("\n"*3 +\
      "="*99)
    print("leftLowerLegScaleParams:")
    for k,v in leftLowerLegScaleParams.items():
      print('{} {}'.format(k,v))
    print("scaledDisplacementLeftKnee: {}".format(scaledDisplacementLeftKnee))
    scaledDisplacementLeftKnee[:,X]*= leftLowerLegScaleParams['xWidthAtKnee']
    scaledDisplacementLeftKnee[:,Y]*= leftLowerLegScaleParams['yHeightAtKnee']
    scaledDisplacementLeftKnee[:,Z]*= leftLowerLegScaleParams['zDepthAtKnee']
    print("scaledDisplacementLeftKnee, (post-'scaling'): {}".format(scaledDisplacementLeftKnee))

    vertsWithResizedLeftLeg = deepcopy(vertices)
    vertsWithResizedLeftLeg[idxsLeftLowerLeg] = resizedLeftLowerLegVerts
    vertsWithResizedLeftLeg[idxsLeftFoot] = resizedLeftFootVerts

    #================================================================================
    # TODO:     leftUpperLegParams  for merging UpperLegs with lowerLegs        (in "`getResizedLeftSMPLX_UpperLeg(... , ... , ... )`")
    """
    resizedLeftUpperLegVerts, leftUpperLegIdxes, leftUpperLegParams = resizedLeftSMPLX_KneeToButtBottom(vertices, joints, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)      # TODO: change "TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN" to      "TIM_UPPER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN

    """

    """
    #getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches,                                customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, TIM_UpperLeg_WIDTH_AKA_X_INCHES, TIM_UpperLeg_DEPTH_AKA_Z_INCHES):    # we don't have this customerEstimatedUpperLegLenInches,
    vertsWithResizedLeftUpperLeg = deepcopy(vertices)
    vertsWithResizedLeftUpperLeg[leftUpperLegIdxes] = resizedLeftUpperLegVerts

    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #   start of code for prettyPrinting /
    #     debugging /
    #     me figuring out (roughly) what the fuck is going on
    #       -NXB, September 5, 2020
    #================================================================================
    L_ANKLE_Y_HEIGHT = -1.2795366
    L_KNEE_Y_HEIGHT  = -0.8582508
    L_TOP_OF_UPPER_LEG_Y_HEIGHT = -0.58      # I "calculated" this value   "-0.58" in    Blender.  -nxb, Aug 14, 2020
    X,Y,Z = 0,1,2
    MIDDLE_OF_BODY_X = 0      # **__ROUGHLY__** correct;   certainly correct enough to distinguish between the left and right lowerLegs (in t-pose with legs "fairly widely" spread)

    belowButtIdxs = np.where(   
      np.less(vertices[:,Y],   
              L_TOP_OF_UPPER_LEG_Y_HEIGHT))[0]
    aboveAnkleIdxs = np.where(   
      np.greater(vertices[:,Y],   
              L_ANKLE_Y_HEIGHT))[0]
    leftSideOfBodyIdxs = np.where(
      np.greater(vertices[:,X],
              MIDDLE_OF_BODY_X))[0]

    # belowButt AND aboveAnkles:
    upperLegsVertsIdxs  = np.intersect1d( aboveAnkleIdxs,     belowButtIdxs)
    leftLegsVertsIdxs   = np.intersect1d( upperLegsVertsIdxs, leftSideOfBodyIdxs)

    #================================================================================
    #   end of code for prettyPrinting /
    #     debugging /
    #     me figuring out (roughly) what the fuck is going on
    #       -NXB, September 5, 2020
    #================================================================================

    # Translation code. comment written August 24, 2020
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)
    # TODO:  put this variable definition of "`lowerLegEndsY`" later, when I'm doing the move the upperLeg "UP,"   above the lowerLeg      (Y)
    lowerLegEndsY = resizedLeftLowerLegVerts[:,Y].max()    # I fixed this bug at 3:00 P.M. EDT on Aug 18, 2020      -nxb    ( "`min()`" ==>  "`max()`"  )         

    lowerLegHeightMagnitude = resizedLeftLowerLegVerts[:,Y].max() - resizedLeftLowerLegVerts[:,Y].min()
    upperLegHeightMagnitude = resizedLeftUpperLegVerts[:,Y].max() - resizedLeftUpperLegVerts[:,Y].min()      # TODO:  remove the "min()" call (min() should always be 0)        -nxb;     August 18, 2020
    LOWER_LEG_____BOUNDARY_SKIN_END_CONST = lowerLegHeightMagnitude / 10  # TODO: fiddle with this LOWER_...CONST.
    UPPER_LEG_____BOUNDARY_SKIN_END_CONST = upperLegHeightMagnitude / 10  # TODO: fiddle with this UPPER_...CONST.
    lowersTopBoundarySkinIdxs = np.where(
      np.greater(
        resizedLeftLowerLegVerts[:,Y],
        lowerLegEndsY - LOWER_LEG_____BOUNDARY_SKIN_END_CONST #     (I have to do math in this line    because this is pre-translation-up-and-down)      -nxb, August 18, 2020
      ))[0]    # TODO:    rename this awkwardly named "LOWER_LEG_____BOUNDARY_SKIN_END_CONST"        -nxb; August 18, 2020
    uppersBottomBoundarySkinIdxs = np.where(
      np.less(
        resizedLeftUpperLegVerts[:,Y],
        UPPER_LEG_____BOUNDARY_SKIN_END_CONST))[0]    # TODO:    rename this awkwardly named "UPPER_LEG_____BOUNDARY_SKIN_END_CONST"        -nxb; August 18, 2020

    # Translation code. comment written August 24, 2020
    lowersTopBoundarySkin     = resizedLeftLowerLegVerts[lowersTopBoundarySkinIdxs    ]     
    uppersBottomBoundarySkin  = resizedLeftUpperLegVerts[uppersBottomBoundarySkinIdxs ]   
    # OR,  more technically, resizedLeftUpperLegVerts[uppersBottomBoundarySkinIdxs, : ]     -August 18, 2020
    lowersCentroid = lowersTopBoundarySkin.mean(axis=0)
    uppersCentroid = uppersBottomBoundarySkin.mean(axis=0)

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


    #print('betas =', betas)     # betas = tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])   #print('betas.shape =', betas.shape)  # torch.Size([1,10])
    print('Vertices shape =', vertices.shape) # (10475,3)
    """
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
        vertex_colors = np.ones([vertices.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8] # gray
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

        pyrender.Viewer(scene, use_raymond_lighting=True)  # NOTE: this line turns on/off the mesh popping up visually AKA "pltshow"  -nxb; August 28, at 11:52 A.M.

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

        pyrender.Viewer(scene, use_raymond_lighting=True)  # NOTE: this line turns on/off the mesh popping up visually AKA "pltshow"  -nxb; August 28, at 11:52 A.M.
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
        raise ValueError('Unknown plotting_module: {}'.format(plotting_module)  )
#========================================================================================


#========================================================================================
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
#========================================================================================



































































































#============================================ BLANK LINES =============================================
