from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import Duct_data

class duct_p:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        fittings=App.ActiveDocument.getObject(label).fittings
        key=fittings[:2]
        material=App.ActiveDocument.getObject(label).material
        st=App.ActiveDocument.getObject(label).standard
        dia=App.ActiveDocument.getObject(label).dia
        def strait_p(self):
            global c00
            sa=Duct_data.strt_dia[dia]
            d=sa[0]
            t1=sa[1]
            #L=App.ActiveDocument.getObject(label).L
            D=d+2*t1
            c00=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c00=c00.cut(c01)
        def p_flange(self):
            global c00
            sa=Duct_data.strt_dia[dia]
            t1=sa[1]
            sa=Duct_data.flange_dia[dia]
            D=sa[0]/2
            n=sa[3]
            h=5
            t=4.5
            D0=D+25
            C=D+15

            c1 = Part.makeCylinder(D0,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            c2 = Part.makeCylinder(D+t1,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(k_index), None, QtGui.QApplication.UnicodeUTF8))
            c00=c1.cut(c2)
            #Part.show(c00)
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
        def a_flange(self):
            global c00
            sa=Duct_data.strt_dia[dia]
            t1=sa[1]
            sa=Duct_data.flange_dia[dia]
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

        def packing(self):#パッキン
            global c00
            sa=Duct_data.flange_dia[dia]
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
        def outlet(self):
            global c01
            sa=Duct_data.strt_dia[dia]
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

        if key=='00':
            L=App.ActiveDocument.getObject(label).L
            L=float(L)
            if st=='Spiral':
                strait_p(self) 
                c1=c00   
            elif st=='Single_flange' or 'Both_flange':
                strait_p(self)
                c1=c00
                if float(dia)<=175:
                     p_flange(self)
                     c2=c00
                     c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                     c1=c1.fuse(c2)
                     if st=='Both_flange':
                         #L=App.ActiveDocument.getObject(label).L
                         p_flange(self)
                         c2=c00
                         c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),-90))
                         c1=c1.fuse(c2)
        
        elif key=='01':#カラー
            #print(st)
            if st=='T_collar':
                sa=Duct_data.strt_dia[dia]
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
                    sa=Duct_data.flange_dia[dia]
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

            elif st=='Flange_collar':
                sa=Duct_data.f_collar_dia[dia]
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

        elif key=='02':#キャップ
            if st=='Pipe_use':
                sa=Duct_data.p_cap_dia[dia]
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
                sa=Duct_data.p_cap_dia[dia]
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
            
        elif key=='03':#フランジ
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            if st=='Plate':
                p_flange(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                
            elif st=='Angle':
                a_flange(self)
                c1=c00
                
            elif st=='Packing':
                packing(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                

        elif key=='04':#ニップル
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None, QtGui.QApplication.UnicodeUTF8))
            if st=='Socket':
                outlet(self)
                c1=c01
                #c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),-90))
                sa=Duct_data.f_collar_dia[dia]
                D1=sa[0]
                t=sa[1]
                sa=Duct_data.strt_dia[dia]
                S=sa[5]
                c2 = Part.makeCylinder(D1/2,S,Base.Vector(-S,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder((D1-2*t)/2,S,Base.Vector(-S,0,0),Base.Vector(1,0,0))
                c2=c2.cut(c3)
                c1=c1.fuse(c2)
                

        elif key=='05':#ベンド
            sa=Duct_data.strt_dia[dia]
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

        elif key=='06':#片落ち管
            #global dia1
            #global dia2

            if st=='Socket':
                sa=Duct_data.reduc_dia[dia]
                L=sa[0]
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=Duct_data.strt_dia[dia1]
                d1=float(sa[0])
                t=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=Duct_data.strt_dia[dia2]
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
            


        elif key=='07' or key=='08':#T字管 クロス
            #global dia1
            #global dia2

            if st=='Socket':
                sa=Duct_data.tee_dia[dia]
                L=float(sa[0])
                l=float(sa[1])
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=Duct_data.strt_dia[dia1]
                d1=float(sa[0])
                t1=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=Duct_data.strt_dia[dia2]
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
                if key=='08':
                    c021 = Part.makeCylinder(d2/2,l,Base.Vector(L/2-W1,-l,0),Base.Vector(0,1,0))
                    c031 = Part.makeCylinder((d2-2*t2)/2,l,Base.Vector(L/2-W1,-l,0),Base.Vector(0,1,0))
                    c1=c1.fuse(c021)
                    c1=c1.cut(c031)
                    c1=c1.cut(c2)
                
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
                if key=='08':
                    dia=dia2
                    outlet(self)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector((L-2*W1)/2,-(l-W2),0),App.Rotation(App.Vector(0,0,1),-90))
                    c1=c1.fuse(c2)

        elif key=='09':#Y管
            #global dia1
            #global dia2

            if st=='Socket':
                label = 'Y_'  +  str(dia) + " "
                sa=Duct_data.tee_dia[dia]
                L=float(sa[2])
                l=float(sa[3])
                L1=float(sa[4])
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                D1=float(dia1)
                D2=float(dia2)
                sa=Duct_data.strt_dia[dia1]
                d1=float(sa[0])
                t1=float(sa[1])
                W1=float(sa[2])
                S1=float(sa[5])
                sa=Duct_data.strt_dia[dia2]
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

        elif key=='10':#ダンパー
            label='VD_' + str(dia)+'_'
            if st=='VD_A':
                sa=Duct_data.dv_dapA[dia]
            d=float(sa[0])
            L=float(sa[2])
            t=float(sa[3])
            sa=Duct_data.strt_dia[dia]
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
        Gui.Selection.addSelection(doc.Name,obj.Name)
        Gui.runCommand('Draft_Move',0)    
        obj.Shape=c1