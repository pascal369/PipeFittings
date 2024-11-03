lst=[
'00_Flange','01_Elbow','02_Tee','03_Reducer_concentric','04_Reducer_eccentric','05_Straight pipe',
'06_Single_flange_straight_pipe','07_Both_flanges_straight_pipe','08_Cap','09_Flange_lid','10_Rap_joint',
'11_Gate_Valve_internal','12_Gate_Valve_external','13_Check_Valve_swing_type','14_Expansion joint_10k','15_Flex_joint',
'16_Expansion joint_7.5k','17_Flow meter_7.5k','18_Densitometer_7.5k']

l_lst={
'00':'フランジ','01':'エルボ','02':'チーズ','03':'同心レジューサ','04':'偏芯レジューサ','05':'直管',
'06':'片フランジ直管','07':'両フランジ直管','08':'キャップ','09':'フランジ蓋','10':'ラップジョイント',
'11':'仕切弁_内ねじ','12':'仕切弁_外ねじ','13':'逆止弁','14':'伸縮継手_10k','15':'フレキシブルジョイント',
'16':'伸縮継手_7.5k'}

mate=['Carbon steel','Stainless steel','Bronze','Cast Iron']
flg_carbon=['JIS5k','JIS7.5k','JIS10k','JIS16k','JIS20k']
flg_stainless=['JIS5k','JIS7.5k','JIS10k','JIS5k_Loose','JIS10k_Loose']
exp_mate=['Carbon steel']
exp_carbon=['JIS10k']


#直管+フランジ
s_flg_carbon=[
'SGP_JIS5k','SGP_JIS7.5k','SGP_JIS10k','SGP_JIS16k','SGP_JIS20k',
'Sch40_JIS5k','Sch40_JIS7.5k','Sch40_JIS10k','Sch40_JIS16k','Sch40_JIS20k',
'Sch80_JIS5k','Sch80_JIS7.5k','Sch80_JIS10k','Sch80_JIS16k','Sch80_JIS20k',
]

s_flg_stainless=[
'Sch10S_JIS5k','Sch10S_JIS7.5k','Sch10S_JIS10k',
'Sch20S_JIS5k','Sch20S_JIS7.5k','Sch20S_JIS10k',
'Sch40_JIS5k','Sch40_JIS7.5k','Sch40_JIS10k',
]

exp_st=['20mm','50mm','100mm','200mm',]

Tube_carbon=['SGP','Sch40','Sch80']
Tube_stainless=['Sch10S','Sch20S','Sch40']

tube_d=[
'006','008','010','015','020','025','032','040','050','065','075',
'080','100','125','150','200','250','300','350','400','450','500',
'550','600','650','700','750','800','850','900','950','1000',
]
Elbow_carbon=[
'045_Long_SGP', '045_Long_Sch40','045_Long_Sch80',
'090_Long_SGP', '090_Long_Sch40','090_Long_Sch80',
'180_Long_SGP', '180_Long_Sch40','180_Long_Sch80',
'045_Short_SGP', '045_Short_Sch40','045_Short_Sch80',
'090_Short_SGP', '090_Short_Sch40','090_Short_Sch80',
'180_Short_SGP', '180_Short_Sch40','180_Short_Sch80',
'090_Large_SGP',
]
Elbow_stainless=[
'045_Long_Sch10S', '045_Long_Sch20S','045_Long_Sch40',
'090_Long_Sch10S', '090_Long_Sch20S','090_Long_Sch40',
'090_Short_Sch10S', '090_Short_Sch20S','090_Short_Sch40',
]

flg_d=[
'010','015','020','025','032','040','050','065','075','080','100','125','150','200','250','300','350',
'400','450','500','550','600','650','700','750','800','900','1000','1200','1350','1500'
]

flg_75=[
'075','100','125','150','200','250','300','350','400','450',
'500','600','700','800','900','1000','1100','1200','1350','1500'
]

reduc_carbon=['SGP', 'Sch40','Sch80','Large']
reduc_stainless=['Sch10S', 'Sch20S','Sch40']
reduc=[
'020x015','025x015','025x020','032x015','032x020','032x025','040x015','040x020','040x025',
'040x032','050x020','050x025','050x032','050x040','065x025','065x032','065x040','065x050',
'080x032','080x040','080x050','080x065','100x040','100x050','100x065','100x080','125x050',
'125x065','125x080','125x100','150x065','150x080','150x100','150x125','200x100',
'200x125','200x150','250x100','250x125','250x150','250x200','300x125','300x150',
'300x200','300x250','350x150','350x200','350x250','350x300','400x200','400x250',
'400x300','400x350','450x250','450x300','450x350','450x400','500x300',
'500x350','500x400','500x450','550x400','550x450','500x500',
'550x400','550x450','550x500','600x450','600x500','600x550',
'650x500','650x550','650x600','7000x550','700x600','700x650',
]

Tee_carbon=['SGP', 'Sch40','Sch80','Large']
Tee_stainless=['Sch10S', 'Sch20S','Sch40']

