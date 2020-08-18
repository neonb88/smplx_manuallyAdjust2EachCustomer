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

# NOTE:   numbering is later
JOINT_NAMES = [#                             # Index:        (1-indexed)             #  `print(joints)` :           These are the value(s) of "joints"

    'pelvis',                                #  1            (1-indexed)                array([[ 0.00116772, -0.36684087,  0.01266907],                    
    'left_hip',                              #  2                                              [ 0.05731141, -0.46138254, -0.01080547],
    'right_hip',                             #  3                                              [-0.05670194, -0.47200772, -0.00388976],
    'spine1',                                #  4                                              [-0.00016842, -0.2564241 , -0.02525561],
    'left_knee',                             #  5                                              [ 0.12454055, -0.8582508 , -0.01745984],
    'right_knee',                            #  6                                              [-0.10742874, -0.8518289 , -0.01834137],
    'spine2',                                #  7                                              [ 0.01004082, -0.10545279, -0.02081327],
    'left_ankle',                            #  8                                              [ 0.07894664, -1.2795366 , -0.05860627],
    'right_ankle',                           #  9                                              [-0.09027385, -1.2867409 , -0.05827895],
    'spine3',                                #  10                                             [ 0.00104884, -0.04760592,  0.00185643],
    'left_foot',                             #  11           (1-indexed)                       [ 0.12325553, -1.3402723 ,  0.07655036],
    'right_foot',                            #  12                                             [-0.12571798, -1.3464106 ,  0.0835339 ],
    'neck',                                  #  13                                             [-0.00853356,  0.11841501, -0.02538398],
    'left_collar',                           #  14                                             [ 0.04347587,  0.02865977, -0.00340382],
    'right_collar',                          #  15                                             [-0.04502762,  0.02920222, -0.00667483],
    'head',                                  #  16                                             [ 0.01442313,  0.2791165 , -0.00232656],
    'left_shoulder',                         #  17                                             [ 0.1844151 ,  0.08908834, -0.01829752],
    'right_shoulder',                        #  18                                             [-0.17538337,  0.08805959, -0.01925886],
    'left_elbow',                            #  19                                             [ 0.4391638 ,  0.01292275, -0.06378978],
    'right_elbow',                           #  20                                             [-0.44787604,  0.04213398, -0.0516878 ],
    'left_wrist',                            #  21           (1-indexed)                       [ 0.7107678 ,  0.03853584, -0.0644381 ],                 
    'right_wrist',                           #  22                                             [-0.7112553 ,  0.04216266, -0.06351002],
    'jaw',                                   #  23                                             [-0.00630535,  0.2782753 , -0.00878998],
    'left_eye_smplhf',                       #  24                                             [ 0.03225888,  0.32489878,  0.06343991],
    'right_eye_smplhf',                      #  25                                             [-0.03226476,  0.32470605,  0.06339288],
    'left_index1',                           #  26                                             [ 0.81685436,  0.02995025, -0.04338149],
    'left_index2',                           #  27                                             [ 0.8480469 ,  0.0176394 , -0.04173926],
    'left_index3',                           #  28                                             [ 0.8546191 , -0.0049023 , -0.04458815],
    'left_middle1',                          #  29                                             [ 0.82498777,  0.0326842 , -0.06839874],
    'left_middle2',                          #  30                                             [ 0.85230005,  0.01646511, -0.07343797],
    'left_middle3',                          #  31           (1-indexed)                       [ 0.8570515 , -0.00787745, -0.0754675 ],                   
    'left_pinky1',                           #  32                                             [ 0.7989061 ,  0.02378787, -0.110934  ],
    'left_pinky2',                           #  33                                             [ 0.8118816 ,  0.00809699, -0.11565237],
    'left_pinky3',                           #  34                                             [ 0.81581193, -0.01166782, -0.11475545],
    'left_ring1',                            #  35                                             [ 0.81268597,  0.02958735, -0.09338035],
    'left_ring2',                            #  36                                             [ 0.83696777,  0.01198877, -0.09480331],
    'left_ring3',                            #  37                                             [ 0.84078133, -0.01267097, -0.09318233],
    'left_thumb1',                           #  38                                             [ 0.7524941 ,  0.01845882, -0.03673416],
    'left_thumb2',                           #  39                                             [ 0.7748769 , -0.00035203, -0.02307999],
    'left_thumb3',                           #  40                                             [ 0.7997036 , -0.00880825, -0.0151321 ],
    'right_index1',                          #  41           (1-indexed)                       [-0.81685334,  0.02995217, -0.04337915],                   
    'right_index2',                          #  42                                             [-0.84804606,  0.01764117, -0.04173668],
    'right_index3',                          #  43                                             [-0.8546183 , -0.00490108, -0.04458622],
    'right_middle1',                         #  44                                             [-0.8249879 ,  0.03268575, -0.06839859],
    'right_middle2',                         #  45                                             [-0.8522992 ,  0.01646494, -0.0734385 ],
    'right_middle3',                         #  46                                             [-0.85705036, -0.00787747, -0.07546893],
    'right_pinky1',                          #  47                                             [-0.79890877,  0.02378785, -0.11093456],
    'right_pinky2',                          #  48                                             [-0.81188387,  0.00809763, -0.11565152],
    'right_pinky3',                          #  49                                             [-0.8158137 , -0.01166702, -0.1147549 ],
    'right_ring1',                           #  50                                             [-0.81268746,  0.02958889, -0.09338124],
    'right_ring2',                           #  51           (1-indexed)                       [-0.83696854,  0.01199053, -0.09480307],                  
    'right_ring3',                           #  52                                             [-0.84078115, -0.01266952, -0.09318303],
    'right_thumb1',                          #  53                                             [-0.75249267,  0.01845726, -0.03673249],
    'right_thumb2',                          #  54                                             [-0.7748742 , -0.0003529 , -0.02307799],
    'right_thumb3',                          #  55                                             [-0.7997017 , -0.00880743, -0.01513037],
    'nose',                                  #  56                                             [ 0.0006566 ,  0.29030228,  0.11580312],
    'right_eye',                             #  57                                             [-0.03385038,  0.32513142,  0.07649847],
    'left_eye',                              #  58                                             [ 0.03536318,  0.32519063,  0.07598893],
    'right_ear',                             #  59                                             [-0.07381061,  0.28936893, -0.01582119],
    'left_ear',                              #  60                                             [ 0.07463837,  0.29583502, -0.01540159],
    'left_big_toe',                          #  61           (1-indexed)                       [ 0.08587752, -1.3413533 ,  0.15359592],                   
    'left_small_toe',                        #  62                                             [ 0.1583467 , -1.349441  ,  0.10331886],
    'left_heel',                             #  63                                             [ 0.09586649, -1.321919  , -0.11576156],
    'right_big_toe',                         #  64                                             [-0.07682333, -1.3432597 ,  0.1514249 ],
    'right_small_toe',                       #  65                                             [-0.1583503 , -1.3494366 ,  0.10331994],
    'right_heel',                            #  66                                             [-0.09758946, -1.3394969 , -0.11382397],
    'left_thumb',                            #  67                                             [ 0.8266802 , -0.03045566, -0.01105154],
    'left_index',                            #  68                                             [ 0.8600181 , -0.0305928 , -0.04570588],
    'left_middle',                           #  69                                             [ 0.85949606, -0.03635204, -0.07336563],
    'left_ring',                             #  70                                             [ 0.84094435, -0.03760117, -0.08549961],
    'left_pinky',                            #  71           (1-indexed)                       [ 0.8199115 , -0.03391033, -0.10966128],                 
    'right_thumb',                           #  72                                             [-0.82493955, -0.03068294, -0.00742552],
    'right_index',                           #  73                                             [-0.8600174 , -0.03059143, -0.04570481],
    'right_middle',                          #  74                                             [-0.8593702 , -0.0365299 , -0.07334706],
    'right_ring',                            #  75                                             [-0.8407924 , -0.03780335, -0.0854249 ],
    'right_pinky',                           #  76                                             [-0.8199128 , -0.03390878, -0.10966286],
    'right_eye_brow1',                       #  77                                             [-0.06182113,  0.32770634,  0.05248649],
    'right_eye_brow2',                       #  78                                             [-0.05296917,  0.34697205,  0.06644153],
    'right_eye_brow3',                       #  79                                             [-0.03783932,  0.35157812,  0.07931057],
    'right_eye_brow4',                       #  80                                             [-0.02212988,  0.34972033,  0.0871692 ],
    'right_eye_brow5',                       #  81           (1-indexed)                       [-0.00855262,  0.34578732,  0.08891223],                      
    'left_eye_brow5',                        #  82                                             [ 0.00831988,  0.345815  ,  0.08876309],
    'left_eye_brow4',                        #  83                                             [ 0.02196119,  0.34964168,  0.08706506],
    'left_eye_brow3',                        #  84                                             [ 0.0377771 ,  0.3504719 ,  0.07949468],
    'left_eye_brow2',                        #  85                                             [ 0.05267157,  0.34367436,  0.06817344],
    'left_eye_brow1',                        #  86                                             [ 0.06155687,  0.3243969 ,  0.05260214],
    'nose1',                                 #  87                                             [-0.00047385,  0.33051234,  0.09219323],
    'nose2',                                 #  88                                             [-0.00031342,  0.31864527,  0.10196953],
    'nose3',                                 #  89                                             [-0.00018841,  0.3091933 ,  0.11008842],
    'nose4',                                 #  90                                             [ 0.00058926,  0.29895297,  0.11753319],
    'right_nose_2',                          #  91           (1-indexed)                       [-0.0117658 ,  0.2830541 ,  0.09648105],                   
    'right_nose_1',                          #  92                                             [-0.00592393,  0.28163287,  0.10103267],
    'nose_middle',                           #  93                                             [ 0.00031996,  0.2801984 ,  0.10287758],
    'left_nose_1',                           #  94                                             [ 0.00668812,  0.28180146,  0.10075313],
    'left_nose_2',                           #  95                                             [ 0.0123584 ,  0.28339824,  0.09594519],
    'right_eye1',                            #  96                                             [-0.0459113 ,  0.32330012,  0.06695977],
    'right_eye2',                            #  97                                             [-0.03678966,  0.32792914,  0.07662641],
    'right_eye3',                            #  98                                             [-0.02648981,  0.32844818,  0.07680909],
    'right_eye4',                            #  99                                             [-0.01920179,  0.32325035,  0.07457975],
    'right_eye5',                            #  100                                            [-0.02625237,  0.32123184,  0.07576789],
    'right_eye6',                            #  101          (1-indexed)                       [-0.03630266,  0.3205297 ,  0.07480837],                 
    'left_eye4',                             #  102                                            [ 0.01882507,  0.32297194,  0.07451135],
    'left_eye3',                             #  103                                            [ 0.02656959,  0.32805052,  0.07689446],
    'left_eye2',                             #  104                                            [ 0.03645853,  0.3278576 ,  0.07596453],
    'left_eye1',                             #  105                                            [ 0.04574738,  0.32314748,  0.06694173],
    'left_eye6',                             #  106                                            [ 0.0366473 ,  0.32021618,  0.07481501],
    'left_eye5',                             #  107                                            [ 0.02630929,  0.32080936,  0.07585728],
    'right_mouth_1',                         #  108                                            [-0.0212661 ,  0.25436354,  0.09208693],
    'right_mouth_2',                         #  109                                            [-0.01475739,  0.26075074,  0.10138992],
    'right_mouth_3',                         #  110                                            [-0.00547952,  0.26434356,  0.106158  ],
    'mouth_top',                             #  111          (1-indexed)                       [ 0.00048655,  0.26377833,  0.10673463],
    'left_mouth_3',                          #  112                                            [ 0.00640037,  0.26481107,  0.10602536],
    'left_mouth_2',                          #  113                                            [ 0.01533341,  0.26189837,  0.10082529],
    'left_mouth_1',                          #  114                                            [ 0.02118983,  0.25492716,  0.09127946],
    'left_mouth_5',  # 59 in OpenPose output #  115                                            [ 0.01550017,  0.25145563,  0.09695999],                        
    'left_mouth_4',  # 58 in OpenPose output #  116                                            [ 0.00579743,  0.2489883 ,  0.10280295],                    
    'mouth_bottom',                          #  117                                            [-0.0000762 ,  0.24872327,  0.10351156],
    'right_mouth_4',                         #  118                                            [-0.00592392,  0.24896303,  0.10338873],
    'right_mouth_5',                         #  119                                            [-0.0157818 ,  0.250759  ,  0.09780645],
    'right_lip_1',                           #  120                                            [-0.02091699,  0.25467443,  0.09137687],
    'right_lip_2',                           #  121          (1-indexed)                       [-0.00564775,  0.25743523,  0.10160793],                  
    'lip_top',                               #  122                                            [ 0.00035901,  0.2574515 ,  0.1016193 ],
    'left_lip_2',                            #  123                                            [ 0.00626217,  0.25775766,  0.10144936],
    'left_lip_1',                            #  124                                            [ 0.02100792,  0.255     ,  0.09118415],
    'left_lip_3',                            #  125                                            [ 0.00635204,  0.25608876,  0.10079525],
    'lip_bottom',                            #  126                                            [-0.00017433,  0.25594825,  0.1017376 ],
    'right_lip_3',                           #  127                                            [-0.00658702,  0.2560653 ,  0.10110453]], dtype=float32)
    # Face contour
    'right_contour_1',                       #                     
    'right_contour_2',                       #                     
    'right_contour_3',                       #  130          (1-indexed)                      
    'right_contour_4',                       #                     
    'right_contour_5',                       #                     
    'right_contour_6',                       #                     
    'right_contour_7',                       #                     
    'right_contour_8',                       #  135                
    'contour_middle',                        #                    
    'left_contour_8',                        #                    
    'left_contour_7',                        #                    
    'left_contour_6',                        #                    
    'left_contour_5',                        #  140          (1-indexed)                     
    'left_contour_4',                        #                    
    'left_contour_3',                        #                    
    'left_contour_2',                        #                    
    'left_contour_1',                        #  144          (1-indexed)
]

#============================================ BLANK LINES =============================================
































































































































































































































































