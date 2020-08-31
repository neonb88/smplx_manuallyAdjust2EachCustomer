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