tee=[
'015x015','020x015','020x020','025x015','025x020','025x025','032x015','032x020','032x025','032x032','040x015',
'040x020','040x025','040x032','040x040','050x020','050x025','050x032','050x040','050x050','065x025','065x032',
'065x040','065x050','065x065','080x032','080x040','080x050','080x065','080x080','100x040','100x050','100x065',
'100x080','100x100','125x050','125x065','125x080','125x100','125x125','150x065','150x080','150x100',
'150x125','150x150','200x100','200x125','200x150','200x200','250x100','250x125','250x150',
'250x200','250x250','300x125','300x150','300x200','300x250','300x300','350x150','350x200',
'350x250','350x300','350x350','400x150','400x200','400x250','400x300','400x350','400x400',
'450x200','450x250','450x300','450x350','450x400','450x450','500x200','500x250','500x300',
'500x350','500x400','500x450','500x500','550x400','550x450','550x500',
'600x450','600x500','600x550','600x600','650x500','650x550','650x600','650x650',
'700x550','700x600','700x650','700x700',
]

rap=['JIS5k','JIS10k']
check=['JIS7.5k','JIS10k',]


#可とう伸縮継手
#         d1    d2  L     L1       c     f      R
exp_20mm={
'020':(   45,   55, 150,  130,     10,   14,    22),
'025':(   50,   60, 150,  130,     10,   16,    22),
'032':(   62,   77, 150,  130,     10,   22,    22),
'040':(   60,   80, 150,  130,     10,   21,    22),
'050':(   75,   95, 150,  130,     10,   29,    22),
'065':(   95,  115, 150,  130,     10,   39,    22),
'075':(  105,  125, 150,  130,     10,   44,    22),
'080':(  105,  125, 150,  130,     10,   44,    22),
'100':(  130,  150, 150,  130,     10,   56,    22),
'125':(  160,  180, 150,  130,     10,   71,    22),
'150':(  190,  210, 200,  180,     10,   83,    30),
'200':(  237,  257, 200,  170,     15,  107,    30),
'250':(  304,  324, 200,  170,     15,  140,    30),
'300':(  341,  366, 200,  170,     15,  156,    33),
'350':(  386,  416, 200,  170,     15,  179,    33),
'400':(  465,  485, 200,  170,     15,  218,    33),
'450':(  515,  535, 200,  170,     15,  243,    33),
'500':(  565,  585, 250,  220,     15,  268,    33),
'550':(  615,  635, 250,  220,     15,  268,    33),
'600':(  665,  685, 250,  210,     20,  311,    33),
}
#                                                   フレキシブルジョイント
#         d1    d2  L     L1       c     f      R   L    R
exp_50mm={
'020':(   45,   55, 250,  230,     10,   14,    22, 100,  20),
'025':(   50,   60, 250,  230,     10,   16,    22, 100,  50),
'032':(   62,   77, 250,  230,     10,   22,    22, 100,  50),
'040':(   60,   80, 250,  230,     10,   21,    22, 100,  50),
'050':(   75,   95, 250,  230,     10,   29,    22, 100,  50),
'065':(   95,  115, 250,  230,     10,   39,    22, 125,  50),
'075':(  105,  125, 300,  280,     10,   44,    22, 125,  50),
'080':(  105,  125, 300,  280,     10,   44,    22, 125,  50),
'100':(  130,  150, 300,  280,     10,   56,    22, 125,  50),
'125':(  160,  180, 300,  280,     10,   71,    22, 125,  50),
'150':(  190,  210, 300,  280,     10,   83,    30, 150,  50),
'200':(  237,  257, 300,  270,     15,  107,    30, 150,  50),
'250':(  304,  324, 300,  270,     15,  140,    30, 175,  50),
'300':(  341,  366, 300,  270,     15,  156,    33, 175,  50),
'350':(  386,  416, 350,  320,     15,  179,    33, 175,  50),
'400':(  465,  485, 350,  320,     15,  218,    33, 175,  50),
'450':(  515,  535, 350,  320,     15,  243,    33, 175,  50),
'500':(  565,  585, 350,  320,     15,  268,    33, 175,  50),
'550':(  615,  635, 350,  320,     15,  268,    33, 175,  50),
'600':(  665,  685, 400,  360,     20,  311,    33, 175,  50),
}

#         d1    d2  L     L1       c     f      R
exp_100mm={
'020':(   45,   55, 350,  330,     10,   14,    22),
'025':(   50,   60, 350,  330,     10,   16,    22),
'032':(   62,   77, 350,  330,     10,   22,    22),
'040':(   60,   80, 350,  330,     10,   21,    22),
'050':(   75,   95, 350,  330,     10,   29,    22),
'065':(   95,  115, 350,  330,     10,   39,    22),
'075':(  105,  125, 350,  330,     10,   44,    22),
'080':(  105,  125, 350,  330,     10,   44,    22),
'100':(  130,  150, 350,  330,     10,   56,    22),
'125':(  160,  180, 350,  330,     10,   71,    22),
'150':(  190,  210, 500,  480,     10,   83,    30),
'200':(  237,  257, 500,  470,     15,  107,    30),
'250':(  304,  324, 500,  470,     15,  140,    30),
'300':(  341,  366, 550,  520,     15,  156,    33),
'350':(  386,  416, 550,  520,     15,  179,    33),
'400':(  465,  485, 550,  520,     15,  218,    33),
'450':(  515,  535, 550,  520,     15,  243,    33),
'500':(  565,  585, 550,  520,     15,  268,    33),
'550':(  615,  635, 550,  520,     15,  268,    33),
'600':(  665,  685, 550,  510,     20,  311,    33),
}

