mate=['Carbon steel','Stainless steel',]
lst=['00_Straight Pipe','01_T_collar','02_Cap','03_Flange','04_Nipple','05_Bend','06_Reducer','07_Tee','08_Cross','09_Y_bend',
'10_Damper']
l_lst={'00':'直管','01':'Tカラー','02':'キャップ','03':'フランジ','04':'ニップル','05':'ベンド','06':'レジューサ','07':'チーズ','08':'クロス','09':'Y_ベンド',
'10':'ダンパー'}
#lst_dv=['00_Straight Pipe','01_Elbow','02_Socket','03_Y90','04_Flange','05_Damper']
#l_lst__dv={'00':'直管','01':'エルボ','02':'ソケット','03':'チーズ','04':'フランジ','05':'ダンパー'}
spiral_d=['75','100','125','150','175','200','225','250','275',
'300','325','350','375','400','450','500','550','600','650']

flg_d=['13','15','20','25','30','40','50','65','75','100','125','150','200','250','300',]
flg_d2=['010','015','020','025','032','040','050','065','080','100','125','150','200','250',
'300','350','400','450','500','600','700','800','900','1000']

reduc_d=[
'100x75','125x100','150x100','150x125','175x100','175x125','175x150','200x100','200x125',
'200x150','200x175','225x125','225x150','225x175','225x200','250x125','250x150','250x175',
'250x200','250x225','275x125','275x150','275x175','275x200','275x225','275x250','300x150',
'300x175','300x200','300x225','300x250','300x275','325x150','325x175','325x200','325x225',
'325x250','325x275','325x300','350x175','350x200','350x225','350x250','350x275','350x300',
'350x325','375x200','375x225','375x250','375x275','375x300','375x325','375x350','400x200',
'400x225','400x250','400x275','400x300','400x325','400x350','400x375','450x225','450x250',
'450x275','450x300','450x325','450x350','450x375','450x400','500x250','500x275','500x300',
'500x325','500x350','500x375','500x400','500x450','550x275','550x300','550x325','550x350',
'550x375','550x400','550x450','550x500','600x300','600x325','600x350','600x375','600x400',
'600x450','600x500','600x550','650x325','650x350','650x375','650x400','650x450','650x500',
'650x550','650x600',
]

tee_d=[
'75x75','100x75','100x100','125x100','150x100','150x125','150x150','175x100','175x125','175x150',
'175x175','200x100','200x125','200x150','200x175','200x200','225x100','225x125','225x150','225x200',
'225x225','250x100','250x125','250x150','250x175','250x200','250x225','275x100','275x125','275x150',
'275x175','275x200','275x225','275x250','275x275','300x100','300x125','300x150','300x175','300x200',
'300x225','300x250','300x275','300x300','325x200','325x225','325x250','325x275','325x300','325x325',
'350x200','350x225','350x250','350x275','350x300','350x325','350x350','375x250','375x275','375x300',
'375x325','375x350','375x375','400x250','400x275','400x300','400x325','400x350','400x375','400x400',
'450x300','450x350','450x400','450x450','500x300','500x350','500x400','500x450','500x500','550x350',
'550x400','550x450','550x500','550x550','600x400','600x450','600x500','600x550','600x600','650x450',
'650x500','650x550','650x600','650x650',
]

pipe_st=['Spiral','Single_flange','Both_flange',]
collar_st=['T_collar',]
cap_st=['Pipe_use','Fitting_use',]
nipple_st=['Socket',]
flg_st=['Plate','Angle','Packing']
bend_st=['90','45',]
reduc_st=['Socket',]
tee_st=['Socket',]
y_st=['Socket',]
damper_st=['VD_A',]

