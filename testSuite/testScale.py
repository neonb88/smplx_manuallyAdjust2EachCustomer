import os.path as osp
import argparse

import numpy as np
import torch

import smplx

#=====================================================
# imports   added by nxb, August 13, 2020   :
import datetime # added by nxb, August 13, 2020
from copy import deepcopy # Aug 14, 2020

# pe and pn:
#from utils import pe, pn # Aug 18, 2020
def pn(n=0):  print('\n'*n) # Aug 18, 2020
def pe(n=89): print('='*n) # Aug 18, 2020
#=====================================================





#=====================================================
def unitLeg(faceIndexingStyle='numpy'):
  '''
    This leg goes straight "up"   (y direction)

    @since August 31, 2020

    @param faceIndexingStyle
      The .obj files'  indexing convention is 1-based (starts at 1, goes to n)
      The numpy faces' indexing convention is 0-based (starts at 0, goes to n-1)
      More formats can be added here and in the code.   -nxb, August 31, 2020


  '''
  # 12 vertices because     this "leg" has 3 heights, and this oversimplified "leg" is 2 rectangular prisms on top of each other.    -nxb, August 31, 2020
  verts = np.array(  # 12 verts
     [[  1,  0,  1],
      [  1,  0, -1],
      [ -1,  0, -1],
      [ -1,  0,  1],
      [  1,  1,  1],
      [  1,  1, -1],
      [ -1,  1, -1],
      [ -1,  1,  1],
      [  1,  2,  1],
      [  1,  2, -1],
      [ -1,  2, -1],
      [ -1,  2,  1]])
  # end verts
  faces_1_based = np.array(   # 20 faces
     [[  1,  2,  4],
      [  2,  3,  4],
      [  1,  2,  5],
      [  2,  5,  6],
      [  1,  4,  5],
      [  4,  5,  8],
      [  4,  7,  8],
      [  3,  4,  7],
      [  2,  3,  7],
      [  2,  6,  7],
      [  9, 10, 12],
      [ 10, 11, 12],
      [  6,  9, 10],
      [  5,  6,  9],
      [  5,  8,  9],
      [  8,  9, 12],
      [  8, 11, 12],
      [  7,  8, 11],
      [  6,  7, 11],
      [  6, 10, 11]])
  if faceIndexingStyle.lower()=='.obj':
    convention='1-based'
    return verts, faces_1_based
  elif faceIndexingStyle.lower()=='numpy':
    convention='0-based'
    return verts, faces_1_based-1

#=====================================================
#            end func def of "unitLeg():"             
#=====================================================
#                  August 31, 2020                    
#=====================================================





#=====================================================
def testScale():
  from examples.nxb_demo import scaleLegLinearlyWithYHeight
  platonicUnitLeg, faces = unitLeg()
  verts, yTop, yBot, xWidthTop, xWidthBot, zDepthTop, zDepthBot = platonicUnitLeg, 2, 0, 4, 2, 4, 2
  scaledLegVs = scaleLegLinearlyWithYHeight( verts, yTop, yBot, xWidthTop, xWidthBot, zDepthTop, zDepthBot  )
  pn(2)
  pe(99)
  print("scaledLegVs:")
  print(scaledLegVs)
  pe(99)
  pn(2)
  from smplx.utils import pyrenderShow
  pyrenderShow(scaledLegVs, faces)
#=====================================================
#            end func def of "testScale()"            
#=====================================================
#                   August 31, 2020                   
#=====================================================






  
if __name__=="__main__":
  testScale()
