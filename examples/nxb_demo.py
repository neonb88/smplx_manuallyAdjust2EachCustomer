#TODO tomorrow (Sat, Aug 29, 2020):    Figure out why changing that variable with the ankle and knee heights (y)    doesn't actually change anything.

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
  #raise Exception( "fucking finish your UpperLeg     code, Bendich.     ('getResizedLeftSMPLX_UpperLeg()'  is the full name)")
  
  '''
    Do a lot of shit here   [insertCode]

      (Coding all this shit might take 
        ~4 hours, give-or-take-a-few-minutes) based on the 
        "experiential data" for the other similar function   
        "getResizedLeftSMPLX_LowerLeg()"
  '''

  # Idea:   have this spit out all the body parts with centroids at (0,0,0) ?    Then it's a different function's job to "put Humpty-Dumpty back together again"      -NXB, August 15, 2020

  # NOTE:    generalize this to be "getResizedLeftSMPLX_BodyPartNameHere(..., otherParams, ...)"  ?
  #   -nxb, August 15, 2020
  '''
    This function can be generalized to each body part?
    Code reuse would prevent some headaches, make it so changing error-catching in just the general function would fix the error(s) for all the body parts rather than just the one, 

    August 15, 2020
  '''


  #===================================================================================================
  # TODO:  find the EXACT RIGHT VERTICES  in SMPL-X that will let us scale the UpperLeg correctly
  #===================================================================================================
  # NOTE: NOTE: NOTE: NOTE: NOTE:  This code isn't perfect.  Ideally, every damn vertex in SMPL-X would be exactly where the customers' vertices are at that time.       
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  # NOTE NOTE NOTE NOTE NOTE
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================

    #===================================================================================================
    #   As of August 17, at 7:31 P.M.  EDT,   the function header was entitled:
    #===================================================================================================
    # function header: "getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches):" 
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

  #====================================================================================================================
  # NOTE
  # NOTE:  slight assumption that causes a problem:  I can't really scale  the upperLeg directly to yHeight==1, because the SMPL-X upperLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  # NOTE
  #====================================================================================================================
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

  return finalResizedLeftUpperLegVertsTranslatedBack, leftUpperLegIdxes, {} # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "makeLeftLeg(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):     ==================================================

#==================================================




# TODO ?    -August 27, 2020
"""

#==================================================
def getResizedLeftSMPLX_LowerLegPrettierDraft2Aug24( 
    verts,
    customerEstimatedLowerLegLenInches,
    customerEstimatedHeightInches,
    prevBodyPartsXStretchingSlashScaling,
    prevBodyPartsZStretchingSlashScaling,
    customerEstimatedMaxLowerLegWidthInches_X, 
    customerEstimatedMaxLowerLegDepthInches_Z)
  # I think I'll rewrite some of this in main() instead.  
  # 3 functions: 1. getResizedFuncCall(ankle-to-calf), 2. getResizedFuncCall(calf-to-knee), and 3. getResizedFuncCall(knee-up-to-bottom-of-butt)      seems like its fewer layer of encapsulation while also being more specific and still easy to understand     (makes more sense to me as a code reader and editor [AKA maintainer] )    than just 
  # 2 functions (1. getRes...Lower(...), and 2. getRes...Upper(...)
  '''
    Prettier result, not necessarily prettier code.
      -nxb, August 24, 2020
  '''
  X,Y,Z=0,1,2

  idxOfSMPLXsLeftCalfWithGreatestCircum = leftCalfIdx             (modelType = 'SMPLX')
  idxOfTopOfSMPLXs_LeftLowerLeg         = topOfLeftLowerLegIdx    (modelType = 'SMPLX')
  idxOfBottomOfSMPLXs_LeftLowerLeg      = bottomOfLeftLowerLegIdx (modelType = 'SMPLX')
  raise Exception ("Fill in the above leftCalfIdx, topOfLeftLowerLegIdx, and bottomOfLeftLowerLegIdx code, Nathan.")

  topsYHeight     = verts[idxOfTopOfSMPLXs_LeftLowerLeg][Y]
  midsYHeight     = verts[idxOfMiddleOfSMPLXs_LeftCalf][Y]
  bottomsYHeight  = verts[idxOfBottomOfSMPLXs_LeftLowerLeg][Y]

  # reuse this code in a function "def scaleLegLinearlyWithYHeight(verts, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches)"
  upperCalfsYHeight = topsYHeight - midsYHeight

  # knee down:
  scaleLegLinearlyWithYHeight()
  # knee up:
  scaleLegLinearlyWithYHeight()

  return LeftLowerLegVerts
#==================================================

"""




