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
import ParamDuct

DEBUG = True # set to True to show debug messages

lst=['00_Round','01_Square',]
kanzai_r=[
'Straight Pipe','Collar','Cap','Flange','Nipple','Bend','Reducer','Tee','Cross','Y_bend',
'Damper'
]
kanzai_r2=['直管','Tカラー','キャップ','フランジ','ニップル']
kanzai_dv=['Straight Pipe','Elbow','Socket','Y90','Flange','Damper']
kanzai_dv2=['直管','エルボ','ソケット','チーズ','フランジ','ダンパー']
spiral_d=[
'75','100','125','150','175','200','225','250','275',
'300','325','350','375','400','450','500','550','600','650'
]

flg_d=['13','15','20','25','30','40','50','65','75','100','125','150','200','250','300',]
flg_d2=['010','015','020','025','032','040','050','065','080','100','125','150','200','250',
'300','350','400','450','500','600','700','800','900','1000'
]

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

pipe_st=['Spiral','Single_flange_SUS','Both_flange_SUS',]
collar_st=['T_collar','Flange_collar',]
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


class ViewProvider:
    def __init__(self, obj):
        obj.Proxy = self

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(270, 292)
        Dialog.move(1000, 0)
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
        #チェックボックス
        self.checkbox = QtGui.QCheckBox(Dialog)
        self.checkbox.setGeometry(QtCore.QRect(180, 113, 90, 23))
        self.checkbox.setObjectName("checkbox")
        #img
        self.label_img = QtGui.QLabel(Dialog)
        self.label_img.setGeometry(QtCore.QRect(0, 190, 270, 100))
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img.setText("")

        self.retranslateUi(Dialog)
        self.comboBox_kanzai.addItems(kanzai_r)
        self.comboBox_standard.addItems(pipe_st)
        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(spiral_d)
        self.comboBox_kanzai.currentIndexChanged[int].connect(self.on_lst)
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
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ダクト材", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
            self.kanzai.setText(QtGui.QApplication.translate("Dialog", "管材", None, QtGui.QApplication.UnicodeUTF8))
            self.label_l.setText(QtGui.QApplication.translate("Dialog", "管材", None, QtGui.QApplication.UnicodeUTF8))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None, QtGui.QApplication.UnicodeUTF8))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None, QtGui.QApplication.UnicodeUTF8))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None, QtGui.QApplication.UnicodeUTF8))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None, QtGui.QApplication.UnicodeUTF8))
            self.checkbox.setText(QtGui.QApplication.translate("Dialog", "ねじ表示", None, QtGui.QApplication.UnicodeUTF8))

        except:
            Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "ダクト材", None))
            self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Create", None))
            self.kanzai.setText(QtGui.QApplication.translate("Dialog", "管材", None))
            self.label_l.setText(QtGui.QApplication.translate("Dialog", "管材", None))
            self.label_standard.setText(QtGui.QApplication.translate("Dialog", "規格", None))
            self.label_dia.setText(QtGui.QApplication.translate("Dialog", "口径", None))
            self.label_4.setText(QtGui.QApplication.translate("Dialog", "ライセンスキー", None))
            self.pushButton_1.setText(QtGui.QApplication.translate("Dialog", "保存", None))
            self.checkbox.setText(QtGui.QApplication.translate("Dialog", "ねじ表示", None))

    def license(self):
        x = self.lineEdit.text()
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        with open(joined_path, mode='w') as ff:
            ff.write(x)
            ff.close()

    def on_lst2(self):#管長

        if k_index==0 :
            L=4000
            try:
              self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None, QtGui.QApplication.UnicodeUTF8))
            except:
              self.label_5.setText(QtGui.QApplication.translate("Dialog", "管長[mm]", None))

            self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))

        else:
            self.label_5.setText(QtGui.QApplication.translate("Dialog", "", None))
            self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(''), None))
    def on_lst(self):
        global sa2
        global xlc
        self.comboBox_standard.clear()
        xcf='2153987651329bc7526586915547'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"data","h_license.txt")
        ff= open(joined_path)
        data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", str(data1), None))
        ff.close()
        #sa=kanzai_r
        #sa2=kanzai_r2
        #self.comboBox_kanzai.clear()
        #self.comboBox_kanzai.addItems(sa)
        #xlc=xcf[13:17]
        xlc='***'
        self.label_l.setText(QtGui.QApplication.translate("Dialog", str(xlc), None))

    def on_standard(self):
        global st
        global FC
        global sa2
        global pic
        st=self.comboBox_standard.currentText()
        if k_index==0:#直管
            if st=='Spiral' :
                sa2=spiral_d
                pic='img_pvc_pipe.png'
                FC='スパイラル直管'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'スパイラル直管', None))
            elif st=='Single_flange_SUS' :
                sa2=spiral_d
                pic='img_Single_flange_sus.png'
                FC='1F直管_SUS'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", '1F直管_SUS', None))
            elif st=='Both_flange_SUS' :
                sa2=spiral_d
                pic='img_Both_flange_sus.png'
                FC='2F直管_SUS'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", '2F直管_SUS', None))
        elif k_index==1:#カラー
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(k_index), None, QtGui.QApplication.UnicodeUTF8))
            sa2=spiral_d[1:]
            if st=='T_collar':
                pic='img_t_collar.png'
                FC='Tカラー'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'Tカラー', None))
            elif st=='Flange_collar':
                pic='img_flange_collar.png'
                FC='フランジカラー'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'フランジカラー', None))
        elif k_index==2:#キャップ
            sa2=spiral_d[:14]
            s_index=self.comboBox_standard.currentIndex()
            if s_index==0:
                pic='img_spiral_cap_pipe_use.png'
            elif s_index==1:
                pic='img_spiral_cap_fitting_use.png'
            elif s_index==2:
                pic='img_sus_cap_pipe_use.png'
            elif s_index==3:
                pic='img_sus_cap_fitting_use.png'
            FC='キャップ'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'キャップ', None))
        elif k_index==3:#フランジ
            s_index=self.comboBox_standard.currentIndex()
            if s_index==0:
                sa2=spiral_d[:5]
                pic='img_flange_plate.png'
                FC='フランジ'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'フランジ', None))
            elif s_index==1:
                sa2=spiral_d[5:]
                pic='img_flange_angle.png'
                FC='フランジ'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'フランジ', None))
            elif s_index==2:
                sa2=spiral_d
                pic='img_spiral_packing.png'
                FC='パッキン'
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'パッキン', None))
        elif k_index==4:#ニップル
            sa2=spiral_d[1:]
            pic='img_spiral_nipple.png'
            FC='ニップル'
            self.label_l.setText(QtGui.QApplication.translate("Dialog", 'ニップル', None))
        elif k_index==5:#ベンド
            sa2=spiral_d[1:]
            if st=='90':
                pic='img_spiral_bend90.png'
            elif st=='45':
                pic='img_spiral_bend45.png'
            FC='ベンド'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'ベンド', None))
        elif k_index==6:#片落管
            sa2=reduc_d
            pic='img_spiral_reduc.png'
            FC='片落管'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", '片落管', None))
        elif k_index==7 or k_index==8:#T字管 クロス
            sa2=tee_d
            if k_index==7:
                pic='img_spiral_tee.png'
            elif k_index==8:
                    pic='img_spiral_cross.png'
            FC= 'T字管'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'T字管', None))
        elif k_index==9:#Y管
            sa2=tee_d
            if st=='Socket':
                pic='img_spiral_y.png'
            FC= 'Y管'
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", 'Y管', None))
        elif k_index==10:#ダンパー
            sa2=spiral_d[:10]
            if st=='VD_A':
                pic='img_spiral_VD_A.png'
            elif st=='VD_B':
                pic='img_VD_B.png'
            FC=  'ダンパー'

        try:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.label_l.setText(QtGui.QApplication.translate("Dialog", FC, None))

        self.comboBox_dia.clear()
        self.comboBox_dia.addItems(sa2)

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "data",pic)
        self.label_img.setPixmap(QtGui.QPixmap(joined_path))

    def on_kanzai(self):
        global dia
        global pic
        global k_index
        k_index=self.comboBox_kanzai.currentIndex()
        dia=self.comboBox_dia.currentText()
        st=self.comboBox_standard.currentText()


        if k_index==0:
            sa=pipe_st
            sa2=spiral_d
        elif k_index==1:#カラー
            sa=collar_st
        elif k_index==2:#キャップ
            sa=cap_st
        elif k_index==3:#フランジ
            sa=flg_st
        elif k_index==4:#ニップル
            sa=nipple_st
        elif k_index==5:#ベンド
            sa=bend_st
        elif k_index==6:#片落管
            sa=reduc_st
        elif k_index==7:#T字管
            sa=tee_st
        elif k_index==8:#クロス
            sa=tee_st
        elif k_index==9:#Y
            sa=y_st
        elif k_index==10:#ダンパー
            sa=damper_st

        self.comboBox_standard.clear()
        self.comboBox_standard.addItems(sa)
        self.comboBox_dia.clear()
        #self.comboBox_dia.addItems(sa2)

    def create(self):
        global st
        st=self.comboBox_standard.currentText()
        dia=self.comboBox_dia.currentText()
        #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
        lsky=self.lineEdit.text()
        #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(xlc), None, QtGui.QApplication.UnicodeUTF8))
        if lsky!=xlc:
            if k_index > 4:
               lsk='ライセンスキーを入力してください。'
               self.label_l.setText(QtGui.QApplication.translate("Dialog", lsk, None))
               return

        def outlet(self):

            global c01
            sa=strt_dia[dia]
            D=float(dia)
            d=float(sa[0])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(dia), None, QtGui.QApplication.UnicodeUTF8))
            t=float(sa[1])
            W=float(sa[2])
            D1=D+2*t
            S=float(sa[5])
            p1=(0,d/2-t,0)
            p2=(0,D1/2,0)
            p3=(W,D1/2,0)
            p4=(W,(d)/2,0)
            p5=(W+S,(d)/2,0)
            p6=(W+S,d/2-t,0)
            plst=[p1,p2,p3,p4,p5,p6,p1]
            pwire=Part.makePolygon(plst)
            pface = Part.Face(pwire)
            c01=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)

        def a_flange(self):
            global c00
            sa=strt_dia[dia]
            t1=sa[1]
            sa=flange_dia[dia]
            d=sa[0]/2
            C=float(sa[2])/2
            n=sa[3]
            A=float(25)
            B=float(25)
            t=3
            r1=4
            r2=2
            x1=r2*(1-1/math.sqrt(2))
            x2=r2-x1
            y1=r1*(1-1/math.sqrt(2))
            y2=r1-y1
            y3=A-(r2+r1+t)
            x=t-r2
            p1=(0,0,0)
            p2=(0,0,A)
            p3=(x,0,A)
            p4=(t-x1,0,A-x1)
            p5=(t,0,A-r2)
            p6=(t,0,A-(r2+y3))
            p7=(t+y1,0,t+y1)
            p8=(t+r1,0,t)
            p9=(B-r2,0,t)
            p10=(B-x1,0,t-x1)
            p11=(B,0,t-r2)
            p12=(B,0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.Arc(Base.Vector(p3),Base.Vector(p4),Base.Vector(p5)).toShape()
            edge4=Part.makeLine(p5,p6)
            edge5=Part.Arc(Base.Vector(p6),Base.Vector(p7),Base.Vector(p8)).toShape()
            edge6=Part.makeLine(p8,p9)
            edge7=Part.Arc(Base.Vector(p9),Base.Vector(p10),Base.Vector(p11)).toShape()
            edge8=Part.makeLine(p11,p12)
            edge9=Part.makeLine(p12,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8,edge9])
            aWire.Placement=App.Placement(App.Vector(0,0,d+t1+0.1),App.Rotation(App.Vector(0,0,1),0))
            c01=Part.makeCircle(d+t1,Base.Vector(0,0,0),Base.Vector(1,0,0),0,360)
            makeSolid=True
            isFrenet=True
            c00 = Part.Wire(c01).makePipeShell([aWire],makeSolid,isFrenet)
            h=5
            for i in range(n):
                k=math.pi*2/n
                if i==0:
                    x=C*math.cos(k/2)
                    y=C*math.sin(k/2)
                    c20 = Part.makeCylinder(h,1.5*t,Base.Vector(0,x,y),Base.Vector(1,0,0))

                else:
                    ks=i*k+k/2
                    x=C*math.cos(ks)
                    y=C*math.sin(ks)
                    c20 = Part.makeCylinder(h,1.5*t,Base.Vector(0,x,y),Base.Vector(1,0,0))
                if i==0:
                    c00=c00.cut(c20)
                else:
                    c00=c00.cut(c20)

        def p_flange(self):#プレートフランジ
            global c00
            sa=strt_dia[dia]
            t1=sa[1]
            sa=flange_dia[dia]
            D=float(sa[0])/2
            n=sa[3]
            h=5
            t=4.5
            D0=D+25
            C=D+15
            c1 = Part.makeCylinder(D0,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c2 = Part.makeCylinder(D+t1,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(k_index), None, QtGui.QApplication.UnicodeUTF8))
            c00=c1.cut(c2)
            for i in range(n):
                k=math.pi*2/n
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

        def packing(self):#パッキン
            global c00
            sa=flange_dia[dia]
            D=float(sa[0])/2
            n=sa[3]
            h=5
            t=3.0
            D0=D+25
            C=D+15
            c1 = Part.makeCylinder(D0,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c2 = Part.makeCylinder(D+t,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c00=c1.cut(c2)
            for i in range(n):
                k=math.pi*2/n
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


        if k_index==0 :#直管
            sa=strt_dia[dia]
            d=float(dia)
            t1=float(sa[1])
            W=float(sa[2])
            p=float(sa[3])
            D1=float(sa[4])
            L=float(self.lineEdit_1.text())
            sa=flange_dia[dia]
            D=float(sa[0])/2
            n=sa[3]
            label = 'Straight_tube_' + st + " " +"_"
            obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
            if k_index==0:
                obj.addProperty("App::PropertyInteger", "k_index",label).k_index=k_index
                obj.addProperty("App::PropertyString", "st",label).st=st
                obj.addProperty("App::PropertyFloat", "d",'pipe').d=d
                obj.addProperty("App::PropertyFloat", "t1",'pipe').t1=t1
                obj.addProperty("App::PropertyFloat", "D",label).D=D
                obj.addProperty("App::PropertyInteger", "n",label).n=n
                obj.addProperty("App::PropertyFloat", "L",'pipe').L=L

            ParamDuct.duct_p(obj)
            obj.ViewObject.Proxy=0
            FreeCAD.ActiveDocument.recompute()   
            return


        elif k_index==1:#カラー
            if st=='T_collar':
                sa=strt_dia[dia]
                d=float(sa[0])
                t=float(sa[1])
                W=float(sa[2])
                D1=d+8*t
                S=float(sa[5])
                D0=float(sa[6])
                if d<=400:
                    p1=(0,D1/2-t,0)
                    p2=(0,D0/2,0)
                    p3=(t,D0/2,0)
                    p4=(t,D1/2,0)
                    p5=(30,D1/2,0)
                    p6=(30+S,d/2,0)
                    p7=(30+S,d/2-t,0)
                    p8=(30-t,d/2-t,0)
                    p9=(30-t,D1/2-t,0)
                    p10=(30,d/2,0)
                    plst=[p1,p2,p3,p4,p5,p10,p6,p7,p8,p9,p1]
                    pwire=Part.makePolygon(plst)
                    pface = Part.Face(pwire)
                    c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                    sa=flange_dia[dia]
                    PCD=(D0-18)/2
                    n=sa[3]
                    h=3.5
                    t=5
                    for i in range(n):
                        k=math.pi*2/n
                        if i==0:
                            x=PCD*math.cos(k/2)
                            y=PCD*math.sin(k/2)
                            c20 = Part.makeCylinder(h,t,Base.Vector(x,0,y),Base.Vector(0,1,0))
                            c20.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-90))
                        else:
                            ks=i*k+k/2
                            x=PCD*math.cos(ks)
                            y=PCD*math.sin(ks)
                            c20 = Part.makeCylinder(h,t,Base.Vector(x,0,y),Base.Vector(0,1,0))
                            c20.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-90))
                        #Part.show(c20)
                        c1=c1.cut(c20)
                elif d>400:
                    outlet(self)
                    c1=c01
                    c1.Placement=App.Placement(App.Vector(30-W,0,0),App.Rotation(App.Vector(0,1,0),0))
                    p1=(0,(d-2*t)/2,0)
                    p2=(0,D0/2,0)
                    p3=(t,D0/2,0)
                    p4=(t,d/2,0)
                    p5=(30-W,d/2,0)
                    p6=(30-W,(d-2*t)/2,0)
                    plst=[p1,p2,p3,p4,p5,p6,p1]
                    pwire=Part.makePolygon(plst)
                    pface = Part.Face(pwire)
                    c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                    c1=c1.fuse(c2)
                b='T_collar'
                label=b + '_' + str(dia) +'_'
            elif st=='Flange_collar':
                sa=f_collar_dia[dia]
                D1=float(sa[0])
                t=float(sa[1])
                D0=float(sa[2])
                L=100
                d=D1+2*t
                p1=(0,d/2,0)
                p2=(0,D1/2,0)
                p3=(L-t,D1/2,0)
                p4=(L-t,D0/2,0)
                p5=(L,D0/2,0)
                p6=(L,d/2,0)
                plst=[p1,p2,p3,p4,p5,p6,p1]
                pwire=Part.makePolygon(plst)
                pface = Part.Face(pwire)
                c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                b='Flange_collar'
                label=b + '_' + str(dia) +'_'

        elif k_index==2:#キャップ
            if st=='Pipe_use':
                sa=p_cap_dia[dia]
                D1=float(sa[0])
                t=float(sa[1])
                l=15
                D0=float(sa[2])
                p1=(0,(D1-2*t)/2,0)
                p2=(0,(D0)/2,0)
                p3=(t,(D0)/2,0)
                p4=(t,(D1)/2,0)
                p5=(l,(D1)/2,0)
                p6=(l,0,0)
                p7=(l-t,0,0)
                p8=(l-t,(D1-2*t)/2,0)
                plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                pwire=Part.makePolygon(plst)
                pface = Part.Face(pwire)
                c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            elif st=='Fitting_use':
                sa=p_cap_dia[dia]
                D1=float(sa[0])
                t=float(sa[1])
                l=float(sa[3])
                D0=float(sa[2])
                p1=(0,(D1)/2,0)
                p2=(0,(D1+2*t)/2,0)
                p3=(l,(D1+2*t)/2,0)
                p4=(l,0,0)
                p5=(l-t,0,0)
                p6=(l-t,D1/2,0)
                plst=[p1,p2,p3,p4,p5,p6,p1]
                pwire=Part.makePolygon(plst)
                pface = Part.Face(pwire)
                c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            b='Cap_'
            label=b + '_' + str(dia) +'_'
        elif k_index==3:#フランジ
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            if st=='Plate':
                p_flange(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                b='Flange_'
                label=b + '_' + str(dia) +'_'
            elif st=='Angle':
                a_flange(self)
                c1=c00
                b='Flange_'
                label=b + '_' + str(dia) +'_'
            elif st=='Packing':
                packing(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                b='Packing_'
                label=b + '_' + str(dia) +'_'

        elif k_index==4:#ニップル
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            if st=='Socket':
                outlet(self)
                c1=c01
                #c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                sa=f_collar_dia[dia]
                D1=sa[0]
                t=sa[1]
                sa=strt_dia[dia]
                S=sa[5]
                c2 = Part.makeCylinder(D1/2,S,Base.Vector(-S,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder((D1-2*t)/2,S,Base.Vector(-S,0,0),Base.Vector(1,0,0))
                c2=c2.cut(c3)
                c1=c1.fuse(c2)
                b='Nipple_'
                label=b + '_' + str(dia) +'_'

        elif k_index==5:#ベンド
            sa=strt_dia[dia]
            t=float(sa[1])
            W=float(sa[2])
            S=float(sa[5])
            D=float(dia)
            d2=D/2
            d0=d2-t
            if st=='45':
                H=0.4*D
            elif st=='90':
                H=D
            r=D
            s=float(st)/2
            s0=math.radians(s)
            edge1 = Part.makeCircle(r, Base.Vector(r,0,0), Base.Vector(0,0,1), 180-2*s, 180)
            edge2 = Part.makeCircle(d2, Base.Vector(0,0,0), Base.Vector(0,1,0), 0, 360)
            edge3 = Part.makeCircle(d0, Base.Vector(0,0,0), Base.Vector(0,1,0), 0, 360)
            aWire = Part.Wire([edge1])
            profile = Part.Wire([edge2])
            profile1 = Part.Wire([edge3])
            makeSolid=True
            isFrenet=True
            c1 = Part.Wire(aWire).makePipeShell([profile],makeSolid,isFrenet)
            c2 = Part.Wire(aWire).makePipeShell([profile1],makeSolid,isFrenet)
            c1=c1.cut(c2)
            if st=='45':
                x=r-r*math.cos(2*s0)
                y=r*math.sin(2*s0)
            elif st=='90':
                x=0
            outlet(self)
            c2=c01
            c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-90))
            c1=c1.fuse(c2)
            c2=c01

            if st=='90':
                c2.Placement=App.Placement(App.Vector(H,H,0),App.Rotation(App.Vector(0,0,1),90-2*s))
                c1=c1.fuse(c2)
            elif st=='45':
                c2.Placement=App.Placement(App.Vector(x,y,0),App.Rotation(App.Vector(0,0,1),90-2*s))
                c1=c1.fuse(c2)
            label = 'Bend_' + st + " " + str(dia) + " "

        elif k_index==6:#片落ち管
            global dia1
            global dia2

            if st=='Socket':
                sa=reduc_dia[dia]
                L=sa[0]
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=strt_dia[dia1]
                d1=float(sa[0])
                t=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=strt_dia[dia2]
                d2=float(sa[0])
                W2=float(sa[2])
                L1=L-(70+W1+W2)
                p1=(0,(d1-2*t)/2,0)
                p2=(0,(d1)/2,0)
                p3=(35-W1,(d1)/2,0)
                p4=(35-W1+L1,(d2)/2,0)
                p5=(L,(d2)/2,0)
                p6=(L,(d2-2*t)/2,0)
                p7=(L-(35-W2),(d2-2*t)/2,0)
                p8=(35-W1,(d1-2*t)/2,0)
                if L1<=(1.4*(D1-D2)+70+W1+W2):
                    plst=[p1,p2,p5,p6,p1]
                    pwire=Part.makePolygon(plst)
                    pface = Part.Face(pwire)
                    c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                elif L1>(1.4*(D1-D2)+70+W1+W2):
                    plst=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                    pwire=Part.makePolygon(plst)
                    pface = Part.Face(pwire)
                    c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                dia=dia1
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),180))
                c1=c1.fuse(c2)
                dia=dia2
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2)
            label = 'Reducer_'  +  str(dia) + " "


        elif k_index==7 or k_index==8:#T字管 クロス
            #global dia1
            #global dia2

            if st=='Socket':
                sa=tee_dia[dia]
                L=float(sa[0])
                l=float(sa[1])
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=strt_dia[dia1]
                d1=float(sa[0])
                t1=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=strt_dia[dia2]
                d2=float(sa[0])
                t2=float(sa[1])
                W2=float(sa[2])
                S2=float(sa[5])
                c1 = Part.makeCylinder(d1/2,L-2*W1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder((d1-2*t1)/2,L-2*W1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                #c1=c1.cut(c2)
                c02 = Part.makeCylinder(d2/2,l,Base.Vector(L/2-W1,0,0),Base.Vector(0,1,0))
                c03 = Part.makeCylinder((d2-2*t2)/2,l,Base.Vector(L/2-W1,0,0),Base.Vector(0,1,0))
                c1=c1.fuse(c02)
                c1=c1.cut(c2)
                c1=c1.cut(c03)
                label = 'Tee_'  +  str(dia) + " "
                if k_index==8:
                    c021 = Part.makeCylinder(d2/2,l,Base.Vector(L/2-W1,-l,0),Base.Vector(0,1,0))
                    c031 = Part.makeCylinder((d2-2*t2)/2,l,Base.Vector(L/2-W1,-l,0),Base.Vector(0,1,0))
                    c1=c1.fuse(c021)
                    c1=c1.cut(c031)
                    c1=c1.cut(c2)
                    label = 'Cross_'  +  str(dia) + " "
                #c2=c2.cut(c3)
                dia=dia1
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),180))
                c1=c1.fuse(c2)
                dia=dia1
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L-2*W1,0,0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2)
                dia=dia2
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector((L-2*W1)/2,l-W2,0),App.Rotation(App.Vector(0,0,1),90))
                c1=c1.fuse(c2)
                if k_index==8:
                    dia=dia2
                    outlet(self)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector((L-2*W1)/2,-(l-W2),0),App.Rotation(App.Vector(0,0,1),-90))
                    c1=c1.fuse(c2)

        elif k_index==9:#Y管
            #global dia1
            #global dia2

            if st=='Socket':
                label = 'Y_'  +  str(dia) + " "
                sa=tee_dia[dia]
                L=float(sa[2])
                l=float(sa[3])
                L1=float(sa[4])
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=strt_dia[dia1]
                d1=float(sa[0])
                t1=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=strt_dia[dia2]
                d2=float(sa[0])
                t2=float(sa[1])
                W2=float(sa[2])
                S2=float(sa[5])
                c1 = Part.makeCylinder(d1/2,L-2*W1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder((d1-2*t1)/2,L-2*W1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c02 = Part.makeCylinder(d2/2,l,Base.Vector(0,0,0),Base.Vector(0,1,0))
                c02.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-45))
                c02.Placement=App.Placement(App.Vector(L1-W1,0,0),App.Rotation(App.Vector(0,0,1),-45))
                c03 = Part.makeCylinder((d2-2*t2)/2,l,Base.Vector(0,0,0),Base.Vector(0,1,0))
                c03.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-45))
                c03.Placement=App.Placement(App.Vector(L1-W1,0,0),App.Rotation(App.Vector(0,0,1),-45))
                c1=c1.fuse(c02)
                c1=c1.cut(c2)
                c1=c1.cut(c03)
                dia=dia1
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),180))
                c1=c1.fuse(c2)
                dia=dia1
                outlet(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L-2*W1,0,0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2)

                dia=dia2
                outlet(self)
                c2=c01
                s0=math.radians(45)
                c2.Placement=App.Placement(App.Vector(L1-W1+(l-W2)*math.cos(s0),(l-W2)*math.sin(s0),0),App.Rotation(App.Vector(0,0,1),45))
                c1=c1.fuse(c2)
                #Part.show(c2)

        elif k_index==10:#ダンパー
            label='VD_' + str(dia)+'_'
            if st=='VD_A':
                sa=dv_dapA[dia]
            d=float(sa[0])
            L=float(sa[2])
            t=float(sa[3])
            sa=strt_dia[dia]
            W=float(sa[2])
            S=float(sa[5])
            L1=W+S
            if st=='VD_A':
                z=L/2-L1
            if d<=150:
                r=25
            elif d>150:
                r=35
            r0=r-6
            r1=r+6
            r2=r1+6
            #本体
            c1=Part.makeCylinder(d/2,2*z,Base.Vector(-z,0,0),Base.Vector(1,0,0))
            #Part.show(c1)
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            #ダンパー
            c21=Part.makeCylinder((d-2*t)/2,2*z,Base.Vector(-z,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c21)
            #Part.show(c1)
            c2=Part.makeCylinder(20/2,d+12+15,Base.Vector(0,-d/2-15,0),Base.Vector(0,1,0))
            c22=Part.makeCylinder(10/2,d/2+40,Base.Vector(r,-(d/2+40),0),Base.Vector(0,1,0))
            c2=c2.fuse(c22)
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(10/2,5,Base.Vector(r,-(d/2+50),0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(20/2,r,Base.Vector(r,-(d/2+75),0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=c2.cut(c21)
            c1=c1.fuse(c2)
            c1=c1.cut(c21)
            c2=Part.makeCylinder(15/2,d,Base.Vector(0,-d/2,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(25/2,15,Base.Vector(0,-d/2-30,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(15/2,10,Base.Vector(0,-d/2-40,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(r2,5,Base.Vector(0,-d/2-45,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(25/2,10,Base.Vector(0,-d/2-52,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c2=Part.makeCylinder(d/2,t,Base.Vector(0,0,-t/2),Base.Vector(0,0,1))
            c1=c1.fuse(c2)
            p1=(0,-(d/2+45),0)
            p2=(0,-(d/2+45),r)
            p3=(r,-(d/2+45),0)
            edge1 = Part.makeCircle(r0, Base.Vector(p1), Base.Vector(0,1,0), 270,0)
            edge2 = Part.makeCircle(6, Base.Vector(p2), Base.Vector(0,1,0), 90, 270)
            edge3 = Part.makeCircle(r+6, Base.Vector(p1), Base.Vector(0,1,0), 270, 0)
            edge4 = Part.makeCircle(6, Base.Vector(p3), Base.Vector(0,1,0), 0, -180)
            aWire=Part.Wire([edge1,edge2,edge3,edge4])
            pface=Part.Face(aWire)
            c2=pface.extrude(Base.Vector(0,5,0))
            c1=c1.cut(c2)
            outlet(self)
            c2=c01
            c2.Placement=App.Placement(App.Vector(-z,0,0),App.Rotation(App.Vector(0,1,0),180))
            c1=c1.fuse(c2)
            c2=c01
            c2.Placement=App.Placement(App.Vector(z,0,0),App.Rotation(App.Vector(0,1,0),0))
            c1=c1.fuse(c2)
        doc=App.ActiveDocument
        F_Obj = doc.addObject("Part::Feature",label)
        F_Obj.Shape=c1
        
class main():
    d = QtGui.QWidget()
    d.setWindowFlags(QtCore.Qt.Window)
    d.ui = Ui_Dialog()
    d.ui.setupUi(d)
    d.show()