#直管 スパイラル
#口径,外径,                                     T_collar,   F_collar
#,,     d,    t,    W,    P,     D1,     S,    D0,         D0
strt_dia={
'75':(   73,  0.5,  6,    60,     79.0,  60,   112,        90),
'100':(  98,  0.5,  6,    87,    104.0,  60,   140,       116),
'125':( 123,  0.5,  6,    86,    129.0,  60,   165,       141),
'150':( 148,  0.5,  6,   140,    154.0,  80,   200,       166),
'175':( 173,  0.5,  6,   138,    179.0,  80,   225,       191),
'200':( 198,  0.5,  6,   137,    204.0,  80,   250,       216),
'225':( 223,  0.5,  6,   136,    229.0,  80,   275,       241),
'250':( 248,  0.5,  6,   136,    254.0,  80,   300,       266),
'275':( 273,  0.5,  6,   136,    279.0,  80,   325,       291),
'300':( 298,  0.5,  6,   135,    304.0,  80,   350,       316),
'325':( 323,  0.6,  7,   135,    329.8, 100,   375,       341),
'350':( 348,  0.6,  7,   135,    354.8, 100,   400,       366),
'375':( 373,  0.6,  7,   135,    379.8, 100,   425,       391),
'400':( 398,  0.6,  7,   135,    404.8, 100,   450,       416),
'450':( 448,  0.6,  7,   135,    454.8, 100,   466,       466),
'500':( 498,  0.6,  7,   134,    504.8, 100,   516,       516),
'550':( 548,  0.6,  7,   134,    554.8, 100,   566,       566),
'600':( 598,  0.6,  7,   134,    604.8, 100,   616,       616),
'650':( 647,  0.8,  8,   134,    656.4, 100,   666,       666),
}

#フランジ
#        D,   D1,   PCD,    n
flange_dia={
'75':(   75,  125,  105,    4),
'100':( 100,  150,  130,    6),
'125':( 125,  175,  155,    6),
'150':( 150,  200,  180,    6),
'175':( 175,  225,  205,    6),
'200':( 200,  250,  230,    8),
'225':( 225,  275,  255,    8),
'250':( 250,  300,  280,    8),
'275':( 275,  325,  305,   12),
'300':( 300,  350,  330,   12),
'325':( 325,  375,  355,   12),
'350':( 350,  400,  380,   12),
'375':( 375,  425,  405,   12),
'400':( 400,  450,  430,   16),
'450':( 450,  500,  480,   16),
'500':( 500,  550,  530,   16),
'550':( 550,  600,  580,   20),
'600':( 600,  650,  630,   20),
'650':( 650,  700,  680,   20),
}

#フランジカラー
#        D1,   t,   D0
f_collar_dia={
'75':(   73,  0.6,   90),
'100':(  98,  0.6,  116),
'125':( 123,  0.6,  141),
'150':( 148,  0.6,  166),
'175':( 173,  0.6,  191),
'200':( 198,  0.6,  216),
'225':( 223,  0.6,  241),
'250':( 248,  0.6,  266),
'275':( 273,  0.6,  291),
'300':( 298,  0.6,  316),
'325':( 323,  0.8,  341),
'350':( 348,  0.8,  366),
'375':( 373,  0.8,  391),
'400':( 398,  0.8,  398),
'450':( 448,  0.8,  448),
'500':( 498,  0.8,  498),
'550':( 548,  0.8,  548),
'600':( 598,  0.8,  598),
'650':( 647,  0.8,  647),
}

#                   pipe
#        D,   t,    D0,   l
p_cap_dia={
'75':(   73,  0.6,   95,  45),
'100':(  98,  0.6,  110,  45),
'125':( 123,  0.6,  135,  45),
'150':( 148,  0.6,  160,  45),
'175':( 173,  0.6,  185,  45),
'200':( 198,  0.6,  210,  45),
'225':( 223,  0.6,  235,  55),
'250':( 248,  0.6,  260,  55),
'275':( 273,  0.6,  285,  55),
'300':( 298,  0.6,  310,  55),
'325':( 323,  0.8,  335,  65),
'350':( 348,  0.8,  360,  65),
'375':( 373,  0.8,  385,  65),
'400':( 398,  0.8,  420,  65),
}

