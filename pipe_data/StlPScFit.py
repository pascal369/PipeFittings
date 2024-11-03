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
import ParamStlPScFit
DEBUG = True # set to True to show debug messages

lst=[
'00_Flange','01_Elbow','02_Bend','03_Tee','04_Y','05_Cross','06_Nipple','07_Union',
'08_Socket','09_Cap','10_Plug','11_Bushing','12_Globe_Valve','13_Gate_Valve','14_Check_Valve','15_Straight_Pipe',
]

l_lst={
'00':'フランジ','01':'エルボ','02':'ベンド','03':'チーズ','04':'Y','05':'クロス','06':'ニップル','07':'ユニオン',
'08':'ソケット','09':'キャップ','10':'プラグ','11':'ブッシング','12':'玉形弁','13':'仕切弁','14':'逆止弁','15':'直管',
}

screw=['Parrallel pipe thread','Taper pipe thread']
flg=['JIS5k','JIS10k']
tube=['SGP','Sch20s','Sch40','Sch40s','Sch80']
tube_d=['06A','08A','10A','15A','20A','25A','32A','40A','50A','65A']
bend_d=['06A','08A','10A','15A','20A','25A','40A','50A']
elbow_st=['45L','90L','90SL','90RL','90RSL']
elbow_d=[
'10Ax08A','15Ax08A','15Ax10A','20Ax10A','20Ax15A','25Ax15A','25Ax20A','32Ax15A','32Ax20A','32Ax25A',
'40Ax15A','40Ax20A','40Ax25A','40Ax32A','50Ax15A','50Ax20A','50Ax25A','50Ax32A','50Ax40A'
]
elbow_rl=[
'10Ax08A','15Ax08A','15Ax10A','20Ax10A','20Ax15A','25Ax15A','25Ax20A','32Ax15A','32Ax20A','32Ax25A',
'40Ax15A','40Ax20A','40Ax25A','40Ax32A','50Ax15A','50Ax20A','50Ax25A','50Ax32A','50Ax40A'
]
elbow_rsl=['25Ax20A','32Ax25A']

tee_st=['T','RT']
tee_d=[
'10Ax10Ax08A','15Ax15Ax08A','15Ax15Ax10A','20Ax20Ax10A','20Ax20Ax15A','25Ax25Ax10A','25Ax25Ax15A',
'25Ax25Ax20A','32Ax32Ax15A','32Ax32Ax20A','32Ax32Ax25A','40Ax40Ax15A','40Ax40Ax20A','40Ax40Ax25A',
'40Ax40Ax32A','50Ax50Ax15A','50Ax50Ax20A','50Ax50Ax25A','50Ax50Ax32A','50Ax50Ax40A',
]

cross_st=['Cr','RCr']
RCr_d=['40Ax40Ax25Ax25A','50Ax50Ax25Ax25A','50Ax50Ax32Ax32A','50Ax50Ax40Ax40A']

nipple_st=['Nipple', 'Reducing_nipple','Hose_nipple','Piece_nipple','Both_nipple']
nipple_R_d=[
'10Ax08A','15Ax08A','15Ax10A','20Ax08A','20Ax10A','20Ax15A','25Ax10A','25Ax15A','25Ax20A','40Ax20A',
'40Ax25A','50Ax20A','50Ax25A','50Ax40A',
]
socket_st=['Socket_parrallel','Socket_taper','Socket_difference']
socket_d=[
'08Ax06A','10Ax06A','08Ax06A','10Ax08A','15Ax08A','15Ax10A','20Ax08A','20Ax10A','20Ax15A','25Ax10A',
'25Ax15A','25Ax20A','32Ax15A','32Ax20A','32Ax25A','40Ax20A','40Ax25A','40Ax32A','50Ax25A','50Ax32A','50Ax40A',
]

cap_st=['cap']
plug_st=['plug']

cros_st=['equal', 'difference']

union_st=['Union']

bend_st=['45B','45SB','90B','90SB']

Y_st=['45Y','90Y']
Y_90RY_d=['40Ax25Ax25A','50Ax40Ax40A']

bush_st=['Bushing']
bush_d=[
'08Ax06A','10Ax08A','15Ax08A','15Ax10A','20Ax08A','20Ax10A','20Ax15A','25Ax08A',
'25Ax10A','25Ax15A','25Ax20A','32Ax10A','32Ax15A','32Ax20A','32Ax25A',
'40Ax10A','40Ax15A','40Ax20A','40Ax32A','40Ax25A','50Ax15A','50Ax20A','50Ax25A',
'50Ax32A',
]

globe_st=['JIS5k','JIS10k']
gate_st=['JIS5k','JIS10k']
check_st=['JIS10k']

#                              基準径(おねじ)            基準径の位置 めねじ   おねじ
#                  山の高さ　丸み　　外径 　有効径   谷径  管端から     部の長さ 部の長さ  肉厚   めねじ部 　おねじ部
#        ピッチP,     h,      r,    D0,     d2,     d1,   a,         l',     l,        t,      A1,   　  A2,      A3,    f
screws={
'06A':(  0.9071, 0.581,   0.12,  9.728,  9.147,  8.566,  3.97,       6,    8,          2.0,    15,      9,       11,     2.5),
'08A':(  1.3368, 0.856,   0.18, 13.157, 12.301, 11.445,  6.01,       8,    11,         2.5,    19,     12,       14,     3.7),
'10A':(  1.3368, 0.856,   0.18, 16.662, 15.806, 14.950,  6.35,       9,    12,         2.2,    23,     14,       17,     3.7),
'15A':(  1.8143, 1.162,   0.25, 20.955, 19.793, 18.631,  8.16,      11,    15,         2.5,    27,     18,       22,     5.0),
'20A':(  1.8143, 1.162,   0.25, 26.441, 25.279, 24.117,  9.53,      13,    17,         3.0,    33,     24,       27,     5.0),
'25A':(  2.3091, 1.479,   0.32, 33.249, 31.770, 30.291, 10.39,      15,    19,         3.0,    41,     30,       34,     6.4),
'32A':(  2.3091, 1.479,   0.32, 41.910, 40.431, 38.952, 12.70,      17,    22,         3.5,    50,     39,       43,     6.4),
'40A':(  2.3091, 1.479,   0.32, 47.803, 46.324, 44.845, 12.70,      18,    22,         3.5,    56,     44,       49,     6.4),
'50A':(  2.3091, 1.479,   0.32, 59.614, 58.135, 56.656, 15.88,      20,    26,         4.0,    69,     56,       61,     7.5),
'65A':(  2.3091, 1.479,   0.32, 75.184, 73.705, 72.226, 17.46,      23,    30,         4.5,    86,     72,       76,     7.5),
}

#直管             1,      2,      3,     4,     5,     6,     7,     8,     9
#                SGP,STPG,STS,STPT,STPA,STPL,         SUS-TP
#                SGP     Sch20, Sch40,  Sch60, Sch80, Sch5S, Sch10S,Sch20S,Sch40
#d0,      d2,    t,      t,     t,      t,     t,     t,     t,     t,     t,
tubes={
'06A':(  10.5,   2.0,    0,    1.7,     2.2,   2.4,   1.00,  1.20,  1.5,  1.7),
'08A':(  13.8,   2.3,    0,    2.2,     2.4,   3.0,   1.20,  1.65,  2.0,  2.2),
'10A':(  17.3,   2.3,    0,    2.3,     2.8,   3.2,   1.20,  1.65,  2.0,  2.3),
'15A':(  21.7,   2.8,    0,    2.8,     3.2,   3.7,   1.65,  2.10,  2.5,  2.8),
'20A':(  27.2,   2.8,    0,    2.9,     3.4,   3.9,   1.65,  2.10,  2.5,  2.9),
'25A':(  34.0,   3.2,    0,    3.4,     3.9,   4.5,   1.65,  2.80,  2.5,  3.4),
'32A':(  42.7,   3.5,    0,    3.6,     4.5,   4.9,   1.65,  2.80,  3.0,  3.6),
'40A':(  48.6,   3.5,    0,    3.7,     4.5,   5.1,   1.65,  2.80,  3.0,  3.7),
'50A':(  60.5,   3.8,  3.2,    3.9,     4.9,   5.5,   1.65,  2.80,  3.5,  3.9),
'65A':(  76.3,   4.2,  4.5,    5.2,     6.0,   7.0,   2.10,  3.00,  3.5,  5.2),
}

# JIS5k   管外形　　　フランジ内径
#         d0,     d2,    d4,      d5,   t0,     E,       n,        f,    d3,    d6,      r,     T
JIS5k={
'15A':(   21.7,  22.2,   60,	  80,	 9,	12,	 4,        1,    44,    29,      1.9,   13),
'20A':(   27.2,  27.7,   65,	  85,	10,	12,	 4,        1,    49,    35,      2.0,   15),
'25A':(   34.0,  34.5,   75,	  95,	10,	12,	 4,        1,    59,    43,      2.0,   17),
'32A':(   42.7,  43.2,   90,	 115,	12,	15,	 4,        2,    70,    52,      2.0,   19),
'40A':(   48.6,  49.1,   95,	 120,	12,	15,	 4,        2,    75,    58,      2.0,   20),
'50A':(   60.5,  61.1,  105,	 130,	14,	15,	 4,        2,    85,    70,      2.0,   24),
'65A':(   76.3,  77.1,  130,	 155,	14,	15,	 4,        2,   110,    89,      2.0,   27),
}


# JIS10k
#         d0,     d2,    d4,      d5,   t0,     E,       n,        f,    d3,    d6,      r,   T
JIS10k={
'15A':(   21.7,  22.2,   70,	  95,	12,	15,	 4,        1,    51,    29,      1.9,   16),
'20A':(   27.2,  27.7,   75,	 100,	14,	15,	 4,        1,    56,    35,      2.0,   20),
'25A':(   34.0,  34.5,   90,	 125,	14,	19,	 4,        1,    67,    43,      2.0,   20),
'32A':(   42.7,  43.2,  100,	 135,	16,	19,	 4,        2,    76,    52,      2.0,   22),
'40A':(   48.6,  49.1,  105,	 140,	16,	19,	 4,        2,    81,    58,      2.0,   24),
'50A':(   60.5,  61.1,  120,	 155,	16,	19,	 4,        2,    96,    70,      2.0,   24),
'65A':(   76.3,  77.1,  140,	 175,	18,	19,	 4,        2,   116,    89,      2.0,   27),
}


#エルボ(同径)
#         A,   A45,   B
elbows = {
'06A':(   17,  16,    25.4),
'08A':(   19,  17,    25.4),
'10A':(  23,  19,    25.4),
'15A':(  27,  21,    25.4),
'20A':(  32,  25,    25.4),
'25A':(  38,  29,    25.4),
'32A':(  46,  34,    31.8),
'40A':(  48,  37,    38.1),
'50A':(  57,  42,    50.8),
'65A':(  69,  49,    63.5),
}

#エルボ(径違い)
#              A,   B,   c0,   m
elbows_rl = {
'10Ax08A':(    20,  22,  0.0,  0),
'15Ax08A':(    24,  24,  2.0,  0),
'15Ax10A':(   26,  25,  0.0,  0),
'20Ax10A':(   28,  28,  3.0,  0),
'20Ax15A':(   29,  30,  1.0,  0),
'25Ax15A':(   32,  33,  3.0,  0),
'25Ax20A':(   34,  35,  2.0,  0),
'32Ax15A':(   34,  38,  9.5,  0),
'32Ax20A':(   38,  40,  6.5,  0),
'32Ax25A':(   40,  42,  2.5,  0),
'40Ax15A':(   35,  42, 12.5,  0),
'40Ax20A':(   38,  43,  9.5,  0),
'40Ax25A':(   41,  45,  5.5,  0),
'40Ax32A':(   45.001,  48,  1.0,  0),
'50Ax15A':(   38,  48,  19.0, 0),
'50Ax20A':(   41,  49,  16.0, 0),
'50Ax25A':(   44,  51,  12.0, 0),
'50Ax32A':(   48,  54,  7.5,  0),
'50Ax40A':(   52,  55,  4.5,  0),
}

#ストリートエルボ(めすおす)
#         A,   B
elbows_sl = {
'06A':(   17,  26),
'08A':(   19,  30),
'10A':(  23,  35),
'15A':(  27,  40),
'20A':(  32,  47),
'25A':(  38,  54),
'32A':(  46,  62),
'40A':(  48,  68),
'50A':(  57,  79),
'65A':(  69,  92),
}

#径違いストリートエルボ(めすおす)
#           A,   B
elbows_rsl = {
'25Ax20A':(   34,  51),
'32Ax25A':( 40,  61),
}

#同径チーズ
#        A
tees_e={
'06A':(17,0),
'08A':(19,0),
'10A':(23,0),
'15A':(27,0),
'20A':(32,0),
'25A':(38,0),
'32A':(46,0),
'40A':(48,0),
'50A':(57,0),
}

#径違いチーズ
#               A,   B
tees_d={
'10Ax10Ax08A':( 20,  22),
'15Ax15Ax08A':( 24,  24),
'15Ax15Ax10A':( 26,  25),
'20Ax20Ax10A':( 28,  28),
'20Ax20Ax15A':( 29,  30),
'25Ax25Ax10A':( 30,  31),
'25Ax25Ax15A':( 32,  33),
'25Ax25Ax20A':( 34,  35),
'32Ax32Ax15A':( 34,  38),
'32Ax32Ax20A':( 38,  40),
'32Ax32Ax25A':( 40,  42),
'40Ax40Ax15A':( 35,  42),
'40Ax40Ax20A':( 38,  43),
'40Ax40Ax25A':( 41,  45),
'40Ax40Ax32A':( 45,  48),
'50Ax50Ax15A':( 38,  48),
'50Ax50Ax20A':( 41,  49),
'50Ax50Ax25A':( 44,  51),
'50Ax50Ax32A':( 48,  54),
'50Ax50Ax40A':( 52,  55),
}

#クロス
#        A
cross_e={
'15A':( 27,0),
'20A':( 32,0),
'25A':( 38,0),
'32A':( 46,0),
'40A':( 48,0),
'50A':( 57,0),
}

#径違いクロス
#                   A,   B
cross_d={
'40Ax40Ax25Ax25A':( 41,  45),
'50Ax50Ax25Ax25A':( 44,  51),
'50Ax50Ax32Ax32A':( 48,  54),
'50Ax50Ax40Ax40A':( 52,  55),
}

#ニップル
#        L,    E,    n,   B,  dk
nipples ={
'06A':(  32,   11,   6,   14, 12.0),
'08A':(  34,   12,   6,   17, 15.0),
'10A':(  36,   13,   6,   21, 19.0),
'15A':(  42,   16,   6,   26, 25.0),
'20A':(  47,   18,   6,   32, 31.0),
'25A':(  52,   20,   6,   38, 37.5),
'32A':(  56,   22.001,   6,   46, 44.5),
'40A':(  60,   23,   6,   52, 52.0),
'50A':(  66,   26.5,   8,   63, 60.0),
}

#ホースニップル(キッツ)
#        L,    E1,   E2,  d0,  d1,   D,   n,   B
nipples_h ={
'08A':(  37,   20,   12,  5,   7,    8,   6,   17),
'10A':(  44,   25,   13,  7,   9,   10.5, 6,   21),
'15A':(  53,   30,   16, 10,  13,   14,   6,   26),
'20A':(  66,   40,   18, 15,  16,   20.5, 6,   32),
'25A':(  80,   50,   20, 20,  22,   27,   6,   38),
'32A':(  90,   56,   22.001, 26,  30,   33.5, 6,   46),
'40A':(  97,   60,   23, 32,  35,   40,   6,   54),
'50A':( 110,   69,   27, 44,  47,   53,   8,   63),
}

#長ニップル(キッツ)
#        L,     E
nipples_p ={
'08A':(  100,   9.8),
'10A':(  100,  10.1),
'15A':(  100,  13.2),
'20A':(  100,  14.6),
'25A':(  100,  16.8),
'32A':(  100,  19.1),
'40A':(  100,  19.1),
'50A':(  100,  23.4),
}

