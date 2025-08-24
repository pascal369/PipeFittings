# -*- coding: utf-8 -*-
import os
import sys
import csv
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCADGui as Gui
import math
import FreeCAD as App
from pipe_data import ParamWeldStlPipe
from pipe_data import WeldStl_data
from pipe_data import ParamStlPScw
from pipe_data import ThreadStl_data
from pipe_data import Pvc_data
from pipe_data import ParamPvc
from pipe_data import Duct_data
from pipe_data import ParamDuct

DEBUG = True # set to True to show debug messages
lang=['English','Japanese']
Pipe_type=['Welded joint','Threaded fitting','PVC fittings','Circular duct fitting']
class Ui_Dialog(object):#05
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 450)
        Dialog.move(1000, 0)
        #種別　type
        self.label_typ= QtGui.QLabel('種別(Type)',Dialog)
        self.label_typ.setGeometry(QtCore.QRect(20, 0, 250, 22))
        self.comboBox_typ = QtGui.QComboBox(Dialog)
        self.comboBox_typ.setGeometry(QtCore.QRect(110, 0, 180, 22))

        #管材   
        self.label_lst= QtGui.QLabel('管材(Fittings)',Dialog)
        self.label_lst.setGeometry(QtCore.QRect(20, 25, 120, 22))
        self.label_lst.setObjectName("label_lst")
        self.comboBox_lst = QtGui.QComboBox(Dialog)
        self.comboBox_lst.setGeometry(QtCore.QRect(110, 25, 180, 22))
        self.comboBox_lst.setObjectName("comboBox_lst")
        self.label_l= QtGui.QLabel(Dialog)
        self.label_l.setGeometry(QtCore.QRect(130, 48, 120, 22))
        #材質
        self.label_material= QtGui.QLabel('材質(Material)',Dialog)
        self.label_material.setGeometry(QtCore.QRect(20, 70, 120, 22))
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
        self.label_standard.setObjectName("label_standard")
        self.comboBox_standard = QtGui.QComboBox(Dialog)
        self.comboBox_standard.setGeometry(QtCore.QRect(110, 93, 180, 22))
        self.comboBox_standard.setObjectName("comboBox_standard")
        #口径
        self.label_dia= QtGui.QLabel('口径(Diameter)',Dialog)
        self.label_dia.setGeometry(QtCore.QRect(20, 116, 120, 22))
        self.label_dia.setObjectName("label_standard")
        self.comboBox_dia = QtGui.QComboBox(Dialog)
        self.comboBox_dia.setGeometry(QtCore.QRect(110, 116, 180, 20))
        self.comboBox_dia.setObjectName("comboBox_dia")

        #切管
        self.label_5 = QtGui.QLabel('Pipe',Dialog)
        self.label_5.setGeometry(QtCore.QRect(100, 145, 61, 16))
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(125, 145, 80, 32)
        self.spinBoxL.setMinimum(10)  # 最小値
        self.spinBoxL.setMaximum(50000)  # 最大値
        self.spinBoxL.setValue(5500)  # 
        self.spinBoxL.setSingleStep(10) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)
        #ステップ
        self.label_step = QtGui.QLabel('Step',Dialog)
        self.label_step.setGeometry(QtCore.QRect(220, 145, 50, 16))
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(220, 160, 50, 16))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)
        #チェックボックス
        self.checkbox = QtGui.QCheckBox('Thread',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(20, 142, 90, 23))
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
        self.label_img.setAlignment(QtCore.Qt.AlignTop)
        self.label_img.setObjectName("label_img")

        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(20, 350, 100, 23))
        self.pushButton_m.setObjectName("pushButton")  

        #spreadsheet
        #self.pushButton_m20 = QtGui.QPushButton('massTally_csv',Dialog)
        #self.pushButton_m20.setGeometry(QtCore.QRect(120, 325, 150, 23))
        self.pushButton_m2 = QtGui.QPushButton('massTally_spreadsheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(20, 325, 188, 23))
        #言語
        self.comboBox_lan = QtGui.QComboBox(Dialog)
        self.comboBox_lan.setGeometry(QtCore.QRect(120, 350, 90, 22))
        #count
        self.pushButton_ct = QtGui.QPushButton('Count',Dialog)
        self.pushButton_ct.setGeometry(QtCore.QRect(20, 375, 100, 23))
        self.le_ct = QtGui.QLineEdit(Dialog)
        self.le_ct.setGeometry(QtCore.QRect(120, 375, 50, 20))
        self.le_ct.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_ct.setText('1')

        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(20, 400, 100, 23))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(120, 400, 50, 20))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')

        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(20, 425, 80, 12))
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(120, 425, 50, 20))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        self.retranslateUi(Dialog)
        self.comboBox_lan.addItems(lang)
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
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("pressed()"), self.update)       
        QtCore.QObject.connect(self.pushButton_ct, QtCore.SIGNAL("pressed()"), self.countCulc)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
        
        
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "PipeFittings", None))
    
    def massImput(self):#質量入力
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g
    def countCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        count=int(self.le_ct.text())
        try:
            obj.addProperty("App::PropertyFloat", "count",label)
            obj.count=count
        except:
            obj.count=count 
    def massCulc(self):#質量計算
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        try:
            g=round(obj.Shape.Volume*g0*1000/10**9 ,2)
        except:
             pass
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g        

    def massTally(self):#parts list spreadsheet
        doc = App.ActiveDocument
        spreadsheet = doc.getObject("Parts_List") 
        if spreadsheet is None:
            spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
            #return  
        # ヘッダー行を記入
        headers = ["No",  "Name", "Dia", "Standard",'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            #spreadsheet.set(f"A{i+1}", str(i + 1))  # 行番号
            spreadsheet.set(f"A{1}", headers[0])
            spreadsheet.set(f"B{1}", headers[1])
            spreadsheet.set(f"C{1}", headers[2])
            spreadsheet.set(f"D{1}", headers[3])
            spreadsheet.set(f"E{1}", headers[4])
            spreadsheet.set(f"F{1}", headers[5])
            spreadsheet.set(f"G{1}", headers[6])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if hasattr(obj, "count") and obj.count > 0:
                try:
                    spreadsheet.set(f"A{row}", str(row-1))  # No
                    spreadsheet.set(f"B{row}", obj.Label)  
                    spreadsheet.set(f"C{row}", obj.dia)
                    #spreadsheet.set(f"D{row}", obj.standard) 
                    try:
                        spreadsheet.set(f"A{row}", str(row-1))  # No
                        spreadsheet.set(f"B{row}", obj.Label)  
                        spreadsheet.set(f"C{row}", obj.dia)
                        
                        try:
                            spreadsheet.set(f"D{row}", 'L='+obj.L+'mm') 
                        except:
                            pass    
                        n=obj.count
                        print(n)
                        spreadsheet.set(f"E{row}", str(n))   # count
                        print(obj.mass)
                        spreadsheet.set(f"F{row}", str(obj.mass))
                        spreadsheet.set(f"G{row}", f"{obj.mass*n:.2f}")  # mass
                    except:
                        pass
                    s=obj.mass*n+s
                    row += 1
                except:
                    print('error')
                    pass    
                spreadsheet.set(f'G{row}',str(s))

        App.ActiveDocument.recompute()
    
    def read_data(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            try:
                type=obj.type
            except:
                pass
            fittings=obj.fittings
            dia=obj.dia
            material=obj.material
            st=obj.standard
            self.comboBox_typ.setCurrentText(type)
            self.comboBox_lst.setCurrentText(fittings)
            self.comboBox_standard.setCurrentText(st)
            self.comboBox_dia.setCurrentText(dia)
            self.comboBox_material.setCurrentText(material)
          
            if obj.Label=='Single_flange_straight_pipe' or obj.Label=='Both_flanges_straight_pipe':
                st=obj.standard
                st2=obj.standard2
                self.comboBox_standard.setCurrentText(st+'_'+st2)
            try:
                L=int(obj.L)
                self.spinBoxL.setValue(int(L))
            except:
                pass
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
            dia=self.comboBox_dia.currentText()
            obj.dia=dia
            st=self.comboBox_standard.currentText()
            try:
                obj.standard=st
            except:
                pass
            material=self.comboBox_material.currentText()
            obj.material=str(material)
            label=self.comboBox_lst.currentText()[3:]
            type=self.comboBox_typ.currentText()
            try:
                obj.addProperty("App::PropertyString", "type",label)
                obj.type=type
            except:
                obj.type=type
                print('error')
                pass    
            try:
                if myShape.Name=='Single_flange_straight_pipe' or myShape.Name=='Both_flanges_straight_pipe':
                     if self.comboBox_material.currentIndex()==0:
                         if material[:3]=='SGP':
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
                     try:
                        L0=self.spinBoxL.value()
                        myShape.L=str(L0)
                     except:
                        myShape=None
                elif myShape.Name[:6]=='Flange':
                    
                    if st=='JIS2k':
                        sa=WeldStl_data.JIS2k[dia]
                    elif st=='JIS5k':
                        if self.comboBox_typ.currentText()=='Welded joint':
                            sa=WeldStl_data.JIS5k[dia] 
                        elif self.comboBox_typ.currentText()=='Threaded fitting':
                            sa=ThreadStl_data.JIS5k[dia] 
                    elif st=='JIS7.5k':
                        sa=WeldStl_data.JIS75k[dia]  
                    elif st=='JIS10k':
                        if self.comboBox_typ.currentText()=='Welded joint':
                            sa=WeldStl_data.JIS10k[dia]
                        elif self.comboBox_typ.currentText()=='Threaded fitting':
                            sa=ThreadStl_data.JIS10k[dia] 
                    elif st=='JIS16k':
                        sa=WeldStl_data.JIS16k[dia]
                    elif st=='JIS20k':
                        sa=WeldStl_data.JIS20k[dia]  
                    t=sa[4]
                    myShape.t=str(t)
                elif myShape.Name[:4]=='Elbo':
                    sa=WeldStl_data.elbo[dia]
                    if st[:8]=='045_Long':
                        B=round(sa[1]*math.tan(22.5/57.3),1)
                        myShape.B=str(B)
                    elif st[:8]=='090_Long' or st[:8]=='090_Large':
                        A=round(sa[1]*math.tan(45),1)  
                        myShape.A=str(A) 
                    elif st[:8]=='180_Long':
                        P=round(sa[1]*2,1)
                        myShape.P=str(P) 
                    elif st[:8]=='045_Short':
                        B=round(sa[1]*math.tan(22.5/57.3),1)   
                        myShape.B=str(B) 
                    elif st[:8]=='090_Short':
                        A=round(sa[1]*math.tan(45),1)  
                        myShape.A=str(A)
                    elif st[:8]=='180_Short':
                        P=round(sa[1]*2,1) 
                        myShape.P=str(P) 

                    elif st=='45L':
                        sa=ThreadStl_data.elbows[obj.dia]
                        A45=sa[1]
                        myShape.A45=str(A45)  
                    elif st=='90L':
                        sa=ThreadStl_data.elbows[obj.dia]
                        A=sa[0]
                        B=sa[1]
                        myShape.A=str(A)     
                        myShape.B=str(B)  
                    elif st=='90SL' :
                        sa=ThreadStl_data.elbows_sl[obj.dia]
                        A=sa[0]
                        B=sa[1] 
                        myShape.A=str(A)     
                        myShape.B=str(B)  
                    elif st=='90RL' :    
                        sa=ThreadStl_data.elbows_rl[obj.dia]
                        A=sa[0]
                        B=sa[1]      
                        myShape.A=str(A)     
                        myShape.B=str(B)  
                    elif st=='90RSL' :
                        sa=ThreadStl_data.elbows_rsl[obj.dia]
                        A=sa[0]
                        B=sa[1]  
                        myShape.A=str(A)     
                        myShape.B=str(B) 
                elif myShape.Name[:3]=='Tee':
                    if self.comboBox_typ=='Welded joint':
                        sa=WeldStl_data.tees[dia]   
                        C=sa[2]  
                        M=sa[3]
                        myShape.C=str(C)    
                        myShape.M=str(M) 
                    elif self.comboBox_typ=='Theaded fitting':
                        if st=='T':
                            sa=ThreadStl_data.tees_e[obj.dia]
                            A=sa[0]
                            myShape.A=str(A) 
                        elif st=='RT':
                            sa=ThreadStl_data.tees_d[obj.dia]
                            A=sa[0]
                            B=sa[1]  
                            myShape.A=str(A) 
                            myShape.B=str(B)   
                elif myShape.Name=='Y':
                    if st=='45Y':
                        sa=ThreadStl_data.Ys_d[obj.dia]
                        A=sa[0]
                        B=sa[1]
                        myShape.A=str(A) 
                        myShape.B=str(B)  
                    elif st=='90Y':
                        sa=ThreadStl_data.Ys_d[obj.dia]
                        A=sa[2]
                        B=sa[3] 
                        myShape.A=str(A) 
                        myShape.B=str(B)    
                elif myShape.Name=='Cross': 
                    st=self.comboBox_standard.currentText()   
                    if st=='Cr':
                        sa=ThreadStl_data.cross_e[obj.dia]
                        A=sa[0]
                        myShape.A=str(A) 
                    elif st=='RCr':
                        sa=ThreadStl_data.cross_d[obj.dia]
                        A=sa[0]
                        B=sa[1]
                        myShape.A=str(A) 
                        myShape.B=str(B) 

                elif myShape.Name=='Bend':    
                    if st[:2]=='45':
                       sa=ThreadStl_data.bends_d[obj.dia]
                       A=sa[0]  
                       myShape.A=str(A)   
                    elif st[:2]=='90':
                       sa=ThreadStl_data.bends_d[obj.dia]
                       A=sa[2]
                       myShape.A=str(A) 
                elif myShape.Name=='Nipple':    
                    sa=ThreadStl_data.nipples_d[obj.dia]
                    L=sa[0]
                    E1=sa[1]
                    E2=sa[2] 
                    myShape.L=str(L)  
                    myShape.E1=str(E1)  
                    myShape.E2=str(E2)         

                elif myShape.Name[:7]=='Reducer':
                    sa=WeldStl_data.reducs[dia]    
                    H=sa[2]
                    myShape.H=str(H) 
                elif myShape.Name[:9]=='Rap_joint':
                    sa=WeldStl_data.raps[obj.dia] 
                    F=sa[4]
                    myShape.F=str(F)
                elif myShape.Name[:19]=='Gate_Valve_internal' or myShape.Name[:19]=='Gate_Valve_external':
                    if self.comboBox_typ.currentText()=='Welded joint':
                        st=self.comboBox_standard.currentText() 
                        if self.comboBox_material.currentIndex()==0:
                            obj.standard=WeldStl_data.exp_carbon
                            i=self.comboBox_standard.currentIndex()
                            obj.standard=WeldStl_data.exp_carbon[i]
                            sa=WeldStl_data.gates_10k_cast[obj.dia] 
                        elif self.comboBox_material.currentIndex()==1:
                            obj.standard=WeldStl_data.exp_carbon
                            i=self.comboBox_standard.currentIndex()
                            obj.standard=WeldStl_data.exp_carbon[i]  
                            sa=WeldStl_data.gates_10k_SUS[obj.dia]
                            
                        L=sa[0]
                        if myShape.Name[:19]=='Gate_Valve_internal':
                            H=sa[1]
                        elif myShape.Name[:19]=='Gate_Valve_external':
                            H=sa[2]  
                        myShape.H=str(H)  
                        myShape.L=str(L) 
                    else:
                        return  
                elif myShape.Name[:10]=='Gate_Valve': 
                    st=self.comboBox_standard.currentText() 
                    if st=='JIS10k':
                        sa= ThreadStl_data.gates_10k[obj.dia]
                    elif st=='JIS5k':
                        sa= ThreadStl_data.gates_5k[obj.dia]
                    L=sa[1]
                    myShape.L=str(L) 
                elif myShape.Name[:11]=='Check_Valve':
                    st=self.comboBox_standard.currentText()
                    if self.comboBox_typ.currentText()=='Welded joint':
                        if st=='JIS10k': 
                            sa=WeldStl_data.checks_10k_cast[dia] 
                        elif st=='JIS7.5k':    
                            sa=WeldStl_data.checks_75k_cast[dia] 
                    elif self.comboBox_typ.currentText()=='Threaded fitting':
                        if st=='JIS10k':
                            sa= ThreadStl_data.checks_10k[obj.dia]
                    L=sa[1]
                    myShape.L=str(L)  
                elif myShape.Name[:9]=='Expansion':
                    st=self.comboBox_standard.currentText() 
                    if st=='20mm':
                        sa=WeldStl_data.exp_20mm[obj.dia]
                    elif st=='50mm':
                        sa=WeldStl_data.exp_50mm[obj.dia] 
                    elif st=='100mm':
                        sa=WeldStl_data.exp_100mm[obj.dia]  
                    elif st=='200mm':
                        sa=WeldStl_data.exp_200mm[obj.dia]    
                    L=sa[2] 
                    myShape.L=str(L)   

                elif myShape.Name[:4]=='Flex':
                    sa=WeldStl_data.exp_50mm[dia]   
                    L=sa[7]
                    myShape.L=str(L)  
                elif myShape.Name[:4]=='Straight_Pipe':
                    if self.comboBox_typ=='Theaded fitting':
                        L=self.spinBoxL.value()
                        myShape.L=L
                App.ActiveDocument.recompute(None,True,True) 
            except:
                #myShape.dia=dia

                pass

            gengo=self.comboBox_lan.currentText()
            label2=self.label_l.text()
            label=self.comboBox_lst.currentText()[3:]
            if gengo=='Japanese':
                obj.Label=label2
            else:
                obj.Label=label 
            print(gengo,label,label2)                  
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
            self.comboBox_standard.clear() 
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
                    ta=WeldStl_data.s_flg_stainless

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
                ta=WeldStl_data.rap
            elif key=='11' or key=='12' :
                material=self.comboBox_material.currentText()
                ta=WeldStl_data.exp_carbon
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

        try:
            self.comboBox_standard.clear()
            self.comboBox_standard.addItems(ta)
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
                        dia=WeldStl_data.flg_d[18:]
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
                    dia=ThreadStl_data.tube_d [3:]
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
                    dia=ThreadStl_data.tube_d[1:]
                    FC="片長ニップル"
                elif st=='Both_nipple':
                    pic='img_' + st + '.png'
                    dia=ThreadStl_data.tube_d[1:]
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

                selection = Gui.Selection.getSelection()
                for obj in selection:    
                    self.comboBox_dia.setCurrentText(obj.dia)

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
        global key
        #global sa
        typ=self.comboBox_typ.currentText()
        key = self.comboBox_lst.currentText()[:2]
        gengo=self.comboBox_lan.currentText()
        if typ=='Welded joint':
            if key=='00' or key=='09' :
                if key=='00':
                    label = 'Flange'
                elif key=='09':
                    label='Flange_Lid'    
                label=self.comboBox_lst.currentText()[3:]
                
                #print(gengo,label,label2,label)  
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                obj.addProperty("App::PropertyEnumeration", "standard",label)

                #label2=self.label_l.text()
                #if gengo=='Japanese':
                #    obj.Label=label2
                #else:
                #    obj.Label=label  

                if self.comboBox_material.currentIndex()==0:
                    obj.standard=WeldStl_data.flg_carbon
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_carbon[i]
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]  

                st=self.comboBox_standard.currentText()
                if st=='JIS2k':
                    sa=WeldStl_data.JIS2k[obj.dia]
                elif st=='JIS5k':
                    sa=WeldStl_data.JIS5k[obj.dia] 
                elif st=='JIS7.5k':
                    sa=WeldStl_data.JIS75k[obj.dia]  
                elif st=='JIS10k':
                    sa=WeldStl_data.JIS10k[obj.dia]
                elif st=='JIS16k':
                    sa=WeldStl_data.JIS16k[obj.dia]
                elif st=='JIS20k':
                    sa=WeldStl_data.JIS20k[obj.dia]  
                t=sa[4]
                obj.addProperty("App::PropertyString", "t",label).t=str(t)
                
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

                st=self.comboBox_standard.currentText()   
                sa=WeldStl_data.elbo[obj.dia]

                if st[:8]=='045_Long':
                    B=round(sa[1]*math.tan(22.5/57.3),1)
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)
                elif st[:8]=='090_Long' or st[:8]=='090_Large':
                    A=round(sa[1]*math.tan(45),1)  
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)  
                elif st[:8]=='180_Long':
                    P=round(sa[1]*2,1)
                    obj.addProperty("App::PropertyString", "P",label).P=str(P)  
                if st[:8]=='045_Short':
                    B=round(sa[1]*math.tan(22.5/57.3),1)
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)
                elif st[:8]=='090_Short':
                    A=round(sa[1]*math.tan(45),1)  
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)  
                elif st[:8]=='180_Short':
                    P=round(sa[1]*2,1)
                    obj.addProperty("App::PropertyString", "P",label).P=str(P)    
                App.activeDocument().recompute(None,True,True)
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

                st=self.comboBox_standard.currentText()   
                sa=WeldStl_data.tees[obj.dia] 
                C=sa[2]
                M=sa[3]
                obj.addProperty("App::PropertyString", "C",label).C=str(C)  
                obj.addProperty("App::PropertyString", "M",label).M=str(M) 

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
                st=self.comboBox_standard.currentText()   
                sa=WeldStl_data.tees[obj.dia] 
                H=sa[2]
                obj.addProperty("App::PropertyString", "H",label).H=str(H) 

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

                st=self.comboBox_standard.currentText()   
                sa=WeldStl_data.tees[obj.dia] 
                H=sa[2]
                obj.addProperty("App::PropertyString", "H",label).H=str(H)             

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
                    st=self.comboBox_standard.currentText() 
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

                st=self.comboBox_standard.currentText()   
                sa=WeldStl_data.raps[obj.dia] 
                F=sa[4]
                obj.addProperty("App::PropertyString", "F",label).F=str(F) 
                obj.standard=st
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
                    sa=WeldStl_data.gates_10k_cast[obj.dia] 
                elif self.comboBox_material.currentIndex()==1:
                    obj.standard=WeldStl_data.flg_stainless
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=WeldStl_data.flg_stainless[i]  
                    sa=WeldStl_data.gates_10k_SUS[obj.dia] 

                st=self.comboBox_standard.currentText()   
                L=sa[0]
                if key=='11':
                    H=sa[1]
                elif key=='12':
                    H=sa[2]    

                obj.addProperty("App::PropertyString", "H",label).H=str(H) 
                obj.addProperty("App::PropertyString", "L",label).L=str(L) 
                st=self.comboBox_standard.currentText()
                obj.standard=st 



            elif key=='13':
                label = 'Check_Valve_swing_type'    
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=dia                
                i=self.comboBox_dia.currentIndex()
                obj.dia=dia[i]
                
                obj.addProperty("App::PropertyEnumeration", "standard",label)
                obj.standard=WeldStl_data.check
                i=self.comboBox_standard.currentIndex()
                obj.standard=WeldStl_data.check[i]
                st=self.comboBox_standard.currentText() 
                if st=='JIS10k':
                    sa= WeldStl_data.checks_10k_cast[obj.dia]
                elif st=='JIS7.5k':
                    sa= WeldStl_data.checks_75k_cast[obj.dia]    
                L=sa[1]
                obj.addProperty("App::PropertyString", "L",label).L=str(L) 

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
                
                st=self.comboBox_standard.currentText() 
                if st=='20mm':
                    sa=WeldStl_data.exp_20mm[obj.dia]
                elif st=='50mm':
                    sa=WeldStl_data.exp_50mm[obj.dia] 
                elif st=='100mm':
                    sa=WeldStl_data.exp_100mm[obj.dia]  
                elif st=='200mm':
                    sa=WeldStl_data.exp_200mm[obj.dia]    
                L=sa[2]
                obj.addProperty("App::PropertyString", "L",label).L=str(L)  
                obj.standard=st




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

                st=self.comboBox_standard.currentText() 
                sa=WeldStl_data.exp_50mm[obj.dia] 
                L=sa[7]
                obj.addProperty("App::PropertyString", "L",label).L=str(L)  
                obj.standard=st     



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
                    obj.standard=ThreadStl_data.flg
                    i=self.comboBox_standard.currentIndex()
                    obj.standard=ThreadStl_data.flg[i]
                elif self.comboBox_material.currentIndex()==1:
                    return
                st=self.comboBox_standard.currentText()
                if st=='JIS5k':
                    sa=ThreadStl_data.JIS5k[obj.dia] 
                elif st=='JIS10k':
                    sa=ThreadStl_data.JIS10k[obj.dia]
                t=sa[4]
                obj.addProperty("App::PropertyString", "t",label).t=str(t)

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

                st=self.comboBox_standard.currentText()   
                if st=='45L':
                    sa=ThreadStl_data.elbows[obj.dia]
                    A45=sa[1]
                    obj.addProperty("App::PropertyString", "A45",label).A45=str(A45)
                elif st=='90L' :
                    sa=ThreadStl_data.elbows[obj.dia]
                    A=sa[0]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)  
                elif st=='90SL' :
                    sa=ThreadStl_data.elbows_sl[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)      
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)   
                elif st=='90RL' :
                    sa=ThreadStl_data.elbows_rl[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)      
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)    
                elif st=='90RSL' :
                    sa=ThreadStl_data.elbows_rsl[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)      
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)          
                

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

                st=self.comboBox_standard.currentText()   
                if st[:2]=='45':
                    sa=ThreadStl_data.bends_d[obj.dia]
                    A=sa[0]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)
                elif st[:2]=='90':
                    sa=ThreadStl_data.bends_d[obj.dia]
                    A=sa[2]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)    



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

                st=self.comboBox_standard.currentText()   
                if st=='T':
                    sa=ThreadStl_data.tees_e[obj.dia]
                    A=sa[0]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)
                elif st=='RT':
                    sa=ThreadStl_data.tees_d[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)  
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)   
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

                st=self.comboBox_standard.currentText()   
                if st=='45Y':
                    sa=ThreadStl_data.Ys_d[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)
                elif st=='90Y':
                    sa=ThreadStl_data.Ys_d[obj.dia]
                    A=sa[2]
                    B=sa[3]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)    

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

                st=self.comboBox_standard.currentText()   
                if st=='Cr':
                    sa=ThreadStl_data.cross_e[obj.dia]
                    A=sa[0]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)
                elif st=='RCr':
                    sa=ThreadStl_data.cross_d[obj.dia]
                    A=sa[0]
                    B=sa[1]
                    obj.addProperty("App::PropertyString", "A",label).A=str(A)    
                    obj.addProperty("App::PropertyString", "B",label).B=str(B)   

            elif key=='06' :
                label = 'Nipple'
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

                st=self.comboBox_standard.currentText()  
                if st=='Nipple':
                    sa=ThreadStl_data.nipples[obj.dia]
                    L=sa[0]
                    E=sa[1]
                    obj.addProperty("App::PropertyString", "L",label).L=str(L)
                    obj.addProperty("App::PropertyString", "E",label).E=str(E)
                elif st=='Reducing_nipple':
                    sa=ThreadStl_data.nipples_d[obj.dia]
                    L=sa[0]
                    E1=sa[1]
                    E2=sa[2]
                    obj.addProperty("App::PropertyString", "L",label).L=str(L)    
                    obj.addProperty("App::PropertyString", "E1",label).E1=str(E1)  
                    obj.addProperty("App::PropertyString", "E2",label).E2=str(E2)
                elif st=='Hose_nipple':
                    sa=ThreadStl_data.nipples_h[obj.dia]
                    L=sa[0]
                    E1=sa[1]
                    E2=sa[2]
                    obj.addProperty("App::PropertyString", "L",label).L=str(L)    
                    obj.addProperty("App::PropertyString", "E1",label).E1=str(E1)  
                    obj.addProperty("App::PropertyString", "E2",label).E2=str(E2) 
                elif st=='Piece_nipple' or st=='Both_nipple':
                    #L=self.spinBoxL.value() 
                    sa=ThreadStl_data.nipples_p[obj.dia]
                    L=sa[0]
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

                st=self.comboBox_standard.currentText() 
                if st=='JIS10k':
                    sa= ThreadStl_data.globes_10k[obj.dia]
                elif st=='JIS5k':
                    sa= ThreadStl_data.globes_5k[obj.dia]
                L=sa[1]
                obj.addProperty("App::PropertyString", "L",label).L=str(L)     

            elif key=='14' :
                label = 'Check_Valve'
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

                st=self.comboBox_standard.currentText() 
                if st=='JIS10k':
                    sa= ThreadStl_data.checks_10k[obj.dia]
                L=sa[1]
                obj.addProperty("App::PropertyString", "L",label).L=str(L)     



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

        Gui.Selection.addSelection(obj)
        try:
            Gui.runCommand('Draft_Move',0)
        except:
            pass
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(obj)  
        Gui.ActiveDocument.ActiveView.fitAll()      

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()


