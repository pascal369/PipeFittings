# -*- coding: utf-8 -*-

import os
import sys
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import ParamPvcPFit
DEBUG = True # set to True to show debug messages

lst=['00_TS','01_DV',]
kanzai_ts=['Straight Pipe','Elbow','Socket','Tee','Flange',]
kanzai_ts2=['直管','エルボ','ソケット','チーズ','フランジ']
kanzai_dv=['Straight Pipe','Elbow','Socket','Y90','Flange','Damper']
kanzai_dv2=['直管','エルボ','ソケット','チーズ','フランジ','ダンパー']
pvc_d=['13','16','20','25','30','40','50','65','75','100','125','150','200','250','300','350','400','450','500']
flg_d=['13','16','20','25','30','40','50','65','75','100','125','150','200','250','300',]
flg_d2=['13','16','20','25','32','40','50','65','80','100','125','150','200','250',
'300','350','400','450','500','600','700','800','900','1000'
]
ts_dsoc_d=[
'16x13','20x13','20x16','25x13','25x16','25x20','30x20','30x25','40x20',
'40x25','40x30','50x20','50x25','50x30','16x13','50x40']
dv_dsoc_d=[
'50x40','65x50','75x50','75x65','100x50','100x65','100x75','125x100',
'150x100','150x125','200x150','250x200','300x250',
]
ts_dtee_d=[
'16x13','20x13','20x16','25x13','25x16','25x20','30x13','30x16','30x20','30x25',
'40x13','40x16','40x20','40x25','40x30','50x13','50x16','50x20','50x25','50x30','50x40'
]

dv_d90Y_d=[
'75x50','75x65','100x50','100x75','150x100','200x100','200x125','200x150',
'250x150','250x200','300x200'
]
pipe_st=[
'VP ','VU ','VPW','VP _Both_flange_5k','VU _Both_flange_5k','VPW_Both_flange_5k',
'VP _Both_flange_10k','VU _Both_flange_10k','VPW_Both_flange_10k',
'VP _Single_flange_5k','VU _Single_flange_5k','VPW_Single_flange_5k',
'VP _Single_flange_10k','VU _Single_flange_10k','VPW_Single_flange_10k',
]
elbow_st=['90','45',]
socket_st=['Socket','Increaser','Valve']
Y90_st=['Same_dia','Difference_dia']
tee_st=['Same_dia','Difference_dia']
flg_st=['JIS5k_socket','JIS10k_socket','JIS5k','JIS10k','JIS5k_lid','JIS10k_lid']
damper_st=['VD_A','VD_B','VD_C_5k','VD_C_10k']

#直管
#口径,外径,硬質塩化ﾋﾞﾆﾙ管,,,,水道用硬質塩化ﾋﾞﾆﾙ管VPW
#,,          VP,          VU,          VPW
#,,     D,   t,    W,     t,    W,     t,   W(kg/m)
strt_dia={
'13':(  18,  2.2,  0.174, 0,    0,     2.5, 0.174),
'16':(  22,  2.7,  0.256, 0,    0,     0,   0),
'20':(  26,  2.7,  0.310, 0,    0,     3.0, 0),
'25':(  32,  3.1,  0.448, 0,    0,     3.5, 0),
'30':(  38,  3.1,  0.542, 0,    0,     3.5, 0),
'40':(  48,  3.6,  0.791, 1.8,  0.413, 4.0, 0.791),
'50':(  60,  4.1,  1.122, 1.8,  0.521, 4.5, 1.122),
'65':(  76,  4.1,  1.445, 2.2,  0.825, 4.5, 1.445),
'75':(  89,  5.5,  2.202, 2.7,  1.159, 5.9, 2.202),
'100':(114,  6.6,  3.409, 3.1,  1.737, 7.1, 3.409),
'125':(140,  7.0,  4.464, 4.1,  2.739, 7.5, 4.464),
'150':(165,  8.9,  6.701, 5.1,  3.941, 9.6, 6.701),
'200':(216, 10.3, 10.129, 6.5,  6.572, 0,   0),
'250':(267, 12.7, 15.481, 7.8,  9.758, 0,   0),
'300':(318, 15.1, 21.962, 9.2, 13.701, 0,   0),
'350':(370,  0,    0,    10.5, 18.051, 0,   0),
'400':(420,  0,    0,    11.8, 23.059, 0,   0),
'450':(470,  0,    0,    13.2, 28.875, 0,   0),
'500':(520,  0,    0,    14.6, 35.346, 0,   0),
}

#管用ねじ
#                                 基準径(おねじ)             基準径の位置  めねじ    おねじ
#                  山の高さ  　丸み　　外径　　 　有効径   谷径     管端から      部の長さ　　部の長さ    肉厚    めねじ部 　おねじ部
#        ピッチP,     h,      r,    D0,     d2,     d1,      a,         l',     l,        t,      A1,   　  A2,      A3,    f
screws={
'10':(  1.3368, 0.856,   0.18, 16.662, 15.806, 14.950,  6.35,       9,    12,         2.2,    23,     14,       17,     3.7),
'13':(  1.8143, 1.162,   0.25, 20.955, 19.793, 18.631,  8.16,      11,    15,         2.5,    27,     18,       22,     5.0),
'16':(  1.8143, 1.162,   0.25, 20.955, 19.793, 18.631,  8.16,      11,    15,         2.5,    27,     18,       22,     5.0),
'20':(  1.8143, 1.162,   0.25, 26.441, 25.279, 24.117,  9.53,      13,    17,         3.0,    33,     24,       27,     5.0),
'25':(  2.3091, 1.479,   0.32, 33.249, 31.770, 30.291, 10.39,      15,    19,         3.0,    41,     30,       34,     6.4),
'30':(  2.3091, 1.479,   0.32, 41.910, 40.431, 38.952, 12.70,      17,    22,         3.5,    50,     39,       43,     6.4),
'40':(  2.3091, 1.479,   0.32, 47.803, 46.324, 44.845, 12.70,      18,    22,         3.5,    56,     44,       49,     6.4),
'50':(  2.3091, 1.479,   0.32, 59.614, 58.135, 56.656, 15.88,      20,    26,         4.0,    69,     56,       61,     7.5),
}

#エルボ
#ｴﾙﾎﾞ
#JIS K 6743
#口径,外径,L90, L45
elbow_ts={
'13':(18,36,33),
'20':(26,50,44),
'25':(32,58,51),
'30':(38,65,56),
'40':(48,82,69),
'50':(60,96,80),
'65':(76,110,0),
'75':(89,120,0),
'100':(114,153,0),
'125':(140,192,0),
'150':(165,230,0),
}

#DVｴﾙﾎﾞ
#JIS K 6743
#口径, 外径,  L90, L45
elbow_dv={
'40':(  48,  49,  36),
'50':(  60,  58,  43),
'65':(  76,  77,  57),
'75':(  89,  88,  65),
'100':(114, 112,  80),
'125':(140, 140, 103),
'150':(165, 168, 124),
'200':(165, 225, 166),
'250':(165, 271, 198),
'300':(165, 318, 228),
}

#TS接合部
#JIS K 6743                                  TSソケット
#口径,外径D1, d1,    T,   l,   d,   D,    t,   L
pvc_ts={
'13':(  18,  18.4,  30,  26,  13,  24,   3.0, 57),
'16':(  22,  22.4,  34,  30,  16,  29,   3.5, 67),
'20':(  26,  26.45, 34,  35,  20,  33,   3.5, 77),
'25':(  32,  32.55, 34,  40,  25,  40,   4.0, 87),
'30':(  38,  38.60, 34,  44,  31,  46,   4.0, 95),
'40':(  48,  48.70, 37,  55,  40,  57,   4.5,117),
'50':(  60,  60.80, 37,  63,  51,  70,   5.0,133),
'65':(  76,  76.60, 47,  61,  67,  87,   6.6,145),
'75':(  89,  89.60, 49,  64,  77, 102,   8.0,155),
'100':(114, 114.70, 56,  84, 100, 130,  10.0,200),
'125':(140, 140.85, 58, 104, 125, 157,  11.0,240),
'150':(165, 166.00, 63, 132, 146, 186,  13.0,300),
}

#DV接合部
#JIS K 6743                                         DVソケット
#口径,外径D1, d1,     d2,     l,   d,     D,   t,    L
pvc_dv={
'40':(  48,  48.30,  47.8,   22,  40.0,  54,  2.7,  47),
'50':(  60,  60.35,  59.5,   25,  51.0,  67,  2.7,  53),
'65':(  76,  76.40,  75.4,   35,  67.0,  83,  3.1,  73),
'75':(  89,  89.45,  88.3,   40,  77.2,  97,  3.1,  84),
'100':(114, 114.55, 113.2,   50,  98.8, 124,  3.6, 104),
'125':(140, 140.70, 139.1,   65, 125.0, 151,  4.5, 134),
'150':(165, 165.85, 163.9,   80, 145.8, 178,  5.4, 164),
'200':(216, 217.30, 214.7,  110, 205.0, 230,  5.5, 225),
'250':(267, 268.55, 265.45, 130, 255.0, 280,  6.0, 266),
'300':(318, 319.75, 316.25, 150, 303.6, 330,  7.2, 307),
}