#         d1    d2  L     L1       c     f      R
exp_200mm={
'020':(   45,   55, 450,  430,     10,   14,    22),
'025':(   50,   60, 450,  430,     10,   16,    22),
'032':(   62,   77, 450,  430,     10,   22,    22),
'040':(   60,   80, 450,  430,     10,   21,    22),
'050':(   75,   95, 450,  430,     10,   29,    22),
'065':(   95,  115, 450,  430,     10,   39,    22),
'075':(  105,  125, 450,  430,     10,   44,    22),
'080':(  105,  125, 450,  430,     10,   44,    22),
'100':(  130,  150, 450,  430,     10,   56,    22),
'125':(  160,  180, 450,  430,     10,   71,    22),
'150':(  190,  210, 600,  580,     10,   83,    30),
'200':(  237,  257, 600,  570,     15,  107,    30),
'250':(  304,  324, 600,  570,     15,  140,    30),
'300':(  341,  366, 650,  620,     15,  156,    33),
'350':(  386,  416, 650,  620,     15,  179,    33),
'400':(  465,  485, 650,  620,     15,  218,    33),
'450':(  515,  535, 650,  620,     15,  243,    33),
'500':(  565,  585, 650,  620,     15,  268,    33),
'550':(  565,  635, 650,  620,     15,  268,    33),
'600':(  615,  685, 650,  610,     20,  311,    33),
}

#ラップジョイント
#                      5k    10k
#         OD,     T,    G,    G,      F,    R
raps={
'015':(   21.7,   2.1,  44,   51,     30,   3),
'020':(   27.2,   2.1,  49,   56,     30,   3),
'025':(   34.0,   2.8,  59,   67,     50,   3),
'032':(   42.7,   2.8,  70,   76,     50,   4),
'040':(   48.6,   2.8,  75,   81,     50,   4),
'050':(   60.5,   2.8,  85,   96,     50,   4),
'065':(   76.3,   3.0, 110,  116,     50,   5),
'080':(   89.1,   3.0, 121,  126,     50,   5),
'100':(  114.3,   3.0, 141,  151,     50,   5),
'125':(  139.8,   3.4, 176,  182,     50,   6),
'150':(  165.2,   3.4, 206,  212,     50,   6),
'200':(  216.3,   4.0, 252,  262,     65,   6),
'250':(  267.4,   4.0, 317,  324,     65,   6),
'300':(  318.5,   4.5, 360,  368,     65,   9),
}

