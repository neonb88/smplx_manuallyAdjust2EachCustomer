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
JOINT_NAMES = [                                 
    'pelvis',                                #  1            (1-indexed)
    'left_hip',                              #  2              
    'right_hip',                             #  3               
    'spine1',                                #  4            
    'left_knee',                             #  5               
    'right_knee',                            #  6                
    'spine2',                                #  7            
    'left_ankle',                            #  8                
    'right_ankle',                           #  9                 
    'spine3',                                #  10           
    'left_foot',                             #  11           (1-indexed)                
    'right_foot',                            #  12               
    'neck',                                  #  13         
    'left_collar',                           #  14                
    'right_collar',                          #  15                 
    'head',                                  #  16         
    'left_shoulder',                         #  17                  
    'right_shoulder',                        #  18                   
    'left_elbow',                            #  19               
    'right_elbow',                           #  20                
    'left_wrist',                            #  21           (1-indexed)                 
    'right_wrist',                           #  22                
    'jaw',                                   #  23        
    'left_eye_smplhf',                       #  24                    
    'right_eye_smplhf',                      #  25                     
    'left_index1',                           #  26                
    'left_index2',                           #  27                
    'left_index3',                           #  28                
    'left_middle1',                          #  29                 
    'left_middle2',                          #  30                 
    'left_middle3',                          #  31           (1-indexed)                   
    'left_pinky1',                           #  32                
    'left_pinky2',                           #  33                
    'left_pinky3',                           #  34                
    'left_ring1',                            #  35               
    'left_ring2',                            #  36               
    'left_ring3',                            #  37               
    'left_thumb1',                           #  38                
    'left_thumb2',                           #  39                
    'left_thumb3',                           #  40                
    'right_index1',                          #  41           (1-indexed)                   
    'right_index2',                          #  42                 
    'right_index3',                          #  43                 
    'right_middle1',                         #  44                  
    'right_middle2',                         #  45                  
    'right_middle3',                         #  46                  
    'right_pinky1',                          #  47                 
    'right_pinky2',                          #  48                 
    'right_pinky3',                          #  49                 
    'right_ring1',                           #  50                
    'right_ring2',                           #  51           (1-indexed)                  
    'right_ring3',                           #  52                
    'right_thumb1',                          #  53                 
    'right_thumb2',                          #  54                 
    'right_thumb3',                          #  55                 
    'nose',                                  #  56         
    'right_eye',                             #  57              
    'left_eye',                              #  58             
    'right_ear',                             #  59              
    'left_ear',                              #  60             
    'left_big_toe',                          #  61           (1-indexed)                   
    'left_small_toe',                        #  62                   
    'left_heel',                             #  63              
    'right_big_toe',                         #  64                  
    'right_small_toe',                       #  65                    
    'right_heel',                            #  66               
    'left_thumb',                            #  67               
    'left_index',                            #  68               
    'left_middle',                           #  69                
    'left_ring',                             #  70              
    'left_pinky',                            #  71           (1-indexed)                 
    'right_thumb',                           #  72                
    'right_index',                           #  73                
    'right_middle',                          #  74                 
    'right_ring',                            #  75               
    'right_pinky',                           #  76                
    'right_eye_brow1',                       #  77                    
    'right_eye_brow2',                       #  78                    
    'right_eye_brow3',                       #  79                    
    'right_eye_brow4',                       #  80                    
    'right_eye_brow5',                       #  81           (1-indexed)                      
    'left_eye_brow5',                        #  82                   
    'left_eye_brow4',                        #  83                   
    'left_eye_brow3',                        #  84                   
    'left_eye_brow2',                        #  85                   
    'left_eye_brow1',                        #  86                   
    'nose1',                                 #  87          
    'nose2',                                 #  88          
    'nose3',                                 #  89          
    'nose4',                                 #  90          
    'right_nose_2',                          #  91           (1-indexed)                   
    'right_nose_1',                          #  92                 
    'nose_middle',                           #  93                
    'left_nose_1',                           #  94                
    'left_nose_2',                           #  95                
    'right_eye1',                            #  96               
    'right_eye2',                            #  97               
    'right_eye3',                            #  98               
    'right_eye4',                            #  99               
    'right_eye5',                            #  100              
    'right_eye6',                            #  101          (1-indexed)                 
    'left_eye4',                             #  102             
    'left_eye3',                             #  103             
    'left_eye2',                             #  104             
    'left_eye1',                             #  105             
    'left_eye6',                             #  106             
    'left_eye5',                             #  107             
    'right_mouth_1',                         #  108                 
    'right_mouth_2',                         #  109                 
    'right_mouth_3',                         #  110                 
    'mouth_top',                             #  111          (1-indexed)                
    'left_mouth_3',                          #  112                
    'left_mouth_2',                          #  113                
    'left_mouth_1',                          #  114                
    'left_mouth_5',  # 59 in OpenPose output #  115                                             
    'left_mouth_4',  # 58 in OpenPose output #  116                                         
    'mouth_bottom',                          #  117                
    'right_mouth_4',                         #  118                 
    'right_mouth_5',                         #  119                 
    'right_lip_1',                           #  120               
    'right_lip_2',                           #  121          (1-indexed)                  
    'lip_top',                               #  122           
    'left_lip_2',                            #  123              
    'left_lip_1',                            #  124              
    'left_lip_3',                            #  125              
    'lip_bottom',                            #  126              
    'right_lip_3',                           #  127               
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