#TSバルブソケット
#       L,    E,    n,   B, W
valve_s_d ={
'10':(  43,   13,   6,  21, 6),
'13':(  50,   16,   6,  24, 6),
'16':(  54,   16,   6,  29, 6),
'20':(  64,   18,   6,  33, 8),
'25':(  71,   20,   6,  40, 8),
'30':(  80,   22,   6,  46,10),
'40':(  92,   23,   6,  57,10),
'50':( 106,   25,   8,  70,12),
}

#ニップル
#        L,    E,    n,   B,  dk
nipples ={
'10':(  36,   13,   6,   21, 19.0),
'13':(  42,   16,   6,   24, 25.0),
'16':(  42,   16,   6,   29, 25.0),
'20':(  47,   18,   6,   33, 31.0),
'25':(  52,   20,   6,   40, 37.5),
'30':(  56,   22,   6,   46, 44.5),
'40':(  60,   23,   6,   57, 52.0),
'50':(  66,   26.5,   8,   70, 60.0),
}

#TSインクリーザ
#        D, D1,L
ts_dsoc={
'16x13':(29,24,61),
'20x13':(33,24,68),
'20x16':(33,29,71),
'25x13':(40,24,86),
'25x16':(40,29,85),
'25x20':(40,33,84),
'30x20':(46,33,93),
'30x25':(46,40,93),
'40x20':(57,33,113),
'40x25':(57,40,114),
'40x30':(57,46,114),
'50x20':(70,33,116),
'50x25':(70,40,140),
'50x30':(70,46,136),
'50x40':(70,57,136),
}

#DVインクリーザ
#           D,   D1,  L
dv_dsoc={
'50x40':(   67,  54,  67),
'65x50':(   83,  67,  80),
'75x50':(   97,  67,  90),
'75x65':(   97,  83, 100),
'100x50':( 124,  67, 105),
'100x65':( 124,  83, 115),
'100x75':( 124,  97, 120),
'125x100':(151, 124, 150),
'150x100':(178, 124, 170),
'150x125':(178, 151, 185),
'200x150':(240, 188, 356),
'250x200':(292, 240, 380),
'300x250':(347, 295, 405),
}

#ﾁｰｽﾞ
#口径, H,  I,  D
ts_tee={
'13':(36, 36, 24),
'16':(43, 43, 29),
'20':(50, 50, 33),
'25':(58, 58, 40),
'30':(65, 65, 46),
'40':(82, 82, 57),
'50':(96, 96, 70),
}

#ダンパーA パイプ式
#口径,   A,    B,    L,  t
dv_dapA={
'50':(  60,   51.0, 150, 3),
'65':(  76,   67.0, 150, 3),
'75':(  89,   83.0, 200, 3),
'100':(114,  107.8, 210, 3),
'125':(140,  131.8, 240, 3),
'150':(165,  154.8, 270, 3),
'200':(216,  203.0, 330, 3),
'250':(267,  251.4, 368, 4),
'300':(318,  299.6, 406, 4),
}

#ダンパーB ソケット式
#口径,   A,    B,    L,  t
dv_dapB={
'50':(  60,   51.0, 125, 3),
'65':(  76,   67.0, 168, 3),
'75':(  89,   83.0, 226, 3),
'100':(114,  107.8, 245, 3),
'125':(140,  131.8, 260, 3),
'150':(165,  154.8, 310, 3),
'200':(216,  203.0, 420, 3),
'250':(267,  251.4, 508, 4),
'300':(318,  299.6, 596, 4),
}

#90Y
#口径,  z1,  z2, z3,   L1,  L2,  L3
dv_90Y={
'50':(  34,  34, 34,   59,  59,  59),
'65':(  42,  43, 42,   77,  78,  77),
'75':(  48,  49, 48,   88,  89,  88),
'100':( 62,  63, 62,  112, 113, 112),
'125':( 75,  76, 75,  140, 141, 140),
'150':( 89,  90, 89,  169, 170, 169),
'200':(115, 116, 115, 225, 226, 225),
'250':(141, 144, 141, 271, 274, 271),
'300':(168, 171, 168, 318, 321, 318),
}

#径違い90Y
#口径,      z1,  z2, z3,   L1,  L2,  L3
dv_d90Y={
'75x50':(   34,  35, 48,   74,  75,  73),
'75x65':(   42,  43, 48,   82,  83,  83),
'100x50':(  34,  35, 62,   84,  85,  87),
'100x75':(  48,  49, 62,   98,  99, 102),
'150x100':( 62,  63, 88,  142, 143, 138),
'200x100':( 62,  63,116,  167, 168, 166),
'200x125':( 76,  73,115,  186, 183, 180),
'200x150':( 88,  88,113,  198, 198, 193),
'250x150':( 86,  94,145,  211, 219, 225),
'250x200':(116, 118,141,  241, 243, 246),
'300x200':(114, 115,165,  254, 255, 270),
}

#ﾁｰｽﾞ
#口径,    H, I,  D, D1
ts_dtee={
'16x13':(41,38, 29, 24),
'20x13':(46,40, 33, 24),
'20x16':(48,45, 33, 29),
'25x13':(51,43, 40, 24),
'25x16':(53,48, 40, 29),
'25x20':(55,53, 40, 33),
'30x13':(55,46, 46, 24),
'30x16':(57,57, 46, 29),
'30x20':(59,56, 46, 33),
'30x25':(62,61, 46, 40),
'40x13':(66,52, 57, 24),
'40x16':(68,57, 57, 29),
'40x20':(70,62, 57, 33),
'40x25':(73,67, 57, 40),
'40x30':(76,71, 57, 46),
'50x13':(74,58, 70, 24),
'50x13':(74,58, 70, 24),
'50x16':(76,63, 70, 29),
'50x20':(78,68, 70, 33),
'50x25':(81,73, 70, 40),
'50x30':(84,77, 70, 46),
'50x40':(90,88, 70, 57),
}

# JIS5k
#        D1,   C,    D,    n,    h,     t,       L
JIS5k_socket={
'13':(   24,  55,   75,	  4,	12,	9,	30),
'16':(   29,  60,   80,	  4,	12,	9,	35),
'20':(   33,  65,   85,	  4,	12,    10,	40),
'25':(   40,  75,   95,	  4,	12,    10,	45),
'30':(   46,  90,  115,	  4,	15,    12,	50),
'40':(   59,  95,  120,	  4,	15,    12,	61),
'50':(   70, 105,  130,	  4,	15,    14,	72),
'65':(   86, 130,  155,	  4,	15,    14,	 76),
'75':(  101, 145,  180,	  8,	19,    14,	 80),
'100':( 129, 165,  200,	  8,	19,    16,	105),
'125':( 156, 200,  235,	  8,	19,    16,	126),
'150':( 185, 230,  265,	  8,	19,    18,	150),
'200':( 238, 280,  320,	 12,	23,    28,	156),
'250':( 300, 345,  385,	 12,	23,    30,	167),
'300':( 341, 390,  430,	 12,	23,    30,	167),
}

# JIS5k                                                                               ラップジョイント
#        d0,     d2,     d4,     d5,    t,      E,       n,      a,      b,      T,      r,    R
JIS5k_2={
'13':(  17.3,	 17.8, 	 55,	 75,	 9,	12,	 4,      0,      0,      0,      0,    0),
'16':(  21.7,	 22.2, 	 60,	 80,	 9,	12,	 4,      0,      0,      0,      0,    3),
'20':(  27.2,	 27.7, 	 65,	 85,	10,	12,	 4,      0,      0,      0,      0,    3),
'25':(  34.0,	 34.5, 	 75,	 95,	10,	12,	 4,      0,      0,      0,      0,    3),
'30':(  42.7,	 43.2, 	 90,	115,	12,	15,	 4,      0,      0,      0,      0,    4),
'40':(  48.6,	 49.1, 	 95,	120,	12,	15,	 4,      0,      0,      0,      0,    4),
'50':(  60.5,	 61.1, 	105,	130,	14,	15,	 4,      0,      0,      0,      0,    4),
'65':(  76.3,	 77.1, 	130,	155,	14,	15,	 4,      0,      0,      0,      0,    5),
'80':(  89.1,	 90.0, 	145,	180,	14,	19,	 4,      0,      0,      0,      0,    5),
'100':(114.3,	115.4, 	165,	200,	16,	19,	 8,      0,      0,      0,      0,    5),
'125':(139.8,	141.2, 	200,	235,	16,	19,	 8,      0,      0,      0,      0,    6),
'150':(165.2,	166.6, 	230,	265,	18,	19,	 8,      0,      0,      0,      0,    6),
'200':(216.3,	218.0, 	280,	320,	20,	23,	 8,      0,      0,      0,      0,    6),
'250':(267.4,	269.0, 	345,	385,	22,	23,	12,      0,      0,      0,      0,    6),
'300':(318.5,	321.0, 	390,	430,	22,	23,	12,      0,      0,      0,      0,    9),
'350':(355.6,	358.1, 	435,	480,	24,	25,	12,      0,      0,      0,      0,    0),
'400':(406.4,	409.0, 	495,	540,	24,	25,	16,      0,      0,      0,      0,    0),
'450':(457.2,	460.0, 	555,	605,	24,	25,	16,      0,      0,      0,      0,    0),
'500':(508.0,	511.0, 	605,	655,	24,	25,	20,      0,      0,      0,      0,    0),
'600':(609.6,	613.0, 	715,	770,	26,	27,	20,      0,      0,      0,      0,    0),
'700':(711.2,	715.0, 	820,	875,	26,	27,	24,      0,      0,      0,      0,    0),
'800':(812.8,	817.0, 	930,	995,	28,	33,	24,      0,      0,      0,      0,    0),
'900':(914.4,	919.0, 1030,   1095,	30,	33,	24,      0,      0,      0,      0,    0),
'1000':(1016.6,1021.0, 1130,   1195,	32,	35,	28,      0,      0,      0,      0,    0),
}