#直管              1,      2,      3,     4,     5,     6,     7,     8,     9       10キャップ
#                 SGP,STPG,STS,STPT,STPA,STPL,         SUS-TP
#             SGP(STK)     Sch20,  Sch40, Sch60, Sch80, Sch5S, Sch10S,Sch20S,Sch40
#d0,      d2,     t,      t,      t,     t,     t,     t,     t,     t,     t,      E
str_tube={
'006':(   10.5,   2.0,    0,    1.7,     2.2,   2.4,   1.00,  1.20,  1.5,  1.7,     0),
'008':(   13.8,   2.3,    0,    2.2,     2.4,   3.0,   1.20,  1.65,  2.0,  2.2,     0),
'010':(   17.3,   2.3,    0,    2.3,     2.8,   3.2,   1.20,  1.65,  2.0,  2.3,     0),
'015':(   21.7,   2.8,    0,    2.8,     3.2,   3.7,   1.65,  2.10,  2.5,  2.8,  25.4),
'020':(   27.2,   2.8,    0,    2.9,     3.4,   3.9,   1.65,  2.10,  2.5,  2.9,  25.4),
'025':(   34.0,   3.2,    0,    3.4,     3.9,   4.5,   1.65,  2.80,  2.5,  3.4,  38.1),
'032':(   42.7,   3.5,    0,    3.6,     4.5,   4.9,   1.65,  2.80,  3.0,  3.6,  38.1),
'040':(   48.6,   3.5,    0,    3.7,     4.5,   5.1,   1.65,  2.80,  3.0,  3.7,  38.1),
'050':(   60.5,   3.8,  3.2,    3.9,     4.9,   5.5,   1.65,  2.80,  3.5,  3.9,  38.1),
'065':(   76.3,   4.2,  4.5,    5.2,     6.0,   7.0,   2.10,  3.00,  3.5,  5.2,  38.1),
'075':(   89.1,   4.2,  4.5,    5.5,     6.6,   7.6,   2.10,  3.00,  4.0,  5.5,  50.8),
'080':(   89.1,   4.2,  4.5,    5.5,     6.6,   7.6,   2.10,  3.00,  4.0,  5.5,  50.8),
'100':(  114.3,   4.5,  4.9,    6.0,     7.1,   8.6,   2.10,  3.00,  4.0,  6.0,  63.5),
'125':(  139.8,   4.5,  5.1,    6.6,     8.1,   9.5,   2.80,  3.40,  5.0,  6.6,  76.2),
'150':(  165.2,   5.0,  5.5,    7.1,     9.3,   11.0,  2.80,  3.40,  5.0,  7.1,  88.9),
'200':(  216.3,   5.8,  6.4,    8.2,    10.3,   12.7,  2.80,  4.00,  6.5,  8.2, 101.6),
'250':(  267.4,   6.6,  6.4,    9.3,    12.7,   15.1,  3.40,  4.00,  6.5,  9.3, 127.0),
'300':(  318.5,   6.9,  6.4,   10.3,    14.3,   17.4,  4.00,  4.50,  6.5, 10.3, 152.4),
'350':(  355.6,   7.9,  7.9,   11.1,    15.1,   19.0,  0.00,  5.00,  8.0, 11.1, 165.1),
'400':(  406.4,   7.9,  7.9,   12.7,    16.7,   21.4,  0.00,  5.00,  8.0, 12.7, 177.8),
'450':(  457.2,   7.9,  7.9,   14.3,    19.0,   23.8,  0.00,  5.00,  8.0, 14.3, 203.2),
'500':(  508.0,   7.9,  9.5,   15.1,    20.6,   26.2,  0.00,  5.50,  9.5, 15.1, 228.6),
'550':(  558.8,   7.9,  9.5,   15.1,    20.6,   26.2,  0.00,  6.50,  9.5, 15.1, 228.6),
'600':(  609.6,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  0.00, 12.7, 17.5, 0.000),
'650':(  660.4,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'700':(  711.2,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'750':(  762.0,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'800':(  812.8,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'850':(  863.6,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'900':(  914.4,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),
'1000':( 1016.0,   7.9,  9.5,   0.00,    0.00,   0.00,  0.00,  8.00, 12.7, 17.5, 0.000),

}

# JIS2k
#         d0,    d2,      d4,     d5,   t,      E,      n,      a,      b,      T,      r
JIS2k={
'450':(  457.2,	 461,	 555,	 605,	22,	23,	16,     0,      0,      0,      0),
'500':(  508.0,  512, 	 605,	 655,	22,	23,	20,     0,      0,      0,      0),
'550':(  558.8,	 563,	 665,	 720,	24,	25,	20,     0,      0,      0,      0),
'600':(  609.6,  614,	 715,	 770,	24,	25,	20,     0,      0,      0,      0),
'650':(  660.4,  664,	 770,	 825,	24,	25,	24,     0,      0,      0,      0),
'700':(  711.2,	 715,	 820,	 875,	24,	25,	24,     0,      0,      0,      0),
'750':(  762.0,  766,	 880,	 945,	24,	27,	24,     0,      0,      0,      0),
'800':(  812.8,	 817,	 930,	 995,	24,	27,	24,     0,      0,      0,      0),
'850':(  863.6,	 868,	 980,	1045,	24,	27,	24,     0,      0,      0,      0),
'900':(  914.4,	 918,	1030,	1095,	24,	27,	24,     0,      0,      0,      0),
'1000':(1016.0,	1020,	1130,	1195,	26,	27,	28,     0,      0,      0,      0),
'1100':(1117.6,	1122,	1240,	1305,	26,	27,	28,     0,      0,      0,      0),
'1200':(1219.2,	1224,	1350,	1420,	26,	27,	32,     0,      0,      0,      0),
'1350':(1371.6,	1376,	1505,	1575,	26,	27,	32,     0,      0,      0,      0),
'1500':(1524.0,	1528,	1660,	1730,	28,	27,	36,     0,      0,      0,      0)
}

# JIS5k                                                                               ラップジョイント
#        d0,     d2,     d4,     d5,    t,      E,       n,      a,      b,      T,      r,    R
JIS5k={
'010':(  17.3,	 17.8, 	 55,	 75,	 9,	12,	 4,      0,      0,      0,      0,    0),
'015':(  21.7,	 22.2, 	 60,	 80,	 9,	12,	 4,      0,      0,      0,      0,    3),
'020':(  27.2,	 27.7, 	 65,	 85,	10,	12,	 4,      0,      0,      0,      0,    3),
'025':(  34.0,	 34.5, 	 75,	 95,	10,	12,	 4,      0,      0,      0,      0,    3),
'032':(  42.7,	 43.2, 	 90,	115,	12,	15,	 4,      0,      0,      0,      0,    4),
'040':(  48.6,	 49.1, 	 95,	120,	12,	15,	 4,      0,      0,      0,      0,    4),
'050':(  60.5,	 61.1, 	105,	130,	14,	15,	 4,      0,      0,      0,      0,    4),
'065':(  76.3,	 77.1, 	130,	155,	14,	15,	 4,      0,      0,      0,      0,    5),
'080':(  89.1,	 90.0, 	145,	180,	14,	19,	 4,      0,      0,      0,      0,    5),
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
'550':(558.8,   562.0,  665,    720,    26,     27,     20,      0,      0,      0,      0,    0),
'600':(609.6,	613.0, 	715,	770,	26,	27,	20,      0,      0,      0,      0,    0),
'700':(711.2,	715.0, 	820,	875,	26,	27,	24,      0,      0,      0,      0,    0),
'800':(812.8,	817.0, 	930,	995,	28,	33,	24,      0,      0,      0,      0,    0),
'900':(914.4,	919.0, 1030,   1095,	30,	33,	24,      0,      0,      0,      0,    0),
'1000':(1016.6,1021.0, 1130,   1195,	32,	35,	28,      0,      0,      0,      0,    0),
}

#フランジ7.5k------------------------------------------------------------------------------------
#          d0,   d2,     d4,   d5,   t,   E,    n
JIS75k={
'075':(    75,   90.0,   168,  211,  18,  19,   4),
'100':(   100,  115.4,   195,  238,  18,  19,   4),
'125':(   125,  141.2,   220,  263,  20,  19,   6),
'150':(   150,  166.6,   247,  290,  22,  19,   6),
'200':(   200,  218.0,   299,  342,  22,  19,   8),
'250':(   250,  269.5,   360,  410,  24,  23,   8),
'300':(   300,  321.0,   414,  464,  24,  23,  10),
'350':(   350,  358.1,   472,  530,  26,  25,  10),
'400':(   400,  409.0,   524,  582,  26,  25,  12),
'450':(   450,  460.0,   585,  652,  28,  27,  12),
'500':(   500,  511.0,   639,  706,  28,  27,  12),
'600':(   600,  613.0,   743,  810,  30,  27,  16),
'700':(   700,  715.0,   854,  928,  32,  33,  16),
'800':(   800,  817.0,   960, 1034,  34,  33,  20),
'900':(   900,  919.0,   1073, 1156, 36,  33,  20),
'1000':( 1000, 1021.0,   1179, 1262, 38,  33,  24),
'1100':( 1100, 1123.0,   1283, 1366, 41,  33,  24),
'1200':( 1200, 1224.0,   1387, 1470, 43,  33,  28),
'1350':( 1350, 1377.0,   1552, 1642, 45,  39,  28),
'1500':( 1500, 1529.0,   1710, 1800, 48,  39,  32),
}

# JIS10k
#          d0,    d2,     d4,     d5,   t,      E,       n,        a,     b,     T,     r
JIS10k={
'010':(    17.3,  17.8,   65,	  90,	12,	15,	 4,        0,     0,     0,     0),
'015':(    21.7,  22.2,   70,	  95,	12,	15,	 4,        0,     0,     0,     0),
'020':(    27.2,  27.7,   75,	 100,	14,	15,	 4,        0,     0,     0,     0),
'025':(    34.0,  34.5,   90,	 125,	14,	19,	 4,        0,     0,     0,     0),
'032':(    42.7,  43.2,  100,	 135,	16,	19,	 4,        0,     0,     0,     0),
'040':(    48.6,  49.1,  105,	 140,	16,	19,	 4,        0,     0,     0,     0),
'050':(    60.5,  61.1,  120,	 155,	16,	19,	 4,        0,     0,     0,     0),
'065':(    76.3,  77.1,  140,	 175,	18,	19,	 4,        0,     0,     0,     0),
'080':(    89.1,  90.0,  150,	 185,	18,	19,	 8,        0,     0,     0,     0),
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

#        d0,     d2,     d4,    d5,     t,      E,      n,      a,       b,      T,      r
JIS16k={
'010':(  17.3,    17.8,  65,     90,     12,     15,     4,      26,      28,     16,     4),
'015':(  21.7,    22.2,  70,     95,     12,     15,     4,      30,      32,     16,     4),
'020':(  27.2,    27.7,  75,    100,     14,     15,     4,      38,      42,     20,     4),
'025':(  34.0,    34.5,  90,    125,     14,     19,     4,      46,      50,     20,     4),
'032':(  42.7,    43.2, 100,    135,     16,     19,     4,      56,      60,     22,     5),
'040':(  48.6,    49.1, 105,    140,     16,     19,     4,      62,      66,     24,     5),
'050':(  60.5,    61.1, 120,    155,     16,     19,     8,      76,      80,     24,     5),
'065':(  76.3,    77.1, 140,    175,     18,     19,     8,      94,      98,     26,     5),
'080':(  89.1,    90.0, 160,    200,     20,     23,     8,     108,     112,     28,     6),
'100':( 114.3,   115.4, 185,    225,     22,     23,     8,     134,     138,     34,     6),
'125':( 139.8,   141.2, 225,    270,     22,     25,     8,     164,     170,     34,     6),
'150':( 165.2,   166.6, 260,    305,     24,     25,    12,     196,     202,     38,     6),
'200':( 216.3,   218.0, 305,    350,     26,     25,    12,     244,     252,     40,     6),
'250':( 267.4,   269.0, 380,    430,     28,     27,    12,     304,     312,     44,     6),
'300':( 318.5,   321.0, 430,    480,     30,     27,    16,     354,     364,     48,     8),
'350':( 355.6,   358.1, 480,    540,     34,     33,    16,     398,     408,     52,     8),
'400':( 406.4,   409.0, 540,    605,     38,     33,    16,     446,     456,     60,    10),
'450':( 457.2,   460.0, 605,    675,     40,     33,    20,     504,     514,     64,    10),
'500':( 508.0,   511.0, 660,    730,     42,     33,    20,     558,     568,     68,    10),
'550':( 558.8,   562.0, 720,    795,     44,     39,    20,     612,     622,     70,    10),
'600':( 609.6,   613.0, 770,    845,     46,     39,    24,     666,     676,     74,    10),
}

#        d0,     d2,     d4,    d5,     t,      E,      n,      a,       b,      T,      r,  f
JIS20k={
'010':(  17.3,    17.8,  65,     90,     14,     15,     4,      26,      28,     16,     4,  1),
'015':(  21.7,    22.2,  70,     95,     14,     15,     4,      30,      32,     16,     4,  1),
'020':(  27.2,    27.7,  75,    100,     16,     15,     4,      38,      42,     20,     4,  1),
'025':(  34.0,    34.5,  90,    125,     16,     19,     4,      46,      50,     20,     4,  1),
'032':(  42.7,    43.2, 100,    135,     18,     19,     4,      56,      60,     22,     5,  2),
'040':(  48.6,    49.1, 105,    140,     18,     19,     4,      62,      66,     24,     5,  2),
'050':(  60.5,    61.1, 120,    155,     18,     19,     8,      76,      80,     24,     5,  2),
'065':(  76.3,    77.1, 140,    175,     20,     19,     8,      94,      98,     26,     5,  2),
'080':(  89.1,    90.0, 160,    200,     22,     23,     8,     108,     112,     28,     6,  2),
'100':( 114.3,   115.4, 185,    225,     24,     23,     8,     134,     138,     34,     6,  2),
'125':( 139.8,   141.2, 225,    270,     26,     25,     8,     164,     170,     34,     6,  2),
'150':( 165.2,   166.6, 260,    305,     28,     25,    12,     196,     202,     38,     6,  2),
'200':( 216.3,   218.0, 305,    350,     30,     25,    12,     244,     252,     40,     6,  2),
'250':( 267.4,   269.0, 380,    430,     34,     27,    12,     304,     312,     44,     6,  2),
'300':( 318.5,   321.0, 430,    480,     36,     27,    16,     354,     364,     48,     8,  3),
'350':( 355.6,   358.1, 480,    540,     40,     33,    16,     398,     408,     52,     8,  3),
'400':( 406.4,   409.0, 540,    605,     46,     33,    16,     446,     456,     60,    10,  3),
'450':( 457.2,   460.0, 605,    675,     48,     33,    20,     504,     514,     64,    10,  3),
'500':( 508.0,   511.0, 660,    730,     50,     33,    20,     558,     568,     68,    10,  3),
'550':( 558.8,   562.0, 720,    795,     52,     39,    20,     612,     622,     70,    10,  3),
'600':( 609.6,   613.0, 770,    845,     54,     39,    24,     666,     676,     74,    10,  3),
}
#              long   short
#口径,    d2,    r,    r,
#
#
#        0,     1,     2,
elbo = {
'015':(  21.7,  38.1,  25.4),
'020':(  27.2,  38.1,  25.4),
'025':(  34.0,  38.1,  25.4),
'032':(  42.7,  47.6,  31.8),
'040':(  48.6,  57.2,  38.1),
'050':(  60.5,  76.2,  50.8),
'065':(  76.3,  95.3,  63.5),
'080':(  89.1, 114.3,  76.2),
'100':( 114.3, 152.4, 101.6),
'125':( 139.8, 190.5, 127.0),
'150':( 165.2, 228.6, 152.4),
'200':( 216.3, 304.8, 203.2),
'250':( 267.4, 381.0, 254.0),
'300':( 318.5, 457.2, 304.8),
'350':( 355.6, 533.4, 355.6),
'400':( 406.4, 609.6, 406.4),
'450':( 457.2, 685.8, 457.2),
'500':( 508.0, 762.0, 508.0),
'550':( 558.8, 838.2, 0.0),
'600':( 609.6, 914.4, 0.0),
'650':( 660.4, 990.6, 0.0),
'700':( 711.2,1066.8, 0.0),
}

#チーズ       0,      1,      2,      3,
#           d1,     d2,     C,      M
tees={
'015x015':( 21.7,   21.7,   25.4,   25.4),
'020x015':( 27.2,   21.7,   28.6,   28.6),
'020x020':( 27.2,   27.2,   28.6,   28.6),
'025x015':( 34.0,   21.7,   38.1,   38.1),
'025x020':( 34.0,   27.2,   38.1,   38.1),
'025x025':( 34.0,   34.0,   38.1,   38.1),
'032x015':( 42.7,   21.7,   47.6,   47.6),
'032x020':( 42.7,   27.2,   47.6,   47.6),
'032x025':( 42.7,   34.0,   47.6,   47.6),
'032x032':( 42.7,   42.7,   47.6,   47.6),
'040x015':( 48.6,   21.7,   57.2,   57.2),
'040x020':( 48.6,   27.2,   57.2,   57.2),
'040x025':( 48.6,   34.0,   57.2,   57.2),
'040x032':( 48.6,   42.7,   57.2,   57.2),
'040x040':( 48.6,   48.6,   57.2,   57.2),
'050x020':( 60.5,   27.2,   63.5,   44.5),
'050x025':( 60.5,   34.0,   63.5,   50.8),
'050x032':( 60.5,   42.7,   63.5,   57.2),
'050x040':( 60.5,   48.6,   63.5,   60.3),
'050x050':( 60.5,   60.5,   63.5,   63.5),
'065x025':( 76.3,   34.0,   76.2,   57.2),
'065x032':( 76.3,   42.7,   76.2,   63.5),
'065x040':( 76.3,   48.6,   76.2,   66.7),
'065x050':( 76.3,   60.5,   76.2,   69.9),
'065x065':( 76.3,   76.3,   76.2,   76.2),
'080x032':( 89.1,   42.7,   85.7,   69.9),
'080x040':( 89.1,   48.6,   85.7,   73.0),
'080x050':( 89.1,   60.5,   85.7,   76.2),
'080x065':( 89.1,   76.3,   85.7,   82.6),
'080x080':( 89.1,   89.1,   85.7,   85.7),
'100x040':(114.3,   48.6,  104.8,   85.7),
'100x050':(114.3,   60.5,  104.8,   88.9),
'100x065':(114.3,   76.3,  104.8,   95.3),
'100x080':(114.3,   89.1,  104.8,   98.4),
'100x100':(114.3,  114.3,  104.8,  104.8),
'125x050':(139.8,   60.5,  123.8,  104.8),
'125x065':(139.8,   76.3,  123.8,  108.0),
'125x080':(139.8,   89.1,  123.8,  111.1),
'125x100':(139.8,  114.3,  123.8,  117.5),
'125x125':(139.8,  139.8,  123.8,  123.8),
'150x065':(165.2,   76.3,  142.9,  120.7),
'150x080':(165.2,   89.1,  142.9,  123.8),
'150x100':(165.2,  114.3,  142.9,  130.2),
'150x125':(165.2,  139.8,  142.9,  136.5),
'150x150':(165.2,  165.2,  142.9,  142.9),
'200x100':(216.3,  114.3,  177.8,  155.6),
'200x125':(216.3,  139.8,  177.8,  161.9),
'200x150':(216.3,  165.2,  177.8,  168.3),
'200x200':(216.3,  216.3,  177.8,  177.8),
'250x100':(267.4,  114.3,  215.9,  184.2),
'250x125':(267.4,  139.8,  215.9,  190.5),
'250x150':(267.4,  165.2,  215.9,  193.7),
'250x200':(267.4,  216.3,  215.9,  203.2),
'250x250':(267.4,  267.4,  215.9,  215.9),
'300x125':(318.5,  139.8,  254.0,  215.9),
'300x150':(318.5,  165.2,  254.0,  219.1),
'300x200':(318.5,  216.3,  254.0,  228.6),
'300x250':(318.5,  267.4,  254.0,  241.3),
'300x300':(318.5,  318.5,  254.0,  254.0),
'350x150':(355.6,  165.2,  279.4,  238.1),
'350x200':(355.6,  216.3,  279.4,  247.7),
'350x250':(355.6,  267.4,  279.4,  257.2),
'350x300':(355.6,  318.5,  279.4,  269.9),
'350x350':(355.6,  355.6,  279.4,  279.4),
'400x150':(406.4,  165.2,  304.8,  263.5),
'400x200':(406.4,  216.3,  304.8,  273.1),
'400x250':(406.4,  267.4,  304.8,  282.6),
'400x300':(406.4,  318.5,  304.8,  295.3),
'400x350':(406.4,  355.6,  304.8,  304.8),
'400x400':(406.4,  406.4,  304.8,  304.8),
'450x200':(457.2,  216.3,  342.9,  298.5),
'450x250':(457.2,  267.4,  342.9,  308.0),
'450x300':(457.2,  318.5,  342.9,  320.7),
'450x350':(457.2,  355.6,  342.9,  330.2),
'450x400':(457.2,  406.4,  342.9,  330.2),
'450x450':(457.2,  457.2,  342.9,  342.9),
'500x200':(508.0,  216.3,  381.0,  323.9),
'500x250':(508.0,  267.4,  381.0,  333.4),
'500x300':(508.0,  318.5,  381.0,  346.1),
'500x350':(508.0,  355.6,  381.0,  355.6),
'500x400':(508.0,  406.4,  381.0,  355.6),
'500x450':(508.0,  457.2,  381.0,  368.3),
'500x500':(508.0,  508.0,  381.0,  381.0),
'550x400':(558.8,  406.4,  419.1,  381.0),
'550x450':(558.8,  457.2,  419.1,  393.7),
'550x500':(558.8,  508.0,  419.1,  406.4),
'550x550':(558.8,  558.8,  419.1,  419.1),
'600x450':(609.6,  457.2,  431.8,  419.1),
'600x500':(609.6,  508.0,  431.8,  431.8),
'600x550':(609.6,  558.8,  431.8,  431.8),
'600x600':(609.6,  609.6,  431.8,  431.8),
'650x500':(660.4,  508.0,  495.3,  457.2),
'650x550':(660.4,  558.8,  495.3,  469.9),
'650x600':(660.4,  609.6,  495.3,  482.6),
'650x650':(660.4,  660.4,  495.3,  495.3),
'700x550':(711.2,  558.8,  520.7,  495.3),
'700x600':(711.2,  609.6,  520.7,  508.0),
'700x650':(711.2,  660.4,  520.7,  520.7),
'700x700':(711.2,  711.2,  520.7,  520.7),
}
#レジューサ
#             d1,     d2,     H
reducs={
'020x015':(   27.2,   21.7,   38.1),
'025x015':(   34.0,   21.7,   50.8),
'025x020':(   34.0,   27.2,   50.8),
'032x015':(   42.7,   21.7,   50.8),
'032x020':(   42.7,   27.2,   50.8),
'032x025':(   42.7,   34.0,   50.8),
'040x015':(   48.6,   21.7,   63.5),
'040x020':(   48.6,   27.2,   63.5),
'040x025':(   48.6,   34.0,   63.5),
'040x032':(   48.6,   42.7,   63.5),
'050x020':(   60.5,   27.2,   76.2),
'050x025':(   60.5,   34.0,   76.2),
'050x032':(   60.5,   42.7,   76.2),
'050x040':(   60.5,   48.6,   76.2),
'065x025':(   76.3,   34.0,   88.9),
'065x032':(   76.3,   42.7,   88.9),
'065x040':(   76.3,   48.6,   88.9),
'065x050':(   76.3,   60.5,   88.9),
'080x032':(   89.1,   42.7,   88.9),
'080x040':(   89.1,   48.6,   88.9),
'080x050':(   89.1,   60.5,   88.9),
'080x065':(   89.1,   76.3,   88.9),
'100x040':(  114.3,   48.6,  101.6),
'100x050':(  114.3,   60.5,  101.6),
'100x065':(  114.3,   76.3,  101.6),
'100x080':(  114.3,   89.1,  101.6),
'125x050':(  139.8,   60.5,  127.0),
'125x065':(  139.8,   76.3,  127.0),
'125x080':(  139.8,   89.1,  127.0),
'125x100':(  139.8,  114.3,  127.0),
'150x065':(  165.2,   76.3,  139.7),
'150x080':(  165.2,   89.1,  139.7),
'150x100':(  165.2,  114.3,  139.7),
'150x125':(  165.2,  139.8,  139.7),
'200x100':(  216.3,  114.3,  152.4),
'200x125':(  216.3,  139.8,  152.4),
'200x150':(  216.3,  165.2,  152.4),
'250x100':(  267.4,  114.3,  177.8),
'250x125':(  267.4,  139.8,  177.8),
'250x150':(  267.4,  165.2,  177.8),
'250x200':(  267.4,  216.3,  177.8),
'300x125':(  318.5,  139.8,  203.2),
'300x150':(  318.5,  165.2,  203.2),
'300x200':(  318.5,  216.3,  203.2),
'300x250':(  318.5,  267.4,  203.2),
'350x150':(  355.6,  165.2,  330.2),
'350x200':(  355.6,  216.3,  330.2),
'350x250':(  355.6,  267.4,  330.2),
'350x300':(  355.6,  318.5,  330.2),
'400x200':(  406.4,  216.3,  355.6),
'400x250':(  406.4,  267.4,  355.6),
'400x300':(  406.4,  318.5,  355.6),
'400x350':(  406.4,  355.6,  355.6),
'450x250':(  457.2,  267.4,  381.0),
'450x300':(  457.2,  318.5,  381.0),
'450x350':(  457.2,  355.6,  381.0),
'450x400':(  457.2,  406.4,  381.0),
'500x300':(  508.0,  318.5,  508.0),
'500x350':(  508.0,  355.6,  508.0),
'500x400':(  508.0,  406.4,  508.0),
'500x450':(  508.0,  457.2,  508.0),
'550x400':(  558.8,  406.4,  508.0),
'550x450':(  558.8,  457.2,  508.0),
'550x500':(  558.8,  508.8,  508.0),
'600x450':(  609.6,  457.2,  508.0),
'600x500':(  609.6,  508.0,  508.0),
'600x550':(  609.6,  558.8,  508.0),
'650x500':(  660.4,  508.0,  609.6),
'650x550':(  660.4,  558.8,  609.6),
'650x600':(  660.4,  609.6,  609.6),
'700x550':(  711.2,  558.8,  609.6),
'700x600':(  711.2,  609.6,  609.6),
'700x650':(  711.2,  660.4,  609.6),

}

#仕切弁　鋳鉄　JIS B 2031----------------------------------------
#                           ハンドル
#         L,    H(内), H(外), w,   a
gates_10k_cast={
'050':(  180,  300,   365,  200,  7),
'065':(  190,  330,   425,  200,  8),
'080':(  200,  380,   490,  224,  8),
'100':(  230,  430,   575,  250, 10),
'125':(  250,  490,   685,  280, 11),
'150':(  270,  560,   795,  300, 13),
'200':(  290,  650,  1000,  355, 15),
'250':(  330,  770,  1210,  400, 17),
'300':(  350,  885,  1420,  450, 19),
}

#仕切弁　ステンレス　JIS B 2031----------------------------------------
#                           ハンドル
#         L,    H(内), H(外), w,   a
gates_10k_SUS={
'050':(  178,  336,   336,  160,  7),
'065':(  190,  375,   375,  180,  8),
'080':(  203,  445,   445,  200,  8),
'100':(  229,  523,   523,  225, 10),
'125':(  254,  606,   606,  250, 11),
'150':(  267,  710,   710,  250, 13),
'200':(  292,  920,   920,  300, 15),
'250':(  330, 1117,  1117,  350, 17),
'300':(  356, 1324,  1324,  400, 19),
}

#逆止弁 鋳鉄　JIS B 2031----------------------------------------
#
#        d,   L,    H,   a,   d1,   R
checks_10k_cast={
'050':(  50,  200,  111,  7,  90,  120),
'065':(  65,  220,  121,  8, 115,  135),
'080':(  80,  240,  145,  8, 130,  150),
'100':( 100,  290,  165, 10, 165,  180),
'125':( 125,  360,  207, 11, 205,  250),
'150':( 150,  410,  225, 13, 240,  300),
'200':( 200,  500,  268, 15, 305,  370),
'250':( 250,  620,  319, 15, 305,  370),
'300':( 300,  700,  356, 15, 305,  370),
'350':( 350,  787,  381, 15, 305,  400),
}

#逆止弁 鋳鉄　水協----------------------------------------
#
#        d,   L,    H,   a,   d1,   R
checks_75k_cast={
'075':( 75,  290,  165, 10, 165,  180),    
'100':( 100,  290,  165, 10, 165,  180),
'125':( 125,  360,  207, 11, 205,  250),
'150':( 150,  410,  225, 13, 240,  300),
'200':( 200,  500,  268, 15, 290,  350),
'250':( 250,  620,  315, 15, 340,  300),
'300':( 300,  700,  356, 15, 390,  450),
'350':( 350,  787,  381, 15, 440,  500),

}

#逆止弁 青銅　JIS B 2031----------------------------------------
#
#        d,   L,    H
checks_10k_bronz={
'050':(  50,  200,  111),
'065':(  65,  220,  121),
'080':(  80,  240,  145),
'100':( 100,  290,  165),
'125':( 125,  360,  207),
'150':( 150,  410,  225),
'200':( 200,  500,  268),
'250':( 250,  620,  315),
'300':( 300,  700,  356),
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