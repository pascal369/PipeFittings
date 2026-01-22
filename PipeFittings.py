# -*- coding: utf-8 -*-
import os
import sys
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCADGui as Gui
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from pivy import coin
from PySide2 import QtCore
from pipe_data import ParamWeldStlPipe
from pipe_data import WeldStl_data
from pipe_data import ParamStlPScw
from pipe_data import ThreadStl_data
from pipe_data import Pvc_data
from pipe_data import ParamPvc
from pipe_data import Duct_data
from pipe_data import ParamDuct

DEBUG = True # set to True to show debug messages
Pipe_type=['Welded joint','Threaded fitting','PVC fittings','Circular duct fitting']
class Ui_Dialog(object):#05
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 340)
        Dialog.move(1000, 0)
        #種別　type
        self.label_typ= QtGui.QLabel('種別(Type)',Dialog)
        self.label_typ.setGeometry(QtCore.QRect(20, 0, 250, 22))
        self.label_typ.setStyleSheet("color: gray;")
        self.comboBox_typ = QtGui.QComboBox(Dialog)
        self.comboBox_typ.setGeometry(QtCore.QRect(110, 0, 180, 22))

        #管材   
        self.label_lst= QtGui.QLabel('管材(Fittings)',Dialog)
        self.label_lst.setGeometry(QtCore.QRect(20, 25, 120, 22))
        self.label_lst.setStyleSheet("color: gray;")
        self.label_lst.setObjectName("label_lst")
        self.comboBox_lst = QtGui.QComboBox(Dialog)
        self.comboBox_lst.setGeometry(QtCore.QRect(110, 25, 180, 22))
        self.comboBox_lst.setObjectName("comboBox_lst")
        self.label_l= QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(130, 48, 120, 22))
        #材質
        self.label_material= QtGui.QLabel('材質(Material)',Dialog)
        self.label_material.setGeometry(QtCore.QRect(20, 70, 120, 22))
        self.label_material.setStyleSheet("color: gray;")
        self.label_material.setObjectName("label_material")
        self.comboBox_material = QtGui.QComboBox(Dialog)
        self.comboBox_material.setGeometry(QtCore.QRect(110, 70, 180, 22))
        self.comboBox_material.setObjectName("comboBox_material")
        
        ta=WeldStl_data.mate[0:2]
        self.comboBox_material.clear()
        self.comboBox_material.addItems(ta)
        
        #規格
        self.label_standard= QtGui.QLabel('規格(Standard)',Dialog)
        self.label_standard.setGeometry(QtCore.QRect(20, 93, 120, 22))
        self.label_standard.setStyleSheet("color: gray;")
        self.label_standard.setObjectName("label_standard")
        self.comboBox_standard = QtGui.QComboBox(Dialog)
        self.comboBox_standard.setGeometry(QtCore.QRect(110, 93, 180, 22))
        self.comboBox_standard.setObjectName("comboBox_standard")
        #口径
        self.label_dia= QtGui.QLabel('口径(Diameter)',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(20, 116, 120, 22))
        self.label_dia.setStyleSheet("color: gray;")
        self.label_dia.setObjectName("label_standard")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(110, 116, 180, 20))
        self.comboBox_dia.setObjectName("comboBox_dia")

        #切管
        self.label_5 = QtGui.QLabel('Pipe',Dialog)
        self.label_5.setGeometry(QtCore.QRect(100, 145, 61, 16))
        self.label_5.setStyleSheet("color: gray;")
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(130, 145, 60, 32)
        self.spinBoxL.setMinimum(10)  # 最小値
        self.spinBoxL.setMaximum(5500)  # 最大値
        self.spinBoxL.setValue(5500)  # 
        self.spinBoxL.setSingleStep(10) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)
        #ステップ
        self.label_step = QtGui.QLabel('Step',Dialog)
        self.label_step.setGeometry(QtCore.QRect(200, 145, 50, 16))
        self.label_step.setStyleSheet("color: gray;")
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(200, 160, 50, 16))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        #チェックボックス
        self.checkbox = QtGui.QCheckBox('Thread',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(20, 142, 90, 23))
        self.checkbox.setStyleSheet("color: gray;")
        self.checkbox.setObjectName("checkbox")        
        #Create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 180, 80, 20))
        self.pushButton.setObjectName("pushButton")
        #upDate
        self.pushButton_1 = QtGui.QPushButton('upDate',Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(180, 180, 80, 20))
        #import
        self.pushButton_2 = QtGui.QPushButton('import',Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 180, 80, 20))
        #img
        self.label_img = QtGui.QLabel(Dialog)
        self.label_img.setGeometry(QtCore.QRect(20, 222, 250, 100))
        self.label_img.setText("")
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img.setObjectName("label_img")
        self.retranslateUi(Dialog)
        self.comboBox_typ.addItems(Pipe_type)
        self.comboBox_lst.addItems(WeldStl_data.lst)
        self.comboBox_material.setCurrentIndex(1)
        self.comboBox_typ.currentIndexChanged[int].connect(self.on_typ)
        self.comboBox_material.setCurrentIndex(0)

        self.comboBox_material.setCurrentIndex(1)
        self.comboBox_material.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox_material.setCurrentIndex(0)
        
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox_lst.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_standard.setCurrentIndex(1)
        self.comboBox_standard.currentIndexChanged[int].connect(self.on_standard)
        self.comboBox_standard.setCurrentIndex(0)

        self.spinBoxL.valueChanged[int].connect(self.spinMove) 
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.f_create)
        QtCore.QObject.connect(self.pushButton_1, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("pressed()"), self.read_data)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "PipeFittings", None))
    def read_data(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            myShape=obj
            fittings=myShape.fittings
            dia=myShape.dia
            material=myShape.material
            st=myShape.standard
            self.comboBox_lst.setCurrentText(fittings)
            self.comboBox_standard.setCurrentText(st)
            self.comboBox_dia.setCurrentText(dia)
            self.comboBox_material.setCurrentText(material)
          
            if myShape.Label=='Single_flange_straight_pipe' or myShape.Label=='Both_flanges_straight_pipe':
                st=myShape.standard
                st2=myShape.standard2
                self.comboBox_standard.setCurrentText(st+'_'+st2)
            try:
                L=int(myShape.L)
                self.spinBoxL.setValue(int(L))
            except:
                myShape=None
    def spinMove(self):
        step=self.le_step.text()
        self.spinBoxL.setSingleStep(int(step)) 
        selection = Gui.Selection.getSelection()
        for obj in selection:
           myShape=obj
           try: 
               L=self.spinBoxL.value()
               myShape.L=str(L)
           except:
               myShape=None     
               pass 
           App.ActiveDocument.recompute() 
    def update(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            myShape=obj
            dia=self.comboBox_dia.currentText()
            myShape.dia=dia
            st=self.comboBox_standard.currentText()
            try:
                myShape.standard=st
            except:
                pass
            material=self.comboBox_material.currentText()
            myShape.material=str(material)
            try:
                if myShape.Name=='Single_flange_straight_pipe' or myShape.Name=='Both_flanges_straight_pipe':
                     if self.comboBox_material.currentIndex()==0:
                         if st[:3]=='SGP':
                            myShape.standard=st[:3]
                            if st[-7:]=='JIS7.5k':
                                dia=WeldStl_data.flg_75[:15]
                            elif st[-5:]=='JIS5k' or st[-6:]=='JIS10k':
                                dia=WeldStl_data.flg_d[:25]
                            elif st[-6:]=='JIS16k' :
                                dia=WeldStl_data.flg_d
                            elif st[-6:]=='JIS20k' :
                                dia=WeldStl_data.flg_d 
                            myShape.standard=st[:3]
                            myShape.standard2=st[4:]
                         else:
                            if st[-7:]=='JIS7.5k' :
                                dia=WeldStl_data.flg_75[:10]
                            elif st[-5:]=='JIS5k' or st[-6:]=='JIS10k':
                                dia=WeldStl_data.flg_d[:15]
                            elif st[-6:]=='JIS16k' :
                                dia=WeldStl_data.flg_d[:15]
                            elif st[-6:]=='JIS20k' :
                                dia=WeldStl_data.flg_d[:15]      
                            myShape.standard=st[:5] 
                            myShape.standard2=st[6:]
                     elif self.comboBox_material.currentIndex()==1:
                        if st[-7:]=='JIS7.5k' :
                                dia=WeldStl_data.flg_75[:10]
                        elif st[-5:]=='JIS5k' or st[-6:]=='JIS10k':
                            dia=WeldStl_data.flg_d[:15]
                        myShape.standard=st[:6] 
                        myShape.standard2=st[7:]

                        # obj.standard=WeldStl_data.Tube_stainless
                        # i=self.comboBox_standard.currentIndex()
                        # obj.standard=WeldStl_data.Tube_stainless[i] 
                                
                try:
                   L0=self.spinBoxL.value()
                   myShape.L=str(L0)
                except:
                   myShape=None
            except:
                return                

        
        App.ActiveDocument.recompute() 
           

    def on_lst3(self):#材質
        self.comboBox_standard.clear()
        typ=self.comboBox_typ.currentText()
        material=self.comboBox_material.currentText()

        if typ=='Welded joint' or typ=='Threaded fitting' :
            if material=='Carbon steel':
                ta=WeldStl_data.Tube_carbon
            elif material=='Stainless steel':
                ta=WeldStl_data.Tube_stainless
            self.comboBox_standard.clear()
            try:
                self.comboBox_standard.addItems(ta)  
            except:
                pass
        elif typ=='PVC fittings':
            ta=Pvc_data.pipe_st
            self.comboBox_standard.clear()
            self.comboBox_standard.addItems(ta)
        elif typ=='Circular duct fitting':
            ta=Duct_data.pipe_st        
            self.comboBox_standard.clear()
            self.comboBox_standard.addItems(ta)

    def on_lst2(self):#管長
        self.comboBox_standard.clear()
        key = self.comboBox_lst.currentText()[:2]
        typ=self.comboBox_typ.currentText()
        if typ=='Welded joint':
            if key=='05' or key=='06' or key=='07':
                L=5500
            else:
                L=''
        elif typ=='Threaded fitting':
            if key=='15':
                L=5500
            elif key=='06':
                L=100    
            else:
                L=''   
        elif typ=='PVC fittings':
            if key=='00':
                L=5500
            else:
                L=''   
        elif typ=='Circular duct fitting':
            if key=='00':
                L=4000
            else:
                L=''          
        else:
            L=''                    

    def on_typ(self):
        
        self.comboBox_lst.clear()
        typ=self.comboBox_typ.currentText()
        self.comboBox_standard.clear()
        if typ=='Welded joint':
            self.comboBox_lst.addItems(WeldStl_data.lst)
            ta=WeldStl_data.mate[0:2]
            self.comboBox_material.clear()
            self.comboBox_material.addItems(ta)
        elif typ=='Threaded fitting':
            self.comboBox_lst.addItems(ThreadStl_data.lst)  
            ta=WeldStl_data.mate[0:2]
            self.comboBox_material.clear()
            self.comboBox_material.addItems(ta)

        elif typ=='PVC fittings':
            ta=Pvc_data.mate
            self.comboBox_material.clear()
            self.comboBox_material.addItems(ta) 
            material=self.comboBox_material.currentText()
            if material=='TS':
                self.comboBox_lst.clear()
                self.comboBox_lst.addItems(Pvc_data.lst_ts) 
            elif material=='DV': 
                self.comboBox_lst.clear()
                self.comboBox_lst.addItems(Pvc_data.lst_dv)  
        elif typ=='Circular duct fitting':
            self.comboBox_lst.addItems(Duct_data.lst)
            ta=Duct_data.mate
            self.comboBox_material.clear()
            self.comboBox_material.addItems(ta)         

    def on_material(self): 
        
        typ=self.comboBox_typ.currentText()
        self.comboBox_standard.cear()
        if typ=='PVC fittings':
            self.comboBox_lst.clear()
            material=self.comboBox_material.currentText()
            if material=='TS':
                self.comboBox_lst.addItems(Pvc_data.lst_ts) 
            elif material=='DV': 
                self.comboBox_lst.addItems(Pvc_data.lst_dv)
        

        
    def on_lst(self):
        global xlc
        st=self.comboBox_standard.currentText()
        typ=self.comboBox_typ.currentText()
        key = self.comboBox_lst.currentText()[:2]
        self.comboBox_standard.clear()
        if  typ=='Welded joint':
            try:
                b=WeldStl_data.l_lst[key]
                self.label_l.setText(QtGui.QApplication.translate("Dialog", b, None))
            except:
                pass
            
            pic='img_h' + key + '.png'
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "pipe_data",pic)
            self.label_img.setPixmap(QtGui.QPixmap(joined_path))
        elif typ=='Threaded fitting':
            try:
                b=ThreadStl_data.l_lst[key] 
                self.label_l.setText(QtGui.QApplication.translate("Dialog", b, None))
                pic='img_' + st + '.png' 
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass  

        elif typ=='PVC fittings':
            try:
                b=Pvc_data.l_lst[key]
                self.label_l.setText(QtGui.QApplication.translate("Dialog", b, None))
                pic='img_' + st + '.png' 
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass 

        elif typ=='Circular duct fitting':
            try:
                b=Duct_data.l_lst[key]
                self.label_l.setText(QtGui.QApplication.translate("Dialog", b, None))
                pic='img_' + st + '.png' 
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass         
        
        if typ=='Welded joint':
            if key=='00' or key=='09':#---------------------------------------------------------
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.flg_carbon
                elif material=='Stainless steel':
                    if key=='00':
                        ta=WeldStl_data.flg_stainless
                    elif key=='09':
                        ta=WeldStl_data.flg_stainless[:3]

            elif key=='01':
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.Elbow_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.Elbow_stainless

            elif key=='02':
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.Tee_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.Tee_stainless

            elif key=='03' or key=='04':
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.reduc_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.reduc_stainless

            elif key=='05' :
                material=self.comboBox_material.currentText()
                try:
                    self.label_lst.setText(QtGui.QApplication.translate("Dialog", str(material), None, QtGui.QApplication.UnicodeUTF8))
                except:
                    self.label_lst.setText(QtGui.QApplication.translate("Dialog", str(material), None))
                if material=='Carbon steel':
                    ta=WeldStl_data.Tube_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.Tube_stainless

            elif key=='06' or key=='07':
                #return
                
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.s_flg_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.s_flg_stainless
            elif key=='08' :
                material=self.comboBox_material.currentText()
                if material=='Carbon steel':
                    ta=WeldStl_data.Tube_carbon
                elif material=='Stainless steel':
                    ta=WeldStl_data.Tube_stainless
            elif key=='10' :
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.rap
            elif key=='11' or key=='12' :
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.rap[1:2]
            elif key=='13' :
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.check
            elif key=='14' :
                self.label_standard.setText(QtGui.QApplication.translate("Dialog", "偏芯量", None))
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.exp_st
            elif key=='15' :
                self.label_standard.setText(QtGui.QApplication.translate("Dialog", "", None))
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.rap[1:2]
            elif key=='16' :
                self.label_standard.setText(QtGui.QApplication.translate("Dialog", "偏芯量", None))
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.exp_st    
        elif typ=='Threaded fitting':
            if key=='00' :#---------------------------------------------------------
                ta=ThreadStl_data.flg
                self.comboBox_standard.clear()
                self.comboBox_standard.addItems(ta)
                st=self.comboBox_standard.currentText()
                dia=ThreadStl_data.tube_d[3:]
                self.comboBox_dia.clear()
                self.comboBox_dia.addItems(dia)
            elif key=='01' :
                ta=ThreadStl_data.elbow_st
            elif key=='02' :
                ta=ThreadStl_data.bend_st
            elif key=='03':
                ta=ThreadStl_data.tee_st
            elif key=='04':
                ta=ThreadStl_data.Y_st
            elif key=='05' :
                ta=ThreadStl_data.cross_st
            elif key=='06' :
                ta=ThreadStl_data.nipple_st
            elif key=='07' :
                ta=ThreadStl_data.union_st
            elif key=='08' :
                ta=ThreadStl_data.socket_st
            elif key=='09' :
                ta=ThreadStl_data.cap_st
            elif key=='10' :
                ta=ThreadStl_data.plug_st
            elif key=='11' :
                ta=ThreadStl_data.bush_st
            elif key=='12' :
                ta=ThreadStl_data.globe_st
            elif key=='13' :
                ta=ThreadStl_data.gate_st
            elif key=='14' :
                ta=ThreadStl_data.check_st
            elif key=='15' :
                ta=ThreadStl_data.tube

        elif typ=='PVC fittings':
            if key=='00' :
                ta=Pvc_data.pipe_st  
            elif key=='01' :
                ta=Pvc_data.elbow_st  
            elif key=='02' :
                ta=Pvc_data.socket_st 
            elif key=='03' :
                ta=Pvc_data.tee_st
            elif key=='04' :
                ta=Pvc_data.flg_st  
            elif key=='05' :
                ta=Pvc_data.damper_st

        elif typ=='Circular duct fitting':
            if key=='00' :
                ta=Duct_data.pipe_st  
            elif key=='01' :
                ta=Duct_data.collar_st 
            elif key=='02' :
                ta=Duct_data.cap_st 
            elif key=='03' :
                ta=Duct_data.flg_st
            elif key=='04' :
                ta=Duct_data.nipple_st  
            elif key=='05' :
                ta=Duct_data.bend_st
            elif key=='06' :
                ta=Duct_data.reduc_st
            elif key=='07' :
                ta=Duct_data.tee_st 
            elif key=='08' :
                ta=Duct_data.tee_st
            elif key=='09' :
                ta=Duct_data.y_st 
            elif key=='10' :
                ta=Duct_data.damper_st    

            #self.comboBox_standard.clear()
            #try:
            #    self.comboBox_standard.addItems(ta)
            #except:
            #    pass  
        try:
            #self.comboBox_standard.clear()
            self.comboBox_standard.addItems(ta)
            
            #print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
            #self.comboBox_dia.clear()
        except:
            pass    

    def on_standard(self):
        global st
        global dia
        key = self.comboBox_lst.currentText()[:2]
        st=self.comboBox_standard.currentText()
        material=self.comboBox_material.currentText()
        typ=self.comboBox_typ.currentText()
        
        if typ=='Welded joint':
            if key=='00' or key=='09' :
                if material=='Carbon steel':
                    if st=='JIS2k':
                        dia=WeldStl_data.flg_d[17:]
                    elif st=='JIS5k':
                        dia=WeldStl_data.flg_d[:25]
                    elif st=='JIS7.5k' :
                        dia=WeldStl_data.flg_75[:18]
                    elif st=='JIS10k':
                        dia=WeldStl_data.flg_d[:25]
                    elif st=='JIS16k' :
                        dia=WeldStl_data.flg_d[:20]
                    elif st=='JIS20k' :
                        dia=WeldStl_data.flg_d[:20]    

                elif material=='Stainless steel':
                    if st=='JIS5k':
                        dia=WeldStl_data.flg_d[:21]
                    elif st=='JIS7.5k' :
                        dia=WeldStl_data.flg_75[:10]
                    elif st=='JIS10k':
                        dia=WeldStl_data.flg_d[:25]
                    if key=='00':
                        if st=='JIS10k_Loose' or st=='JIS5k_Loose':
                            dia=WeldStl_data.flg_d[1:20]
            elif key=='01':
                material=self.comboBox_material.currentText()
                st=self.comboBox_standard.currentText()
                pic='img_' + st[:3] + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if material=='Carbon steel':
                    if st[4:8]=='Long':
                        if st[-3:]=='SGP':
                            dia=WeldStl_data.flg_d[1:19]
                        else:
                            dia=WeldStl_data.flg_d[1:19]
                    elif st[4:9]=='Short':
                        dia=WeldStl_data.flg_d[3:19]

                    elif st[4:9]=='Large':
                        dia=WeldStl_data.flg_d[18:23]
                elif material=='Stainless steel':
                    if st[4:8]=='Long':
                        dia=WeldStl_data.flg_d[1:15]
                    elif st[4:9]=='Short':
                        if st[:3]=='090':
                            dia=WeldStl_data.flg_d[3:15]
            elif key=='02':
                material=self.comboBox_material.currentText()
                st=self.comboBox_standard.currentText()
                pic='img_tee' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if material=='Carbon steel':
                    if st=='Large':
                        dia=WeldStl_data.tee[59:]
                    else:
                        dia=WeldStl_data.tee[:59]
                elif material=='Stainless steel':
                    if st=='Sch10S' or st=='Sch20S':
                        dia=WeldStl_data.tee [:59]
                    else:
                        dia=WeldStl_data.tee
            elif key=='03' or key=='04':
                material=self.comboBox_material.currentText()
                st=self.comboBox_standard.currentText()
                if key=='03':
                    pic='img_reduc_c' + '.png'
                elif key=='04':
                    pic='img_reduc_e' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if material=='Carbon steel':
                    if st=='SGP':
                        dia=WeldStl_data.reduc[:49]
                    elif st=='Large':
                        dia=WeldStl_data.reduc[62:]
                    else:
                        dia=WeldStl_data.reduc
                elif material=='Stainless steel':
                    if st=='Sch10S' or st=='Sch20S':
                        self.label_lst.setText(QtGui.QApplication.translate("Dialog", str(st), None))
                        dia=WeldStl_data.reduc[:45]
                    else:
                        dia=WeldStl_data.reduc[:45]
            elif key=='05':
                material=self.comboBox_material.currentText()
                st=self.comboBox_standard.currentText()
                dia=WeldStl_data.tube_d
            elif key=='06' or key=='07':
                st=self.comboBox_standard.currentText()
                
                if st[:3]=='SGP':
                    if st[-7:]=='JIS7.5k' :
                        dia=WeldStl_data.flg_75[:15]
                    elif st[-5:]=='JIS5k' or st[-6:]=='JIS10k':
                        dia=WeldStl_data.flg_d[:25]
                    elif st[-6:]=='JIS16k' :
                        dia=WeldStl_data.flg_d
                    elif st[-6:]=='JIS20k' :
                        dia=WeldStl_data.flg_d 
                else:
                    if st[-7:]=='JIS7.5k' :
                        dia=WeldStl_data.flg_75[:10]
                    elif st[-5:]=='JIS5k' or st[-6:]=='JIS10k':
                        dia=WeldStl_data.flg_d[:15]
                    elif st[-6:]=='JIS16k' :
                        dia=WeldStl_data.flg_d[:15]
                    elif st[-6:]=='JIS20k' :
                        dia=WeldStl_data.flg_d[:15]    
            elif key=='08':
                material=self.comboBox_material.currentText()
                st=self.comboBox_standard.currentText()
                dia=WeldStl_data.tube_d[3:]
            elif key=='10':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                pic='img_Rap_joint' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                dia=WeldStl_data.flg_d[1:15]
            elif key=='11':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                pic='img_Gate_Valve_fint' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if st=='JIS5k':
                    dia=WeldStl_data.flg_d[6:14]
                elif st=='JIS10k':
                    dia=WeldStl_data.flg_d[6:15]
            elif key=='12':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                pic='img_Gate_Valve_fext' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if st=='JIS5k':
                    dia=WeldStl_data.flg_d[6:14]
                elif st=='JIS10k':
                    dia=WeldStl_data.flg_d[6:15]
            elif key=='13':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                pic='img_Check_Valve_f' + '.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                if st=='JIS7.5k':
                    dia=WeldStl_data.flg_75[:7]
                elif st=='JIS10k':
                    dia=WeldStl_data.flg_d[6:16]
            elif key=='14':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                if st=='20mm':
                    pic='exp_20.png'
                elif st=='50mm':
                    pic='exp_50.png'
                elif st=='100mm':
                    pic='exp_100.png'
                elif st=='200mm':
                    pic='exp_200.png'
                try:
                    base=os.path.dirname(os.path.abspath(__file__))
                    joined_path = os.path.join(base, "pipe_data",pic)
                    self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                    dia=WeldStl_data.flg_d[2:20]
                except:
                    pass    
            elif key=='15':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                pic='img_flex_joint.png'
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                dia=WeldStl_data.flg_d[2:15]
            elif key=='16':
                st=self.comboBox_standard.currentText()
                material=self.comboBox_material.currentText()
                if st=='20mm':
                    pic='exp_20.png'
                elif st=='50mm':
                    pic='exp_50.png'
                elif st=='100mm':
                    pic='exp_100.png'
                elif st=='200mm':
                    pic='exp_200.png'
                try:
                    base=os.path.dirname(os.path.abspath(__file__))
                    joined_path = os.path.join(base, "pipe_data",pic)
                    self.label_img.setPixmap(QtGui.QPixmap(joined_path))
                    dia=WeldStl_data.flg_75[:10]
                except:
                    pass        
            try:
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass    
        elif typ=='Threaded fitting':
            if key=='00' :
                pic='img_n' + key + '.png'
                dia=ThreadStl_data.tube_d[3:]
                FC='フランジ'
            elif key=='01':
                pic='img_' + st + '.png'
                if st=='90RL':
                    dia=ThreadStl_data.elbow_rl
                    FC="径違いめすエルボ"
                elif st=='90RSL':
                    dia=ThreadStl_data.elbow_rsl
                    FC= "径違いめすおすエルボ"
                elif st=='45L':
                    dia=ThreadStl_data.tube_d
                    FC="45エルボ"
                elif st=='90L':
                    dia=ThreadStl_data.tube_d
                    FC="エルボ"
                elif st=='90SL':
                    dia=ThreadStl_data.tube_d
                    FC="めすおすエルボ"
            elif key=='02':
                pic='img_' + st + '.png'
                st=self.comboBox_standard.currentText()
                if st=='45B' :
                    dia=ThreadStl_data.bend_d
                    FC="45ベンド"
                elif st=='90B':
                    dia=ThreadStl_data.bend_d
                    FC="90ベンド"
                elif st=='45SB':
                    dia=ThreadStl_data.bend_d
                    FC="45めすおすベンド"
                elif st=='90SB':
                    dia=ThreadStl_data.bend_d
                    FC="90めすおすベンド"
            elif key=='04' :
                pic='img_' + st + '.png'
                if st=='45Y':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.bend_d
                    FC="45Y"
                elif st=='90Y':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.bend_d
                    FC="90Y"
                elif st=='90RY':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.Y_90RY_d
                    FC="90RY"
            elif key=='03' or key=='05' :
                pic='img_' + st + '.png'
                if st=='T':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="同径チーズ"
                elif st=='RT':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tee_d
                    FC="径違いチーズ"
                elif st=='Cr':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d [1:]
                    FC="同径クロス"
                elif st=='RCr':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.RCr_d
                    FC="径違いクロス"
            elif key=='06':
                if st=='Nipple' :
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="同径ニップル"
                elif st=='Piece_nipple':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="片長ニップル"
                elif st=='Both_nipple':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="両長ニップル"
                elif st=='Reducing_nipple' :
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.nipple_R_d
                    FC="径違いニップル"
                elif st=='Hose_nipple':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d[1:]
                    FC="ホースニップル"
                elif st=='Piece_nipple':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d[1:]
                    FC="片長ニップル"
            elif key=='07':
                pic='img_' + st + '.png'
                dia=ThreadStl_data.tube_d
                FC='直管'
            elif key=='08':
                if st=='Socket_parrallel':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="ソケット"
                elif st=='Socket_taper':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="テーパソケット"
                elif st=='Socket_difference':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.socket_d
                    FC="径違いソケット"
            elif key=='09':
                if st=='cap':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="キャップ"
            elif key=='10':
                if st=='plug':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d
                    FC="プラグ"
            elif key=='11':
                if st=='Bushing':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.bush_d
                    FC="ブッシング"
            elif key=='12':
                pic='img_Globe_Valve.png'
                if st=='JIS5k':
                    dia=ThreadStl_data.tube_d[3:]
                elif st=='JIS10k':
                    dia=ThreadStl_data.tube_d[1:]
                FC="玉形弁"
            elif key=='13':
                pic='img_Gate_Valve.png'
                if st=='JIS5k':
                    dia=ThreadStl_data.tube_d[3:]
                elif st=='JIS10k':
                    dia=ThreadStl_data.tube_d[3:]
                FC= "仕切弁"
            elif key=='14':
                pic='img_Check_Valve.png'
                if st=='JIS10k':
                    dia=ThreadStl_data.tube_d[2:]
                FC= "逆止弁"
            elif key=='15':
                pic='img_Straight_Pipe.png'
                dia=ThreadStl_data.tube_d
                FC="直管"

            try:
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass

        elif typ=='PVC fittings':
            if material=='TS':
                if key=='00' :
                    if st[:2]=='VP' :
                        dia=Pvc_data.pvc_d[:15]
                        pic='img_pvc_pipe.png'
                    elif st[:2]=='VU' :
                        dia=Pvc_data.pvc_d[5:]
                        pic='img_pvc_pipe.png'
                    elif st[:3]=='VPW' :
                        dia=Pvc_data.pvc_d[5:12]
                        pic='img_pvc_pipe.png'
                    if st[3:7]=='Both' or st[4:8]=='Both':
                        pic='img_h07.png'
                        FC='2F直管'
                    elif st[3:9]=='Single' or st[4:10]=='Single':
                        pic='img_h06.png'
                        FC='1F直管'
                elif key=='01' :
                    FC='エルボ'
                    if st=='90':
                        pic='img_ts90E.png'
                        dia=Pvc_data.pvc_d[:12]
                    elif st=='45':
                        pic='img_ts45E.png'
                        dia=Pvc_data.pvc_d[:7]
                elif key=='02':#ソケット
                    if st=='Socket':
                        dia=Pvc_data.pvc_d[:12]
                        FC='ソケット'
                        pic='img_ts_same_socket.png'
                    elif st=='Increaser':
                        dia=Pvc_data.ts_dsoc_d
                        FC='インクリーザ'
                        pic='img_ts_diff_socket.png'
                    elif st=='Valve':
                        dia=Pvc_data.pvc_d[:7]
                        FC='バルブソケット'
                        pic='img_ts_valve_socket.png' 
                elif key=='03':#チーズ
                    if st=='Same_dia':
                        dia=Pvc_data.pvc_d[:7]
                        FC='チーズ'
                        pic='img_ts_same_tee.png'
                    elif st=='Difference_dia':
                        dia=Pvc_data.ts_dtee_d
                        FC='径違いチーズ'
                        pic='img_ts_diff_tee.png'               
                elif key=='04':#フランジ
                    if st=='JIS5k_socket':
                        dia=Pvc_data.flg_d[:12]
                        FC='TS_JIS5kフランジ'
                        pic='img_ts_flange_socket.png'
                    elif st=='JIS10k_socket':
                        dia=Pvc_data.flg_d[:12]
                        FC='TS_JIS10kフランジ'
                        pic='img_ts_flange_socket.png'
                    elif st=='JIS5k':
                        dia=Pvc_data.flg_d2
                        FC='JIS5kフランジ'
                        pic='img_h00.png'
                    elif st=='JIS10k':
                        dia=Pvc_data.flg_d2
                        FC='JIS10kフランジ'
                        pic='img_h00.png'
                    elif st=='JIS5k_lid':
                        dia=Pvc_data.flg_d2
                        FC='JIS5kフランジ蓋'
                        pic='img_h09.png'
                    elif st=='JIS10k_lid':
                        dia=Pvc_data.flg_d2
                        FC='JIS10kフランジ蓋'
                        pic='img_h09.png'        
            elif material=='DV':
                if key=='00':#直管
                    FC='直管'
                    if st[:2]=='VP' :
                        dia=Pvc_data.pvc_d[:15]
                        pic='img_pvc_pipe.png'

                    elif st[:2]=='VU' :
                        dia=Pvc_data.pvc_d[5:]
                        pic='img_pvc_pipe.png'
                    elif st[:3]=='VPW' :
                        dia=Pvc_data.pvc_d[5:12]
                        pic='img_pvc_pipe.png'
                    if st[3:7]=='Both' or st[4:8]=='Both':
                        pic='img_h07.png'
                        FC='2F直管'
                    elif st[3:9]=='Single' or st[4:10]=='Single':
                        pic='img_h06.png'
                        FC='1F直管'
                elif key=='01':#エルボ
                    FC='エルボ'
                    dia=Pvc_data.pvc_d[5:15]
                    if st=='90':
                        pic='img_dv90E.png'
                    elif st=='45':
                        pic='img_dv45E.png'
                elif key=='02':#ソケット
                    if st=='Socket':
                        dia=Pvc_data.pvc_d[5:15]
                        FC='ソケット'
                        pic='img_dv_same_socket.png'
                    elif st=='Increaser':
                        dia=Pvc_data.dv_dsoc_d
                        FC='インクリーザ'
                        pic='img_dv_increaser.png'
                    elif st=='Valve':
                        dia=Pvc_data.pvc_d[:7]
                        FC='バルブソケット'
                        pic='img_ts_valve_socket.png'
                elif key=='03':#90Y
                    if st=='Same_dia':
                        dia=Pvc_data.pvc_d[6:15]
                        FC='90°Y'
                        pic='img_dv_90Y.png'
                    elif st=='Difference_dia':
                        dia=Pvc_data.dv_d90Y_d
                        FC='径違い90°Y'
                        pic='img_dv_diff_90Y.png'
                    elif st=='Large_bend':
                        dia=Pvc_data.pvc_d[:7]
                        FC='大曲り90°Y'
                        pic='img_dv_lb90Y.png'
                elif key=='04':#フランジ
                    if st=='JIS5k_socket':
                        dia=Pvc_data.flg_d[:12]
                        FC='TS_JIS5kフランジ+ソケット'
                        pic='img_ts_flange_socket.png'
                    elif st=='JIS10k_socket':
                        dia=Pvc_data.flg_d[:12]
                        FC='TS_JIS10kフランジ+ソケット'
                        pic='img_ts_flange_socket.png'
                    elif st=='JIS5k':
                        dia=Pvc_data.flg_d2
                        self.label_l.setText(QtGui.QApplication.translate("Dialog", 'JIS5kフランジ', None))
                        pic='img_h00.png'
                    elif st=='JIS10k':
                        dia=Pvc_data.flg_d2
                        FC='JIS10kフランジ'
                        pic='img_h00.png'
                    elif st=='JIS5k_lid':
                        dia=Pvc_data.flg_d2
                        FC='JIS5kフランジ蓋'
                        pic='img_h09.png'
                    elif st=='JIS10k_lid':
                        dia=Pvc_data.flg_d2
                        FC='JIS10kフランジ蓋'
                        pic='img_h09.png'

                elif key=='05':#ダンパー
                    dia=Pvc_data.pvc_d[6:15]
                    if st=='VD_A':
                        pic='img_VD_A.png'
                        FC='ダンパー_単管式'
                    elif st=='VD_B':
                        pic='img_VD_B.png'
                        FC='ダンパー_ソケット式'
                    elif st=='VD_C_5k' or st=='VD_C_10k':
                        pic='img_VD_C.png'
                        FC='ダンパー_フランジ式'
            try:
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass
        
        elif typ=='Circular duct fitting':
            if key=='00' :
                dia=Duct_data.spiral_d
                pic='img_' + st + '.png' 
                FC='直管'
            elif key=='01' :
                dia=Duct_data.spiral_d
                if st=='T_collar':
                    pic='img_T_collar.png'
                    FC='Tカラー' 

            elif key=='02' :
                dia=Duct_data.spiral_d
                if st=='Pipe_use':
                  pic='img_spiral_cap_pipe_use.png'
                elif st=='Fitting_use':
                   pic='img_spiral_cap_fitting_use.png' 
                FC='キャップ'       
            elif key=='03' :
                dia=Duct_data.spiral_d
                if st=='Plate':
                  pic='img_flange_plate.png'
                elif st=='Angle':
                   pic='img_flange_angle.png' 
                elif st=='Packing':
                   pic='img_spiral_packing.png'   
                FC='フランジ'
            elif key=='04' :
                dia=Duct_data.spiral_d
                pic='img_spiral_nipple.png'
                FC='ニップル' 
            elif key=='05' :
                dia=Duct_data.spiral_d
                if st=='90':
                  pic='img_spiral_bend90.png'
                elif st=='45':
                  pic='img_spiral_bend45.png'  
                FC='ベンド'  
            elif key=='06' :
                dia=Duct_data.reduc_d
                pic='img_spiral_reduc.png'
                FC='片落管'
            elif key=='07' or key=='08':
                dia=Duct_data.tee_d
                if key=='07':
                    pic='img_spiral_tee.png'
                    FC='T字管'
                elif key=='08':
                    pic='img_spiral_cross.png'
                    FC='クロス'
            elif key=='09' :
                dia=Duct_data.reduc_d
                pic='img_spiral_y.png'
                FC='Y管'
            elif key=='10' :
                dia=Duct_data.spiral_d
                if st=='VD_A':
                    pic='img_spiral_VD_A.png'
                FC=  'ダンパー'   

            try:
                base=os.path.dirname(os.path.abspath(__file__))
                joined_path = os.path.join(base, "pipe_data",pic)
                self.label_img.setPixmap(QtGui.QPixmap(joined_path))
            except:
                pass
        try:
            self.comboBox_dia.clear()
            self.comboBox_dia.addItems(dia)
        except:
            pass
        
    def f_create(self):
        typ=self.comboBox_typ.currentText()
        #lsky=self.lineEdit.text()
        key = self.comboBox_lst.currentText()[:2]

        if typ=='Welded joint':
            if key=='00' :
                label = 'Flange'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]  
                  
            elif key=='01':
                label = 'Elbow'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.Elbow_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Elbow_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.Elbow_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Elbow_stainless[i]  
            
            elif key=='02':
                label = 'Tee'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.Tee_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tee_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.Tee_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tee_stainless[i]  
            
            elif key=='03':
                label = 'Reducer_concentric'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.reduc_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.reduc_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.reduc_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.reduc_stainless[i]  
            elif key=='04':
                label = 'Reducer_eccentric'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.reduc_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.reduc_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.reduc_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.reduc_stainless[i]          

            elif key=='05' :
                label = 'Straight_tube'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.Tube_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tube_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.Tube_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tube_stainless[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L)    
            
            elif key=='06' or key=='07':
                if key=='06':
                    label = 'Single_flange_straight_pipe'
                elif key=='07':
                    label = 'Both_flanges_straight_pipe'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.Tube_carbon
                    i=self.comboBox_standard.currentIndex()
                    if st[:3]=='SGP':
                        obj.standard=st[:3]
                    else :
                        obj.standard=st[:5]    
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.Tube_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tube_stainless[i] 
                obj.addProperty("App::PropertyEnumeration", "standard2",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard2=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    if st[-5:]=='JIS5k':
                        obj.standard2=st[-5:]
                    elif st[-7:]=='JIS7.5k':
                        obj.standard2=st[-7:] 
                    else:
                        obj.standard2=st[-6:]     
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard2=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard2=WeldStl_data.flg_stainless[i]  
                obj.addProperty("App::PropertyString", "L",label).L=str(L)    
            
            elif key=='08' :
                label = 'Cap'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.Tube_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tube_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.Tube_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.Tube_stainless[i]  
            
            elif key=='09':
                label = 'Flange_lid'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]      

            elif key=='10' :#ラップジョイント
                label = 'Rap_joint'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]      

            elif key=='11' or key=='12':
                if key=='11':
                    label = 'Gate_Valve_internal'
                elif key=='12':
                    label = 'Gate_Valve_external'    

                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]      

            elif key=='13':
                label = 'Check_Valve_swing_type'    
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.check
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.check[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.check
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.check[i]      

            elif key=='14'or key=='16':
                i=self.comboBox_dia.currentIndex()
                if key=='14':
                    label = 'Expansion joint_10k_'  + str(dia[i])  
                elif key=='16':
                    label = 'Expansion joint_7.5k_' + str(dia[i])  
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.exp_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.exp_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.exp_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.exp_st[i] 
            elif key=='15':
                label = 'Flex_joint_10k'    
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.rap
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.rap[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.rap
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.rap[i]         

            obj.addProperty("App::PropertyEnumeration", "material",label)
            obj.material=WeldStl_data.mate[:2]
            i=self.comboBox_material.currentIndex()
            obj.material=WeldStl_data.mate[i]

            fittings=self.comboBox_lst.currentText()
            obj.addProperty("App::PropertyString", "fittings",label).fittings=fittings
            ParamWeldStlPipe.welded_p(obj) 
            obj.ViewObject.Proxy=0   
        
        elif typ=='Threaded fitting':
            if key=='00' :
                label = 'Flange'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]  

            elif key=='01' :
                label = 'Elbow'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.elbow_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.elbow_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.elbow_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.elbow_st[i]  

            elif key=='02' :
                label = 'Bend'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.bend_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.bend_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.bend_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.bend_st[i] 

            elif key=='03' :
                label = 'Tee'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.tee_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.tee_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.tee_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.tee_st[i] 

            elif key=='04' :
                label = 'Y'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.Y_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.Y_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.Y_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.Y_st[i] 

            elif key=='05' :
                label = 'Cross'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.cross_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.cross_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.cross_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.cross_st[i]  

            elif key=='06' :
                label = 'Nipple'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.nipple_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.nipple_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.nipple_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.nipple_st[i]  
                obj.addProperty("App::PropertyString", "L",label).L=str(L)    
                
            elif key=='07' :
                label = 'Union'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.union_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.union_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.union_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.union_st[i]  

            elif key=='08' :
                label = 'Socket'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.socket_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.socket_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.socket_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.socket_st[i]  

            elif key=='09' :
                label = 'Cap'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.cap_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.cap_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.cap_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.cap_st[i] 

            elif key=='10' :
                label = 'Plug'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.plug_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.plug_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.plug_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.plug_st[i] 

            elif key=='11' :
                label = 'Bushing'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.bush_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.bush_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.bush_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.bush_st[i]  

            elif key=='12' :
                label = 'Globe_Valve'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.globe_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.globe_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.globe_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.globe_st[i] 

            elif key=='13' :
                label = 'Gate_Valve'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.gate_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.gate_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.gate_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.gate_st[i] 

            elif key=='14' :
                label = 'Gate_Valve'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.check_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.check_st[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.check_st
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.check_st[i] 

            elif key=='15' :
                label = 'Straight_Pipe'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                if self.comboBox_material.currentIndex()==0:
                    obj.standard=ThreadStl_data.tube
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.tube[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=ThreadStl_data.tube
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.tube[i]  
                obj.addProperty("App::PropertyString", "L",label).L=str(L)                       

            obj.addProperty("App::PropertyEnumeration", "material",label)
            obj.material=WeldStl_data.mate[:2]
            i=self.comboBox_material.currentIndex()
            obj.material=WeldStl_data.mate[i]

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
            else:
                obj.addProperty("App::PropertyBool",'Thread',label).Thread = False

            fittings=self.comboBox_lst.currentText()
            obj.addProperty("App::PropertyString", "fittings",label).fittings=fittings
            ParamStlPScw.threaded_p(obj) 
            obj.ViewObject.Proxy= 0  

        elif typ=='PVC fittings':
            material=self.comboBox_material.currentText()
            if key=='00' :
                label = 'Straight_Pipe'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.pipe_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.pipe_st[i]  
                obj.addProperty("App::PropertyString", "L",label).L=str(L)                         

            elif key=='01' :
                label = 'Elbow'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.elbow_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.elbow_st[i] 
            elif key=='02' :
                label = 'Socket'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.socket_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.socket_st[i]
            elif key=='03' :
                if material=='TS':
                    label = 'Tee'
                elif material=='DV':
                    label='Y90'    

                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.tee_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.tee_st[i]  
            elif key=='04' :
                label = 'Flange'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.flg_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.flg_st[i]    
            elif key=='05' :
                label = 'Damper'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]    

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Pvc_data.damper_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Pvc_data.damper_st[i]     


            obj.addProperty("App::PropertyEnumeration", "material",label)
            obj.material=Pvc_data.mate[:2]
            i=self.comboBox_material.currentIndex()
            obj.material=Pvc_data.mate[i]

            if self.checkbox.isChecked():
                obj.addProperty("App::PropertyBool",'Thread',label).Thread = True
            else:
                obj.addProperty("App::PropertyBool",'Thread',label).Thread = False

            fittings=self.comboBox_lst.currentText()
            obj.addProperty("App::PropertyString", "fittings",label).fittings=fittings
            ParamPvc.pvc_p(obj) 
            obj.ViewObject.Proxy= 0 
        elif typ=='Circular duct fitting':
            material=self.comboBox_material.currentText()
            if key=='00' :
                label = 'Straight_Pipe'
                L=self.spinBoxL.value()
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]

                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.pipe_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.pipe_st[i]  
                obj.addProperty("App::PropertyString", "L",label).L=str(L)   
            elif key=='01' :
                label = 'T_collar'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.collar_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.collar_st[i]
            elif key=='02' :
                label = 'Cap'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i] 
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.cap_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.cap_st[i]
            elif key=='03' :
                label = 'Flange'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]  
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.flg_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.flg_st[i]
            elif key=='04' :
                label = 'Nipple'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i] 
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.nipple_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.nipple_st[i] 
            elif key=='05' :
                label = 'Bend'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.bend_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.bend_st[i] 
            elif key=='06' :
                label = 'Reducer'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i] 
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.reduc_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.reduc_st[i] 
            elif key=='07' :
                label = 'Tee'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]  
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.tee_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.tee_st[i]    
            elif key=='08' :
                label = 'Cross'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i] 
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.tee_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.tee_st[i] 
            elif key=='09' :
                label = 'Y_bend'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i] 
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.y_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.y_st[i] 
            elif key=='10' :
                label = 'Damper'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]     
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=Duct_data.damper_st
                i=self.comboBox_standard.currentIndex()
                obj.standard=Duct_data.damper_st[i]  
            
            obj.addProperty("App::PropertyEnumeration", "material",label)
            obj.material=WeldStl_data.mate[:2]
            i=self.comboBox_material.currentIndex()
            obj.material=WeldStl_data.mate[i]

            fittings=self.comboBox_lst.currentText()
            obj.addProperty("App::PropertyString", "fittings",label).fittings=fittings
            ParamDuct.duct_p(obj) 
            obj.ViewObject.Proxy= 0  

        view = Gui.ActiveDocument.ActiveView
        
        obj.ViewObject.Visibility = True
        
        sep = coin.SoSeparator()
        trans = coin.SoTranslation()
        sep.addChild(trans)
        view.getSceneGraph().addChild(sep)
        
        callbacks = {}
        
        # -----------------------------
        def move_cb(info):
            pos = info["Position"]
            p = view.getPoint(pos)
            trans.translation.setValue(p)
            obj.Placement.Base = p
        
        # -----------------------------
        def click_cb(info):
            if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                # ★ 直接 finish() を呼ばない
                QtCore.QTimer.singleShot(0, finish)
        
        # -----------------------------
        def key_cb(info):
            if info.get("Key") == "ESCAPE":
                QtCore.QTimer.singleShot(0, cancel)
        
        # -----------------------------
        def finish():
            try:
                view.removeEventCallback("SoLocation2Event", callbacks["move"])
                view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                view.removeEventCallback("SoKeyboardEvent", callbacks["key"])
            except:
                pass
        
            obj.ViewObject.Visibility = True
        
            try:
                view.getSceneGraph().removeChild(sep)
            except:
                pass
        
            App.ActiveDocument.recompute()
        
        # -----------------------------
        def cancel():
            finish()
            try:
                App.ActiveDocument.removeObject(obj.Name)
            except:
                pass
        
        # -----------------------------
        callbacks["move"]  = view.addEventCallback("SoLocation2Event", move_cb)
        callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)
        callbacks["key"]   = view.addEventCallback("SoKeyboardEvent", key_cb)
        
class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()