#径違いニップル
#            L,    E1,   E2,   n,   B
nipples_d ={
'10Ax08A':(  35,   13,   12,   6,  21),
'15Ax08A':(  38,   16,   12,   6,  26),
'15Axx10A':( 39,   16,   13,   6,  26),
'20Ax08A':(  41,   18,   12,   6,  32),
'20Ax10A':(  42,   18,   13,   6,  32),
'20Ax15A':(  45,   18,   16,   6,  32),
'25Ax10A':(  45,   20,   13,   6,  38),
'25Ax15A':(  48,   20,   16,   6,  38),
'25Ax20A':(  50,   20,   18,   6,  38),
'40Ax20A':(  55,   23,   18,   6,  54),
'40Ax25A':(  57,   23,   20,   6,  54),
'50Ax20A':(  59,   25,   18,   8,  63),
'50Ax25A':(  61,   25,   20,   8,  63),
'50Ax40A':(  64,   25,   23,   8,  63),
}

#ユニオン
#        b1,     b2,     d1,     n,  B1(つば),B2(ナット),dk,  H
unions_d={
'06A':(  15.0,   16.5,   12.5,   8,  15,    25,     12.0, 13.0),
'08A':(  17.0,   18.0,   16.5,   8,  19,    31,     15.0, 13.5),
'10A':(  19.0,   20.5,   20.0,   8,  23,    37,     19.0, 16.0),
'15A':(  21.0,   21.5,   24.0,   8,  27,    42,     25.0, 17.0),
'20A':(  24.5,   26.0,   30.0,   8,  33,    49,     31.0, 18.5),
'25A':(  27.0,   29.0,   38.0,   8,  41,    59,     37.5, 20.0),
'32A':(  30.0,   32.0,   46.0,  10,  50,    69,     44.5, 22.0),
'40A':(  33.0,   35.5,   53.0,  10,  56,    78,     52.0, 24.5),
'50A':(  37.0,   39.5,   65.0,  10,  69,    93,     60.0, 27.0),
}

#ソケット   パラレル         テーパー
#        D,      L,    D,  L
socket_p={
'06A':(  13.8,   20,   15.0, 23),
'08A':(  17.0,   25,   19.0, 29),
'10A':(  21.0,   26,   22.0, 30),
'15A':(  25.0,   33,   27.0, 38),
'20A':(  31.0,   36,   33.0, 40),
'25A':(  38.0,   43,   40.0, 45),
'32A':(  47.0,   48,   49.0, 51),
'40A':(  53.0,   48,   55.5, 54),
'50A':(  66.0,   56,   68.0, 64),
}

#径違いソケット
#          L
sockets_d={
'08Ax06A':(25,0),
'10Ax06A':(28,0),
'10Ax08A':(28,0),
'15Ax08A':(34,0),
'15Ax10A':(34,0),
'20Ax08A':(38,0),
'20Ax10A':(38,0),
'20Ax15A':(38,0),
'25Ax10A':(42,0),
'25Ax15A':(42,0),
'25Ax20A':(42,0),
'32Ax15A':(48,0),
'32Ax20A':(48,0),
'32Ax25A':(48,0),
'40Ax20A':(52,0),
'40Ax25A':(52,0),
'40Ax32A':(52,0),
'50Ax25A':(58,0),
'50Ax32A':(58,0),
'50Ax40A':(58,0),
}

#キャップ
#        D,      H
caps_d={
'06A':(  18,   15.5),
'08A':(  22,   17.5),
'10A':(  26,   19.5),
'15A':(  30,   21.0),
'20A':(  36,   24.0),
'25A':(  44,   28.0),
'32A':(  53,   30.0),
'40A':(  60,   32.0),
'50A':(  73,   36.0),
}

#プラグ
#        L,    B,      b
plugs_d={
'06A':(  16,   7,      7),
'08A':(  19,   9,      8),
'10A':(  21,  12,      9),
'15A':(  25,  14,     10),
'20A':(  28,  17,     11),
'25A':(  31,  19,     12),
'32A':(  35,  23,     13),
'40A':(  36,  26,     14),
'50A':(  41,  32,     15),
}

#ベンド    45ベンド    90ベンド
#        A,   r,   A,   r
bends_d={
'06A':(  25,  20,  32,  20),
'08A':(  29,  24,  38,  24),
'10A':(  35,  28,  44,  28),
'15A':(  38,  34,  52,  34),
'20A':(  45,  45,  65,  45),
'25A':(  55,  55,  82,  55),
'40A':(  70,  82, 115,  82),
'50A':(  85, 105, 140, 105),
}

#Y       45Y       90Y
#        A,   B,   A,   B
Ys_d={
'06A':(  10,  25,  10,  17),
'08A':(  13,  31,  13,  19),
'10A':(  14,  35,  14,  23),
'15A':(  18,  42,  18,  28),
'20A':(  20,  50,  20,  32),
'25A':(  23,  62,  23,  38),
'40A':(  30,  82,  30,  48),
'50A':(  34,  99,  34,  57),
}

#RY
#                A,   B
RYs_d={
'40Ax25Ax25A':(  28,  38),
'50Ax40Ax40A':(  31,  48),
}

#ブッシング
#            L,    E,    n,   B
bushs_d ={
'08Ax06A':(  17,   12,   6,  17),
'10Ax08A':(  18,   13,   6,  21),
'15Ax08A':(  21,   16,   6,  26),
'15Axx10A':( 21,   16,   6,  26),
'20Ax08A':(  24,   18,   6,  32),
'20Ax10A':(  24,   18,   6,  32),
'20Ax15A':(  24,   18,   6,  32),
'25Ax08A':(  27,   20,   6,  38),
'25Ax10A':(  27,   20,   6,  38),
'25Ax15A':(  27,   20,   6,  38),
'25Ax20A':(  27,   20,   6,  38),
'32Ax10A':(  30,   22,   6,  46),
'32Ax15A':(  30,   22,   6,  46),
'32Ax20A':(  30,   22,   6,  46),
'32Ax25A':(  30,   22,   6,  46),

'40Ax10A':(  32,   23,   6,  54),
'40Ax15A':(  32,   23,   6,  54),
'40Ax20A':(  32,   23,   6,  54),
'40Ax32A':(  32,   23,   6,  54),
'40Ax25A':(  32,   23,   6,  54),
'50Ax15A':(  36,   25,   8,  63),
'50Ax20A':(  36,   25,   8,  63),
'50Ax25A':(  36,   25,   8,  63),
'50Ax32A':(  36,   25,   8,  63),
}

#                 引っかかり　　外径/谷径　　　有効径　　　  内径/谷径   面取り      ナット高
#        ピッチP,    H1,     d/D,       d2/D2,    d1/D1,     dk,     m,     m1,    s0,    e0,  x0
regular={
'M3':(    0.50,   0.271,    3,        2.675,    2.459,      5.3,   2.4,  1.8,    5.5,   6.4, 0.0),
'M4':(    0.70,   0.379,    4,        3.545,    3.242,      6.8,   3.2,  2.4,    7.0,   8.1, 0.2),
'M5':(    0.80,   0.433,    5,        4.480,    4.134,      7.8,   4.0,  3.2,    8.0,   9.2, 0.0),
'M6':(    1.00,   0.541,    6,        5.350,    4.917,      9.8,   5.0,  3.6,   10.0,  11.5, 0.0),
'M8':(    1.25,   0.677,    8,        7.188,    6.647,     12.5,   6.5,  5.0,   13.0,  15.0, 0.0),
'M10':(   1.50,   0.812,   10,        9.026,    8.376,     16.5,   8.0,  6.0,   17.0,  19.6, 0.0),
'M12':(   1.75,   0.947,   12,       10.863,   10.106,     18.0,  10.0,  7.0,   19.0,  21.9, 0.2),
'M16':(   2.00,   1.083,   16,       14.701,   13.835,     23.0,  13.0, 10.0,   24.0,  27.7, 0.8),
'M20':(   2.50,   1.353,   20,       18.376,   17.294,     29.0,  16.0, 12.0,   30.0,  34.6, 1.0),
'M24':(   3.00,   1.624,   24,       22.051,   20.752,     34.0,  19.0, 14.0,   36.0,  41.6, 0.0),
'M30':(   3.50,   1.894,   30,       27.727,   26.211,     44.0,  24.0, 18.0,   46.0,  53.1, 0.0),
'M36':(   4.00,   2.165,   36,       33.402,   31.670,     53.0,  29.0, 21.0,   55.0,  63.5, 0.0)
}

#玉形弁　JIS B 2011
#       弁座  面間　ハンドル　　　　　肉厚　　R     弁棒   二面幅
#       d,   L,   H0,  D1, a,     d1,   d3,   s1,   s2,   s3,  d4,  Nut
globes_5k={
'15A':( 15,  60,  90,  63, 2.0,   32,   8.5,  29,   23,   26,  6,   'M6'),
'20A':( 20,  70, 105,  63, 2.5,   38,   8.5,  35,   23,   26,  6,   'M6'),
'25A':( 25,  80, 120,  80, 2.5,   48,  10.0,  44,   29,   29,  8,   'M8'),
'32A':( 32, 100, 135, 100, 3.0,   58,  11.0,  54,   35,   32,  8,   'M8'),
'40A':( 40, 110, 145, 100, 3.5,   66,  11.0,  60,   38,   32,  8,   'M8'),
'50A':( 50, 135, 175, 125, 4.0,   82,  13.0,  74,   46,   38, 10,   'M10'),
}

#玉形弁　JIS B 2011
#       弁座  面間　ハンドル　　　　　肉厚　　R     弁棒   二面幅
#       d,   L,   H0,  D1, a,     d1,   d3,   s1,   s2,   s3,  d4,  Nut
globes_10k={
'08A':( 10,  50,  90,  50, 2.5,   24,   8.5,  21,   21,   26,  6,   'M6'),
'10A':( 12,  55,  95,  63, 2.5,   26,   8.5,  24,   21,   26,  6,   'M6'),
'15A':( 15,  65, 110,  63, 3.0,   34,   8.5,  29,   23,   26,  6,   'M6'),
'20A':( 20,  80, 125,  80, 3.0,   40,  10.0,  35,   29,   29,  8,   'M8'),
'25A':( 25,  90, 140, 100, 3.0,   50,  11.0,  44,   32,   32,  8,   'M8'),
'32A':( 32, 105, 170, 125, 3.5,   60,  13.0,  54,   35,   38, 10,   'M10'),
'40A':( 40, 120, 180, 125, 4.0,   68,  13.0,  60,   41,   38, 10,   'M10'),
'50A':( 50, 140, 205, 140, 4.5,   84,  15.0,  74,   50,   41, 12,   'M12'),
'65A':( 65, 180, 240, 180, 4.5,   84,  15.0,  74,   50,   41, 12,   'M12'),
'80A':( 80, 200, 275, 200, 4.5,   84,  15.0,  74,   50,   41, 12,   'M12'),
}

#仕切弁　JIS B 2011
#       弁座  面間　ハンドル　　　　　肉厚　　R     弁棒   二面幅
#       d,   L,   H0,  D1, a,     d1,   d3,   s1,   s2,   s3,  d4,  Nut
gates_5k={
'15A':( 15,  50, 145,  63, 2.0,   32,   8.5,  29,   26,   26,  6,   'M6'),
'20A':( 20,  60, 165,  63, 2.5,   38,   8.5,  35,   29,   26,  6,   'M6'),
'25A':( 25,  65, 190,  80, 2.5,   48,  10.0,  44,   32,   29,  8,   'M8'),
'32A':( 32,  75, 225, 100, 3.0,   58,  11.0,  54,   38,   32,  8,   'M8'),
'40A':( 40,  85, 255, 100, 3.5,   66,  11.0,  60,   46,   32,  8,   'M8'),
'50A':( 50,  95, 305, 125, 4.0,   82,  13.0,  74,   58,   38, 10,   'M10'),
}

#仕切弁　JIS B 2011
#       弁座  面間　ハンドル　　　　　肉厚　　R     弁棒   二面幅
#       d,   L,   H0,  D1, a,     d1,   d3,   s1,   s2,   s3,  d4,  Nut
gates_10k={
'15A':( 15,  55, 150,  63, 3.0,   34,   8.5,  29,   26,   26,  6,   'M6'),
'20A':( 20,  65, 175,  80, 3.0,   40,  10.0,  35,   32,   29,  8,   'M8'),
'25A':( 25,  70, 205, 100, 3.5,   50,  11.0,  44,   38,   32,  8,   'M8'),
'32A':( 32,  80, 245, 125, 3.5,   60,  13.0,  54,   46,   38, 10,   'M10'),
'40A':( 40,  90, 275, 125, 4.0,   68,  13.0,  60,   50,   38, 10,   'M10'),
'50A':( 50, 100, 325, 140, 4.5,   84,  15.0,  74,   63,   41, 12,   'M12'),
}