#片落管
#           L
reduc_dia={
'100x75':(   60,),
'125x100':(  65,),
'150x100':( 100,),
'150x125':(  65,),
'175x100':( 175,),
'175x125':( 100,),
'175x150':(  65,),
'200x100':( 210,),
'200x125':( 175,),
'200x150':( 100,),
'200x175':(  65,),
'225x125':( 210,),
'225x150':( 175,),
'225x175':( 100,),
'225x200':(  65,),
'250x125':( 245,),
'250x150':( 210,),
'250x175':( 175,),
'250x200':( 100,),
'250x225':(  65,),
'275x125':( 280,),
'275x150':( 245,),
'275x175':( 210,),
'275x200':( 175,),
'275x225':( 100,),
'275x250':(  65,),
'300x150':( 280,),
'300x175':( 245,),
'300x200':( 210,),
'300x225':( 175,),
'300x250':( 100,),
'300x275':(  65,),
'325x150':( 315,),
'325x175':( 280,),
'325x200':( 245,),
'325x225':( 210,),
'325x250':( 175,),
'325x275':( 100,),
'325x300':(  65,),
'350x175':( 315,),
'350x200':( 280,),
'350x225':( 245,),
'350x250':( 210,),
'350x275':( 175,),
'350x300':( 100,),
'350x325':(  65,),
'375x200':( 315,),
'375x225':( 280,),
'375x250':( 245,),
'375x275':( 210,),
'375x300':( 175,),
'375x325':( 140,),
'375x350':( 105,),
'400x200':( 350,),
'400x225':( 315,),
'400x250':( 280,),
'400x275':( 245,),
'400x300':( 210,),
'400x325':( 175,),
'400x350':( 140,),
'400x375':( 105,),
'450x225':( 385,),
'450x250':( 350,),
'450x275':( 315,),
'450x300':( 280,),
'450x325':( 245,),
'450x350':( 210,),
'450x375':( 175,),
'450x400':( 140,),
'500x250':( 420,),
'500x275':( 385,),
'500x300':( 350,),
'500x325':( 315,),
'500x350':( 280,),
'500x375':( 245,),
'500x400':( 210,),
'500x450':( 140,),
'550x275':( 455,),
'550x300':( 420,),
'550x325':( 385,),
'550x350':( 350,),
'550x375':( 315,),
'550x400':( 280,),
'550x450':( 210,),
'550x500':( 140,),
'600x300':( 490,),
'600x325':( 455,),
'600x350':( 420,),
'600x375':( 385,),
'600x400':( 350,),
'600x450':( 280,),
'600x500':( 210,),
'600x550':( 140,),
'650x325':( 525,),
'650x350':( 490,),
'650x375':( 455,),
'650x400':( 420,),
'650x450':( 350,),
'650x500':( 280,),
'650x550':( 210,),
'650x600':( 140,),
}

