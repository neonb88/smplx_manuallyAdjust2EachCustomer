
def getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches, customerEstimatedHeightInches, customerEstimatedMaxLowerLegWidthInches_X, customerEstimatedMaxLowerLegDepthInches_Z, customerEstimatedMaxUpperLegWidthInches_X,  customerEstimatedMaxUpperLegDepthInches_Z):

  # Idea:   have this spit out all the body parts with centroids at (0,0,0) ?    Then it's a different function's job to "put Humpty-Dumpty back together again"      -NXB, August 15, 2020

  # NOTE:    generalize this to be "getResizedLeftSMPLX_BodyPartNameHere(..., otherParams, ...)"  ?
  #   -nxb, August 15, 2020
  '''
  # Idea: This function can be generalized to each body part?  Code reuse would prevent some headaches, make it so changing error-catching in just the general function would fix the error(s) for all the body parts rather than just the one, 

    # -nxb, August 15, 2020
  '''

def scaleLegLinearlyWithYHeight(verts, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches):
  '''
    This old code was pasted here at
      4:47 P.M. on    August 31, 2020

    -NXB
  '''
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

  # TODO: write this function with proper error-checking.     rewrite this with proper error-checking, proper input of parameters into the function "scaleLegLinearlyWithYHeight(verts,  ... ,  ... ,  ... ,  ... ,  ... ,  ... )"    instead of just "moreParams" as we put in the funccall to scaleLegLinearlyWithYHeight() on line 619 in the function entitled "makeLeftLeg()"       -nxb, August 27, 2020





  # TODO
  # TODO:   make sure "`np.isclose()`" has a high enough tolerance.     (ie. the assertion shouldn't fail when everything is fine)     -nxb, August 24, 2020
  # TODO
  #assert np.isclose(verts[:,Y].max(), yTop)       and    np.isclose(verts[:,Y].min(), yBot)      # TODO: rewrite this with proper error-checking, proper input of parameters into the function "scaleLegLinearlyWithYHeight(verts,  ... ,  ... ,  ... ,  ... ,  ... ,  ... )"    instead of just "moreParams" as we put in the funccall to scaleLegLinearlyWithYHeight() on line 619 in the function entitled "makeLeftLeg()"
  # TODO
  # TODO:   make sure "`np.isclose()`" has a high enough tolerance.     (ie. the assertion shouldn't fail when everything is fine)     -nxb, August 24, 2020
  # TODO

#===================================================================================================
# in main()
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








#===================================================================================================
# in main()

    # TODO: automate estimating customer's lowerLeg length from video(s) and OpenPose.  -nxb, August 14, 2020

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


#===================================================================================================


#===================================================================================================
# old docstring for "leftLowerLeg(...)"
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
#===================================================================================================
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
  # NOTE NOTE NOTE NOTE NOTE    this iteration isn't perfect.  Especially when it comes to the measurement detail(s) from just a few "regular" RGB images
  # NOTE: NOTE: NOTE: NOTE: NOTE:  slight assumption that causes a problem:  I can't really scale  the lowerLeg directly to yHeight==1, because the SMPL-X lowerLeg we get in T-Pose IS SLANTED, not completely "vertical," EVEN WHEN the pose is the "canonical T-Pose"
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  # NOTE NOTE NOTE NOTE NOTE
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
  #===================================================================================================