#逆止弁(スイング式)　JIS B 2011
#       弁座  面間　    　肉厚　 　R     二面幅
#       d,   L,  H0,  a,     d1,   s1,   s2
checks_10k={
'10A':( 12,  55, 40,  3.0,   34,   24,   21),
'15A':( 15,  65, 45,  3.0,   34,   29,   23),
'20A':( 20,  80, 50,  3.0,   40,   35,   29),
'25A':( 25,  90, 60,  3.5,   50,   44,   32),
'32A':( 32, 105, 70,  3.5,   60,   54,   35),
'40A':( 40, 120, 80,  4.0,   68,   60,   41),
'50A':( 50, 140, 95,  4.5,   84,   74,   50),
}

      
class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 292)
        Dialog.move(1000, 0)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #管種
        self.label_lst= QtGui.QLabel(Dialog)
        self.label_lst.setGeometry(QtCore.QRect(20, 0, 160, 22))
        self.label_lst.setObjectName("label_lst")
        self.comboBox_lst = QtGui.QComboBox(Dialog)
        self.comboBox_lst.setGeometry(QtCore.QRect(70, 0, 160, 22))
        self.comboBox_lst.setObjectName("comboBox_lst")
        self.label_l= QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(70, 22, 160, 22))
        self.label_l.setObjectName("label_l")
        #規格
        self.label_standard= QtGui.QLabel(Dialog)
        self.label_standard.setGeometry(QtCore.QRect(20, 45, 50, 22))
        self.label_standard.setObjectName("label_standard")
        self.comboBox_standard = QtGui.QComboBox(Dialog)
        self.comboBox_standard.setGeometry(QtCore.QRect(70, 45, 160, 22))
        self.comboBox_standard.setObjectName("comboBox_standard")
        #口径
        self.label_dia= QtGui.QLabel(Dialog)
        self.label_dia.setGeometry(QtCore.QRect(20, 68, 50, 22))
        self.label_dia.setObjectName("label_standard")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(70, 68, 160, 20))
        self.comboBox_dia.setObjectName("comboBox_dia")
        #切管
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(75, 94, 61, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_1 = QtGui.QLineEdit(Dialog)
        self.lineEdit_1.setGeometry(QtCore.QRect(127, 94, 45,15))
        self.lineEdit_1.setObjectName("lineEdit_1")
        #ライセンスキー
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(75, 119, 170, 15))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 119, 50, 15))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_1 = QtGui.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(192, 117, 40, 20))
        self.pushButton_1.setObjectName("pushButton_1")
        #Create
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 144, 150, 20))
        self.pushButton.setObjectName("pushButton")
        #チェックボックス
        self.checkbox = QtGui.QCheckBox(Dialog)
        self.checkbox.setGeometry(QtCore.QRect(180, 90, 90, 23))
        self.checkbox.setObjectName("checkbox")
        #img
        self.label_img = QtGui.QLabel(Dialog)
        self.label_img.setGeometry(QtCore.QRect(0, 174, 250, 100))
        self.label_img.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base, "data","JIS_Flange.png")
        self.label_img.setPixmap(QtGui.QPixmap(img_path))
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img.setObjectName("label_img")
        self.retranslateUi(Dialog)
        self.retranslateUi(Dialog)
        self.comboBox_lst.addItems(lst)
        ta=flg
        self.comboBox_standard.clear()
        self.comboBox_standard.addItems(ta)
        dia=tube_d[3:]
        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(dia)
        self.comboBox_lst.setCurrentIndex(1)
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_lst2)
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_lst.setCurrentIndex(0)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_standard)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.f_create)
        QtCore.QObject.connect(self.pushButton_1, QtCore.SIGNAL("pressed()"), self.license)
        QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL("checked()"), self.f_create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        try:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ねじ込み継手", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
            self.label_l.setText(QtGui.QApplication.translate("Dialog", "管材", None, QtGui.QApplication.UnicodeUTF8))
            self.label_lst.setText(QtGui.QApplication.translate("Dialog", "管材", None, QtGui.QApplication.UnicodeUTF8))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None, QtGui.QApplication.UnicodeUTF8))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None, QtGui.QApplication.UnicodeUTF8))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None, QtGui.QApplication.UnicodeUTF8))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
            self.checkbox.setText(QtGui.QApplication.translate("Dialog", "ねじ表示", None, QtGui.QApplication.UnicodeUTF8))

        except:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ねじ込み継手", None))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))
            self.label_l.setText(QtGui.QApplication.translate("Dialog", "管材", None))
            self.label_lst.setText(QtGui.QApplication.translate("Dialog", "管材", None))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None))
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None))
            self.checkbox.setText(QtGui.QApplication.translate("Dialog", "ねじ表示", None))

    def on_lst3(self):#
        ta=lst
        self.comboBox_lst.clear()
        self.comboBox_lst.addItems(ta)

    def on_lst2(self):#管長
        #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
        if key=='06' :
            L=100
        elif key=='15' :
            L=5500
        else :
            L=''

        self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))

    def license(self):
        x = self.lineEdit.text()
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        with open(joined_path, mode='w') as ff:
            ff.write(x)
            ff.close()

    def on_lst(self):
        global key
        global ta
        global dia
        global sa
        global xlc
        self.comboBox_standard.clear()
        key = self.comboBox_lst.currentText()[:2]
        sa=l_lst[key]
        b=sa
        self.label_l.setText(QtGui.QApplication.translate("Dialog", str(sa), None))
        pic='img_n' + key + '.png'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "data",pic)
        self.label_img.setPixmap(QtGui.QPixmap(joined_path))
        xcf='2153987651329bc7526586915547'
        
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        ff= open(joined_path)
        data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", str(data1), None))
        ff.close()
        if key=='00' :#---------------------------------------------------------
            ta=flg
            self.comboBox_standard.clear()
            self.comboBox_standard.addItems(ta)
            st=self.comboBox_standard.currentText()
            dia=tube_d[3:]
            self.comboBox_dia.clear()
            self.comboBox_dia.addItems(dia)
        elif key=='01' :
            ta=elbow_st
        elif key=='02' :
            ta=bend_st
        elif key=='03':
            ta=tee_st
        elif key=='04':
            ta=Y_st
        elif key=='05' :
            ta=cross_st
        elif key=='06' :
            ta=nipple_st
        elif key=='07' :
            ta=union_st
        elif key=='08' :
            ta=socket_st
        elif key=='09' :
            ta=cap_st
        elif key=='10' :
            ta=plug_st
        elif key=='11' :
            ta=bush_st
        elif key=='12' :
            ta=globe_st
        elif key=='13' :
            ta=gate_st
        elif key=='14' :
            ta=check_st
        elif key=='15' :
            ta=tube
        self.comboBox_standard.clear()
        self.comboBox_standard.addItems(ta)
        #xlc=xcf[13:17]
        xlc='***'
        #self.label_l.setText(QtGui.QApplication.translate("Dialog", xlc, None, QtGui.QApplication.UnicodeUTF8))
    def on_standard(self):
        global FC
        global dia
        global pic
        st=self.comboBox_standard.currentText()
        if key=='00' :
            pic='img_n' + key + '.png'
            dia=tube_d[3:]
            FC='フランジ'
        elif key=='01':
            pic='img_' + st + '.png'
            #st=self.comboBox_standard.currentText()
            if st=='90RL':
                dia=elbow_rl
                FC="径違いめすエルボ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いめすエルボ", None))
            elif st=='90RSL':
                dia=elbow_rsl
                FC= "径違いめすおすエルボ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いめすおすエルボ", None))
            elif st=='45L':
                dia=tube_d
                FC="45エルボ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "45エルボ", None))
            elif st=='90L':
                dia=tube_d
                FC="エルボ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "エルボ", None))
            elif st=='90SL':
                dia=tube_d
                FC="めすおすエルボ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "めすおすエルボ", None))

        elif key=='02':
            pic='img_' + st + '.png'
            st=self.comboBox_standard.currentText()
            if st=='45B' :
                dia=bend_d
                FC="45ベンド"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "45ベンド", None))
            elif st=='90B':
                dia=bend_d
                FC="90ベンド"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "90ベンド", None))
            elif st=='45SB':
                dia=bend_d
                FC="45めすおすベンド"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "45めすおすベンド", None))
            elif st=='90SB':
                dia=bend_d
                FC="90めすおすベンド"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "90めすおすベンド", None))

        elif key=='04' :
            pic='img_' + st + '.png'
            if st=='45Y':
                pic='img_' + st + '.png'
                dia=bend_d
                FC="45Y"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "45Y", None))
            elif st=='90Y':
                pic='img_' + st + '.png'
                dia=bend_d
                FC="90Y"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "90Y", None))
            elif st=='90RY':
                pic='img_' + st + '.png'
                dia=Y_90RY_d
                FC="90RY"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "90RY", None))

        elif key=='03' or key=='05' :
            pic='img_' + st + '.png'
            if st=='T':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="同径チーズ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "同径チーズ", None))
            elif st=='RT':
                pic='img_' + st + '.png'
                dia=tee_d
                FC="径違いチーズ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いチーズ", None))
            elif st=='Cr':
                pic='img_' + st + '.png'
                dia=tube_d [1:]
                FC="同径クロス"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "同径クロス", None))
            elif st=='RCr':
                pic='img_' + st + '.png'
                dia=RCr_d
                FC="径違いクロス"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いクロス", None))
        elif key=='06':
            if st=='Nipple' :
                pic='img_' + st + '.png'
                dia=tube_d
                FC="同径ニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "同径ニップル", None))
            elif st=='Piece_nipple':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="片長ニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "片長ニップル", None))
            elif st=='Both_nipple':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="両長ニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "両長ニップル", None))
            elif st=='Reducing_nipple' :
                pic='img_' + st + '.png'
                dia=nipple_R_d
                FC="径違いニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いニップル", None))
            elif st=='Hose_nipple':
                pic='img_' + st + '.png'
                dia=tube_d[1:]
                FC="ホースニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "ホースニップル", None))
            elif st=='Piece_nipple':
                pic='img_' + st + '.png'
                dia=tube_d[1:]
                FC="片長ニップル"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "片長ニップル", None))

        elif key=='07':
            pic='img_' + st + '.png'
            dia=tube_d
            FC='直管'
        elif key=='08':
            if st=='Socket_parrallel':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="ソケット"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "ソケット", None))
            elif st=='Socket_taper':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="テーパソケット"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "テーパソケット", None))
            elif st=='Socket_difference':
                pic='img_' + st + '.png'
                dia=socket_d
                FC="径違いソケット"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "径違いソケット", None))

        elif key=='09':
            if st=='cap':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="キャップ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "キャップ", None))

        elif key=='10':
            if st=='plug':
                pic='img_' + st + '.png'
                dia=tube_d
                FC="プラグ"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "プラグ", None))
        elif key=='11':
            if st=='Bushing':
                pic='img_' + st + '.png'
                dia=bush_d
                FC="ブッシング"
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", "ブッシング", None))
        elif key=='12':
            pic='img_Globe_Valve.png'
            if st=='JIS5k':
                dia=tube_d[3:]
            elif st=='JIS10k':
                dia=tube_d[1:]
            FC="玉形弁"
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", "玉形弁", None))
        elif key=='13':
            pic='img_Gate_Valve.png'
            if st=='JIS5k':
                dia=tube_d[3:]
            elif st=='JIS10k':
                dia=tube_d[3:]
            FC= "仕切弁"
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", "仕切弁", None))
        elif key=='14':
            pic='img_Check_Valve.png'
            if st=='JIS10k':
                dia=tube_d[2:]
            FC= "逆止弁"
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", "逆止弁", None))

        elif key=='15':
            pic='img_Straight_Pipe.png'
            dia=tube_d
            FC="直管"
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", "直管", None))

        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(dia)
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "data",pic)
        self.label_img.setPixmap(QtGui.QPixmap(joined_path))
        #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(pic), None, QtGui.QApplication.UnicodeUTF8))
        try:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None))

    def f_create(self):
        lsky=self.lineEdit.text()
        if lsky!=xlc:
            if key > '04':
               lsk='ライセンスキーを入力してください。'
               try:
                   self.label_l.setText(QtGui.QApplication.translate("Dialog", lsk, None, QtGui.QApplication.UnicodeUTF8))
               except:
                   self.label_l.setText(QtGui.QApplication.translate("Dialog", lsk, None))
               return

        def Flange(self):#フランジ本体
            global c00
            global c1
            global st
            global F_Obj
            global label
            global value
            key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            if st=='JIS5k':
                sa = JIS5k[key_1]
            elif st=='JIS10k':
                sa = JIS10k[key_1]
            d0=float(sa[0])/2
            d2=float(sa[1])/2
            d4=float(sa[2])/2
            d5=float(sa[3])/2
            t0=float(sa[4])
            E0=float(sa[5])/2
            n0=int(sa[6])
            f=float(sa[7])
            d3=float(sa[8])/2
            d6=float(sa[9])/2
            r=float(sa[10])
            T=float(sa[11])
            x1=d6-r
            x2=d6+r
            x3=d5-r
            y1=t0+r
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(T), None, QtGui.QApplication.UnicodeUTF8))
            y2=T-r
            x4=r/math.sqrt(2)
            x5=r*(1-1/math.sqrt(2))
            p1=(0,0,0)
            p2=(0,0,T)
            p3=(x1,0,T)
            p4=(x1+x4,0,y2+x4)
            p5=(d6,0,y2)
            p6=(d6,0,y1)
            p7=(d6+x5,0,y1-x4)
            p8=(d6+r,0,t0)
            p9=(x3,0,t0)
            p10=(x3+x4,0,t0-x5)
            p11=(d5,0,t0-r)
            p12=(d5,0,f)
            p13=(d3,0,f)
            p14=(d3,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            edge6=Part.makeLine(p8,p9)
            edge7=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p13)
            edge10=Part.makeLine(p13,p14)
            edge11=Part.makeLine(p14,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11])
            #Part.show(aWire)
            pface=Part.Face(aWire)
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            ks=0

            for i in range(n0):
                k=2*math.pi/n0
                r0=d4
                if i==0:
                    x=r0*math.cos(k/2)
                    y=r0*math.sin(k/2)
                else:
                    ks=i*k+k/2
                    x=r0*math.cos(ks)
                    y=r0*math.sin(ks)
                c20 = Part.makeCylinder(E0,t0,Base.Vector(x,y,0),Base.Vector(0,0,1))
                if i==0:
                    c00=c00.cut(c20)
                else:
                    c00=c00.cut(c20)

        def cutter_01(self): #おねじ　ねじなし
            global c00
            global c10
            global pipe
            #key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            a=float(sa[6])
            l=float(sa[8])*1.2
            s=math.atan(0.5/16)
            d10=D0-a*math.tan(s)
            d20=d10+l*math.tan(s)
            t=float(sa[9])
            A2=float(sa[11])/2
            sa1=tubes[key_1]
            A20=float(sa1[0])/2
            t=sa1[3]
            d0=A20-t

            if key=='00':
                p1=Base.Vector(0,0,0)
                p2=Base.Vector(d10,0,0)
                p3=Base.Vector(D0,0,a)
                p4=Base.Vector(0,0,a)
                p5=Base.Vector(d20,0,l)
                p6=Base.Vector(0,0,l)
            else:
                if key=='11' or key=='02' or key=='10':
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
            #Part.show(c10)

        def cutter_01a(self): #おねじ　ねじなし 管用
            global c00
            global c10
            global pipe
            #key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            a=float(sa[6])

            a=sa[6]
            f=sa[13]
            l=a+f

            s=math.atan(0.5/16)
            d10=D0-a*math.tan(s)
            d20=d10+l*math.tan(s)
            t=float(sa[9])
            A2=float(sa[11])/2
            sa1=tubes[key_1]
            A20=float(sa1[0])/2
            t=sa1[3]
            d0=A20-t

            if key=='00':
                p1=Base.Vector(0,0,0)
                p2=Base.Vector(d10,0,0)
                p3=Base.Vector(D0,0,a)
                p4=Base.Vector(0,0,a)
                p5=Base.Vector(d20,0,l)
                p6=Base.Vector(0,0,l)
            else:
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
            #Part.show(c10)
        def cutter_011(self): #めねじカッター　ねじなし穴
            global c00
            global c10
            global pipe
            #key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            a=float(sa[6])
            l=float(sa[7])
            s=math.atan(0.5/16)
            x=l*math.tan(s)
            d10=D0-x
            p1=Base.Vector(0,0,0)
            p2=Base.Vector(D0,0,0)
            p3=Base.Vector(d10,0,l)
            p4=Base.Vector(0,0,l)

            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c10=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            #Part.show(c10)

        def male_thread(self):#おねじ　ねじあり カッター用
            global c00
            global c10
            global pipe
            global p
            global h
            global r
            global D0
            global d1
            global a
            #key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            l=float(sa[8])*1.2
            if key=='01':
                #a=0.8*l
                a=float(sa[6])
            else:
                a=float(sa[6])
            s=math.atan(0.5/16)
            d10=d1-a*math.tan(s)
            d20=d10+l*math.tan(s)
            p1=Base.Vector(0,0,0)
            p2=Base.Vector(d10,0,0)
            p3=Base.Vector(d20,0,l)
            p4=Base.Vector(0,0,l)
            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c10=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            cb1= Part.makeCylinder(d10,p,Base.Vector(0,0,-p),Base.Vector(0,0,1),360)
            c10=c10.fuse(cb1)
            #ねじ断面
            c0=0
            x0=d10+(h-r)
            sr=27.5
            s=math.radians(sr)
            s0=math.degrees(math.atan(0.5/16))
            x=r*math.sin(s)
            y=r*math.cos(s)
            z1=(h-r+c0)*math.tan(s)+r/(math.cos(s))
            p1=(0,0,0)
            p2=(-x,0,y)
            p3=(h-2*r+x,0,p/2-y)
            p4=(h-r,0,p/2)
            p5=(h-2*r,0,p/2)
            p6=(h-2*r,0,-p/2)
            p7=(h-r,0,-p/2)
            p8=(h-2*r+x,0,-(p/2-y))
            p9=(-x,0,-y)
            p10=(h-r+1,0,p/2)
            p11=(h-r+1,0,-p/2)
            p12=(h-r+c0,0,z1)
            p13=(h-r+c0,0,-z1)
            edge1 = Part.makeCircle(r, Base.Vector(p1), Base.Vector(0,1,0), 90+sr, 270-sr)
            edge2 = Part.makeLine(p2,p12)
            edge3 = Part.makeLine(p12,p13)
            edge4 = Part.makeLine(p13,p9)
            #らせん_sweep
            helix=Part.makeHelix(p,l+0.1,d10,s0,False)
            #Part.show(helix)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            cutProfile.Placement=App.Placement(App.Vector(-x0,0,-p/2),App.Rotation(App.Vector(0,1,0),s0))
            wface=Part.Face(cutProfile)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c10=c10.fuse(pipe)
            #Part.show(c10)

        def male_thread2(self):#おねじ　ねじあり　軸用
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            #global key_1
            global c00
            global c10
            global pipe
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
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

            if key=='11' or key=='02' or key=='10' :
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
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
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
            #Part.show(helix)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            #Part.show(cutProfile)
            if key_1=='20A' or key_1=='32A' or key_1=='40A' :
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
            #Part.show(c10)
            #面取り



        def male_thread3(self):#R平行おねじ　ねじあり　軸用
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            global key_1
            global c00
            global c10
            global pipe
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径

            a=float(sa[6])
            t=float(sa[9])
            A2=float(sa[11])/2

            sa=socket_p[key_1]
            l=float(sa[1])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
            d0=A2-t+0.001
            s=0
            s0=math.degrees(s)
            d10=d1-a*math.tan(s)
            d11=d10-p*math.tan(s)
            d20=d10+l*math.tan(s)
            d21=d20+p*math.tan(s)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            p1=Base.Vector(0,0,0)
            p2=Base.Vector(d10,0,0)
            p3=Base.Vector(0,0,l)
            p4=Base.Vector(d20,0,l)
            p5=Base.Vector(0,0,-p)
            p6=Base.Vector(d11,0,-p)
            p7=Base.Vector(0,0,l+p)
            p8=Base.Vector(d21,0,l+p)
            plist=[p5,p7,p8,p6,p5]
            pwire=Part.makePolygon(plist)
            #Part.show(pwire)
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
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
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
            #Part.show(helix)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            if key_1=='20A' or key_1=='32A' or key_1=='40A':
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p/2),App.Rotation(App.Vector(0,1,0),-s0))
            else:
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p),App.Rotation(App.Vector(0,1,0),-s0))
            wface=Part.Face(cutProfile)
            #Part.show(wface)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c10=c10.fuse(pipe)

            #Part.show(c10)

            p3=Base.Vector(0,0,l)
            p5=Base.Vector(0,0,-2*p)
            c11 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p5)),Base.Vector(0,0,1))
            #Part.show(c11)
            c10=c10.cut(c11)
            c12 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p3)),Base.Vector(0,0,1))
            #Part.show(c12)
            c10=c10.cut(c12)

        def hexagon(self):
            global c10
            dia=self.comboBox_dia.currentText()
            sa1=tubes[key_1]
            d2=float(sa1[0])/2
            t=sa1[3]
            d0=d2-t

            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(dia), None, QtGui.QApplication.UnicodeUTF8))

            if key=='11':
                sa=bushs_d[dia]
                L00=sa[0]
                sa = nipples[key_1]
            else:
                sa = nipples[key_1]
                L00=sa[0]
            L=L00
            E=sa[1]
            n=sa[2]
            B=sa[3]/2
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L), None, QtGui.QApplication.UnicodeUTF8))

            #sa = nipples[key_1]
            dk=float(sa[4])/2
            if key=='11':
                H=L-E
            else:
                H=L-2*E

            x1=B
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(B), None, QtGui.QApplication.UnicodeUTF8))
            s=math.pi/n
            e0=x1/math.cos(s)
            x=e0*math.cos(s)
            y=e0*math.sin(s)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(B), None, QtGui.QApplication.UnicodeUTF8))
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
            #Part.show(w10)
            wface = Part.Face(w10)
            c1=wface.extrude(Base.Vector(0,0,H))
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H), None, QtGui.QApplication.UnicodeUTF8))
            #面取り
            p1=(dk,0,H)
            p2=(e0,0,H)
            p3=(e0,0,H-(e0-dk)*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0,0,1),360)
            c1=c1.cut(c2)
            p1=(dk,0,0)
            p2=(e0,0,0)
            p3=(e0,0,(e0-dk)*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
            c10=c1.cut(c2)
            #Part.show(c10)

        def hexagon2(self):
            global c10

            sa = nipples_h[key_1]
            L=sa[0]
            E1=sa[1]
            E2=sa[2]
            d0=sa[3]
            n=sa[6]
            B=sa[7]/2

            sa=nipples[key_1]
            dk=float(sa[4])/2
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d0), None, QtGui.QApplication.UnicodeUTF8))
            H=L-(E1+E2)
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
            #六角面
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c1=wface.extrude(Base.Vector(0,0,H))
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H), None, QtGui.QApplication.UnicodeUTF8))
            #面取り
            p1=(dk,0,H)
            p2=(e0,0,H)
            p3=(e0,0,H-(e0-dk)*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0,0,1),360)
            c1=c1.cut(c2)
            p1=(dk,0,0)
            p2=(e0,0,0)
            p3=(e0,0,(e0-dk)*math.tan(math.pi/6))
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0.0,0.0),Base.Vector(0.0,0.0,1.0),360)
            c10=c1.cut(c2)

        def hexagon3(self):#メートルネジ　ナット
            global c10

            doc=App.ActiveDocument
            V=FreeCAD.Vector
            #key=self.comboBox_2.currentText()
            sa = regular[key_1]
            p=float(sa[0])
            H1=float(sa[1])
            D0=float(sa[2])/2
            D2=float(sa[3])/2
            D1=float(sa[4])/2
            dk=float(sa[5])/2
            m=float(sa[6])
            m1=float(sa[7])
            s0=float(sa[8])
            e0=float(sa[9])/2
            x0=float(sa[10])
            # directions
            XP = V(1,0,0)
            XN = V(-1,0,0)
            YP = V(0,1,0)
            YN = V(0,-1,0)
            ZP = V(0,0,1)
            ZN = V(0,0,-1)

            H0=0.866025*p
            x=H1+H0/4
            y=x*math.tan(math.pi/6)
            a=p/2-y

            #六角面
            x1=e0*math.cos(math.pi/6)
            y1=e0*math.sin(math.pi/6)
            p1=(x1,y1,0)
            p2=(0,e0,0)
            p3=(-x1,y1,0)
            p4=(-x1,-y1,0)
            p5=(0,-e0,0)
            p6=(x1,-y1,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            table='1'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(table), None, QtGui.QApplication.UnicodeUTF8))
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1+1,H)
            c2=c2.cut(c3)
            Part.show(c2)


        if key=='00':
            global c00
            global pipe
            global c10
            global label
            key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            if st=='JIS5k':
                sa = JIS5k[key_1]
            elif st=='JIS10k':
                sa = JIS10k[key_1]
            Flange(self)
            c1=c00
            #Part.show(c1)
            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c1=c1.cut(c2)
            else:
                cutter_01(self)
                c2=c10
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label = 'Flange_' + st + "_" + str(key_1)+'_'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(label), None, QtGui.QApplication.UnicodeUTF8))
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
            vo = F_Obj.ViewObject
            value=0
            vo.Transparency = value

        elif key=='01':
            #global key_1
            dia=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            if st=='45L' or st=='90L':
                key_1=self.comboBox_dia.currentText()
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                sa=elbows[key_1]
                A=sa[0]
                A45=sa[1]
                B=sa[2]
                sa1=screws[key_1]
                t=sa1[9]
                A1=float(sa1[10])/2
                L=float(sa1[7])
                r=0.7*2*A1
                if st=='45L':
                    s0=22.5
                    La=A45
                elif st=='90L':
                    s0=45.0
                    La=A
                d0=A1-t
                s=math.radians(s0)
                L_2=r*math.tan(s)
                L1=La-L_2
                x=r*math.cos(2*s)
                y=r*math.sin(2*s)
                x1=L1*math.cos(math.pi/2-2*s)
                y1=L1*math.sin(math.pi/2-2*s)
                x2=(L1-L)*math.cos(math.pi/2-2*s)
                y2=(L1-L)*math.sin(math.pi/2-2*s)
                p1=(0,0,0)
                p2=(0,0,L1)
                p3=(r,0,L1)
                p4=(r-x,0,L1+y)
                p5=(r-x+x1,0,L1+y+y1)
                p6=(0,0,L)
                p7=(r-x+x2,0,L1+y+y2)
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeCircle(r, Base.Vector(p3), Base.Vector(0,1,0),180,180+2*s0)
                edge3 = Part.makeLine(p4,p5)
                edge4 = Part.makeCircle(A1, Base.Vector(0,0,L1), Base.Vector(0,0,1), 0, 360)
                edge5 = Part.makeCircle(d0+0.1, Base.Vector(0,0,L1), Base.Vector(0,0,1), 0, 360)
                edge6 = Part.makeLine(p6,p2)
                edge7 = Part.makeLine(p4,p7)
                aWire = Part.Wire([edge1,edge2,edge3])
                if st=='45L':
                    aWire2 = Part.Wire([edge6,edge2,edge7])
                elif st=='90L':
                    aWire2 = Part.Wire([edge2])

                profile = Part.Wire([edge4])
                profile1 = Part.Wire([edge5])
                makeSolid=True
                isFrenet=True
                c1 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
                c2 = Part.Wire(aWire2).makePipeShell([profile1],makeSolid,isFrenet)
                c1=c1.cut(c2)
                #Part.show(c1)
                #Part.show(c2)

                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                    #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.cut(c2)
                    #c1=c1.cut(c21)
            elif st=='90SL':
                key_1=self.comboBox_dia.currentText()
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                sa=elbows_sl[key_1]
                A=sa[0]
                B=sa[1]
                sa1=screws[key_1]
                t=sa1[9]
                d1=float(sa1[10])/2
                d2=float(sa1[11])/2
                d01=d1-t
                d02=d2-t
                L01=float(sa1[7])
                L02=float(sa1[8])
                r=d1
                L1=A-r
                L2=B-r
                s0=45
                p1=(0,0,0)
                p2=(0,0,L01)
                p3=(0,0,L1)
                p4=(r,0,L1)
                p5=(r,0,A)
                p6=(B-L02,0,A)
                p7=(B,0,A)
                edge1 = Part.makeLine(p1,p3)
                edge2 = Part.makeCircle(r, Base.Vector(p4), Base.Vector(0,1,0),180,180+2*s0)
                edge3 = Part.makeLine(p5,p6)
                aWire2 = Part.Wire([edge2])
                circle1=Part.makeCircle(d1, Base.Vector(p1), Base.Vector(0,0,1), 0, 360)
                circle2=Part.makeCircle(d1, Base.Vector(p3), Base.Vector(0,0,1), 0, 360)
                circle21=Part.makeCircle(d01, Base.Vector(p3), Base.Vector(0,0,1), 0, 360)
                circle3=Part.makeCircle(d2, Base.Vector(p5), Base.Vector(1,0,0), 0, 360)
                circle31=Part.makeCircle(d02, Base.Vector(p5), Base.Vector(1,0,0), 0, 360)
                circle4=Part.makeCircle(d2, Base.Vector(p6), Base.Vector(1,0,0), 0, 360)
                profile1 = Part.Wire([circle1])
                profile2 = Part.Wire([circle2])
                profile21 = Part.Wire([circle21])
                profile3 = Part.Wire([circle3])
                profile31 = Part.Wire([circle31])
                profile4 = Part.Wire([circle4])
                makeSolid=True
                isFrenet=True
                #外径
                c1 = Part.makeCylinder(d1,L1,Base.Vector((p1)),Base.Vector(0,0,1))
                c2 = Part.Wire(aWire2).makePipeShell([profile2,profile3],makeSolid,isFrenet)
                c3 = Part.makeCylinder(d2,L2-L02,Base.Vector((p5)),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)
                #内径
                c11 = Part.makeCylinder(d01,L1-L01,Base.Vector((p2)),Base.Vector(0,0,1))
                c21 = Part.Wire(aWire2).makePipeShell([profile21,profile31],makeSolid,isFrenet)
                c31 = Part.makeCylinder(d02,L2-L02,Base.Vector((p5)),Base.Vector(1,0,0))
                c11=c11.fuse(c21)
                c11=c11.fuse(c31)
                c1=c1.cut(c11)
                if self.checkbox.isChecked():
                    s0=45
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread2(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                    #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c1=c1.cut(c2)
                    cutter_01(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                    #Part.show(c2)
            elif st=='90RL':
                dia=self.comboBox_dia.currentText()
                st=self.comboBox_standard.currentText()
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                sa=elbows_rl[dia]
                A=sa[0]
                B=sa[1]
                c0=sa[2]
                sa1=screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L01=float(sa1[7])
                sa1=screws[key_2]
                t2=sa1[9]
                d2=float(sa1[10])/2
                L02=float(sa1[7])
                s0=45
                s=math.radians(s0)
                La=A
                Lb=B
                r=2
                d01=d1-t1
                d02=d2-t2
                L1=A-L01

                L2=B-L02
                m=d1-d2
                m1=d01-d02
                p1=(0,0,0)
                p2=(d1,0,0)
                p3=(d1,0,A-m)
                p4=(0,0,A+d2)
                p5=(0,0,L01-(m-m1))
                p6=(d01,0,L01-(m-m1))
                p7=(d01,0,A-m)
                p8=(0,0,A-m)
                p9=(L2,0,A)
                p10=(B,0,A)
                p11=(0,0,A+d01-m)
                #外径
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeCircle(d1, Base.Vector(p8), Base.Vector(0,1,0),270,0)
                edge4 = Part.makeLine(p4,p1)
                aWire = Part.Wire([edge1,edge2,edge3,edge4])
                pface = Part.Face(aWire)
                c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)

                c2 = Part.makeCylinder(d2+0.001,B,Base.Vector((p10)),Base.Vector(1,0,0))#枝管
                c2.Placement=App.Placement(App.Vector(-B,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.fuse(c2)

                #内径
                edge1 = Part.makeLine(p5,p6)
                edge2 = Part.makeLine(p6,p7)
                edge3 = Part.makeCircle(d01, Base.Vector(p8), Base.Vector(0,1,0),270,0)
                edge4 = Part.makeLine(p11,p5)
                aWire = Part.Wire([edge1,edge2,edge3,edge4])
                pface = Part.Face(aWire)
                #Part.show(pface)
                c11=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c11.Placement=App.Placement(App.Vector(0,0,m-m1),App.Rotation(App.Vector(0,0,1),0))
                c21 = Part.makeCylinder(d02+0.001,L2,Base.Vector((p9)),Base.Vector(1,0,0))#枝管
                c21.Placement=App.Placement(App.Vector(-L2,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.cut(c21)
                c1=c1.cut(c11)

                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L2,0,A),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                    #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),0))
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(y+y1), None, QtGui.QApplication.UnicodeUTF8))
                    c1=c1.cut(c2)

            elif st=='90RSL':
                #global key_1
                dia=self.comboBox_dia.currentText()
                st=self.comboBox_standard.currentText()
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                sa=elbows_rsl[dia]
                A=sa[0]
                B=sa[1]
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                sa1=screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L01=float(sa1[7])
                sa1=screws[key_2]
                t2=sa1[9]
                d2=float(sa1[11])/2
                L02=float(sa1[8])
                s0=45
                s=math.radians(s0)
                La=A
                Lb=B
                r=2
                d01=d1-t1
                d02=d2-t2
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(y+y1), None, QtGui.QApplication.UnicodeUTF8))
                L1=A-L01
                L2=B-L02
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L1), None, QtGui.QApplication.UnicodeUTF8))
                m=d1-d2
                m1=d01-d02
                p1=(0,0,0)
                p2=(d1,0,0)
                p3=(d1,0,A-m)
                p4=(0,0,A+d2)
                p5=(0,0,L01-(m-m1))
                p6=(d01,0,L01-(m-m1))
                p7=(d01,0,A-m)
                p8=(0,0,A-m)
                p9=(L2,0,A)
                p10=(B,0,A)
                p11=(0,0,A+d01-m)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                #外径
                edge1 = Part.makeLine(p1,p2)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeCircle(d1, Base.Vector(p8), Base.Vector(0,1,0),270,0)
                edge4 = Part.makeLine(p4,p1)
                aWire = Part.Wire([edge1,edge2,edge3,edge4])
                pface = Part.Face(aWire)
                c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c2 = Part.makeCylinder(d2,B-L02,Base.Vector((p10)),Base.Vector(1,0,0))#枝管
                c2.Placement=App.Placement(App.Vector(-B,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.fuse(c2)
                #Part.show(c1)
                #内径
                edge1 = Part.makeLine(p5,p6)
                edge2 = Part.makeLine(p6,p7)
                edge3 = Part.makeCircle(d01, Base.Vector(p8), Base.Vector(0,1,0),270,0)
                edge4 = Part.makeLine(p11,p5)
                aWire = Part.Wire([edge1,edge2,edge3,edge4])
                pface = Part.Face(aWire)
                #Part.show(pface)
                c11=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c11.Placement=App.Placement(App.Vector(0,0,m-m1),App.Rotation(App.Vector(0,0,1),0))
                c21 = Part.makeCylinder(d02,L2,Base.Vector((p9)),Base.Vector(1,0,0))#枝管
                c21.Placement=App.Placement(App.Vector(-L2,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.cut(c21)
                c1=c1.cut(c11)
                #Part.show(c1)
                #Part.show(c21)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread2(self)
                    c2=c10
                    #Part.show(c2)
                    c2.Placement=App.Placement(App.Vector(B+0.001,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                    #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),0))
                    c1=c1.cut(c2)
                    #Part.show(c1)
                    key_1=key_2
                    cutter_01(self)
                    c2=c10
                    #Part.show(c2)
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(y+y1), None, QtGui.QApplication.UnicodeUTF8))
                    c1=c1.fuse(c2)

            doc=App.ActiveDocument
            label = 'Elbow_' + st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='02':
            dia=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            key_1=self.comboBox_dia.currentText()
            sa1=screws[key_1]
            A1=float(sa1[10])/2
            A2=float(sa1[11])/2
            L=float(sa1[7])
            LL=float(sa1[8])

            sa=tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            D0=A1-t

            if st[:2]=='45':
                s0=22.5
                sa=bends_d[key_1]
                La=sa[0]
                r=sa[1]
            elif st[:2]=='90':
                s0=45
                sa=bends_d[key_1]
                La=sa[2]
                if dia=='50A' or dia=='10A':
                    r=float(sa[3])*0.9
                else:
                    r=sa[3]

            a=1.8*L
            b=a
            d0=A2-t
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st[:2]), None, QtGui.QApplication.UnicodeUTF8))
            s=math.radians(s0)
            L_2=r*math.tan(s)
            L1=La-L_2
            x=r*math.cos(2*s)
            y=r*math.sin(2*s)
            x1=L1*math.cos(math.pi/2-2*s)
            y1=L1*math.sin(math.pi/2-2*s)
            x2=(L1-L)*math.cos(math.pi/2-2*s)
            y2=(L1-L)*math.sin(math.pi/2-2*s)
            x3=(L1-b)*math.cos(math.pi/2-2*s)
            y3=(L1-b)*math.sin(math.pi/2-2*s)
            p1=(0,0,0)
            p2=(0,0,L1)
            p3=(r,0,L1)
            p4=(r-x,0,L1+y)
            p5=(r-x+x1,0,L1+y+y1)
            p6=(0,0,L)
            p7=(r-x+x2,0,L1+y+y2)
            p8=((r-r*math.cos(2*s))+x3,0,L1+y+y3)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(r, Base.Vector(p3), Base.Vector(0,1,0),180,180+2*s0)
            edge3 = Part.makeLine(p4,p5)
            edge4 = Part.makeCircle(A2, Base.Vector(0,0,L1), Base.Vector(0,0,1), 0, 360)
            edge5 = Part.makeCircle(d0, Base.Vector(0,0,L1), Base.Vector(0,0,1), 0, 360)
            edge6 = Part.makeLine(p6,p2)
            edge7 = Part.makeLine(p4,p7)
            aWire = Part.Wire([edge1,edge2,edge3])
            aWire2 = Part.Wire([edge6,edge2,edge7])
            aWire3 = Part.Wire([edge6,edge2,edge7])
            profile = Part.Wire([edge4])
            profile1 = Part.Wire([edge5])
            makeSolid=True
            isFrenet=True
            c1 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c22 = Part.Wire(aWire2).makePipeShell([profile1],makeSolid,isFrenet)
            c23 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)

            if st=='45B' or st=='90B':
                c2 = Part.makeCylinder(A1,a,Base.Vector(0,0,0),Base.Vector(0,0,1))
                c1=c1.cut(c2)
                c=(A1-A2)*math.sqrt(2)
                p10=Base.Vector(0,0,0)
                p20=Base.Vector(A1,0,0)
                p30=Base.Vector(A1,0,a-c)
                p40=Base.Vector(A2,0,a)
                p50=Base.Vector(0,0,a)
                plist=[p10,p20,p30,p40,p50,p1]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c1=c1.fuse(c2)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                c1=c1.fuse(c2)

                p10=Base.Vector(0,0,L)
                p20=Base.Vector(0,0,a)
                p30=Base.Vector(d0,0,a)
                p40=Base.Vector(D0,0,L)
                plist=[p10,p20,p30,p40,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,L),Base.Vector(0,0,1),360)
                c1=c1.cut(c2)
                c3=c2
                c3.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                c1=c1.cut(c3)

                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.cut(c2)
                c1=c1.cut(c22)
            elif st=='45SB' or st=='90SB':
                c2 = Part.makeCylinder(A1,a,Base.Vector(0,0,0),Base.Vector(0,0,1))
                c2 = Part.makeCylinder(A1,a,Base.Vector(0,0,0),Base.Vector(0,0,1))
                c1=c1.cut(c2)
                c=(A1-A2)*math.sqrt(2)
                p10=Base.Vector(0,0,0)
                p20=Base.Vector(A1,0,0)
                p30=Base.Vector(A1,0,a-c)
                p40=Base.Vector(A2,0,a)
                p50=Base.Vector(0,0,a)
                plist=[p10,p20,p30,p40,p50,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c1=c1.fuse(c2)
                p10=Base.Vector(0,0,L)
                p20=Base.Vector(0,0,a)
                p30=Base.Vector(d0,0,a)
                p40=Base.Vector(D0,0,L)
                plist=[p10,p20,p30,p40,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,L),Base.Vector(0,0,1),360)
                c1=c1.cut(c2)
                c3=c2
                c3.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                #c1=c1.cut(c3)
                c4 = Part.makeCylinder(2*d0,LL,Base.Vector((p1)),Base.Vector(0,0,1))
                c4.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                c1=c1.cut(c4)
                #Part.show(c4)

                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread2(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.fuse(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c1=c1.cut(c2)
                    cutter_01(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.fuse(c2)
                c1=c1.cut(c23)
            doc=App.ActiveDocument
            label ='Bend_'+st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='04':
            dia=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            sa1=screws[key_1]
            A1=float(sa1[10])/2
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A1), None, QtGui.QApplication.UnicodeUTF8))
            A2=float(sa1[11])/2
            L=float(sa1[7])
            LL=float(sa1[8])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L), None, QtGui.QApplication.UnicodeUTF8))
            sa1=screws[key_2]
            A10=float(sa1[10])/2
            A20=float(sa1[11])/2
            L0=float(sa1[7])
            LL0=float(sa1[8])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            sa=tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            D0=A1-t
            sa=tubes[key_2]
            d20=float(sa[0])/2
            t0=sa[3]
            D00=A10-t0
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(D00), None, QtGui.QApplication.UnicodeUTF8))
            if st=='45Y':
                s0=22.5
                sa=Ys_d[key_1]
                A=sa[0]
                B=sa[1]
            elif st=='90Y':
                s0=45
                sa=Ys_d[key_1]
                A=sa[2]
                B=sa[3]
            elif st=='90RY':
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(dia), None, QtGui.QApplication.UnicodeUTF8))
                s0=45
                sa=RYs_d[dia]
                A=sa[0]
                B=sa[1]
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
            a=1.8*L
            a0=1.8*L0
            a1=1.3*L
            b=a
            d0=A2-t
            d00=A20-t0

            if st=='45Y' or st=='90Y':
                x=B*math.cos(math.pi/4)
                y=B*math.sin(math.pi/4)
                x1=(B-a)*math.cos(math.pi/4)
                y1=(B-a)*math.sin(math.pi/4)
                x2=(B-L)*math.cos(math.pi/4)
                y2=(B-L)*math.sin(math.pi/4)
                p1=(0,0,0)
                p2=(0,0,A)
                p3=(0,0,A+B)
                p4=(x,0,A+y)
                p5=(x1,0,A+y1)
                p6=(x2,0,A+y2)
                p7=(-x,0,A+y)
                p8=(-x1,0,A+y1)
                p9=(-x2,0,A+y2)
                if st=='45Y':
                    c1 = Part.makeCylinder(A2,(A+B),Base.Vector(p1),Base.Vector(0,0,1))
                    c11 = Part.makeCylinder(d0,(A+B),Base.Vector(p1),Base.Vector(0,0,1))
                    c21 = Part.makeCylinder(d0,B,Base.Vector(p1),Base.Vector(1,0,0))
                    c21.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),135))
                else:#90Y
                    c1 = Part.makeCylinder(A2,A,Base.Vector(p1),Base.Vector(0,0,1))
                    c11 = Part.makeCylinder(d0,A,Base.Vector(p1),Base.Vector(0,0,1))
                    c2 = Part.makeCylinder(A2,B,Base.Vector(p1),Base.Vector(1,0,0))
                    c2.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),225))
                    c1=c1.fuse(c2)
                    c22 = Part.makeCylinder(d0,B,Base.Vector(p1),Base.Vector(1,0,0))
                    c22.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),225))
                    c1=c1.cut(c11)
                c2 = Part.makeCylinder(A2,B,Base.Vector(p1),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),-45))
                c1=c1.fuse(c2)
                c21 = Part.makeCylinder(d0,B,Base.Vector(p1),Base.Vector(1,0,0))
                c21.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),-45))
                c1=c1.cut(c11)
                c2 = Part.makeCylinder(A2,a,Base.Vector(p1),Base.Vector(0,0,1))#(1)カット
                c1=c1.cut(c2)
                if st=='45Y':
                    c3=c2#(3)カット
                    c3.Placement=App.Placement(App.Vector(p3),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c3)
                elif st=='90Y':
                    c3=c2#(7)カット
                    c3.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                    c1=c1.cut(c3)
                c4=c2#(4)カット
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                c=(A1-A2)*math.sqrt(2)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
                p10=Base.Vector(0,0,0)
                p20=Base.Vector(A1,0,0)
                p30=Base.Vector(A1,0,a-c)
                p40=Base.Vector(A2,0,a)
                p50=Base.Vector(0,0,a)
                plist=[p10,p20,p30,p40,p50,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)#(1)ネック
                c1=c1.fuse(c2)
                if st=='45Y':
                    c3=c2
                    c3.Placement=App.Placement(App.Vector(p3),App.Rotation(App.Vector(0,1,0),180))#(3)ネック
                    c1=c1.fuse(c3)
                elif st=='90Y':
                    c3=c2
                    c3.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))#(7)ネック
                    c1=c1.fuse(c3)
                c4=c2
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))#(4)ネック
                c1=c1.fuse(c4)
                p10=Base.Vector(0,0,L)
                p20=Base.Vector(0,0,a)
                p30=Base.Vector(d0,0,a)
                p40=Base.Vector(D0,0,L)
                plist=[p10,p20,p30,p40,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,L),Base.Vector(0,0,1),360)#(1)接続部カット
                c1=c1.cut(c2)
                if st=='45Y':
                    c3=c2
                    c3.Placement=App.Placement(App.Vector(0,0,A+B),App.Rotation(App.Vector(0,1,0),180))#(3)接続部カット
                    c1=c1.cut(c3)
                elif st=='90Y':
                    c3=c2
                    c3.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))#(7)接続部カット
                    c1=c1.cut(c3)
                c4=c2
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))#(4)接続部カット
                c1=c1.cut(c4)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    if st=='45Y':
                        male_thread(self)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(0,0,A+B-L),App.Rotation(App.Vector(0,1,0),0))
                        c1=c1.cut(c2)
                    elif st=='90Y':
                        male_thread(self)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(p9),App.Rotation(App.Vector(0,1,0),315))
                        c1=c1.cut(c2)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p6),App.Rotation(App.Vector(0,1,0),45))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)#(1)
                    c2=c10
                    c1=c1.cut(c2)
                    if st=='45Y':
                        cutter_011(self)#(4)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(p3),App.Rotation(App.Vector(0,1,0),180))
                        c1=c1.cut(c2)
                    elif st=='90Y':
                        cutter_011(self)#(7)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                        c1=c1.cut(c2)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                    c1=c1.cut(c2)
                    c1=c1.cut(c21)

            elif st=='90RY':
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                #c1=c1.cut(c22)
                x=B*math.cos(math.pi/4)
                y=B*math.sin(math.pi/4)
                x1=(B-a)*math.cos(math.pi/4)
                y1=(B-a)*math.sin(math.pi/4)
                x2=(B-L)*math.cos(math.pi/4)
                y2=(B-L)*math.sin(math.pi/4)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
                p1=(0,0,0)
                p2=(0,0,A)
                p3=(0,0,A+B)
                p4=(x,0,A+y)
                p5=(x1,0,A+y1)
                p6=(x2,0,A+y2)
                p7=(-x,0,A+y)
                p8=(-x1,0,A+y1)
                p9=(-x2,0,A+y2)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
                c1 = Part.makeCylinder(A2,A,Base.Vector(p1),Base.Vector(0,0,1))
                c11 = Part.makeCylinder(d0,A,Base.Vector(p1),Base.Vector(0,0,1))
                #Part.show(c1)
                c2 = Part.makeCylinder(A20,B,Base.Vector(p1),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),225))
                c1=c1.fuse(c2)
                c22 = Part.makeCylinder(d00,B,Base.Vector(p1),Base.Vector(1,0,0))
                c22.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),225))
                c1=c1.cut(c11)
                c2 = Part.makeCylinder(A20,B,Base.Vector(p1),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),-45))
                c1=c1.fuse(c2)
                c21 = Part.makeCylinder(d00,B,Base.Vector(p1),Base.Vector(1,0,0))
                c21.Placement=App.Placement(App.Vector(p2),App.Rotation(App.Vector(0,1,0),-45))
                c1=c1.cut(c11)
                c2 = Part.makeCylinder(A2,a,Base.Vector(p1),Base.Vector(0,0,1))#(1)カット
                c3=Part.makeCylinder(A20,a0,Base.Vector(p1),Base.Vector(0,0,1))#(7)カット
                c3.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                c1=c1.cut(c3)
                c4=c3#(4)カット
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                c=(A1-A2)*math.sqrt(2)
                c0=(A10-A20)*math.sqrt(2)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
                p10=Base.Vector(0,0,0)
                p20=Base.Vector(A1,0,0)
                p30=Base.Vector(A1,0,a-c)
                p40=Base.Vector(A2,0,a)
                p50=Base.Vector(0,0,a)
                plist=[p10,p20,p30,p40,p50,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)#(1)ネック
                c1=c1.fuse(c2)
                p10=Base.Vector(0,0,0)
                p20=Base.Vector(A10,0,0)
                p30=Base.Vector(A10,0,a0-c0)
                p40=Base.Vector(A20,0,a0)
                p50=Base.Vector(0,0,a0)
                plist=[p10,p20,p30,p40,p50,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)#(1)ネック
                c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))#(7)ネック
                c1=c1.fuse(c2)
                c4=c2
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))#(4)ネック
                c1=c1.fuse(c4)
                p10=Base.Vector(0,0,L)
                p20=Base.Vector(0,0,a)
                p30=Base.Vector(d0,0,a)
                p40=Base.Vector(D0,0,L)
                plist=[p10,p20,p30,p40,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,L),Base.Vector(0,0,1),360)#(1)接続部カット
                c1=c1.cut(c2)
                p10=Base.Vector(0,0,L0)
                p20=Base.Vector(0,0,a0)
                p30=Base.Vector(d00,0,a0)
                p40=Base.Vector(D00,0,L0)
                plist=[p10,p20,p30,p40,p10]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,L0),Base.Vector(0,0,1),360)#(7)接続部カット
                c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))#(7)接続部カット
                c1=c1.cut(c2)
                c4=c2
                c4.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))#(4)接続部カット
                c1=c1.cut(c4)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p9),App.Rotation(App.Vector(0,1,0),315))
                    c1=c1.cut(c2)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p6),App.Rotation(App.Vector(0,1,0),45))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)#(1)
                    c2=c10
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)#(7)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                    c1=c1.cut(c2)

                    c2=c10
                    c2.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                    c1=c1.cut(c2)
                c1=c1.cut(c21)
                c1=c1.cut(c22)
            doc=App.ActiveDocument
            label ='Y_'+st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='03' or key=='05':
            #key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='T' or st=='Cr':
                sa=tees_e[key_1]
                A=sa[0]
                sa1=screws[key_1]
                t=sa1[9]
                d1=float(sa1[10])/2
                L=float(sa1[7])
                d0=d1-t
                if st=='T':
                    x=0
                else:
                    x=A
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d1), None, QtGui.QApplication.UnicodeUTF8))
                #外径
                c1 = Part.makeCylinder(d1,2*A,Base.Vector((-A,0,0)),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d1,x+A,Base.Vector((0,-x,0)),Base.Vector(0,1,0))
                c1=c1.fuse(c2)
                #内径
                c3 = Part.makeCylinder(d0,2*A-2*L,Base.Vector((-A+L,0,0)),Base.Vector(1,0,0))
                if st=='Cr':
                    c4 = Part.makeCylinder(d0,2*(A-L),Base.Vector((0,-A+L,0)),Base.Vector(0,1,0))
                else:
                    c4 = Part.makeCylinder(d0,(A-L),Base.Vector((0,0,0)),Base.Vector(0,1,0))

                c3=c3.fuse(c4)
                c1=c1.cut(c3)
                #Part.show(c1)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-A+L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    #Part.show(c2)
                    male_thread(self)
                    c21=c10
                    c21.Placement=App.Placement(App.Vector(A-L,0,0),App.Rotation(App.Vector(0,1,0),90))
                    #c2=c2.fuse(21)
                    c1=c1.cut(c21)
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,A-L,0),App.Rotation(App.Vector(1,0,0),270))
                    if st=='Cr':
                        male_thread(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,-A+L,0),App.Rotation(App.Vector(1,0,0),90))
                        c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-A,0,0),App.Rotation(App.Vector(0,1,0),90))
                    cutter_011(self)
                    c21=c10
                    c21.Placement=App.Placement(App.Vector(A,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,A,0),App.Rotation(App.Vector(1,0,0),90))
                    #Part.show(c2)
                    if st=='Cr':
                        cutter_011(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,-A,0),App.Rotation(App.Vector(1,0,0),270))
                        #Part.show(c21)
                        #c21.Placement=App.Placement(App.Vector(0,-x,0),App.Rotation(App.Vector(1,0,0),90))
                        c2=c2.fuse(c21)

                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(y+y1), None, QtGui.QApplication.UnicodeUTF8))
                    c1=c1.cut(c2)
                    #Part.show(c1)
            elif st=='RT'or st=='RCr':
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                if st=='RT':
                    sa=tees_d[dia]
                    A=sa[0]
                    B=sa[1]

                elif st=='RCr':
                    sa=cross_d[dia]
                    A=sa[0]
                    B=sa[1]
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(A), None, QtGui.QApplication.UnicodeUTF8))
                sa1=screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L1=float(sa1[7])
                d01=d1-t1
                sa1=screws[key_2]
                t2=sa1[9]
                d2=float(sa1[10])/2
                L2=float(sa1[7])
                d02=d2-t2
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                if st=='RT':
                    #外径
                    c1 = Part.makeCylinder(d1,2*A,Base.Vector((-A,0,0)),Base.Vector(1,0,0))
                    c2 = Part.makeCylinder(d2,B,Base.Vector((0,0,0)),Base.Vector(0,1,0))
                    c1=c1.fuse(c2)
                    #内径
                    c3 = Part.makeCylinder(d01,2*A-2*L1,Base.Vector((-A+L1,0,0)),Base.Vector(1,0,0))
                    c4 = Part.makeCylinder(d02,B-L2,Base.Vector((0,0,0)),Base.Vector(0,1,0))
                elif st=='RCr':
                    #外径
                    c1 = Part.makeCylinder(d1,2*A,Base.Vector((-A,0,0)),Base.Vector(1,0,0))
                    c2 = Part.makeCylinder(d2,2*B,Base.Vector((0,-B,0)),Base.Vector(0,1,0))
                    c1=c1.fuse(c2)
                    #内径
                    c3 = Part.makeCylinder(d01,2*A-2*L1,Base.Vector((-A+L1,0,0)),Base.Vector(1,0,0))
                    c4 = Part.makeCylinder(d02,2*B-2*L2,Base.Vector((0,-B+L2,0)),Base.Vector(0,1,0))


                c3=c3.fuse(c4)
                c1=c1.cut(c3)
                #Part.show(c1)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-A+L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    #Part.show(c2)
                    male_thread(self)
                    c21=c10
                    c21.Placement=App.Placement(App.Vector(A-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    #c2=c2.fuse(21)
                    c1=c1.cut(c21)
                    key_1=key_2
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,B-L2,0),App.Rotation(App.Vector(1,0,0),270))
                    c1=c1.cut(c2)
                    if st=='RCr':
                        male_thread(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,-(B-L2),0),App.Rotation(App.Vector(1,0,0),90))
                        c1=c1.cut(c21)
                        #Part.show(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-A,0,0),App.Rotation(App.Vector(0,1,0),90))
                    cutter_011(self)
                    c21=c10
                    c21.Placement=App.Placement(App.Vector(A,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,B,0),App.Rotation(App.Vector(1,0,0),90))
                    c1=c1.cut(c2)
                    if st=='RCr':
                        cutter_011(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,-B,0),App.Rotation(App.Vector(1,0,0),270))
                        c1=c1.cut(c21)
                        #Part.show(c21)
            doc=App.ActiveDocument
            label = 'Tee_' + st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='06':
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='Nipple'or st=='Reducing_nipple':
                if st=='Nipple':
                    sa=nipples[key_1]
                    L=sa[0]
                    E1=sa[1]
                    n=sa[2]
                    B=sa[3]
                    dk=sa[4]
                    sa1=screws[key_1]
                    L1=sa1[8]
                    A1=float(sa1[11])/2
                    sa2=tubes[key_1]
                    d1=float(sa2[0])/2
                    t1=sa2[3]
                    x1=E1-L1
                    d01=d1-t1
                    H=L-2*E1
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(x1), None, QtGui.QApplication.UnicodeUTF8))
                elif st=='Reducing_nipple':
                    sa=nipples_d[dia]
                    L=sa[0]
                    E1=sa[1]
                    E2=sa[2]
                    H=L-(E1+E2)
                    sa=nipples[key_1]
                    n=sa[2]
                    B=float(sa[3])/2
                    dk=float(sa[4])/2
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(E1), None, QtGui.QApplication.UnicodeUTF8))
                    sa1=screws[key_1]
                    L1=sa1[8]
                    A1=float(sa1[11])/2
                    sa1=screws[key_2]
                    L2=sa1[8]
                    A2=float(sa1[11])/2
                    sa2=tubes[key_1]
                    d1=float(sa2[0])/2
                    t1=sa2[3]
                    x1=E1-L1
                    d01=d1-t1
                    sa2=tubes[key_2]
                    d2=float(sa2[0])/2
                    t2=sa2[3]
                    x2=E2-L2
                    d02=d2-t2
                hexagon(self)
                c1=c10

                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(E1), None, QtGui.QApplication.UnicodeUTF8))
                c11 = Part.makeCylinder(A1,x1,Base.Vector((-x1,0,0)),Base.Vector(1,0,0))
                c12 = Part.makeCylinder(d01,x1,Base.Vector((-x1,0,0)),Base.Vector(1,0,0))
                c11=c11.cut(c12)
                c1=c1.fuse(c11)
                #Part.show(c1)
                if st=='Nipple':
                    E2=E1
                    A2=A1
                    d02=d01
                    x2=x1
                c11 = Part.makeCylinder(A2,x2,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c12 = Part.makeCylinder(d02,x2,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c11=c11.cut(c12)
                c1=c1.fuse(c11)
                #Part.show(c1)
                #ナット部穴
                p1=(0,0,0)
                p2=(0,0,d01)
                p3=(H,0,d02)
                p4=(H,0,0)
                plist=[p1,p2,p3,p4,p1]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                #Part.show(pface)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c1=c1.cut(c2)

                if self.checkbox.isChecked():
                    male_thread2(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-E1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    #Part.show(c1)
                    key_1=key_2
                    male_thread2(self)
                    c2=c10
                    if st=='Nipple':
                        E2=E1
                    c2.Placement=App.Placement(App.Vector(H+E2,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_01(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(-E1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    key_1=key_2
                    cutter_01(self)
                    c21=c10
                    if st=='Nipple':
                        E2=E1
                    c21.Placement=App.Placement(App.Vector(H+E2,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.fuse(c21)

            elif st=='Hose_nipple':
                sa1=screws[key_1]
                LL1=sa1[8]
                A1=float(sa1[11])/2
                sa=nipples_h[key_1]
                L=sa[0]
                E1=sa[1]
                E2=sa[2]
                d0=sa[3]/2
                d1=sa[4]/2
                D=sa[5]/2
                sa=tubes[key_1]
                d2=sa[0]/2
                t2=sa[3]
                d02=d2-t2
                x=E2-LL1
                s=math.radians(15)
                h=D-d0
                H1=L-(E1+E2)
                L1=h/(math.tan(s)*2)
                d1=d0+h/2
                n=int(E1/L1)
                c1 = Part.makeCylinder(D,E1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,E1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(n), None, QtGui.QApplication.UnicodeUTF8))
                for i in range(n):
                    p1=(i*L1,0,d1)
                    p2=(i*L1,0,D)
                    p3=(L1,0,D)
                    p4=((i+1)*L1,0,D)
                    if i==0:
                        plist=[p1,p2,p3,p1]
                    else:
                        plist=[p1,p2,p4,p1]
                    pwire=Part.makePolygon(plist)
                    pface = Part.Face(pwire)
                    c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                    c1=c1.cut(c2)
                hexagon2(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(E1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
                c2 = Part.makeCylinder(A1,x,Base.Vector(E1+H1,0,0),Base.Vector(1,0,0))
                c21 = Part.makeCylinder(d02,x,Base.Vector(E1+H1,0,0),Base.Vector(1,0,0))
                c2=c2.cut(c21)
                c1=c1.fuse(c2)
                p1=(0,0,0)
                p2=(0,0,d0)
                p3=(H1,0,d02)
                p4=(H1,0,0)
                plist=[p1,p2,p3,p4,p1]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                #Part.show(pface)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c2.Placement=App.Placement(App.Vector(E1,0,0),App.Rotation(App.Vector(0,0,1),0))
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(E1), None, QtGui.QApplication.UnicodeUTF8))
                c1=c1.cut(c2)
                if self.checkbox.isChecked():
                    male_thread2(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_01(self)
                    c21=c10
                    c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c21)

            elif st=='Piece_nipple' or st=='Both_nipple':
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                sa=screws[key_1]
                a=sa[6]
                f=sa[13]
                L1=a+f
                sa=tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d0=d2-t
                L=float(self.lineEdit_1.text())
                if st=='Piece_nipple':
                    c1 = Part.makeCylinder(d2,L-L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c2 = Part.makeCylinder(d0,L-L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2)
                    if self.checkbox.isChecked():
                        male_thread2(self)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c2)
                    else:
                        cutter_01a(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c21)
                elif st=='Both_nipple':
                    c1 = Part.makeCylinder(d2,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c2 = Part.makeCylinder(d0,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2)
                    if self.checkbox.isChecked():
                        male_thread2(self)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c2)
                        male_thread2(self)
                        c2=c10
                        c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                        c1=c1.fuse(c2)
                    else:
                        cutter_01a(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c21)
                        cutter_01a(self)
                        c21=c10
                        c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                        c1=c1.fuse(c21)

            doc=App.ActiveDocument
            label =  st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='07':
            global w10
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia
            sa=unions_d[key_1]
            b1=sa[0]
            d1=sa[2]/2
            n=sa[3]
            B1=sa[4]/2
            B2=sa[5]/2
            dk=sa[6]/2*2.0
            H=sa[7]
            L1=b1-H/2
            sa=screws[key_1]
            l=sa[7]
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            #ナット8角
            if n==8:
                s=float(math.radians(45))/2
                e0=B1/math.cos(s)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))

                def plst8(self):
                    global w10
                    p1=(e0*math.cos(s),e0*math.sin(s),0)
                    p2=(e0*math.cos(3*s),e0*math.sin(3*s),0)
                    p3=(-e0*math.cos(math.pi-5*s),e0*math.sin(math.pi-5*s),0)
                    p4=(-e0*math.cos(math.pi-7*s),e0*math.sin(math.pi-7*s),0)
                    p5=(-e0*math.cos(s),-e0*math.sin(s),0)
                    p6=(-e0*math.cos(3*s),-e0*math.sin(3*s),0)
                    p7=(e0*math.cos(3*s),-e0*math.sin(3*s),0)
                    p8=(e0*math.cos(s),-e0*math.sin(s),0)
                    plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(e0), None, QtGui.QApplication.UnicodeUTF8))
                    w10=Part.makePolygon(plist)
                    #Part.show(w10)
                    return

                plst8(self)
                #Part.show(w10)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
                w11=w10
                e0=B2/math.cos(s)
                plst8(self)
                w12=w10

            elif n==10:
                s=float(math.radians(36))/2
                e0=B1/math.cos(s)
                def plst10(self):
                    global w10
                    p1=(e0*math.cos(s),e0*math.sin(s),0)
                    p2=(e0*math.cos(3*s),e0*math.sin(3*s),0)
                    p3=(0,e0,0)
                    p4=(-e0*math.cos(3*s),e0*math.sin(3*s),0)
                    p5=(-e0*math.cos(s),e0*math.sin(s),0)
                    p6=(-e0*math.cos(s),-e0*math.sin(s),0)
                    p7=(-e0*math.cos(3*s),-e0*math.sin(3*s),0)
                    p8=(0,-e0,0)
                    p9=(e0*math.cos(3*s),-e0*math.sin(3*s),0)
                    p10=(e0*math.cos(s),-e0*math.sin(s),0)
                    #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(B1), None, QtGui.QApplication.UnicodeUTF8))
                    plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
                    w10=Part.makePolygon(plist)

                    return

                plst10(self)
                #Part.show(w10)
                w11=w10
                e0=B2/math.cos(s)
                plst10(self)
                w12=w10

            wface = Part.Face(w11)
            c1=wface.extrude(Base.Vector(0,0,L1))
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))

            wface = Part.Face(w12)
            c2=wface.extrude(Base.Vector(0,0,H))
            c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)

            wface = Part.Face(w11)
            c2=wface.extrude(Base.Vector(0,0,L1))
            c2.Placement=App.Placement(App.Vector(L1+H,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)
            h1=H-(e0-dk)*math.tan(math.pi/6)
            p1=(dk,0,H)
            p2=(e0,0,H)
            p3=(e0,0,h1)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            w10.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c1.cut(c2)

            h1=(e0-dk)*math.tan(math.pi/6)
            p1=(dk,0,0)
            p2=(e0,0,0)
            p3=(e0,0,h1)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            w10.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            #Part.show(w10)
            wface=Part.Face(w10)
            #Part.show(wface)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c1.cut(c2)
            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(l,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                male_thread(self)
                c2=c10
                #Part.show(c2)
                c2.Placement=App.Placement(App.Vector(b1*2-l,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                #Part.show(c2)
                c2 = Part.makeCylinder(d1,b1*2-2*l,Base.Vector(l,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
            else:
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(b1*2,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                #Part.show(c2)
                c2 = Part.makeCylinder(d1,b1*2-2*l,Base.Vector(l,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                #Part.show(c2)

            doc=App.ActiveDocument
            label =  st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='08':
            #global key_1
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            st=self.comboBox_standard.currentText()
            if st=='Socket_parrallel':
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
                dia=self.comboBox_dia.currentText()
                key_1=dia
                sa=screws[key_1]
                D0=sa[3]/2
                sa=socket_p[key_1]
                D=sa[0]/2
                L=sa[1]
                c1 = Part.makeCylinder(D,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                #Part.show(c1)
                if self.checkbox.isChecked():
                    male_thread3(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)

                else:

                   c2 = Part.makeCylinder(D0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                   c1=c1.cut(c2)
            elif st=='Socket_taper':
                dia=self.comboBox_dia.currentText()
                key_1=dia
                sa=screws[key_1]
                D0=sa[3]/2
                sa=screws[key_1]
                L1=sa[7]
                sa=tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d0=d2-t
                sa=socket_p[key_1]
                D=sa[2]/2
                L=sa[3]
                c1 = Part.makeCylinder(D,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)

            elif st=='Socket_difference':
                dia=self.comboBox_dia.currentText()

                key_1=dia[:3]
                key_2=dia[-3:]
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))
                sa=screws[key_1]
                L1=sa[7]
                sa=screws[key_2]
                L2=sa[7]

                sa=tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d01=d2-t

                sa=tubes[key_2]
                d2=sa[0]/2
                t=sa[3]
                d02=d2-t

                sa=sockets_d[dia]
                La=sa[0]

                L12=L1*1.1
                L22=L2*1.1
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L12), None, QtGui.QApplication.UnicodeUTF8))
                Lb=La-(L12+L22)
                sa=socket_p[key_1]
                D1=sa[0]/2
                sa=socket_p[key_2]
                D2=sa[0]/2
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(D1), None, QtGui.QApplication.UnicodeUTF8))
                edge1 = Part.makeCircle(D1, Base.Vector(0,0,0), Base.Vector(1,0,0), 0, 360)
                edge2 = Part.makeCircle(D1, Base.Vector(L12,0,0), Base.Vector(1,0,0), 0, 360)
                edge3 = Part.makeCircle(D2, Base.Vector(L12+Lb,0,0), Base.Vector(1,0,0), 0, 360)
                edge4 = Part.makeCircle(D2, Base.Vector(La,0,0), Base.Vector(1,0,0), 0, 360)

                edge5 = Part.makeCircle(d01, Base.Vector(L1,0,0), Base.Vector(1,0,0), 0, 360)
                edge6 = Part.makeCircle(d02, Base.Vector(La-L2,0,0), Base.Vector(1,0,0), 0, 360)
                #Part.show(edge2)
                #Part.show(edge3)
                prof1=Part.Wire(edge1)
                prof2=Part.Wire(edge2)
                prof3=Part.Wire(edge3)
                prof4=Part.Wire(edge4)

                prof5=Part.Wire(edge5)
                prof6=Part.Wire(edge6)

                Solid=True
                ruled=False
                closed=False
                maxDegree=5
                c1= Part.makeLoft([prof1,prof2],Solid,ruled,closed,maxDegree)
                c2= Part.makeLoft([prof2,prof3],Solid,ruled,closed,maxDegree)
                c3= Part.makeLoft([prof3,prof4],Solid,ruled,closed,maxDegree)
                c1=c1.fuse(c2)
                c1=c1.fuse(c3)

                c2= Part.makeLoft([prof5,prof6],Solid,ruled,closed,maxDegree)
                c1=c1.cut(c2)

                #Part.show(c1)
                if self.checkbox.isChecked():
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(La-L2,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c10
                    c2.Placement=App.Placement(App.Vector(La,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)

            doc=App.ActiveDocument
            label =  st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        if key=='09' :

            key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=tubes[key_1]
            t=float(sa[3])


            sa=caps_d[key_1]
            d2=float(sa[0])/2
            H=float(sa[1])-t

            sa=screws[key_1]
            l=sa[7]
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            d0=d2-t
            D=2*d0
            R0=D
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L12), None, QtGui.QApplication.UnicodeUTF8))
            r=0.1*D
            h=0.194*D
            L=H-h
            x=d0-r
            s=45.00
            x1=x+r*math.cos(math.radians(s))
            s2=math.degrees(math.asin(x1/R0))
            x11=R0*math.sin(math.radians(15))
            y11=R0*math.cos(math.radians(15))+(H-R0)
            x2=H-R0
            p1=(d0,0,0)
            p2=(d0,L,0)
            p3=(x+r*math.cos(math.radians(s)),L+r*math.sin(math.radians(s)),0)
            p4=(0,H,0)
            p5=(0,x2,0)
            p6=(d2,0,0)
            p7=(d2,L,0)
            p8=(x+(r+t)*math.cos(math.radians(s)),L+(r+t)*math.sin(math.radians(s)),0)
            p9=(0,H+t,0)
            p10=(x,L,0)
            p11=(-d0,0,0)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeCircle(r, Base.Vector(x,L,0), Base.Vector(0,0,1),0, s)
            edge3=Part.Arc(Base.Vector((x+r*math.cos(math.radians(s))),L+r*math.sin(math.radians(s)),0),Base.Vector(R0*math.sin(math.radians(15)),R0*math.cos(math.radians(15))+(H-R0),0),Base.Vector(0,H,0)).toShape()
            edge4 = Part.makeLine(p1,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeCircle(r+t, Base.Vector(x,L,0), Base.Vector(0,0,1),0, s)
            edge7=Part.Arc(Base.Vector((x+(r+t)*math.cos(math.radians(s))),L+(r+t)*math.sin(math.radians(s)),0),Base.Vector((R0+t)*math.sin(math.radians(15)),(R0+t)*math.cos(math.radians(15))+(H-R0),0),Base.Vector(0,H+t,0)).toShape()
            edge8 = Part.makeLine(p4,p9)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            pface=Part.Face(aWire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,1,0),360)

            c2=Part.makeCylinder(d2,l,Base.Vector(0,0,0),Base.Vector(0,1,0))
            c1=c1.cut(c2)
            c1=c1.fuse(c2)

            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,l,0),App.Rotation(App.Vector(1,0,0),90))
                c1=c1.cut(c2)
                #Part.show(c2)
            else:
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),270))
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label = st + "_" + key_1 +"_"
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        if key=='10' :

            key_1=self.comboBox_dia.currentText()
            st=self.comboBox_standard.currentText()
            sa=screws[key_1]
            l=sa[8]

            sa=tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            d0=d2-t


            sa=plugs_d[key_1]
            L=float(sa[0])
            B=float(sa[1])
            b=float(sa[2])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L-1.3*b), None, QtGui.QApplication.UnicodeUTF8))
            c1=Part.makeBox(b,B,B,Base.Vector((0,-B/2,-B/2)),Base.Vector(0,0,1))
            #c2 = Part.makeCylinder(B,b,Base.Vector(0,B/2,B/2),Base.Vector(1,0,0))
            #c1=c1.fuse(c2)
            #Part.show(c1)
            c3 = Part.makeCylinder(B,b,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(1.3*B/2,b,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.cut(c3)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),45))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1[:1]), None, QtGui.QApplication.UnicodeUTF8))


            if self.checkbox.isChecked():
                male_thread2(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(l+b,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                #Part.show(c2)
            else:
                cutter_01(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(l+b,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)

            if float(key_1[:2])>=25:
                c2 = Part.makeCylinder(0.8*B/2,1.3*b,Base.Vector(0.3*b,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(0.8*d0,L-1.3*b,Base.Vector(1.3*b,0,0),Base.Vector(1,0,0))
                c2=c2.fuse(c3)
                #Part.show(c2)
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label =st + "_" + str(key_1)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='11':

            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]

            sa=bushs_d[dia]
            L=sa[0]
            E=sa[1]
            n=sa[2]
            B=sa[3]
            H=L-E
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key_1), None, QtGui.QApplication.UnicodeUTF8))

            sa=nipples[key_1]
            dk=float(sa[4])/2
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(dia), None, QtGui.QApplication.UnicodeUTF8))
            sa1=screws[key_1]
            L1=sa1[8]
            A1=float(sa1[11])/2

            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(dia), None, QtGui.QApplication.UnicodeUTF8))

            sa1=screws[key_2]
            L2=sa1[7]
            A2=float(sa1[11])/2

            sa2=tubes[key_1]
            d1=float(sa2[0])/2
            t1=sa2[3]
            x1=E-L1
            d01=d1-t1

            sa2=tubes[key_2]
            d2=float(sa2[0])/2
            t2=sa2[3]
            x2=E-L2
            d02=d2-t2
            hexagon(self)
            c1=c10
            #Part.show(c1)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            if E-L1>0:
                c2 = Part.makeCylinder(A1,E-L1,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)

            #Part.show(c1)
            if self.checkbox.isChecked():
                male_thread2(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(E+H,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                key_1=key_2
                male_thread2(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L2,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)

            else:
                cutter_01(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(E+H,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                key_1=key_2
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
            c2 = Part.makeCylinder(d01,L-L2,Base.Vector(L2,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(L), None, QtGui.QApplication.UnicodeUTF8))
            doc=App.ActiveDocument
            label =  st + "_" + str(dia)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='12':

            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='JIS5k':
                sa=globes_5k[key_1]
            elif st=='JIS10k':
                sa=globes_10k[key_1]

            d=float(sa[0])
            L=float(sa[1])
            H0=float(sa[2])
            D1=float(sa[3])/2
            a=float(sa[4])
            d1=float(sa[5])
            d3=float(sa[6])/2
            s1=float(sa[7])/2
            s2=float(sa[8])/2
            d4=float(sa[10])/2
            d41=sa[11]
            sa=screws[key_1]
            L1=float(sa[7])
            A1=float(sa[10])/2


            x1=L/2-1.1*L1
            s=math.asin(x1/d1)
            y1=d1-s1
            d10=0.9*2*s2+2*1.0*a
            d11=0.9*2*s2
            H=0.7*L1
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            p1=(H,0,0)
            p2=(H,0,-A1)
            p3=(1.1*L1,0,-A1)
            p4=(L/2,0,-y1)
            p5=(L-1.1*L1,0,-A1)
            p6=(L-H,0,-A1)
            p7=(L-H,0,0)
            p8=(L/2,0,-1.3*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p8),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeLine(p7,p1)

            #本体
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface=Part.Face(aWire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c2 = Part.makeCylinder(d10/2,1.5*A1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c1=c1.fuse(c2)
            c2 = Part.makeCylinder(d11/2,1.5*A1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c1=c1.cut(c2)

            #本体カット
            p1=(-0.2*L1,0,0)
            p2=(L/2,0,-1.3*A1+a)
            p3=(L+0.2*L1,0,0)
            edge1 = Part.makeLine(p1,p3)
            edge2=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            aWire=Part.Wire([edge1,edge2])
            pface=Part.Face(aWire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c1.cut(c20)
            #Part.show(c1)
            #弁座
            k=15
            k0=(90-k)/2
            x=A1*math.tan(math.radians(k))
            x1=1.1*L1
            y2=a*2
            x2=y2*math.tan(math.radians(k0))
            x4=y2*math.sin(math.radians(k0))
            x5=x2-x4
            y5=y2*math.sin(math.radians(k))
            y6=y2-y5
            x3=y6*math.tan(math.radians(k))
            y3=y2*math.cos(math.radians(k0))
            y4=y2-y3

            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(y6), None, QtGui.QApplication.UnicodeUTF8))
            p1=(x1,0,2*A1)
            p2=(x1,0,A1)
            p3=(x1+x,0,0)
            p4=(L-(1.1*L1+x),0,0)
            p5=(L-1.1*L1,0,-A1)
            p6=(L-1.1*L1,0,-2*A1)
            p7=(x1+x-x3,0,y6)
            p8=(x1+x+x5,0,y4)
            p9=(x1+x+x2,0,0)
            p10=(x1+x+x2,0,y2)
            p11=(L-(x1+x+x2),0,0)
            p12=(L-(x1+x+x5),0,-y4)
            p13=(L-(x1+x)+x3,0,-y6)
            p14=(L-(x1+x+x2),0,-y2)

            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p7)
            edge3 = Part.Arc(Base.Vector(p7),Base.Vector(p8),Base.Vector(p9)).toShape()
            edge4 = Part.makeLine(p9,p11)
            edge5 = Part.Arc(Base.Vector(p11),Base.Vector(p12),Base.Vector(p13)).toShape()
            edge6 = Part.makeLine(p13,p5)
            edge7 = Part.makeLine(p5,p6)
            aWire = Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7])
            p1=(x1-a/2,-2*A1,2*A1)
            p2=(x1-a/2,2*A1,2*A1)
            p3=(x1+a/2,2*A1,2*A1)
            p4=(x1+a/2,-2*A1,2*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p1)
            profile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            c3 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c4=c3.common(c20)
            c1=c1.fuse(c4)
            c2 = Part.makeCylinder(d/2,a,Base.Vector(L/2,0,-a/2),Base.Vector(0,0,1))#d
            c1=c1.cut(c2)
            #Part.show(c1)
            #六角面
            x1=s1
            s=math.pi/6
            e0=x1/math.cos(s)
            x=e0*math.cos(s)
            y=e0*math.sin(s)
            p1=(x,y,0)
            p2=(0,e0,0)
            p3=(-x,y,0)
            p4=(-x,-y,0)
            p5=(0,-e0,0)
            p6=(x,-y,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.extrude(Base.Vector(0,0,0.7*L1))
            c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)
            c3=c2
            c3.Placement=App.Placement(App.Vector(L-0.7*L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c3)

            #弁棒受
            h=0.75*H0
            y1=1.5*A1
            y0=y1-2*a
            y2=y1+1.5*a
            y3=y2+1.5*a
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H0), None, QtGui.QApplication.UnicodeUTF8))
            y4=0.7*h
            p1=(d3,0,y0)
            p2=(d3,0,y2)
            p3=(s2-a,0,y2)
            p4=(s2-a,0,y3)
            p5=(1.5*d3,0,y4)
            p6=(d3,0,y4)
            p7=(d3,0,y4+a)
            p8=(1.5*d3,0,y4+a)
            p9=(1.5*d3,0,h)
            p10=(1.5*d3+a,0,h)
            p11=(1.5*d3+a,0,y4)
            p12=(s2,0,y3)
            p13=(s2,0,y2)
            p14=(1.2*s2,0,y2)
            p15=(1.2*s2,0,y1)
            p16=(0.89*s2,0,y1)
            p17=(0.89*s2,0,y0)
            p18=(0.9*s2-a,0,y0)
            p19=(0.9*s2-a,0,y1)
            p20=(d3+a,0,y1)
            p21=(d3+a,0,y0)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H0), None, QtGui.QApplication.UnicodeUTF8))
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #Part.show(c2)
            #キャップ
            p1=(1.5*d3+2*a,0,h-3*a)
            p2=(1.5*d3+2*a,0,h+a)
            p3=(d3,0,h+a)
            p4=(d3,0,h)
            p5=(1.5*d3+a+0.1,0,h)
            p6=(1.5*d3+a+0.1,0,h-3*a)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #弁棒
            hm=d3+3
            y1=H0-(hm+d3+a/2)
            p1=(0,0,a/2)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H0), None, QtGui.QApplication.UnicodeUTF8))
            p2=(0.55*d,0,a/2)
            p3=(0.55*d,0,2.5*a)
            p4=(d3-0.1,0,2.5*a)
            p5=(d3-0.1,0,y1)
            p6=(d4-0.1,0,y1)
            p7=(d4-0.1,0,H0)
            p8=(0,0,H0)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            #Part.show(wface)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #トーラス
            D10=D1-d3
            c2=Part.makeTorus(D10,0.7*d3)
            c2.Placement=App.Placement(App.Vector(L/2,0,y1+0.7*d3),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)

            #ボス
            wface=Part.makePlane(1.4*d3,1.5*d3,Base.Vector(d4,0,y1),Base.Vector(1,0,0))
            #Part.show(wface)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #Part.show(c1)
            #スポーク
            for i in range(3):
                c2 = Part.makeCylinder(0.5*d3,D1-2*d3,Base.Vector(d3,0,y1+0.7*d3),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                c1=c1.fuse(c2)

            #ナット
            key_2=d41
            sa = regular[key_2]
            p=float(sa[0])
            H1=float(sa[1])
            D0=float(sa[2])/2
            D2=float(sa[3])/2
            D1=float(sa[4])/2
            dk=float(sa[5])/2
            m=float(sa[6])
            m1=float(sa[7])
            s0=float(sa[8])
            e0=float(sa[9])/2
            x0=float(sa[10])
            H00=0.866025*p
            x=H1+H00/4
            y=x*math.tan(math.pi/6)
            a=p/2-y

            #六角面
            x1=e0*math.cos(math.pi/6)
            y11=e0*math.sin(math.pi/6)
            p1=(x1,y11,0)
            p2=(0,e0,0)
            p3=(-x1,y11,0)
            p4=(-x1,-y11,0)
            p5=(0,-e0,0)
            p6=(x1,-y11,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)

            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(table), None, QtGui.QApplication.UnicodeUTF8))
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1,H)
            c2=c2.cut(c3)
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-hm),App.Rotation(App.Vector(1,0,0),0))
            #Part.show(c2)
            c1=c1.fuse(c2)

            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                #key_1=key_2
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)

            else:
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label = 'Globe Valve_'+str(st) + '_' + str(key_1)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='13':
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='JIS5k':
                sa=gates_5k[key_1]
            elif st=='JIS10k':
                sa=gates_10k[key_1]
            d=float(sa[0])/2
            L=float(sa[1])
            H0=float(sa[2])
            D1=float(sa[3])/2
            a=float(sa[4])
            d1=float(sa[5])
            d3=float(sa[6])/2
            s1=float(sa[7])/2
            s2=float(sa[8])/2
            d4=float(sa[10])/2
            d41=sa[11]
            sa=screws[key_1]
            L1=float(sa[7])
            A1=float(sa[10])/2
            t=float(sa[9])
            d0=A1-t
            x1=L/2-1.1*L1
            s=math.asin(x1/d1)
            y1=d1-s1
            d10=0.9*2*s2+2*1.0*a
            d11=0.9*2*s2
            H=0.7*L1
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(key), None, QtGui.QApplication.UnicodeUTF8))
            p1=(H,0,0)
            p2=(H,0,-A1)
            p3=(1.1*L1,0,-A1)
            p4=(L/2,0,-y1)
            p5=(L-1.1*L1,0,-A1)
            p6=(L-H,0,-A1)
            p7=(L-H,0,0)
            p8=(L/2,0,-1.3*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p8),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeLine(p7,p1)
            #本体
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface=Part.Face(aWire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c2 = Part.makeCylinder(d10/2,1.5*A1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c1=c1.fuse(c2)
            c2 = Part.makeCylinder(d11/2,A1,Base.Vector(L/2,0,A1+2*a),Base.Vector(0,0,1))
            c1=c1.cut(c2)
            #Part.show(c1)
            #本体カット
            p1=(L1,0,0)
            p2=(L1,0,-d0)
            p3=(1.1*L1,0,-A1+a)
            p4=(L/2,0,-1.3*A1+a)
            p5=(L-1.1*L1,0,-A1+a)
            p6=(L-L1,0,-d0)
            p7=(L-L1,0,0)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeLine(p7,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface=Part.Face(aWire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c1.cut(c20)
            #弁座
            st=math.radians(4)
            g4=2*0.7*d3
            g3=A1*math.tan(st)
            g2=g4-g3
            g5=A1*math.tan(st)
            g6=g4+g5
            g1=g2*math.tan(st)
            g8=g1/math.sin(st)
            g7=g8-g1
            p1=(L/2-g6,0,2*A1)
            p2=(L/2-g6,0,A1)
            p3=(L/2-g4,0,0)
            p4=(L/2-g2,0,-A1)
            p5=(L/2,0,-(A1+g7))
            p6=(L/2,0,-(A1+g1))
            p7=(L/2+g2,0,-A1)
            p8=(L/2+g4,0,0)
            p9=(L/2+g6,0,A1)
            p10=(L/2+g6,0,2*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4=Part.Arc(Base.Vector(p4),Base.Vector(p5),Base.Vector(p7)).toShape()
            edge5 = Part.makeLine(p7,p8)
            edge6 = Part.makeLine(p8,p9)
            edge7 = Part.makeLine(p9,p10)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7])
            #Part.show(aWire)
            p1=(L/2-g6-a,-2*A1,2*A1)
            p2=(L/2-g6-a,2*A1,2*A1)
            p3=(L/2-g6,2*A1,2*A1)
            p4=(L/2-g6,-2*A1,2*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeLine(p3,p4)
            edge4 = Part.makeLine(p4,p1)
            profile = Part.Wire([edge1,edge2,edge3,edge4])
            makeSolid=True
            isFrenet=True
            c2 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c3=c2.common(c20)
            c1=c1.fuse(c3)
            c2=Part.makeBox(1.1*d,2*g6,2*a,Base.Vector(L/2-1.1*d/2,-2*g6/2,A1),Base.Vector(0,0,1))
            c1=c1.cut(c2)
            #六角面
            x1=s1
            s=math.pi/6
            e0=x1/math.cos(s)
            x=e0*math.cos(s)
            y=e0*math.sin(s)
            p1=(x,y,0)
            p2=(0,e0,0)
            p3=(-x,y,0)
            p4=(-x,-y,0)
            p5=(0,-e0,0)
            p6=(x,-y,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.extrude(Base.Vector(0,0,0.7*L1))
            c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)
            c3=c2
            c3.Placement=App.Placement(App.Vector(L-0.7*L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c3)
            #弁棒受
            h=0.75*H0
            y1=1.5*A1
            y0=y1-2*a
            y2=y1+1.5*a
            y3=y2+1.5*a
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H0), None, QtGui.QApplication.UnicodeUTF8))
            y4=0.7*h
            p1=(d3,0,y0)
            p2=(d3,0,y2)
            p3=(s2-a,0,y2)
            p4=(s2-a,0,y3)
            p5=(1.5*d3,0,y4)
            p6=(d3,0,y4)
            p7=(d3,0,y4+a)
            p8=(1.5*d3,0,y4+a)
            p9=(1.5*d3,0,h)
            p10=(1.5*d3+a,0,h)
            p11=(1.5*d3+a,0,y4)
            p12=(s2,0,y3)
            p13=(s2,0,y2)
            p14=(1.2*s2,0,y2)
            p15=(1.2*s2,0,y1)
            p16=(0.89*s2,0,y1)
            p17=(0.89*s2,0,y0)
            p18=(0.9*s2-a,0,y0)
            p19=(0.9*s2-a,0,y1)
            p20=(d3+a,0,y1)
            p21=(d3+a,0,y0)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(H0), None, QtGui.QApplication.UnicodeUTF8))
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #Part.show(c2)
            #キャップ
            p1=(1.5*d3+2*a,0,h-3*a)
            p2=(1.5*d3+2*a,0,h+a)
            p3=(d3,0,h+a)
            p4=(d3,0,h)
            p5=(1.5*d3+a+0.1,0,h)
            p6=(1.5*d3+a+0.1,0,h-3*a)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #弁棒
            g9=A1-1.2*d
            g10=1.2*d
            g11=g9*math.tan(st)
            g12=g6-g11
            g13=2.2*g10*math.tan(st)
            hm=d3+3
            y1=H0-(hm+d3+a/2)
            p1=(0,0,g10)
            p4=(d3-0.1,0,g10)
            p5=(d3-0.1,0,y1)
            p6=(d4-0.1,0,y1)
            p7=(d4-0.1,0,H0)
            p8=(0,0,H0)
            plist=[p1,p4,p5,p6,p7,p8,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            #Part.show(wface)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #Part.show(c2)

            #弁体


            c2 = Part.makeCylinder(g10,2*g12,Base.Vector(L/2-g12,0,0),Base.Vector(1,0,0))
            c1=c1.fuse(c2)

            c2 = Part.makeCylinder(d,L/2-(L1+g12/3),Base.Vector(L1,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)

            c2 = Part.makeCylinder(d,L/2-(L1+g12/3),Base.Vector(L/2+g12/3,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)



            p1=(L/2-g12,-A1,-A1)
            p2=(L/2-g12,-A1,A1)
            p3=(L/2-g13,-A1,-A1)
            plist=[p1,p2,p3,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)


            #トーラス
            D10=D1-d3
            c2=Part.makeTorus(D10,0.7*d3)
            c2.Placement=App.Placement(App.Vector(L/2,0,y1+0.7*d3),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)

            #ボス
            wface=Part.makePlane(1.4*d3,1.5*d3,Base.Vector(d4,0,y1),Base.Vector(1,0,0))
            #Part.show(wface)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #Part.show(c1)
            #スポーク
            for i in range(3):
                c2 = Part.makeCylinder(0.5*d3,D1-2*d3,Base.Vector(d3,0,y1+0.7*d3),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                c1=c1.fuse(c2)

            #ナット
            key_2=d41
            sa = regular[key_2]
            p=float(sa[0])
            H1=float(sa[1])
            D0=float(sa[2])/2
            D2=float(sa[3])/2
            D1=float(sa[4])/2
            dk=float(sa[5])/2
            m=float(sa[6])
            m1=float(sa[7])
            s0=float(sa[8])
            e0=float(sa[9])/2
            x0=float(sa[10])
            H00=0.866025*p
            x=H1+H00/4
            y=x*math.tan(math.pi/6)
            a=p/2-y

            #六角面
            x1=e0*math.cos(math.pi/6)
            y11=e0*math.sin(math.pi/6)
            p1=(x1,y11,0)
            p2=(0,e0,0)
            p3=(-x1,y11,0)
            p4=(-x1,-y11,0)
            p5=(0,-e0,0)
            p6=(x1,-y11,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)

            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(table), None, QtGui.QApplication.UnicodeUTF8))
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1,H)
            c2=c2.cut(c3)
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-hm),App.Rotation(App.Vector(1,0,0),0))
            #Part.show(c2)
            c1=c1.fuse(c2)
            #Part.show(c1)

            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                #key_1=key_2
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)

            else:
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label = 'Gate Valve_' + str(key_1)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='14':
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            key_2=dia[-3:]
            sa=checks_10k[key_1]
            d=float(sa[0])/2
            L=float(sa[1])
            H0=float(sa[2])
            a=float(sa[3])
            d1=float(sa[4])
            s1=float(sa[5])/2
            s2=float(sa[6])/2
            sa=screws[key_1]
            L1=float(sa[7])
            A1=float(sa[10])/2
            t=float(sa[9])
            d0=A1-t

            x1=L/2-1.1*L1
            s=math.asin(x1/d1)
            #y1=d1-s1
            y1=2*A1
            d10=2*s2+2*a
            d11=2*s2
            H=0.7*L1
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d0), None, QtGui.QApplication.UnicodeUTF8))
            p1=(H,0,0)
            p2=(H,0,-A1)
            p3=(1.1*L1,0,-A1)
            p4=(L/2,0,-y1)
            p5=(L-1.1*L1,0,-A1)
            p6=(L-H,0,-A1)
            p7=(L-H,0,0)
            p8=(L/2,0,-1.3*A1)
            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p8),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeLine(p7,p1)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d0), None, QtGui.QApplication.UnicodeUTF8))

            #本体
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface=Part.Face(aWire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c2 = Part.makeCylinder(d10/2,y1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c1=c1.fuse(c2)
            #本体窓
            c2 = Part.makeCylinder(d11/2,y1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c1=c1.cut(c2)
            #キャップ
            x5=d11/2-0.1
            x6=x5-1.4*a
            x7=x6+0.7*a
            x8=1.4*a*(1-1/math.sqrt(2))
            x9=0.7*a*(1-1/math.sqrt(2))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d0), None, QtGui.QApplication.UnicodeUTF8))
            p1=(0,0,H0-0.7*a)
            p2=(0,0,H0)
            p3=(x6,0,H0)
            p4=(x5-x8,0,H0-x8)
            p5=(x5,0,H0-1.4*a)
            p6=(x5,0,y1+0.7*a)
            p7=(d10/2,0,y1+0.7*a)
            p8=(d10/2,0,y1)
            p9=(x5,0,y1)
            p10=(x5,0,y1-a)
            p11=(x7,0,y1-a)
            p12=(x7,0,H0-1.4*a)
            p13=(x7-x9,0,H0-0.7*a-x9)
            p14=(x6,0,H0-0.7*a)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4=Part.makeLine(p5,p6)
            edge5=Part.makeLine(p6,p7)
            edge6=Part.makeLine(p7,p8)
            edge7=Part.makeLine(p8,p9)
            edge8=Part.makeLine(p9,p10)
            edge9=Part.makeLine(p10,p11)
            edge10=Part.makeLine(p11,p12)
            edge11=Part.Arc(Base.Vector(p12),Base.Vector(p13),Base.Vector(p14)).toShape()
            edge12=Part.makeLine(p14,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9,edge10,edge11,edge12])
            #Part.show(aWire)
            pface=Part.Face(aWire)
            c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            #Part.show(c2)
            c1=c1.fuse(c2)
            #本体カット
            p1=(L1,0,0)
            p2=(L1,0,-d0)
            p3=(1.1*L1,0,-A1+a)
            p4=(L/2,0,-1.3*A1+a)
            p5=(L-1.1*L1,0,-A1+a)
            p6=(L-L1,0,-d0)
            p7=(L-L1,0,0)

            edge1 = Part.makeLine(p1,p2)
            edge2 = Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4 = Part.makeLine(p5,p6)
            edge5 = Part.makeLine(p6,p7)
            edge6 = Part.makeLine(p7,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6])
            pface=Part.Face(aWire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            #Part.show(c20)
            c1=c1.cut(c20)
            #六角面
            x1=s1
            s=math.pi/6
            e0=x1/math.cos(s)
            x=e0*math.cos(s)
            y=e0*math.sin(s)
            p1=(x,y,0)
            p2=(0,e0,0)
            p3=(-x,y,0)
            p4=(-x,-y,0)
            p5=(0,-e0,0)
            p6=(x,-y,0)
            plist=[p1,p2,p3,p4,p5,p6,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.extrude(Base.Vector(0,0,0.7*L1))
            c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)
            c3=c2
            c3.Placement=App.Placement(App.Vector(L-0.7*L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c3)
            #Part.show(c1)
            #弁体仕切り
            wface=Part.makePlane(4*A1,a,Base.Vector(1.3*L1,-2*A1,-2*A1),Base.Vector(0,1,0))
            c2=wface.extrude(Base.Vector(0,4*A1,0))
            #流路
            c22 = Part.makeCylinder(d,L/2,Base.Vector(1.3*L1,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c22)
            if key_1>='25A':
                c2.Placement=App.Placement(App.Vector(a,0,-1.5*a),App.Rotation(App.Vector(0,1,0),-8))
            else:
                c2.Placement=App.Placement(App.Vector(a,0,-0.8*a),App.Rotation(App.Vector(0,1,0),-8))
            c3=c2.common(c20)
            c1=c1.fuse(c3)
            #弁体
            c2 = Part.makeCylinder(1.2*d,a,Base.Vector(1.3*L1+a,0,0),Base.Vector(1,0,0))
            if key_1>='25A':
                c2.Placement=App.Placement(App.Vector(a,0,-1.5*a),App.Rotation(App.Vector(0,1,0),-8))
            else:
                c2.Placement=App.Placement(App.Vector(a,0,-0.8*a),App.Rotation(App.Vector(0,1,0),-8))
            c1=c1.fuse(c2)

            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                #key_1=key_2
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)

            else:
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)

            doc=App.ActiveDocument
            label = 'Check Valve_' + str(key_1)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1

        elif key=='15':
            st=self.comboBox_standard.currentText()
            dia=self.comboBox_dia.currentText()
            key_1=dia[:3]
            sa=screws[key_1]
            p=sa[0]
            h=sa[1]
            r=sa[2]
            D0=sa[3]
            d2=sa[4]
            d1=sa[5]
            a=sa[6]
            l=sa[7]
            A2=sa[11]/2
            f=sa[13]
            L1=a+f
            sa=tubes[key_1]
            A20=sa[0]/2
            if st=='SGP':
                t=sa[1]
            elif st=='Sch40':
                t=sa[3]
            elif st=='Sch60':
                t=sa[4]
            elif st=='Sch80':
                t=sa[5]
            elif st=='Sch5s':
                t=sa[6]
            elif st=='Sch10s':
                t=sa[7]
            elif st=='Sch20s':
                t=sa[8]
            L=float(self.lineEdit_1.text())
            '''    
            #print(t)    
            d0=d2-(t+.1)
            
            c1 = Part.makeCylinder(d2,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
            #c2 = Part.makeCylinder(d0,L,Base.Vector(L1,0,0),Base.Vector(1,0,0))
            #c1=c1.cut(c2)
            

            if self.checkbox.isChecked():
                male_thread(self)
                c2=c10
                #Part.show(c2)
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
                male_thread(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                c2 = Part.makeCylinder(d0,L+L1,Base.Vector(-L1/2,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                #Part.show(c2)
            else:
                cutter_01a(self)
                c21=c10
                c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c21)
                cutter_01a(self)
                c21=c10
                c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c21)

            doc=App.ActiveDocument
            label =   "Straight_Pipe_" + str(st) +'_' + str(dia)+'_'+str(L)+'_'
            F_Obj = doc.addObject("Part::Feature",label)
            F_Obj.Shape=c1
            Gui.SendMsgToActiveView("ViewFit")
            '''
            label = 'Straight_tube_' + st + " " + key_1 +"_"
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            obj.addProperty("App::PropertyString", "key",label).key=key
            obj.addProperty("App::PropertyFloat", "a",label).a=a
            obj.addProperty("App::PropertyFloat", "f",label).f=f
            obj.addProperty("App::PropertyFloat", "d2",label).d2=d2
            obj.addProperty("App::PropertyFloat", "t",label).t=t
            obj.addProperty("App::PropertyFloat", "p",label).p=p
            obj.addProperty("App::PropertyFloat", "h",label).h=h
            obj.addProperty("App::PropertyFloat", "r",label).r=r
            obj.addProperty("App::PropertyFloat", "D0",label).D0=D0
            obj.addProperty("App::PropertyFloat", "d1",label).d1=d1
            obj.addProperty("App::PropertyFloat", "L",label).L=L
            obj.addProperty("App::PropertyFloat", "A20",label).A20=A20
            obj.addProperty("App::PropertyFloat", "l",label).l=l
            obj.addProperty("App::PropertyFloat", "A2",label).A2=A2
            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'IsChecked',label).IsChecked = True
            else:
                obj.addProperty("App::PropertyBool",'IsChecked',label).IsChecked = False
            ParamStlPScFit.StraightPipe(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute() 

class main():

    d = QtGui.QWidget()
    d.setWindowFlags(QtCore.Qt.Window)
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.show()