#             T管         Y管
#             L,    l,    L,   l,   L1
tee_dia={
'75x75':(     135,  67.5, 205, 141, 65),
'100x75':(    135,  80.0, 205, 159, 53),
'100x100':(   160,  80.0, 240, 171, 70),
'125x100':(   160,  92.5, 240, 189, 58),
'125x125':(   185,  92.5, 275, 201, 75),
'150x100':(   160,  92.5, 240, 207, 45),
'150x125':(   185, 105.0, 275, 219, 63),
'150x150':(   210, 105.0, 310, 232, 80),
'175x100':(   160, 117.5, 240, 224, 33),
'175x125':(   185, 117.5, 275, 237, 50),
'175x150':(   210, 117.5, 310, 249, 68),
'175x175':(   235, 117.5, 345, 262, 85),
'200x100':(   160, 130.0, 240, 242, 20),
'200x125':(   185, 130.0, 275, 254, 38),
'200x150':(   210, 130.0, 310, 267, 55),
'200x175':(   235, 130.0, 345, 279, 73),
'200x200':(   260, 130.0, 380, 202, 80),
'225x100':(   160, 142.5, 240, 260,  8),
'225x125':(   185, 142.5, 275, 272, 25),
'225x150':(   210, 142.5, 310, 285, 43),
'225x200':(   260, 142.5, 380, 310, 78),
'225x225':(   285, 142.5, 415, 322, 95),
'250x100':(   160, 155.0, 240, 277, -5),
'250x125':(   185, 155.0, 275, 290, 13),
'250x150':(   210, 155.0, 310, 302, 30),
'250x175':(   235, 155.0, 345, 315, 48),
'250x200':(   260, 155.0, 380, 327, 65),
'250x225':(   285, 155.0, 415, 340, 83),
'250x250':(   310, 155.0, 450, 352,100),
'275x100':(   160, 167.5, 240, 295,-20),
'275x125':(   185, 167.5, 275, 307,  0),
'275x150':(   210, 167.5, 310, 320, 18),
'275x175':(   235, 167.5, 345, 332, 35),
'275x200':(   260, 167.5, 380, 345, 53),
'275x225':(   285, 167.5, 315, 355, 70),
'275x250':(   310, 167.5, 450, 370, 88),
'275x275':(   335, 167.5, 485, 380,105),
'300x100':(   160, 180.0, 240, 313,-30),
'300x125':(   185, 180.0, 275, 325,-13),
'300x150':(   210, 180.0, 310, 338,  5),
'300x175':(   235, 180.0, 345, 350, 23),
'300x200':(   280, 180.0, 380, 363, 40),
'300x225':(   285, 180.0, 415, 375, 58),
'300x250':(   310, 180.0, 450, 385, 75),
'300x275':(   335, 180.0, 485, 400, 93),
'300x300':(   360, 180.0, 520, 413,110),
'325x200':(   260, 192.5, 380, 380, 28),
'325x225':(   285, 192.5, 415, 390, 45),
'325x250':(   310, 192.5, 450, 405, 63),
'325x275':(   335, 192.5, 485, 415, 80),
'325x300':(   360, 192.5, 520, 430, 98),
'325x325':(   385, 192.5, 555, 440,115),
'350x200':(   260, 205.0, 380, 398, 15),
'350x225':(   285, 205.0, 415, 410, 33),
'350x250':(   310, 205.0, 450, 423, 50),
'350x275':(   335, 205.0, 485, 435, 68),
'350x300':(   360, 205.0, 520, 448, 85),
'350x325':(   385, 205.0, 555, 460,103),
'350x350':(   410, 205.0, 590, 470,120),
'375x250':(   310, 217.5, 450, 440, 38),
'375x275':(   235, 217.5, 485, 453, 55),
'375x300':(   360, 217.5, 520, 465, 73),
'375x325':(   385, 217.5, 555, 478, 90),
'375x350':(   410, 217.5, 590, 490,108),
'375x375':(   435, 217.5, 625, 503,125),
'400x250':(   310, 230.0, 450, 458, 25),
'400x275':(   335, 230.0, 485, 471, 43),
'400x300':(   360, 230.0, 520, 483, 60),
'400x325':(   385, 230.0, 555, 495, 78),
'400x350':(   410, 230.0, 590, 508, 95),
'400x375':(   435, 230.0, 625, 521,113),
'400x400':(   460, 230.0, 660, 533,130),
'450x300':(   360, 255.0, 520, 519, 35),
'450x350':(   410, 255.0, 590, 544, 70),
'450x400':(   460, 255.0, 660, 569,105),
'450x450':(   510, 255.0, 730, 594,140),
'500x300':(   360, 280.0, 520, 554, 10),
'500x350':(   410, 280.0, 590, 579, 45),
'500x400':(   460, 280.0, 660, 604, 80),
'500x450':(   510, 280.0, 730, 629,115),
'500x500':(   560, 280.0, 800, 654,150),
'550x350':(   410, 305.0, 590, 614, 20),
'550x400':(   460, 305.0, 660, 639, 55),
'550x450':(   510, 305.0, 730, 664, 90),
'550x500':(   560, 305.0, 800, 689,125),
'550x550':(   610, 305.0, 870, 714,160),
'600x400':(   460, 330.0, 660, 675, 30),
'600x450':(   510, 330.0, 730, 700, 65),
'600x500':(   560, 330.0, 800, 725,100),
'600x550':(   610, 330.0, 870, 750,135),
'600x600':(   660, 330.0, 940, 775,170),
'650x450':(   510, 355.0, 730, 735, 40),
'650x500':(   560, 355.0, 800, 760, 75),
'650x550':(   610, 355.0, 870, 785,110),
'650x600':(   660, 355.0, 940, 810,145),
'650x650':(   710, 355.0,1010, 835,180),
}

#ダンパーA パイプ式
#口径,   d,    B,    L,  t
dv_dapA={

'75':(  73,   83.0, 200, 0.5),
'100':( 98,  107.8, 210, 0.5),
'125':(123,  131.8, 240, 0.5),
'150':(148,  154.8, 270, 0.5),
'200':(198,  203.0, 330, 0.5),
'250':(248,  251.4, 368, 0.5),
'300':(298,  299.6, 406, 0.5),
}