  #===============================================================
  #  Old Code from func   "getResizedLeftSMPLX_LowerLeg(...)"  :  
  #     -August 31, 2020
  #===============================================================
  '''
  leftLegAnkleToCalfCenteredOnOrigin = scaleLegLinearlyWithYHeight(
    leftLowerLegVertsCenteredOnOrigin, yHeightValueAtKneeWithSMPLX_BodyNormalizedTo1, yHeightValueAtAnkleWithSMPLX_BodyNormalizedTo1, TimsRealCalfXWidthInches, TimsRealAnkleXWidthInches, TimsRealCalfZDepthInches, TimsRealAnkleZDepthInches)   # FIXME:     there's a lot of crap in here that should be changed.     -nxb on August 28, 2020      at 1:15 P.M. EDT
  '''
    # as of August 31, 2020,   this line did NOTHING.  Because leftLegAnkleToCalfCenteredOnOrigin is NEVER reincorporated back into the main "verts" that are "`pyrender.show(...)`n" to the coder .    -nxb

    # TODO:  work backward from this function call.   (joints['ankleHeightY'] and/or vertices['calf'] )     -nxb, August 27, 2020
  """
  leftLowerLegVertsCenteredOnOrigin = scaleLegLinearlyWithYHeight(
    leftLowerLegVertsCenteredOnOrigin, yTop, yBot, xWidthAtTopYHeight_RealCustomerInches, xWidthAtBotYHeight_RealCustomerInches, zDepthAtTopYHeight_RealCustomerInches, zDepthAtBotYHeight_RealCustomerInches ) # TODO TODO TODO TODO TODO
  """
    # NOTE:  why did I want the function "scaleLegLinearlyWithYHeight" to spit out the other params?
  #====================================================================================
  # Here the lowerLeg is normally proportioned again because we're using the customer's **__ACTUAL__**   Depth, Width, and Height.     
  #   -nxb, August 17, 2020
  #====================================================================================
  #leftLowerLegVertsCenteredOnOriginScaledToRealLowerLegLenInches = leftLowerLegVertsCenteredOnOriginNormalizedTo1 * customerEstimatedLowerLegLenInches
  #leftLowerLegVertsCenteredOnOrigin *= customerEstimatedLowerLegLenInches
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 





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
                                             # from func "main()" in examples/nxb_demo.py :
                                             #resizedLeftSMPLX_Leg(vertices, customerEstimatedLowerLegLenInches,                                customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, TIM_LOWER_LEG_WIDTH_AKA_X_INCHES, TIM_LOWER_LEG_DEPTH_AKA_Z_INCHES):    # we don't have this customerEstimatedLowerLegLenInches, 
    """

    # also from "main()" in "examples/nxb_demo.py"
    # TODO:     leftUpperLegParams  for merging UpperLegs with lowerLegs        (in "`getResizedLeftSMPLX_UpperLeg(... , ... , ... )`")
    resizedLeftUpperLegVerts, leftUpperLegIdxes, leftUpperLegParams = getResizedLeftSMPLX_UpperLeg(vertices, TIM_LOWER_LEG_LENGTH_INCHES_____ESTIMATED_AND_CALCULATED_BY_NATHAN, TIM_SELF_REPORTED_HEIGHT_INCHES, TIM_ANKLE_WIDTH_AKA_X_INCHES, TIM_ANKLE_DEPTH_AKA_Z_INCHES, NXB_LOWER_LEG_WIDTH_AKA_X_INCHES, NXB_LOWER_LEG_DEPTH_AKA_Z_INCHES)
    #getResizedLeftSMPLX_UpperLeg(vertices, customerEstimatedUpperLegLenInches,                                customerEstimatedHeightInches, prevBodyPartsXStretchingSlashScaling, prevBodyPartsZStretchingSlashScaling, TIM_UpperLeg_WIDTH_AKA_X_INCHES, TIM_UpperLeg_DEPTH_AKA_Z_INCHES):    # we don't have this customerEstimatedUpperLegLenInches, 
    vertsWithResizedLeftUpperLeg = deepcopy(vertices)
    vertsWithResizedLeftUpperLeg[leftUpperLegIdxes] = resizedLeftUpperLegVerts
   """
 









#==================================================
def makeLeftLeg(TODO_TODO_TODO_TODO_TODO_____params):  # from examples/nxb_demo.py; August 31, 2020
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


  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 
  #       TODO:  find the exact right vertex (multiple vertic(es), ESPECIALLY when the WHOLE BODY comes into play)  in SMPL-X that will let us scale the lowerLeg correctly 


  """
def scaleLegLinearlyWithYHeight(...):
  August 31, 2020
  """
    #  NOTE: The correct, well-thought-through lines are below.   -nxb, August 27, 2020
    #currsHeight = yVal - yBot        # NOTE: I read these lines again, and I'm PRETTY sure I don't need them to get the right answer.     -nxb, August 27, 2020
    #height - currsHeight / height    # NOTE: I read these lines again, and I'm PRETTY sure I don't need them to get the right answer.     -nxb, August 27, 2020
    #  NOTE: The correct, well-thought-through lines are below.   -nxb, August 27, 2020









  """
  # from "main(...)" in nxb_demo.py   (-nxb;     August 31, 2020)
    """
      NXB's lowerLeg (measured with a real measuring tape) is roughly 
        18 inches, 
          and my calculation says 
        17.89 inches for Tim Schrader's lowerLeg.  
      So my calculation is is probably MOSTLY correct.    
    """
    #    -nxb;   on August 14, 2020      (more technically, 8:19 P.M. EDT    on August 14, 2020)