#==================================================
def scaleLegLinearlyWithYHeight(verts, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches):
  # TODO:  make this fast (AKA "performant").   (vectorize it)        -nxb; August 24, 2020 at    5:15 P.M.

  # NOTE:   the code is fairly performant.   (about 5 secs.   O(5 seconds)   )       At least while I'm only scaling the LowerLeg, most of the time is spent on file-IO rather than in this method.     (see output from "cProfile" below ) :     



#============================================================================================================
  '''     Some output from the "cProfile" command       (sort by total time taken)
=============================================================================================================
          Some output from the "cProfile" command       (sort by total time taken)
=============================================================================================================
    "`p3 -m cProfile -s tottime examples/nxb_demo.py --model-folder /home/nathan_bendich/Downloads/SMPL-X_Models/models/ --plot-joints=True --gender="male" `"        -nxb, August 28, 2020
=============================================================================================================
 








==========================================================================
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
==========================================================================

======================================================================================================
     1336    0.596    0.000    0.596    0.000 {method 'read' of '_io.FileIO' objects}
    91/88    0.558    0.006    0.562    0.006 {built-in method _imp.create_dynamic}
      322    0.316    0.001    0.316    0.001 {method 'decompress' of 'zlib.Decompress' objects}
     1336    0.209    0.000    0.209    0.000 {built-in method marshal.loads}
     5603    0.201    0.000    0.201    0.000 {built-in method posix.stat}
      396    0.157    0.000    0.157    0.000 {method 'read' of '_io.BufferedReader' objects}
     2292    0.154    0.000    0.154    0.000 {method 'format' of 'str' objects}
  286/207    0.147    0.001    0.181    0.001 {built-in method numpy.core._multiarray_umath.implement_array_function}
     1336    0.115    0.000    0.711    0.001 <frozen importlib._bootstrap_external>:830(get_data)
     1081    0.114    0.000    0.114    0.000 {built-in method builtins.compile}
2725/2666    0.113    0.000    0.289    0.000 {built-in method builtins.__build_class__}
======================================================================================================

  '''

  # TODO:  make this fast (AKA "performant").   (vectorize it)        -nxb; August 24, 2020 at    5:15 P.M.

  # TODO:  fix all these "hell-names" while also making sure the names are actually descriptive to future readers.  Perhaps you should just document?    -nxb, August 27, 2020 at 6:12 P.M.
  #   There's no way to make everything PERFECT, Bendich.
  #   By "hell-names," I mean shit like "xWidthAtTopYHeight_RealCustomerInches", "xWidthAtBotYHeight_RealCustomerInches",   -nxb, August 27, 2020 at 6:12 P.M.
  #   It was even worse at other time(s):  ridiculously long names and shit like "xWidth_RealCustomerMeasure_InInches_atTopYHeightTheYValueOfWhichIsInPixelInches"
  #   -nxb, August 27, 2020 at 6:12 P.M.

  # TODO:  find the bug(s) in this function    and/or approach.   -nxb;   Aug 24, 3:39 P.M.
  # TODO: rename variables so it's clear to future-NXB that xWidthAtBotYHeight_RealCustomerInches, xWidthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches, and zDepthAtTopYHeight_RealCustomerInches are REAL_CUSTOMER_MEASURES_IN_INCHES.
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

  # TODO: write this function with proper error-checking.     rewrite this with proper error-checking, proper input of parameters into the function "scaleLegLinearlyWithYHeight(verts,  ... ,  ... ,  ... ,  ... ,  ... ,  ... )"    instead of just "moreParams" as we put in the funccall to scaleLegLinearlyWithYHeight() on line 619 in the function entitled "getResizedLeftSMPLX_LowerLeg()"       -nxb, August 27, 2020





  # TODO
  # TODO:   make sure "`np.isclose()`" has a high enough tolerance.     (ie. the assertion shouldn't fail when everything is fine)     -nxb, August 24, 2020
  # TODO
  #assert np.isclose(verts[:,Y].max(), yTop)       and    np.isclose(verts[:,Y].min(), yBot)      # TODO: rewrite this with proper error-checking, proper input of parameters into the function "scaleLegLinearlyWithYHeight(verts,  ... ,  ... ,  ... ,  ... ,  ... ,  ... )"    instead of just "moreParams" as we put in the funccall to scaleLegLinearlyWithYHeight() on line 619 in the function entitled "getResizedLeftSMPLX_LowerLeg()"
  # TODO
  # TODO:   make sure "`np.isclose()`" has a high enough tolerance.     (ie. the assertion shouldn't fail when everything is fine)     -nxb, August 24, 2020
  # TODO

  X,Y,Z=0,1,2
  verts_ = deepcopy(verts) # b/c accessor, not mutator method.  -nxb, August 24, 2020
  """ In other words, side effects and state are BAD;
    Using "deepcopy" is more "functional" than mutating the original numpy.ndarray, which is    GOOD.  """

  #height = yTop-yBot        # NOTE: I read these lines again, and I'm PRETTY sure I don't need them to get the right answer.     -nxb, August 27, 2020
  #=======================================
  # along the height of the leg:
  #=======================================
  for i,yVal in enumerate(verts_[:,Y]):
  #=======================================

    #  NOTE: The correct, well-thought-through lines are below.   -nxb, August 27, 2020
    #currsHeight = yVal - yBot        # NOTE: I read these lines again, and I'm PRETTY sure I don't need them to get the right answer.     -nxb, August 27, 2020
    #height - currsHeight / height    # NOTE: I read these lines again, and I'm PRETTY sure I don't need them to get the right answer.     -nxb, August 27, 2020
    #  NOTE: The correct, well-thought-through lines are below.   -nxb, August 27, 2020

    #========================
    #   x (width) scaling:   
    #========================
    m = slope = (xWidthAtTopYHeight_RealCustomerInches - xWidthAtBotYHeight_RealCustomerInches) / (yTop - yBot)
    # it's kind of hard to understand this code.  See reasons in extended documentation below   (search for "DOCUMENTATION for this code" as of August 28, 2020)
    b = yInterceptOnTheGraph = xWidthAtTopYHeight_RealCustomerInches - (m*yTop)
    xScaling = m*yVal + b
    pn(2)
    pe(99)
    print("m: ")
    print(m)
    pe(99)
    pn(2)
    """
    pn(2)
    pe(99)
    print("type(xScaling): ")
    print(type(xScaling) )
    print("i: ")
    print(i)
    print("X: ")
    print(X)
    print("verts_[i,X].shape: ")
    print(verts_[i,X].shape)
    pe(99)
    pn(2)
    """
    verts_[i,X] *= xScaling

    #========================
    #   z (depth) scaling:   
    #========================
    m = slope = (zDepthAtTopYHeight_RealCustomerInches - zDepthAtBotYHeight_RealCustomerInches) / (yTop - yBot)  # it's kind of hard to understand this code.  See reasons in extended documentation below
    b = yInterceptOnTheGraph = zDepthAtTopYHeight_RealCustomerInches - (m*yTop)
    zScaling = m*yVal + b # again, not quite y = m*x+b.  See thorougher documentation after the function for reasoning -August 24, 2020. 
    verts_[i,Z] *= zScaling
    pn(1)
    pe(99)
    print(' '*30 + "xScaling:")
    print(' '*33 + str(xScaling) )    # why are these both 5.0?     -nxb, August 28, at 1:53 P.M.
    print(' '*30 + "zScaling:")
    print(' '*33 + str(zScaling) )    # why are these both 5.0?     -nxb, August 28, at 1:53 P.M.
    pe(99)
    pn(1)
  #============================================
  #end "for i, yVal in enumerate(verts_[:,Y]):"
  #============================================

  return verts_  # 90% sure this is a deepcopy so this isn't where the bug is   -nxb, August 28, 2020      at 1:31 P.M.

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
def getResizedLeftSMPLX_LowerLeg(vertices, joints, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):
  # NOTE:   even with "`pyrender.show()`" ,   this code is fairly performant.   (about 5 secs.   O(5 seconds)   )       At least while I'm only scaling the LowerLeg, most of the time is spent on file-IO rather than in this method.
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
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE: NOTE: NOTE: NOTE: NOTE:  slight assumption that causes a problem:  I can't really scale  the lowerLeg directly to yHeight==1, because the SMPL-X lowerLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  # NOTE NOTE NOTE NOTE NOTE
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================



















  #======================================================
  # TODO    TODO TODO TODO TODO
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  #======================================================
  #              ACTUAL CODE starts here:
  #======================================================
  # NOTE NOTE NOTE NOTE NOTE
  # NOTE NOTE NOTE NOTE NOTE
  # TODO TODO  TODO TODO TODO
  #======================================================





    #===================================================================================================
    #   As of August 15, at 8:31 P.M.  EDT,   the function header was entitled:
    #===================================================================================================
    # function header " getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches): "
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
  '''
  pe(99)
  print("leftLowerLegVerts.shape: ")
  print(leftLowerLegVerts.shape)
  print("joints.shape")
  print(joints.shape)
  print("joints[:3]:")
  print(joints[:3])
  print("jointsCenteredOnOrigin[:3]:")
  print(jointsCenteredOnOrigin[:3])
  print("origLowerLegCentroid")
  print(origLowerLegCentroid)
  pe(99)
  print("jointsCenteredOnOrigin.shape")
  print(jointsCenteredOnOrigin.shape)
  print("origLowerLegCentroid.shape")
  print(origLowerLegCentroid.shape)
  pe(99)
  '''

  #====================================================================================
  # Scale down:
  #   Normalize lowerLegLen to 1:
  #     NOTE:  (lowerLegLen is ALMOST exactly "`Y`," but not **__QUITE__**)
  #     NOTE: maintains proportions of lowerLeg;   **doesn't lose information**    -nxb; August 14, 2020
  #====================================================================================
  currHeightX = leftLowerLegVertsCenteredOnOrigin[:,X].max() - leftLowerLegVertsCenteredOnOrigin[:,X].min()
  currHeightY = leftLowerLegVertsCenteredOnOrigin[:,Y].max() - leftLowerLegVertsCenteredOnOrigin[:,Y].min()
  currHeightZ = leftLowerLegVertsCenteredOnOrigin[:,Z].max() - leftLowerLegVertsCenteredOnOrigin[:,Z].min()
  leftLowerLegVertsCenteredOnOrigin[:,X] /= currHeightX
  leftLowerLegVertsCenteredOnOrigin[:,Y] /= currHeightY
  leftLowerLegVertsCenteredOnOrigin[:,Z] /= currHeightZ

  jointsCenteredOnOrigin[:,X] /= currHeightX
  jointsCenteredOnOrigin[:,Y] /= currHeightY
  jointsCenteredOnOrigin[:,Z] /= currHeightZ
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
  jointsCenteredOnOrigin[:,X] *= customerEstimatedMaxLowerLegWidthInches_X
  jointsCenteredOnOrigin[:,Y] *= customerEstimatedLowerLegLenInches
  jointsCenteredOnOrigin[:,Z] *= customerEstimatedMaxLowerLegDepthInches_Z

  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  # TODO TODO TODO TODO TODO
  # TODO TODO TODO TODO TODO:    put in the real params "yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches,"     and "zDepthAtBotYHeight_RealCustomerInches" into func "scaleLegLinearlyWithYHeight(... ,  ... ,  ... ,  ... ,  ... ,  ... )"        instead of just "moreParams" (August 27, 2020)
  moreParams=1 # TODO TODO TODO TODO TODO:    put in the real params "yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches,"     and "zDepthAtBotYHeight_RealCustomerInches" into func "scaleLegLinearlyWithYHeight(... ,  ... ,  ... ,  ... ,  ... ,  ... )"        instead of just "moreParams" (August 27, 2020)
  # TODO TODO TODO TODO TODO:    put in the real params "yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches,"     and "zDepthAtBotYHeight_RealCustomerInches" into func "scaleLegLinearlyWithYHeight(... ,  ... ,  ... ,  ... ,  ... ,  ... )"        instead of just "moreParams" (August 27, 2020)
  # TODO TODO TODO TODO TODO
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================

  #===================================================================================================
  def customersCalfXWidthInches(customerImgFname="timsFrontView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
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
  NXBsRealCalfXWidthInches = TimsRealCalfXWidthInches  =  customersCalfXWidthInches(customerImgFname="timsFrontView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )     # FIXME:   this is actually Nathan's; (I didn't measure Tim's yet)        -nxb; August 28, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  TimsRealCalfXWidthInches  =  5  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #===================================================================================================

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
  NXBsRealKneeZDepthInches  = TimsRealCalfZDepthInches=  customersCalfZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  TimsRealCalfZDepthInches  =  5  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME:     calculate it from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  #===================================================================================================

  #===================================================================================================
  def customersAnkleXWidthInches(customerImgFname="timsSideView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
    NXBs_REAL_ANKLE_X_WIDTH_IN_INCHES = 2.5
    return NXBs_REAL_ANKLE_X_WIDTH_IN_INCHES
  NXBsRealAnkleXWidthInches = TimsRealAnkleXWidthInches = customersAnkleXWidthInches(customerImgFname="timsSideView_0_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )
  #======================================================================================================
  # FIXME: ======================================================================================= FIXME
  #TimsRealAnkleXWidthInches  =  5  # FIXME:     calculate Tim's from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME: ======================================================================================= FIXME
  #======================================================================================================

  #===================================================================================================
  #def customersAnkleZDepthInches(customerImgFname, OpenPoseKPS, binaryMask):
  def customersAnkleZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') ):
    NXBs_REAL_ANKLE_Z_DEPTH_IN_INCHES = 3.5
    return NXBs_REAL_ANKLE_Z_DEPTH_IN_INCHES
  NXBsRealAnkleZDepthInches = TimsRealAnkleZDepthInches = customersAnkleZDepthInches(customerImgFname="timsSideView_90_Degrees.jpg    TODO: fill in Tim's real filename locally on my Ubuntu machine", OpenPoseKPS=np.random.random((25,2)), binaryMask=np.random.random((640,480)).astype('bool') )

  #======================================================================================================
  # FIXME: ======================================================================================= FIXME
  #TimsRealAnkleZDepthInches  =  5  # FIXME:     calculate Tim's from the video / from a few images rather than doing it this way with a CONST.       -nxb, August 27, 2020
  # FIXME: ======================================================================================= FIXME
  #======================================================================================================





  # TODO: change this from "calf" to "knee" ?   Briefly (ie. today)    requires less work.     -nxb; August 28, 2020
  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1   = -0.3      # where the Knee  is on the SMPL-X model      (y-dimension is foot to scalp)      (these were hard-coded before August 27, 2020 -nxb)
  yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1  = -0.25     # where the Ankle is on the SMPL-X model      (y-dimension is foot to scalp)      (these were hard-coded before August 27, 2020 -nxb)
  LEFT_KNEE   = 4 # TODO: double-check this indexing?  (1-based vs. 0-based)
  LEFT_ANKLE  = 7   # see   "`/home/nathan_bendich/Dropbox/vr_mall_backup/IMPORTANT/smplx_manuallyAdjust2EachCustomer/smplx/joint_names.py`"  for details.
  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1   = jointsCenteredOnOrigin[LEFT_KNEE  , Y]    #  8.715
  yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1  = jointsCenteredOnOrigin[LEFT_ANKLE , Y]    # -9.715
  pn(2)
  pe(len("yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1:" )  +4   )
  print("  yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1 : " )    #  8.715
  print(yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1 )
  print("  yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1: ")     # -9.393
  print(yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1)
  pe(len("yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1:" )  +4   )
  pn(2)

  leftLegAnkleToCalfCenteredOnOrigin =scaleLegLinearlyWithYHeight(
    # TODO:  work backward from this function call.   (joints['ankleHeightY'] and/or vertices['calf'] )     -nxb, August 27, 2020
    leftLowerLegVertsCenteredOnOrigin, yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1, yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1, TimsRealCalfXWidthInches, TimsRealAnkleXWidthInches, TimsRealCalfZDepthInches, TimsRealAnkleZDepthInches)   # FIXME:     there's a lot of crap in here that should be changed.     For instance,     -nxb on August 28, 2020      at 1:15 P.M. EDT

  """
  leftLowerLegVertsCenteredOnOrigin = scaleLegLinearlyWithYHeight(
    leftLowerLegVertsCenteredOnOrigin, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches ) # TODO TODO TODO TODO TODO
  """
    # NOTE:  why did I want the function "scaleLegLinearlyWithYHeight" to spit out the ?
  #====================================================================================
  # Here the lowerLeg is normally proportioned again because we're using the customer's **__ACTUAL__**   Depth, Width, and Height.     
  #   -nxb, August 17, 2020
  #====================================================================================
  #leftLowerLegVertsCenteredOnOriginScaledToRealLowerLegLenInches = leftLowerLegVertsCenteredOnOriginNormalizedTo1 * customerEstimatedLowerLegLenInches
  #leftLowerLegVertsCenteredOnOrigin *= customerEstimatedLowerLegLenInches
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 

  # Translate:
  #   Translate back to original centroid: 
  #     (where the rest of the SMPL-X body STILL is)
  finalResizedLeftLowerLegVertsTranslatedBack = leftLowerLegVertsCenteredOnOrigin + origLowerLegCentroid
  # Set yMin to 0:        (see docstring for more details)
  finalResizedLeftLowerLegVertsTranslatedBack[:,Y] -=  finalResizedLeftLowerLegVertsTranslatedBack[:,Y].min()

  leftLowerLegXYZScaleParams = {  # TODO:  copy all this for UpperLeg.   (-nxb; August 19, 2020)
    'X' : customerEstimatedMaxLowerLegWidthInches_X / currHeightX,
    'Y' : customerEstimatedLowerLegLenInches        / currHeightY,
    'Z' : customerEstimatedMaxLowerLegDepthInches_Z / currHeightZ,
  }
  return finalResizedLeftLowerLegVertsTranslatedBack, leftLowerLegIdxes, leftLowerLegXYZScaleParams # TODO: either    A) fill out this "params" or       B) don't return another value.       SOMEHOW "makeLeftLeg(... , ... ,)" needs to know what the other function did to resize the leg      -August 18, 2020
#================================================== end function def of   "getResizedLeftSMPLX_LowerLeg(vertices, customerEstimatedLowerLegLenInches, customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, customerEstimatedMaxLowerLegWidthInches_X,  customerEstimatedMaxLowerLegDepthInches_Z):    # we don't have this customerEstimatedLowerLegLenInches, ==================================================






















































#==================================================
# TODO:  resurrect a general version of this (ie. all you have to do is tell it "lLowerLegLen" or "lUpperLegLen" and it spits out a properly resized   'numpy.ndarray' variable    "`SMPLX_Verts`"
"""
  # TODO:  resurrect a general version of this (ie. all you have to do is tell it "lLowerLegLen" or "lUpperLegLen" and it spits out a properly resized   'numpy.ndarray' variable    "`SMPLX_Verts`"
def filterVerts(vs):
  '''
    TODO:  generalize w/ a keyword arguments?      (ie. "lLowerLeg" or "lUpperLeg" or "lFoot" or whatever)
      -nxb; Aug 14, 2020
  '''
  return filterVertsLeftLowerLeg(vs)
"""
#==================================================

#==================================================
def leftUpperLegIndices(vs):
#def filterVertsLeftLowerLeg(vs):
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
def leftLowerLegIndices(vs):
#def filterVertsLeftLowerLeg(vs):
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
def makeLeftLeg(TODO_TODO_TODO_TODO_TODO_____params):
  '''
    Given the lowerLeg and upperLeg

    1.  Translates them on top of each other
    2.  Resizes to the appropriate extent
  '''
  # PARAMS:   NOTE TODO:
#def makeLeftLeg(... , ... , ...    ...(nParams is variable)  ):
  # TODO:  uncomment the "`raise Exception(...)  `" line
  #raise Exception( "fucking finish your UpperLeg     code, Bendich.     ('getResizedLeftSMPLX_UpperLeg()'  is the full name)")    # TODO:    re-raise this exception
    # TODO:    finish this function
    # TODO:    finish this function
    # TODO:    finish this function
    # TODO:    finish this function
    # TODO:    finish this function

  print("fucking finish your UpperLeg     code, Bendich.     ('getResizedLeftSMPLX_UpperLeg()'  is the full name)")

  X,Y,Z=0,1,2
  """
  leftUpperLegVerts
  leftLowerLegVerts
  #leftLowerLegVerts
  leftLegIdxes = np.concatenate(leftLowerLegIdxes, leftUpperLegIdxes) # maybe I have to type "`idxes[0]`"    to dereference the np.ndarray from the list

  resizedLeftUpperLegVerts[:,Y] += resizedLeftLowerLegVerts[:,Y].max() # I fixed this bug at 3:00 P.M. EDT on Aug 18, 2020      -nxb    ( "`min()`" ==>  "`max()`"  )
  resizedLeftUpperLegVerts[:,Y] += resizedLeftLowerLegVerts[:,Y].max() # I fixed this bug at 3:00 P.M. EDT on Aug 18, 2020      -nxb    ( "`min()`" ==>  "`max()`"  )
  # TODO:   more shit;   more shit from the main()    into this "boyo"
  # TODO:   more shit;   more shit from the main()    into this "boyo"
  # TODO:   more shit;   more shit from the main()    into this "boyo"
  # TODO:   more shit;   more shit from the main()    into this "boyo"
  # TODO:   more shit;   more shit from the main()    into this "boyo"
  """
  return
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
    betas = torch.zeros([1, 10], dtype=torch.float32)    #originally random      -nxb, August 13, 2020
    #betas[0]=4     # NOTE: changing the betas actually changes the verts.    -nxb, August 13, 2020
    expression = torch.randn([1, 10], dtype=torch.float32)

    output = model(betas=betas, expression=expression,
                   return_verts=True)
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    joints = output.joints.detach().cpu().numpy().squeeze()
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
    resizedLeftLowerLegVerts, leftLowerLegIdxes, leftLowerLegParams = getResizedLeftSMPLX_LowerLeg(vertices, joints, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, TIM_ANKLE_WIDTH_AKA_X_INCHES, TIM_ANKLE_DEPTH_AKA_Z_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)
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
    # Translation code. comment written August 24, 2020
    #====================================================================

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


    # Translation code. comment written August 24, 2020
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

    # Translation code. comment written August 24, 2020
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

    # Translation code. comment written August 24, 2020
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
        vertex_colors = np.ones([vertices.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8] # gray
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

        #"""
        resizedTrimesh =  trimesh.Trimesh(vertsWithResizedLeftLeg, model.faces,
                                   vertex_colors=vertex_colors) # nxb, Aug 13, 2020
        #"""
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

        #pyrender.Viewer(scene, use_raymond_lighting=True)  # NOTE: this line turns on/off the mesh popping up visually AKA "pltshow"  -nxb; August 28, at 11:52 A.M.
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