# JIS10k
#        D1,   C,    D,    n,    h,     t,       L
JIS10k_socket={
'13':(   25.5,  65,   90, 4,	15,   14,	30),
'16':(   31.0,  70,   95, 4,	15,   14,	35),
'20':(   35.0,  75,  100, 4,	15,   15,	40),
'25':(   42.5,  90,  125, 4,	19,   15,	46),
'30':(   48.5, 100,  135, 4,	19,   16,	50.5),
'40':(   60.5, 105,  140, 4,	19,   16,	61.5),
'50':(   73.0, 120,  155, 4,	19,   20,	71),
'65':(   90.0, 140,  175, 4,	19,   22,       70),
'75':(  105.0, 150,  185, 8,	19,   22,	73),
'100':( 131.0, 175,  210, 8,	19,   22,	93),
'125':( 158.0, 210,  250, 8,	23,   24,      114),
'150':( 185.0, 240,  280, 8,	23,   26,      142),
'200':( 238.0, 290,  330,12,	23,   28,      156),
'250':( 300.0, 355,  400,12,	25,   30,      167),
'300':( 341.0, 400,  445,16,	25,   30,      167),
}

# JIS10k
#          d0,    d2,     d4,     d5,   t,      E,       n,        a,     b,     T,     r
JIS10k_2={
'13':(    17.3,  17.8,   65,	  90,	12,	15,	 4,        0,     0,     0,     0),
'16':(    21.7,  22.2,   70,	  95,	12,	15,	 4,        0,     0,     0,     0),
'20':(    27.2,  27.7,   75,	 100,	14,	15,	 4,        0,     0,     0,     0),
'25':(    34.0,  34.5,   90,	 125,	14,	19,	 4,        0,     0,     0,     0),
'32':(    42.7,  43.2,  100,	 135,	16,	19,	 4,        0,     0,     0,     0),
'40':(    48.6,  49.1,  105,	 140,	16,	19,	 4,        0,     0,     0,     0),
'50':(    60.5,  61.1,  120,	 155,	16,	19,	 4,        0,     0,     0,     0),
'65':(    76.3,  77.1,  140,	 175,	18,	19,	 4,        0,     0,     0,     0),
'80':(    89.1,  90.0,  150,	 185,	18,	19,	 8,        0,     0,     0,     0),
'100':(   114.3, 115.4,  175,	 210,	18,	19,	 8,        0,     0,     0,     0),
'125':(   139.8, 141.2,  210,	 250,	20,	23,	 8,        0,     0,     0,     0),
'150':(   165.2, 166.6,  240,	 280,	22,	23,	 8,        0,     0,     0,     0),
'200':(   216.3, 218.0,  290,	 330,	22,	23,	12,        0,     0,     0,     0),
'250':(   267.4, 269.0,  355,	 400,	24,	25,	12,	 288,	292,	36,	6),
'300':(   318.5, 321.0,  400,	 445,	24,	25,	16,	 340,	346,	38,	6),
'350':(   355.6, 358.1,  445,	 490,	26,	25,	16,	 380,	386,	42,	6),
'400':(   406.4, 409.0,  510,	 560,	28,	27,	16,	 436,	442,	44,	6),
'450':(   457.2, 460.0,  565,	 620,	30,	27,	20,	 496,	502,	48,	6),
'500':(   508.0, 511.0,  620,	 675,	30,	27,	20,	 548,	554,	48,	6),
'550':(   558.8, 562.0,	 680,	 745,	32,	33,	20,	 604,	610,	52,	6),
'600':(   609.6, 613.0,  730,	 795,	32,	33,	24,	 656,	662,	52,	6),
'650':(   660.4, 664.0,  780,	 845,	34,	33,	24,	 706,	712,	56,	6),
'700':(   711.2, 715.0,  840,	 905,	34,	33,	24,	 762,	770,	58,	6),
'750':(   762.0, 766.0,  900,	 970,	36,	33,	24,	 816,	824,	62,	6),
'800':(   812.8, 817.0,  950,	1020,	36,	33,	28,	 868,	876,	64,	6),
'850':(   863.6, 863.6, 1000,	1070,	36,	33,	28,	 920,	928,	66,	6),
'900':(   914.4, 919.0, 1050,	1120,	38,	33,	28,	 971,	979,	70,	6),
'1000':( 1016.0,1021.0,	1160,	1235,	40,	39,	28,	1073,	1081,	74,	6),
'1200':( 1219.2,1224.0,	1380,	1465,	44,	39,	32,	1280,	1290,	78,	6),
'1350':( 1371.6,1376.0,	1540,	1630,	48,	46,	36,	1432,	1442,	82,	6),
'1500':( 1524.0,1528.0,	1700,	1795,	50,	46,	40,	1590,	1602,	86,	6),
}


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 292)
        Dialog.move(1000, 0)
        #管種
        self.label_lst= QtGui.QLabel(Dialog)
        self.label_lst.setGeometry(QtCore.QRect(20, 0, 160, 22))
        self.label_lst.setObjectName("label_lst")
        self.comboBox_lst = QtGui.QComboBox(Dialog)
        self.comboBox_lst.setGeometry(QtCore.QRect(70, 0, 160, 22))
        self.comboBox_lst.setObjectName("comboBox_lst")

        #管材
        self.kanzai= QtGui.QLabel(Dialog)
        self.kanzai.setGeometry(QtCore.QRect(20, 23, 50, 22))
        self.kanzai.setObjectName("label_standard")
        self.comboBox_kanzai = QtGui.QComboBox(Dialog)
        self.comboBox_kanzai.setGeometry(QtCore.QRect(70, 23, 160, 22))
        self.comboBox_kanzai.setObjectName("comboBox_standard")
        self.label_l= QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(70, 45, 160, 22))
        self.label_l.setObjectName("label_l")
        #規格
        self.label_standard= QtGui.QLabel(Dialog)
        self.label_standard.setGeometry(QtCore.QRect(20, 68, 50, 22))
        self.label_standard.setObjectName("label_standard")
        self.comboBox_standard = QtGui.QComboBox(Dialog)
        self.comboBox_standard.setGeometry(QtCore.QRect(70, 68, 160, 22))
        self.comboBox_standard.setObjectName("comboBox_standard")
        #口径
        self.label_dia= QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(20, 91, 50, 22))
        self.label_dia.setObjectName("label_standard")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(70, 91, 160, 20))
        self.comboBox_dia.setObjectName("comboBox_dia")
        #切管
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(75, 117, 61, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(127, 117, 45,15))
        self.lineEdit_1.setObjectName("lineEdit_1")
        #ライセンスキー
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(75, 142, 170, 15))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 142, 50, 15))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_1 = QtGui.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(192, 140, 40, 20))
        self.pushButton_1.setObjectName("pushButton_1")
        #Create
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 167, 150, 20))
        self.pushButton.setObjectName("pushButton")
        #img
        self.label_img = QtGui.QLabel(Dialog)
        self.label_img.setGeometry(QtCore.QRect(0, 190, 270, 100))
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img.setText("")

        self.retranslateUi(Dialog)
        self.comboBox_lst.addItems(lst)
        self.comboBox_standard.addItems(pipe_st)
        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(pvc_d)

        self.comboBox_lst.setCurrentIndex(1)
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox_lst.setCurrentIndex(0)

        self.comboBox_kanzai.setCurrentIndex(1)
        self.comboBox_kanzai.currentIndexChanged[int].connect(self.on_kanzai)
        self.comboBox_kanzai.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_kanzai.currentIndexChanged[int].connect(self.on_lst2)
        self.comboBox_kanzai.setCurrentIndex(0)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_lst2)
        QtCore.QObject.connect(self.pushButton_1, QtCore.SIGNAL("pressed()"), self.license)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)

    def retranslateUi(self, Dialog):
        try:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "塩ビ管継手", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
            self.kanzai.setText(QtGui.QApplication.translate("Dialog", "管材", None, QtGui.QApplication.UnicodeUTF8))
            self.label_lst.setText(QtGui.QApplication.translate("Dialog", "継手", None, QtGui.QApplication.UnicodeUTF8))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None, QtGui.QApplication.UnicodeUTF8))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None, QtGui.QApplication.UnicodeUTF8))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None, QtGui.QApplication.UnicodeUTF8))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None, QtGui.QApplication.UnicodeUTF8))

        except:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "塩ビ管継手", None))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))
            self.kanzai.setText(QtGui.QApplication.translate("Dialog", "管材", None))
            self.label_lst.setText(QtGui.QApplication.translate("Dialog", "継手", None))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None))

    def license(self):
        x = self.lineEdit.text()
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        with open(joined_path, mode='w') as ff:
            ff.write(x)
            ff.close()

    def on_lst2(self):#管長
        if key=='00' or key=='01':
            if k_index==0 :
                L=4000
            else:
                L=''
            self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
    def on_lst(self):
        global key
        global sa2
        global xlc
        self.comboBox_standard.clear()
        key = self.comboBox_lst.currentText()[:2]
        xcf='2153987651329bc7526586915547'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        ff= open(joined_path)
        data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", str(data1), None))
        ff.close()
        if key=='00' :#---------------------------------------------------------
            sa=kanzai_ts
            sa2=kanzai_ts2
        elif key=='01' :
            sa=kanzai_dv
            sa2=kanzai_dv2

        self.comboBox_kanzai.clear()
        self.comboBox_kanzai.addItems(sa)
        #xlc=xcf[13:17]
        xlc='***'
    def on_standard(self):
        global st
        global sa2
        global pic
        global FC
        st=self.comboBox_standard.currentText()

        if key=='00':
            if k_index==0:#直管
                FC='直管'
                if st[:2]=='VP' :
                    sa2=pvc_d[:15]
                    pic='img_pvc_pipe.png'
                elif st[:2]=='VU' :
                    sa2=pvc_d[5:]
                    pic='img_pvc_pipe.png'
                elif st[:3]=='VPW' :
                    sa2=pvc_d[5:12]
                    pic='img_pvc_pipe.png'
                if st[3:7]=='Both' or st[4:8]=='Both':
                    pic='img_h07.png'
                    FC='2F直管'
                elif st[3:9]=='Single' or st[4:10]=='Single':
                    pic='img_h06.png'
                    FC='1F直管'
            elif k_index==1:#エルボ
                FC='エルボ'
                if st=='90':
                    sa2=pvc_d[:12]
                    pic='img_ts90E.png'
                elif st=='45':
                    sa2=pvc_d[:7]
                    pic='img_ts45E.png'
            elif k_index==2:#ソケット
                if st=='Socket':
                    sa2=pvc_d[:12]
                    FC='ソケット'
                    pic='img_ts_same_socket.png'
                elif st=='Increaser':
                    sa2=ts_dsoc_d
                    FC='インクリーザ'
                    pic='img_ts_diff_socket.png'
                elif st=='Valve':
                    sa2=pvc_d[:7]
                    FC='バルブソケット'
                    pic='img_ts_valve_socket.png'
            elif k_index==3:#チーズ
                if st=='Same_dia':
                    sa2=pvc_d[:7]
                    FC='チーズ'
                    pic='img_ts_same_tee.png'
                elif st=='Difference_dia':
                    sa2=ts_dtee_d
                    FC='径違いチーズ'
                    pic='img_ts_diff_tee.png'
            elif k_index==4:#フランジ
                if st=='JIS5k_socket':
                    sa2=flg_d[:12]
                    FC='TS_JIS5kフランジ'
                    pic='img_ts_flange_socket.png'
                elif st=='JIS10k_socket':
                    sa2=flg_d[:12]
                    FC='TS_JIS10kフランジ'
                    pic='img_ts_flange_socket.png'
                elif st=='JIS5k':
                    sa2=flg_d2
                    FC='JIS5kフランジ'
                    pic='img_h00.png'
                elif st=='JIS10k':
                    sa2=flg_d2
                    FC='JIS10kフランジ'
                    pic='img_h00.png'
                elif st=='JIS5k_lid':
                    sa2=flg_d2
                    FC='JIS5kフランジ蓋'
                    pic='img_h09.png'
                elif st=='JIS10k_lid':
                    sa2=flg_d2
                    FC='JIS10kフランジ蓋'
                    pic='img_h09.png'

                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None))


        elif key=='01':
            if k_index==0:#直管
                FC='直管'
                if st[:2]=='VP' :
                    sa2=pvc_d[:15]
                    pic='img_pvc_pipe.png'
                elif st[:2]=='VU' :
                    sa2=pvc_d[5:]
                    pic='img_pvc_pipe.png'
                elif st[:3]=='VPW' :
                    sa2=pvc_d[5:12]
                    pic='img_pvc_pipe.png'
                if st[3:7]=='Both' or st[4:8]=='Both':
                    pic='img_h07.png'
                    FC='2F直管'
                elif st[3:9]=='Single' or st[4:10]=='Single':
                    pic='img_h06.png'
                    FC='1F直管'
            elif k_index==1:#エルボ
                FC='エルボ'
                sa2=pvc_d[5:15]
                if st=='90':
                    pic='img_dv90E.png'
                elif st=='45':
                    pic='img_dv45E.png'
            elif k_index==2:#ソケット
                if st=='Socket':
                    sa2=pvc_d[5:15]
                    FC='ソケット'
                    pic='img_dv_same_socket.png'
                elif st=='Increaser':
                    sa2=dv_dsoc_d
                    FC='インクリーザ'
                    pic='img_dv_increaser.png'
                elif st=='Valve':
                    sa2=pvc_d[:7]
                    FC='バルブソケット'
                    pic='img_ts_valve_socket.png'
            elif k_index==3:#90Y
                if st=='Same_dia':
                    sa2=pvc_d[6:15]
                    FC='90°Y'
                    pic='img_dv_90Y.png'
                elif st=='Difference_dia':
                    sa2=dv_d90Y_d
                    FC='径違い90°Y'
                    pic='img_dv_diff_90Y.png'
                elif st=='Large_bend':
                    sa2=pvc_d[:7]
                    FC='大曲り90°Y'
                    pic='img_dv_lb90Y.png'
            elif k_index==4:#フランジ
                if st=='JIS5k_socket':
                    sa2=flg_d[:12]
                    FC='TS_JIS5kフランジ+ソケット'
                    pic='img_ts_flange_socket.png'
                elif st=='JIS10k_socket':
                    sa2=flg_d[:12]
                    FC='TS_JIS10kフランジ+ソケット'
                    pic='img_ts_flange_socket.png'
                elif st=='JIS5k':
                    sa2=flg_d2
                    self.label_l.setText(QtGui.QApplication.translate("Dialog", 'JIS5kフランジ', None))
                    pic='img_h00.png'
                elif st=='JIS10k':
                    sa2=flg_d2
                    FC='JIS10kフランジ'
                    pic='img_h00.png'
                elif st=='JIS5k_lid':
                    sa2=flg_d2
                    FC='JIS5kフランジ蓋'
                    pic='img_h09.png'
                elif st=='JIS10k_lid':
                    sa2=flg_d2
                    FC='JIS10kフランジ蓋'
                    pic='img_h09.png'

            elif k_index==5:#ダンパー
                sa2=pvc_d[6:15]
                if st=='VD_A':
                    pic='img_VD_A.png'
                    FC='ダンパー_単管式'
                elif st=='VD_B':
                    pic='img_VD_B.png'
                    FC='ダンパー_ソケット式'
                elif st=='VD_C_5k' or st=='VD_C_10k':
                    pic='img_VD_C.png'
                    FC='ダンパー_フランジ式'

        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(sa2)
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "data",pic)
        self.label_img.setPixmap(QtGui.QPixmap(joined_path))
        try:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None))
    def on_kanzai(self):
        global dia
        global pic
        global k_index
        global sa2

        k_index=self.comboBox_kanzai.currentIndex()
        dia=self.comboBox_dia.currentText()
        st=self.comboBox_standard.currentText()
        if key=='00' or key=='01':
            if k_index==0:
                sa=pipe_st
                sa2=pvc_d[:15]
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str('4000'), None))

            elif k_index==1:#エルボ
                sa=elbow_st
                if key=='00':
                    sa2=pvc_d[:10]
                elif key=='01':
                    sa2=pvc_d[5:]
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(''), None))
            elif k_index==2:#ソケット
                if key=='00':
                    sa=socket_st
                elif key=='01':
                    sa=socket_st[:2]

            elif k_index==3:#チーズ
                sa=tee_st
            elif k_index==4:#フランジ
                sa=flg_st
            elif k_index==5:#ダンパー
                sa=damper_st

            self.comboBox_standard.clear()
            try:
                self.comboBox_standard.addItems(sa)
            except:
                pass
            self.comboBox_dia.clear()
            self.comboBox_dia.addItems(sa2)

    def create(self):
        global st
        global dia
        st=self.comboBox_standard.currentText()
        dia=self.comboBox_dia.currentText()
        lsky=self.lineEdit.text()
        if lsky!=xlc:
            if key > '04':
               lsk='ライセンスキーを入力してください。'
               self.label_l.setText(QtGui.QApplication.translate("Dialog", lsk, None))
               return

        def cutter_01(self): #おねじ　ねじなし
            global c10
            sa=screws[dia]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            a=float(sa[6])
            l=float(sa[8])
            s=math.atan(0.5/16)
            d10=D0-a*math.tan(s)
            d20=d10+l*math.tan(s)
            t=float(sa[9])
            A2=float(sa[11])/2
            sa1=strt_dia[dia]
            A20=float(sa1[0])/2
            t=sa1[1]
            d0=0
            p1=Base.Vector(d0,0,0)
            p2=Base.Vector(d10,0,0)
            p3=Base.Vector(D0,0,a)
            p4=Base.Vector(d0,0,a)
            p5=Base.Vector(d20,0,l)
            p6=Base.Vector(d0,0,l)
            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c10=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            plist=[p4,p3,p5,p6,p4]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c10=c10.fuse(c20)

        def male_thread2(self):#おねじ　ねじあり　軸用
            global c00
            global c10
            global pipe
            sa=screws[dia]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            l=float(sa[8])*1.2
            a=float(sa[6])
            t=float(sa[9])
            A2=float(sa[11])/2
            d0=A2-t+0.001
            s=math.atan(0.5/16)
            s0=math.degrees(s)
            d10=d1-a*math.tan(s)
            d11=d10-p*math.tan(s)
            d20=d10+l*math.tan(s)
            d21=d20+p*math.tan(s)
            d0=0
            p1=Base.Vector(d0,0,0)
            p2=Base.Vector(d10,0,0)
            p3=Base.Vector(d0,0,l)
            p4=Base.Vector(d20,0,l)
            p5=Base.Vector(d0,0,-p)
            p6=Base.Vector(d11,0,-p)
            p7=Base.Vector(d0,0,l+p)
            p8=Base.Vector(d21,0,l+p)
            plist=[p5,p7,p8,p6,p5]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c10=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)

            #ねじ断面
            c0=0
            x0=d11+(h-r)
            sr0=27.5
            sr=math.radians(sr0)
            x=r*math.sin(sr)
            y=r*math.cos(sr)
            m=h-r+0.5
            z=m*math.tan(sr)+y
            p1=(0,0,0)
            p2=(x,0,y)
            p3=(-m,0,z)
            p4=(-m,0,-z)
            p5=(x,0,-y)
            edge1 = Part.makeCircle(r, Base.Vector(p1), Base.Vector(0,1,0), 270+sr0, 90-sr0)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p5)
            #らせん_sweep
            helix=Part.makeHelix(p,l+2*p,d11,s0,False)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            if dia=='20' or dia=='30' or dia=='40':
               cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p/2),App.Rotation(App.Vector(0,1,0),-s0))
            else:
               cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p),App.Rotation(App.Vector(0,1,0),-s0))
            wface=Part.Face(cutProfile)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c10=c10.fuse(pipe)
            p3=Base.Vector(0,0,l)
            p5=Base.Vector(0,0,-2*p)
            c11 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p5)),Base.Vector(0,0,1))
            c10=c10.cut(c11)
            c12 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p3)),Base.Vector(0,0,1))
            c10=c10.cut(c12)
            Part.show(c10)

        def hexagon(self):
            global c10
            sa1=strt_dia[dia]
            d2=float(sa1[0])/2
            t=float(sa1[1])
            d0=d2-t

            sa=valve_s_d[dia]
            L00=float(sa[0])
            W=float(sa[4])
            sa = nipples[dia]
            L=L00
            E=float(sa[1])
            n=sa[2]
            B=float(sa[3])/2
            dk=float(sa[4])/2
            x1=B
            s=math.pi/n
            e0=x1/math.cos(s)
            x=e0*math.cos(s)
            y=e0*math.sin(s)
            if n==6:
               p1=(x,y,0)
               p2=(0,e0,0)
               p3=(-x,y,0)
               p4=(-x,-y,0)
               p5=(0,-e0,0)
               p6=(x,-y,0)
               plist=[p1,p2,p3,p4,p5,p6,p1]
            elif n==8:
               p1=(e0*math.cos(s),e0*math.sin(s),0)
               p2=(e0*math.cos(3*s),e0*math.sin(3*s),0)
               p3=(-e0*math.cos(math.pi-5*s),e0*math.sin(math.pi-5*s),0)
               p4=(-e0*math.cos(math.pi-7*s),e0*math.sin(math.pi-7*s),0)
               p5=(-e0*math.cos(s),-e0*math.sin(s),0)
               p6=(-e0*math.cos(3*s),-e0*math.sin(3*s),0)
               p7=(e0*math.cos(3*s),-e0*math.sin(3*s),0)
               p8=(e0*math.cos(s),-e0*math.sin(s),0)
               plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            #ポリゴン
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c10=wface.extrude(Base.Vector(0,0,W))
            c10.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))

            #Part.show(c10)

        def flange(self):#フランジ

            global c00
            if st=='JIS5k_socket' :
                sa=JIS5k_socket[dia]
            elif st=='JIS10k_socket' :
                sa=JIS10k_socket[dia]

            D1=float(sa[0])/2
            C=float(sa[1])/2
            D=float(sa[2])/2
            n0=sa[3]
            h=float(sa[4])/2
            t=float(sa[5])
            L=float(sa[6])
            c1 = Part.makeCylinder(D,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c2 = Part.makeCylinder(D1,L-t,Base.Vector(0,0,t),Base.Vector(0,0,1))
            c00=c1.fuse(c2)
            for i in range(n0):
                k=math.pi*2/n0
                if i==0:
                    x=C*math.cos(k/2)
                    y=C*math.sin(k/2)
                    c20 = Part.makeCylinder(h,t,Base.Vector(x,y,0),Base.Vector(0,0,1))
                else:
                    ks=i*k+k/2
                    x=C*math.cos(ks)
                    y=C*math.sin(ks)
                    c20 = Part.makeCylinder(h,t,Base.Vector(x,y,0),Base.Vector(0,0,1))
                if i==0:
                    c00=c00.cut(c20)
                else:
                    c00=c00.cut(c20)

        def ts_junc(self):#TSカッター
            global c00
            global dia
            sa=pvc_ts[dia]
            d1=float(sa[1])/2
            T=float(sa[2])
            l=float(sa[3])
            d=float(sa[4])/2
            D=float(sa[5])/2
            t=float(sa[6])
            d2=d1-(l/T)
            p1=(0,0,0)
            p2=(0,d2,0)
            p3=(l,d1,0)
            p4=(l,0,0)
            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)

        def dv_junc(self):#DVカッター
            global c00
            global dia
            sa=pvc_dv[dia]
            d1=float(sa[1])/2
            d2=float(sa[2])/2
            l=float(sa[3])
            d=float(sa[4])/2
            D=float(sa[5])/2
            t=float(sa[6])

            p1=(0,0,0)
            p2=(0,d2,0)
            p3=(l,d1,0)
            p4=(l,0,0)
            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
        def Flange1(self):
           global c01
           C0=0
           if st[-2:]=='5k':
               sa = JIS5k_2[dia]
               #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None))
           elif st[-3:]=='10k' :
               sa = JIS10k_2[dia]

           d0=float(sa[0])
           d2=float(sa[1])
           d4=float(sa[2])
           d5=float(sa[3])
           k0=float(sa[4])
           E0=float(sa[5])
           n0=sa[6]
           a0=0
           b0=0
           t0=0
           r0=0
           p1=(d2/2,0,0)
           p2=(d5/2,0,0)
           p3=(d5/2,0,k0)
           p4=(b0/2,0,k0)
           p5=(a0/2,0,t0)
           p6=(d2/2,0,t0)
           p7=(d2/2+C0,0,0)
           p8=(d2/2,0,C0)
           plist=[p1,p2,p3,p4,p5,p6,p1]
           pwire=Part.makePolygon(plist)
           pface = Part.Face(pwire)
           c01=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
           c2=Part.makeCylinder(d2/2,k0)
           c01=c01.cut(c2)
           if st=='JIS10k_Loose' or st=='JIS5k_Loose':
               plist=[p1,p7,p8,p1]
               pwire=Part.makePolygon(plist)
               pface = Part.Face(pwire)
               c22=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
               c01=c01.cut(c22)
           ks=0
           for i in range(n0):
               k=2*math.pi/n0
               r=d4/2
               if i==0:
                   x=r*math.cos(k/2)
                   y=r*math.sin(k/2)
               else:
                   ks=i*k+k/2
                   x=r*math.cos(ks)
                   y=r*math.sin(ks)
               c3 = Part.makeCylinder(E0/2,k0,Base.Vector(x,y,0),Base.Vector(0,0,1))
               if i==0:
                   c01=c01.cut(c3)
               else:
                   c01=c01.cut(c3)

        def Flange2(self):
           global c01
           global label
           if st=='JIS5k_lid' :
               sa = JIS5k_2[dia]
           elif st=='JIS10k_lid' :
               sa = JIS10k_2[dia]

           d0=float(sa[0])
           d2=float(sa[1])
           d4=float(sa[2])
           d5=float(sa[3])
           k0=float(sa[4])
           E0=float(sa[5])
           n0=sa[6]
           a0=0
           b0=0
           t0=0
           r0=0
           p1=(d2/2,0,0)
           p2=(d5/2,0,0)
           p3=(d5/2,0,k0)
           p4=(b0/2,0,k0)
           p5=(a0/2,0,t0)
           p6=(d2/2,0,t0)
           plist=[p1,p2,p3,p4,p5,p6,p1]
           pwire=Part.makePolygon(plist)
           pface = Part.Face(pwire)
           c01=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
           ks=0
           for i in range(n0):
               k=2*math.pi/n0
               r=d4/2
               if i==0:
                   x=r*math.cos(k/2)
                   y=r*math.sin(k/2)
               else:
                   ks=i*k+k/2
                   x=r*math.cos(ks)
                   y=r*math.sin(ks)
               c3 = Part.makeCylinder(E0/2,k0,Base.Vector(x,y,0),Base.Vector(0,0,1))
               if i==0:
                   c01=c01.cut(c3)
               else:
                   c01=c01.cut(c3)

        if key=='00' or key=='01':
            if k_index==0:#直管
                sa=strt_dia[dia]
                D=float(sa[0])
                if st[:2]=='VP' or st[:2]=='VU' or st[:3]=='VPW':
                    if st[:2]=='VP' :
                        t=float(sa[1])
                    elif st[:2]=='VU' :
                        t=float(sa[3])
                    elif st[:3]=='VPW' :
                        t=float(sa[5])
                    D=self.comboBox_dia.currentText()
                    L=float(self.lineEdit_1.text())
                label = 'Straight_tube_' 
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyInteger", "k_index",label).k_index=k_index
                obj.addProperty("App::PropertyEnumeration", "key",label)
                obj.key=lst
                obj.addProperty("App::PropertyEnumeration", "st",label)
                obj.st=pipe_st
                i=self.comboBox_standard.currentIndex()
                obj.st=pipe_st[i]
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=pvc_d
                i=self.comboBox_dia.currentIndex()
                obj.dia=pvc_d[i]
                obj.addProperty("App::PropertyFloat", "L",label).L=L
                ParamPvcPFit.pvc_p(obj)
                obj.ViewObject.Proxy=0
                FreeCAD.ActiveDocument.recompute()   
                return
            elif k_index==1:#エルボ
                if key=='00':
                    if st=='45' or st=='90':
                        sa=pvc_ts[dia]
                        D1=float(sa[0])
                        l=float(sa[3])
                        D=float(sa[5])
                        d=float(sa[4])
                        s0=float(st)/2
                        sa=elbow_ts[dia]
                        if st=='90':
                            b='TS90Elbow_'
                            L=float(sa[1])
                        elif st=='45':
                            b='TS45Elbow_'
                            L=float(sa[2])
                        label=b + '_' + str(dia) +'_'
                        c3=Part.makeSphere(D1/2)
                        c31=Part.makeSphere(d/2)
                        c3=c3.cut(c31)
                        s=2*math.radians(s0)
                        x=D1/2+5
                        x1=x*math.tan(math.pi/2-s)
                        p1=(-x,-x,-x)
                        p2=(-x,0,-x)
                        p3=(0,0,-x)
                        p4=(-x1,x,-x)
                        p5=(x,x,-x)
                        p6=(x,-x,-x)
                        plist=[p1,p2,p3,p4,p5,p6,p1]
                        pwire=Part.makePolygon(plist)
                        pface = Part.Face(pwire)
                        c4=pface.extrude(Base.Vector(0,0,2*x))
                        c3=c3.cut(c4)
                        c1=Part.makeCylinder(D/2,L,Base.Vector(0,-L,0),Base.Vector(0,1,0))
                        c11=Part.makeCylinder((d)/2,L,Base.Vector(0,-L,0),Base.Vector(0,1,0))
                        c2=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c21=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90-2*s0))
                        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90-2*s0))
                        c1=c1.fuse(c2)
                        ts_junc(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,-(L-l),0),App.Rotation(App.Vector(0,0,1),-90))
                        c1=c1.cut(c2)
                        c2=c00
                        x=L-l
                        x1=x*math.cos(math.pi/2-s)
                        y1=x*math.sin(math.pi/2-s)
                        c2.Placement=App.Placement(App.Vector(x1,y1,0),App.Rotation(App.Vector(0,0,1),(90-2*s0)))
                        #Part.show(c2)
                        c1=c1.cut(c2)
                        c1=c1.fuse(c3)
                        c1=c1.cut(c11)
                        c1=c1.cut(c21)
                if key=='01':
                    if st=='45' or st=='90':
                        sa=pvc_dv[dia]
                        D1=float(sa[0])
                        l=float(sa[3])
                        D=float(sa[5])
                        d=float(sa[4])
                        t=float(sa[6])
                        s0=float(st)/2
                        sa=elbow_dv[dia]
                        if st=='90':
                            b='DV90Elbow'
                            L=float(sa[1])
                            label=b + '_' + str(dia) +'_'
                            s0=float(st)
                            x=2*t+D1/2
                            #R部
                            c3=Part.makeTorus(x,D1/2,Base.Vector(0,0,0),Base.Vector(0,0,1),0,360,s0)
                            c3.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),s0))
                            c31=Part.makeTorus(x,d/2,Base.Vector(0,0,0),Base.Vector(0,0,1),0,360,s0)
                            c31.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),s0))
                            c3=c3.cut(c31)
                            #垂直
                            c1=Part.makeCylinder((D1+3*t)/2,(L-x+2*t),Base.Vector(-x,-(L-x),0),Base.Vector(0,1,0))
                            c11=Part.makeCylinder(d/2,(L-x),Base.Vector(-x,-(L-x),0),Base.Vector(0,1,0))
                            c1=c1.cut(c11)
                            #水平
                            c2=Part.makeCylinder((D1+3*t)/2,(L-x+2*t),Base.Vector(-2*t,x,0),Base.Vector(1,0,0))
                            c21=Part.makeCylinder(d/2,(L-x),Base.Vector(0,x,0),Base.Vector(1,0,0))
                            c2=c2.cut(c21)
                            c1=c1.fuse(c2)
                            c1=c1.fuse(c3)
                            c1=c1.cut(c31)
                            #受口
                            dv_junc(self)
                            c2=c00
                            c2.Placement=App.Placement(App.Vector(0,x,0),App.Rotation(App.Vector(0,1,0),0))
                            c1=c1.cut(c2)
                            c2=c00
                            c2.Placement=App.Placement(App.Vector(-x,0,0),App.Rotation(App.Vector(0,0,1),-90))
                            c1=c1.cut(c2)
                        elif st=='45':
                            b='DV45Elbow'
                            L=float(sa[2])
                            label=b + '_' + str(dia) +'_'
                            s0=float(st)
                            s=math.radians(s0)
                            x=2*t+D1/2
                            y1=x*math.tan(s/2)
                            x2=x*math.cos(s)
                            y2=x*math.sin(s)

                            #R部
                            c3=Part.makeTorus(x,D1/2,Base.Vector(0,0,0),Base.Vector(0,0,1),0,360,45)
                            c31=Part.makeTorus(x,d/2,Base.Vector(0,0,0),Base.Vector(0,0,1),0,360,45)
                            c3=c3.cut(c31)
                            c3.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),135))
                            #垂直
                            c1=Part.makeCylinder((D1+3*t)/2,(L-y1+2*t),Base.Vector(-x,-(L-y1),0),Base.Vector(0,1,0))
                            c11=Part.makeCylinder(d/2,(L-y1+2*t),Base.Vector(-x,-(L-y1),0),Base.Vector(0,1,0))
                            c1=c1.cut(c11)
                            #Part.show(c11)
                            #水平
                            c2=Part.makeCylinder((D1+3*t)/2,(L-y1+2*t),Base.Vector(-(x-x2+2*t),y2-y1,0),Base.Vector(1,0,0))
                            c21=Part.makeCylinder(d/2,(L-y1),Base.Vector(-(x-x2+2*t),y2-y1,0),Base.Vector(1,0,0))
                            c2=c2.cut(c21)
                            c2.Placement=App.Placement(App.Vector(x2-x,y2,0),App.Rotation(App.Vector(0,0,1),45))
                            c1=c1.fuse(c2)
                            #受口

                            z=L-l
                            x3=(2*t)/math.sqrt(2)
                            y3=x3
                            x4=(L-l)/math.sqrt(2)
                            y4=x4
                            x5=x-x4
                            y5=y1+y4
                            dv_junc(self)
                            c2=c00
                            c2.Placement=App.Placement(App.Vector(-x5,y5,0),App.Rotation(App.Vector(0,0,1),45))
                            c1=c1.cut(c2)
                            c2=c00
                            c2.Placement=App.Placement(App.Vector(-x,-(z-y1),0),App.Rotation(App.Vector(0,0,1),-90))
                            c1=c1.cut(c2)
                            c1=c1.fuse(c3)
                            c1=c1.cut(c31)

            elif k_index==2:#ソケット
                if st=='Socket' :
                    label='Socket_' + str(dia)+'_'
                    if key=='00':
                        sa=pvc_ts[dia]
                    elif key=='01':
                        sa=pvc_dv[dia]
                    d1=float(sa[1])/2
                    T=float(sa[2])
                    l=float(sa[3])
                    d=float(sa[4])
                    D=float(sa[5])
                    L=float(sa[7])

                    c1=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    c2=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2)

                    if key=='00':
                        ts_junc(self)
                    elif key=='01':
                        dv_junc(self)

                    c2=c00
                    c2.Placement=App.Placement(App.Vector(l,0,0),App.Rotation(App.Vector(0,0,1),180))
                    c1=c1.cut(c2)

                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L-l,0,0),App.Rotation(App.Vector(0,0,1),0))
                    c1=c1.cut(c2)

                elif st=='Increaser' :
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                    global dia1
                    global dia2
                    label='Increaser_' + str(dia)+'_'
                    if key=='00':
                        sa=ts_dsoc[dia]
                    elif key=='01':
                        sa=dv_dsoc[dia]
                    D=float(sa[0])/2
                    D1=float(sa[1])/2
                    L=float(sa[2])
                    key1=dia.find('x')
                    key2=key1+1
                    dia1=dia[:key1]
                    dia2=dia[key2:]
                    if key=='00':
                        sa=pvc_ts[dia1]
                    elif key=='01':
                        sa=pvc_dv[dia1]
                    l1=float(sa[3])
                    d21=float(sa[4])/2
                    t1=float(sa[6])
                    if key=='00':
                        sa=pvc_ts[dia2]
                    elif key=='01':
                        sa=pvc_dv[dia2]

                    l2=float(sa[3])
                    d22=float(sa[4])/2
                    t2=float(sa[6])

                    x1=l1
                    x2=l2
                    p1=(0,0,0)
                    p2=(0,D,0)
                    p3=(x1,D,0)
                    p4=(L-x2,D1,0)
                    p5=(L,D1,0)
                    p6=(L,0,0)
                    plist=[p1,p2,p3,p4,p5,p6,p1]
                    pwire=Part.makePolygon(plist)
                    pface = Part.Face(pwire)
                    c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)

                    p1=(l1,0,0)
                    p2=(l1,d21,0)
                    p3=(L-l2,d22,0)
                    p4=(L-l2,0,0)
                    plist=[p1,p2,p3,p4,p1]
                    pwire=Part.makePolygon(plist)
                    pface = Part.Face(pwire)
                    c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                    c1=c1.cut(c2)
                    dia=dia1
                    if key=='00':
                        ts_junc(self)
                    elif key=='01':
                        dv_junc(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(l1,0,0),App.Rotation(App.Vector(0,0,1),180))
                    c1=c1.cut(c2)
                    dia=dia2
                    if key=='00':
                        ts_junc(self)
                    elif key=='01':
                        dv_junc(self)

                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L-l2,0,0),App.Rotation(App.Vector(0,0,1),0))
                    c1=c1.cut(c2)

                elif st=='Valve' :
                    sa=valve_s_d[dia]
                    L=float(sa[0])
                    E=float(sa[1])
                    W=float(sa[4])
                    sa=screws[dia]
                    l=float(sa[8])
                    x=E-l
                    if x<=0:
                        x=0
                    hexagon(self)
                    c1=c10
                    sa=strt_dia[dia]
                    D=sa[0]/2
                    if x > 0 :
                        c2=Part.makeCylinder(D,x,Base.Vector(0,0,W),Base.Vector(0,0,1))
                        c1=c1.fuse(c2)
                    cutter_01(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,l+W+x),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.fuse(c2)
                    sa=pvc_ts[dia]
                    D=float(sa[5])/2
                    d=float(sa[4])/2
                    L2=l+W+x
                    L3=L-L2
                    c2=Part.makeCylinder(D,L3,Base.Vector(0,0,-L3),Base.Vector(0,0,1))
                    c1=c1.fuse(c2)
                    c2=Part.makeCylinder(d,L,Base.Vector(0,0,-L3),Base.Vector(0,0,1))
                    c1=c1.cut(c2)
                    ts_junc(self)
                    c2=c00
                    sa=pvc_ts[dia]
                    l=float(sa[3])
                    c2.Placement=App.Placement(App.Vector(0,0,-(L3-l)),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                    c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))

            elif k_index==3:#チーズ Y
                if key=='00':
                    label='TS_T_' + str(dia)+'_'
                    if st=='Same_dia' :
                        sa=ts_tee[dia]
                        H=float(sa[0])
                        I=float(sa[1])
                        D=float(sa[2])
                        sa=pvc_ts[dia]
                        l=float(sa[3])
                        d=float(sa[4])
                        c1=Part.makeCylinder(D/2,2*H,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c3=Part.makeCylinder(d/2,2*H,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c2=Part.makeCylinder(D/2,I,Base.Vector(H,0,0),Base.Vector(0,1,0))
                        c4=Part.makeCylinder(d/2,I,Base.Vector(H,0,0),Base.Vector(0,1,0))
                        c1=c1.fuse(c2)
                        ts_junc(self)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(l,0,0),App.Rotation(App.Vector(0,0,1),180))
                        c1=c1.cut(c20)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(2*H-l,0,0),App.Rotation(App.Vector(0,0,1),0))
                        c1=c1.cut(c20)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(H,I-l,0),App.Rotation(App.Vector(0,0,1),90))
                        c1=c1.cut(c20)
                        c1=c1.cut(c3)
                        c1=c1.cut(c4)

                    elif st=='Difference_dia' :
                        sa=ts_dtee[dia]
                        H=float(sa[0])
                        I=float(sa[1])
                        D=float(sa[2])
                        D1=float(sa[3])
                        key1=dia.find('x')
                        key2=key1+1
                        dia1=dia[:key1]
                        dia2=dia[key2:]
                        sa=pvc_ts[dia1]
                        l1=float(sa[3])
                        d=float(sa[4])
                        sa=pvc_ts[dia2]
                        l2=float(sa[3])
                        d1=float(sa[4])
                        c1=Part.makeCylinder(D/2,2*H,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c3=Part.makeCylinder(d/2,2*H,Base.Vector(0,0,0),Base.Vector(1,0,0))
                        c2=Part.makeCylinder(D1/2,I,Base.Vector(H,0,0),Base.Vector(0,1,0))
                        c4=Part.makeCylinder(d1/2,I,Base.Vector(H,0,0),Base.Vector(0,1,0))
                        c1=c1.fuse(c2)
                        dia=dia1
                        ts_junc(self)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(l1,0,0),App.Rotation(App.Vector(0,0,1),180))
                        c1=c1.cut(c20)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(2*H-l1,0,0),App.Rotation(App.Vector(0,0,1),0))
                        c1=c1.cut(c20)
                        dia=dia2
                        ts_junc(self)
                        c20=c00
                        c20.Placement=App.Placement(App.Vector(H,I-l2,0),App.Rotation(App.Vector(0,0,1),90))
                        c1=c1.cut(c20)
                        c1=c1.cut(c3)
                        c1=c1.cut(c4)
                elif key=='01':#90Y
                    if st=='Same_dia' :
                        label='Y90_' + str(dia) + '_'
                        sa=dv_90Y[dia]
                        z1=float(sa[0])
                        z2=float(sa[1])
                        z3=float(sa[2])
                        L1=float(sa[3])
                        L2=float(sa[4])
                        L3=float(sa[5])
                        sa=pvc_dv[dia]
                        D1=float(sa[0])
                        l=float(sa[3])
                        d=float(sa[4])
                        t=float(sa[6])
                        L0=L1-z1+2*t
                        c1=Part.makeCylinder(D1/2,z1+z2,Base.Vector(-z2,0,0),Base.Vector(1,0,0))
                        c11=Part.makeCylinder((D1+3*t)/2,L0,Base.Vector(-L2,0,0),Base.Vector(1,0,0))
                        c12=Part.makeCylinder((D1+3*t)/2,L0,Base.Vector(z1-2*t,0,0),Base.Vector(1,0,0))
                        c1=c1.fuse(c11)
                        c1=c1.fuse(c12)
                        c2=Part.makeCylinder(D1/2,L3-z3+2*t,Base.Vector(0,0,0),Base.Vector(0,1,0))
                        c21=Part.makeCylinder((D1+3*t)/2,L0,Base.Vector(0,L3-L0,0),Base.Vector(0,1,0))
                        c2=c2.fuse(c21)
                        c1=c1.fuse(c2)
                        c2=Part.makeCylinder(d/2,L1+L2,Base.Vector(-L2,0,0),Base.Vector(1,0,0))
                        c1=c1.cut(c2)
                        c2=Part.makeCylinder(d/2,L3,Base.Vector(0,0,0),Base.Vector(0,1,0))
                        c1=c1.cut(c2)
                        dv_junc(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(L1-l,0,0),App.Rotation(App.Vector(0,0,1),0))
                        c1=c1.cut(c2)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(-(L2-l),0,0),App.Rotation(App.Vector(0,1,0),180))
                        c1=c1.cut(c2)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,L3-l,0),App.Rotation(App.Vector(0,0,1),90))
                        c1=c1.cut(c2)
                    elif st=='Difference_dia' :
                        label='Y90_' + str(dia) + '_'
                        sa=dv_d90Y[dia]
                        z1=float(sa[0])
                        z2=float(sa[1])
                        z3=float(sa[2])
                        L1=float(sa[3])
                        L2=float(sa[4])
                        L3=float(sa[5])

                        key1=dia.find('x')
                        key2=key1+1

                        dia1=dia[:key1]
                        dia2=dia[key2:]

                        sa=pvc_dv[dia1]
                        D01=float(sa[0])
                        l1=float(sa[3])
                        d1=float(sa[4])
                        t1=float(sa[6])

                        sa=pvc_dv[dia2]
                        D02=float(sa[0])
                        l2=float(sa[3])
                        d2=float(sa[4])
                        t2=float(sa[6])

                        L00=L1-z1+2*t1
                        L01=L3-z3+2*t2

                        c1=Part.makeCylinder(D01/2,z1+z2,Base.Vector(-z2,0,0),Base.Vector(1,0,0))
                        c11=Part.makeCylinder((D01+3*t1)/2,L00,Base.Vector(-L2,0,0),Base.Vector(1,0,0))
                        c12=Part.makeCylinder((D01+3*t1)/2,L00,Base.Vector(z1-2*t1,0,0),Base.Vector(1,0,0))
                        c1=c1.fuse(c11)
                        c1=c1.fuse(c12)

                        c2=Part.makeCylinder(D02/2,L3-l2,Base.Vector(0,0,0),Base.Vector(0,1,0))
                        c21=Part.makeCylinder((D02+3*t2)/2,L01,Base.Vector(0,L3-L01,0),Base.Vector(0,1,0))
                        c2=c2.fuse(c21)
                        c1=c1.fuse(c2)

                        c2=Part.makeCylinder(d1/2,L1+L2,Base.Vector(-L2,0,0),Base.Vector(1,0,0))
                        c1=c1.cut(c2)
                        c2=Part.makeCylinder(d2/2,L3,Base.Vector(0,0,0),Base.Vector(0,1,0))
                        c1=c1.cut(c2)
                        dia=dia1
                        dv_junc(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(L1-l1,0,0),App.Rotation(App.Vector(0,0,1),0))
                        c1=c1.cut(c2)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(-(L2-l2),0,0),App.Rotation(App.Vector(0,1,0),180))
                        c1=c1.cut(c2)

                        dia=dia2
                        dv_junc(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,L3-l2,0),App.Rotation(App.Vector(0,0,1),90))
                        c1=c1.cut(c2)

            elif k_index==4:#フランジ
                if st=='JIS5k_socket' or st=='JIS10k_socket':
                    if st=='JIS5k_socket':
                        sa=JIS5k_socket[dia]
                    elif st=='JIS10k_socket':
                        sa=JIS10k_socket[dia]
                    L=float(sa[6])
                    if key=='00':
                        sa=pvc_ts[dia]
                        label='TS_Flange_' + str(dia)+'_'
                    elif key=='01':
                        sa=pvc_ts[dia]
                        label='DV_Flange_' + str(dia)+'_'
                    l=float(sa[3])
                    d=float(sa[4])
                    flange(self)
                    c1=c00
                    if key=='00':
                        ts_junc(self)
                        sa=pvc_ts[dia]
                    elif key=='01':
                        ts_junc(self)
                        sa=pvc_ts[dia]
                    c2=c00

                    l=float(sa[3])
                    c2.Placement=App.Placement(App.Vector(0,0,L-l),App.Rotation(App.Vector(0,1,0),-90))
                    c1=c1.cut(c2)
                    c2 = Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(0,0,1))
                    c1=c1.cut(c2)

                elif st=='JIS5k' or st=='JIS10k':
                    if st=='JIS5k':
                        sa=JIS5k_2[dia]
                        label='Flange_' + str(dia)+'_'

                    elif st=='JIS10k':
                        sa=JIS10k_2[dia]
                        label='Flange_' + str(dia)+'_'
                    Flange1(self)
                    c1=c01

                elif st=='JIS5k_lid' or st=='JIS10k_lid':
                    if st=='JIS5k_lid':
                        sa=JIS5k_2[dia]
                        label='Flange_' + str(dia)+'_'
                    elif st=='JIS10k_lid':
                        sa=JIS10k_2[dia]
                        label='Flange_' + str(dia)+'_'
                    Flange2(self)
                    c1=c01

            elif k_index==5:#ダンパー

                label=str(st) +'_'  + str(dia)+'_'
                if st=='VD_A':
                    sa=dv_dapA[dia]
                elif st=='VD_B':
                    sa=dv_dapB[dia]
                elif st=='VD_C_5k':
                    sa=dv_dapA[dia]
                elif st=='VD_C_10k':
                    sa=dv_dapA[dia]

                D=float(sa[0])
                L=float(sa[2])
                t1=float(sa[3])
                sa=pvc_dv[dia]
                D1=float(sa[0])
                l=float(sa[3])
                d=float(sa[4])
                t=float(sa[6])
                if st=='VD_A':
                    z=L/2
                elif st=='VD_B':
                    z=L/2-l
                elif st=='VD_C_5k' or st=='VD_C_10k':
                    z=L/2-l+25

                if d<=150:
                    r=25
                elif d>150:
                    r=35
                r0=r-6
                r1=r+6
                r2=r1+6
                #本体
                c1=Part.makeCylinder(D1/2,2*z,Base.Vector(-z,0,0),Base.Vector(1,0,0))
                if st=='VD_B':
                    L0=L/2-z
                    c2=Part.makeCylinder((D1+3*t)/2,L0,Base.Vector(-L/2,0,0),Base.Vector(1,0,0))
                    c02=Part.makeCylinder((d)/2,L0,Base.Vector(-L/2,0,0),Base.Vector(1,0,0))
                    c2=c2.cut(c02)
                    c1=c1.fuse(c2)
                    dv_junc(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-(L/2-l),0,0),App.Rotation(App.Vector(0,0,1),180))
                    c1=c1.cut(c2)
                    c2=Part.makeCylinder((D1+3*t)/2,L0,Base.Vector(z,0,0),Base.Vector(1,0,0))
                    c02=Part.makeCylinder((d)/2,L0,Base.Vector(z,0,0),Base.Vector(1,0,0))
                    c2=c2.cut(c02)
                    c1=c1.fuse(c2)
                    dv_junc(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector((L/2-l),0,0),App.Rotation(App.Vector(0,0,1),0))
                    c1=c1.cut(c2)
                elif st=='VD_C_5k' or st=='VD_C_10k':
                    L0=L/2-z-10
                    Flange1(self)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector(-z-5,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector(z+5,0,0),App.Rotation(App.Vector(0,1,0),-90))
                    c1=c1.fuse(c2)

                #ダンパー
                c21=Part.makeCylinder(d/2,2*z,Base.Vector(-z,0,0),Base.Vector(1,0,0))
                c2=Part.makeCylinder(20/2,D1+12+15,Base.Vector(0,-D1/2-15,0),Base.Vector(0,1,0))
                c22=Part.makeCylinder(10/2,D1/2+40,Base.Vector(r,-(D1/2+40),0),Base.Vector(0,1,0))
                c2=c2.fuse(c22)
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(10/2,5,Base.Vector(r,-(D1/2+50),0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(20/2,r,Base.Vector(r,-(D1/2+75),0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=c2.cut(c21)
                c1=c1.fuse(c2)
                c1=c1.cut(c21)
                c2=Part.makeCylinder(15/2,D1,Base.Vector(0,-D1/2,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(25/2,15,Base.Vector(0,-D1/2-30,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(15/2,10,Base.Vector(0,-D1/2-40,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(r2,5,Base.Vector(0,-D1/2-45,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(25/2,10,Base.Vector(0,-D1/2-52,0),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                c2=Part.makeCylinder(d/2,t1,Base.Vector(0,0,-t1/2),Base.Vector(0,0,1))
                c1=c1.fuse(c2)
                p1=(0,-(D1/2+45),0)
                p2=(0,-(D1/2+45),r)
                p3=(r,-(D1/2+45),0)
                edge1 = Part.makeCircle(r0, Base.Vector(p1), Base.Vector(0,1,0), 270,0)
                edge2 = Part.makeCircle(6, Base.Vector(p2), Base.Vector(0,1,0), 90, 270)
                edge3 = Part.makeCircle(r+6, Base.Vector(p1), Base.Vector(0,1,0), 270, 0)
                edge4 = Part.makeCircle(6, Base.Vector(p3), Base.Vector(0,1,0), 0, -180)
                aWire=Part.Wire([edge1,edge2,edge3,edge4])
                pface=Part.Face(aWire)
                c2=pface.extrude(Base.Vector(0,5,0))
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

class my_Main():
    d = QtGui.QWidget()
    d.setWindowFlags(QtCore.Qt.Window)
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.show()






