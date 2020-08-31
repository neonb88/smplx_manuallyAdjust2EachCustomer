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
