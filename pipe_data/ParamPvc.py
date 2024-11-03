# -*- coding: utf-8 -*-
from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
from . import Pvc_data
from . import WeldStl_data
DEBUG = True # set to True to show debug messages
class pvc_p:
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
        key_1=App.ActiveDocument.getObject(label).dia
        Thread=App.ActiveDocument.getObject(label).Thread

        def cutter_01(self): #おねじ　ねじなし
            global c10
            sa=Pvc_data.screws[dia]
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
            sa1=Pvc_data.strt_dia[dia]
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
            sa=Pvc_data.screws[dia]
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
            sa1=Pvc_data.strt_dia[dia]
            d2=float(sa1[0])/2
            t=float(sa1[1])
            d0=d2-t

            sa=Pvc_data.valve_s_d[dia]
            L00=float(sa[0])
            W=float(sa[4])
            sa = Pvc_data.nipples[dia]
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
                sa=Pvc_data.JIS5k_socket[dia]
            elif st=='JIS10k_socket' :
                sa=Pvc_data.JIS10k_socket[dia]

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
            #global dia
            sa=Pvc_data.pvc_ts[dia]
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
            #global dia
            sa=Pvc_data.pvc_dv[dia]
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
               sa = Pvc_data.JIS5k_2[dia]
               #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st), None))
           elif st[-3:]=='10k' :
               sa = Pvc_data.JIS10k_2[dia]

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
               sa = Pvc_data.JIS5k_2[dia]
           elif st=='JIS10k_lid' :
               sa = Pvc_data.JIS10k_2[dia]

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

        #if key=='00' :
        key==fittings[:3]
        if key=='00':#直管
            sa=Pvc_data.strt_dia[dia]
            D=float(sa[0])
            L=App.ActiveDocument.getObject(label).L
            L=float(L)
            
            if st[:2]=='VP' or st[:2]=='VU' or st[:3]=='VPW':
                if st[:2]=='VP' :
                    t=float(sa[1])
                elif st[:2]=='VU' :
                    t=float(sa[3])
                elif st[:3]=='VPW' :
                    t=float(sa[5])
                d=D-2*t
                
                c1=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                #Part.show(c1)
                
            if st[3:7]=='Both' or st[4:8]=='Both':

                c1=Part.makeCylinder(D/2,L-2*t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                c2=Part.makeCylinder(d/2,L-2*t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)

                Flange1(self)
                #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(st[3:7]), None))
                c2=c01
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
                c2=c01
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.fuse(c2)
                #Part.show(c2)
            elif st[3:9]=='Single' or st[4:10]=='Single':
                c1=Part.makeCylinder(D/2,L-t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                c2=Part.makeCylinder(d/2,L-t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                Flange1(self)
                c2=c01
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
            
        elif key=='01':#エルボ
            if material=='TS':
                if st=='45' or st=='90':
                    sa=Pvc_data.pvc_ts[dia]
                    D1=float(sa[0])
                    l=float(sa[3])
                    D=float(sa[5])
                    d=float(sa[4])
                    s0=float(st)/2
                    sa=Pvc_data.elbow_ts[dia]
                    if st=='90':
                        #b='TS90Elbow_'
                        L=float(sa[1])
                    elif st=='45':
                        #b='TS45Elbow_'
                        L=float(sa[2])
                    #label=b + '_' + str(dia) +'_'
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
                    #Part.show(c1)
            elif material=='DV':
                if st=='45' or st=='90':
                    sa=Pvc_data.pvc_dv[dia]
                    D1=float(sa[0])
                    l=float(sa[3])
                    D=float(sa[5])
                    d=float(sa[4])
                    t=float(sa[6])
                    s0=float(st)/2
                    sa=Pvc_data.elbow_dv[dia]
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
        
        elif key=='02':#ソケット
            if st=='Socket' :
                label='Socket_' + str(dia)+'_'
                if material=='TS':
                    sa=Pvc_data.pvc_ts[dia]
                elif material=='DV':
                    sa=Pvc_data.pvc_dv[dia]
                d1=float(sa[1])/2
                T=float(sa[2])
                l=float(sa[3])
                d=float(sa[4])
                D=float(sa[5])
                L=float(sa[7])

                c1=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)

                if material=='TS':
                    ts_junc(self)
                elif material=='DV':
                    dv_junc(self)

                c2=c00
                c2.Placement=App.Placement(App.Vector(l,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.cut(c2)

                c2=c00
                c2.Placement=App.Placement(App.Vector(L-l,0,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.cut(c2)

            elif st=='Increaser' :
                if material=='TS':
                    sa=Pvc_data.ts_dsoc[dia]
                elif material=='DV':
                    sa=Pvc_data.dv_dsoc[dia]
                D=float(sa[0])/2
                D1=float(sa[1])/2
                L=float(sa[2])
                key1=dia.find('x')
                key2=key1+1
                dia1=dia[:key1]
                dia2=dia[key2:]
                if material=='TS':
                    sa=Pvc_data.pvc_ts[dia1]
                elif material=='DV':
                    sa=Pvc_data.pvc_dv[dia1]
                l1=float(sa[3])
                d21=float(sa[4])/2
                t1=float(sa[6])
                if material=='TS':
                    sa=Pvc_data.pvc_ts[dia2]
                elif material=='DV':
                    sa=Pvc_data.pvc_dv[dia2]

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
                if material=='TS':
                    ts_junc(self)
                elif material=='DV':
                    dv_junc(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(l1,0,0),App.Rotation(App.Vector(0,0,1),180))
                c1=c1.cut(c2)
                dia=dia2
                if material=='TS':
                    ts_junc(self)
                elif material=='DV':
                    dv_junc(self)

                c2=c00
                c2.Placement=App.Placement(App.Vector(L-l2,0,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.cut(c2)

            elif st=='Valve' :
                sa=Pvc_data.valve_s_d[dia]
                L=float(sa[0])
                E=float(sa[1])
                W=float(sa[4])
                sa=Pvc_data.screws[dia]
                l=float(sa[8])
                x=E-l
                if x<=0:
                    x=0
                hexagon(self)
                c1=c10
                sa=Pvc_data.strt_dia[dia]
                D=sa[0]/2
                if x > 0 :
                    c2=Part.makeCylinder(D,x,Base.Vector(0,0,W),Base.Vector(0,0,1))
                    c1=c1.fuse(c2)
                cutter_01(self)
                c2=c10
                c2.Placement=App.Placement(App.Vector(0,0,l+W+x),App.Rotation(App.Vector(0,1,0),180))
                c1=c1.fuse(c2)
                sa=Pvc_data.pvc_ts[dia]
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
                sa=Pvc_data.pvc_ts[dia]
                l=float(sa[3])
                c2.Placement=App.Placement(App.Vector(0,0,-(L3-l)),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))

        elif key=='03':#チーズ Y
            if material=='TS':
                if st=='Same_dia' :
                    sa=Pvc_data.ts_tee[dia]
                    H=float(sa[0])
                    I=float(sa[1])
                    D=float(sa[2])
                    sa=Pvc_data.pvc_ts[dia]
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
                    sa=Pvc_data.ts_dtee[dia]
                    H=float(sa[0])
                    I=float(sa[1])
                    D=float(sa[2])
                    D1=float(sa[3])
                    key1=dia.find('x')
                    key2=key1+1
                    dia1=dia[:key1]
                    dia2=dia[key2:]
                    sa=Pvc_data.pvc_ts[dia1]
                    l1=float(sa[3])
                    d=float(sa[4])
                    sa=Pvc_data.pvc_ts[dia2]
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
            elif material=='DV':#90Y
                if st=='Same_dia' :
                    sa=Pvc_data.dv_90Y[dia]
                    z1=float(sa[0])
                    z2=float(sa[1])
                    z3=float(sa[2])
                    L1=float(sa[3])
                    L2=float(sa[4])
                    L3=float(sa[5])
                    sa=Pvc_data.pvc_dv[dia]
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
                    sa=Pvc_data.dv_d90Y[dia]
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
                    sa=Pvc_data.pvc_dv[dia1]
                    D01=float(sa[0])
                    l1=float(sa[3])
                    d1=float(sa[4])
                    t1=float(sa[6])
                    sa=Pvc_data.pvc_dv[dia2]
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

        elif key=='04':#フランジ
            if st=='JIS5k_socket' or st=='JIS10k_socket':
                if st=='JIS5k_socket':
                    sa=Pvc_data.JIS5k_socket[dia]
                elif st=='JIS10k_socket':
                    sa=Pvc_data.JIS10k_socket[dia]
                L=float(sa[6])
                if material=='TS':
                    sa=Pvc_data.pvc_ts[dia]
                    label='TS_Flange_' + str(dia)+'_'
                elif material=='DV':
                    sa=Pvc_data.pvc_ts[dia]
                    label='DV_Flange_' + str(dia)+'_'
                l=float(sa[3])
                d=float(sa[4])
                flange(self)
                c1=c00
                if material=='TS':
                    ts_junc(self)
                    sa=Pvc_data.pvc_ts[dia]
                elif material=='DV':
                    ts_junc(self)
                    sa=Pvc_data.pvc_ts[dia]
                c2=c00

                l=float(sa[3])
                c2.Placement=App.Placement(App.Vector(0,0,L-l),App.Rotation(App.Vector(0,1,0),-90))
                c1=c1.cut(c2)
                c2 = Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(0,0,1))
                c1=c1.cut(c2)

            elif st=='JIS5k' or st=='JIS10k':
                if st=='JIS5k':
                    sa=Pvc_data.JIS5k_2[dia]
                    label='Flange_' + str(dia)+'_'

                elif st=='JIS10k':
                    sa=Pvc_data.JIS10k_2[dia]
                    label='Flange_' + str(dia)+'_'
                Flange1(self)
                c1=c01

            elif st=='JIS5k_lid' or st=='JIS10k_lid':
                if st=='JIS5k_lid':
                    sa=Pvc_data.JIS5k_2[dia]
                    label='Flange_' + str(dia)+'_'
                elif st=='JIS10k_lid':
                    sa=Pvc_data.JIS10k_2[dia]
                    label='Flange_' + str(dia)+'_'
                Flange2(self)
                c1=c01

        elif key=='05':#ダンパー
            if st=='VD_A':
                sa=Pvc_data.dv_dapA[dia]
            elif st=='VD_B':
                sa=Pvc_data.dv_dapB[dia]
            elif st=='VD_C_5k':
                sa=Pvc_data.dv_dapA[dia]
            elif st=='VD_C_10k':
                sa=Pvc_data.dv_dapA[dia]

            D=float(sa[0])
            L=float(sa[2])
            t1=float(sa[3])
            sa=Pvc_data.pvc_dv[dia]
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
        Gui.Selection.addSelection(doc.Name,obj.Name)
        Gui.runCommand('Draft_Move',0)    
        obj.Shape=c1 






