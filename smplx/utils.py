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

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np
import torch


def to_tensor(array, dtype=torch.float32):
    if 'torch.tensor' not in str(type(array)):
        return torch.tensor(array, dtype=dtype)


class Struct(object):
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def to_np(array, dtype=np.float32):
    if 'scipy.sparse' in str(type(array)):
        array = array.todense()
    return np.array(array, dtype=dtype)


def rot_mat_to_euler(rot_mats):
    # Calculates rotation matrix to euler angles
    # Careful for extreme cases of eular angles like [0.0, pi, 0.0]

    sy = torch.sqrt(rot_mats[:, 0, 0] * rot_mats[:, 0, 0] +
                    rot_mats[:, 1, 0] * rot_mats[:, 1, 0])
    return torch.atan2(-rot_mats[:, 2, 0], sy)

#===================================================================================================
#                           After this point, it's all NXB's code.
#                                  -nxb, August 31, 2020
#===================================================================================================
def pyrenderShow(verts, faces):
    import pyrender
    import trimesh
    import trimesh.exchange.obj #  Added by nxb on   August 13, 2020
    vertex_colors = np.ones([verts.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8] # gray
    print("verts.shape:")
    print(verts.shape)
    print("faces.shape:")
    print(faces.shape)
    resizedTrimesh =  trimesh.Trimesh(verts, faces, vertex_colors=vertex_colors)
    mesh = pyrender.Mesh.from_trimesh(resizedTrimesh)
    scene = pyrender.Scene()
    scene.add(mesh)
    pyrender.Viewer(scene, use_raymond_lighting=True)

#==================================================
def filterVertsBtwn(verts, min_, max_, axis='y'):
  '''
    @since: August 31, 2020
    @param verts
    @param min_
    @param max_
    @param axis
    @returns   The indices and actual vertices from @param "verts" that are greater than @param "min_" and less than @param "max_" along the axis @param "axis"
  '''

  X,Y,Z = 0,1,2

  #=======================================================================================
  # NOTE: the variable named "`whichColumn`" refers to "which column in the numpy array?"
  #   Not a spatial "column" related to the body or an anatomical location within SMPL-X
  #=======================================================================================
  if axis.lower()=='x':
    whichColumn = X
  if axis.lower()=='y':
    whichColumn = Y
  if axis.lower()=='z':
    whichColumn = Z


  belowMaxIdxs = np.where(   
    np.less(verts[:,whichColumn],   
            max_))[0]
  aboveMinIdxs = np.where(   
    np.greater(verts[:,whichColumn],   
            min_))[0]   
  pPrintVarNXB("belowMaxIdxs: ", belowMaxIdxs)
  pPrintVarNXB("aboveMinIdxs: ", aboveMinIdxs)
  # NOTE: above, "0" is just which element of the output of 
  #   "`np.where(...)`"  the indices are in.  
  #   The output of np.where() is a tuple.
  desiredsIdxs = np.intersect1d( belowMaxIdxs, aboveMinIdxs )
  return desiredsIdxs, verts[desiredsIdxs]
# TODO:   test this func ("filterVertsBtwn")


#==================================================
#            end func "filterVertsBtwn"
#==================================================
#                 August 31, 2020
#==================================================








def pn(n=0):  print('\n'*n) # Aug 18, 2020
def pe(n=89): print('='*n)  # Aug 18, 2020
def pPrintVarNXB(var, varName, nNewlines=2, nEquals=99):
    pn(nNewlines)
    pe(nEquals)
    #print("m: ")
    print(varName)
    print(var)
    pe(nEquals)
    pn(nNewlines)
  
