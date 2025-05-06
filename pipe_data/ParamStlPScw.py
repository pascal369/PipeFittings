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
from . import ThreadStl_data
from . import WeldStl_data
DEBUG = True # set to True to show debug messages
class threaded_p:
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
        def Flange(self):#フランジ本体
            global c00
            if st=='JIS5k':
                sa = ThreadStl_data.JIS5k[key_1]
            elif st=='JIS10k':
                sa = ThreadStl_data.JIS10k[key_1]
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
            sa=ThreadStl_data.screws[key_1]
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
            sa1=ThreadStl_data.tubes[key_1]
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            plist=[p4,p3,p5,p6,p4]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=c00.fuse(c20)
        def cutter_01a(self): #おねじ　ねじなし 管用
            global c00
            sa=ThreadStl_data.screws[key_1]
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
            sa1=ThreadStl_data.tubes[key_1]
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            plist=[p4,p3,p5,p6,p4]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c20=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c00=c00.fuse(c20)
        def cutter_011(self): #めねじカッター　ねじなし穴
            global c00
            sa=ThreadStl_data.screws[key_1]
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
        def male_thread(self):#おねじ　ねじあり カッター用
            global c00
            sa=ThreadStl_data.screws[key_1]
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            cb1= Part.makeCylinder(d10,p,Base.Vector(0,0,-p),Base.Vector(0,0,1),360)
            c00=c00.fuse(cb1)
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
            helix=Part.makeHelix(p,l+0.15,d10,s0,False)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])

            cutProfile.Placement=App.Placement(App.Vector(-x0,0,0),App.Rotation(App.Vector(0,1,0),s0))
            
            wface=Part.Face(cutProfile)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.fuse(pipe)
            #Part.show(c00)
        def male_thread2(self):#おねじ　ねじあり　軸用
            global c00
            sa=ThreadStl_data.screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            l=float(sa[8])*1.0
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
            if key=='11' or key=='10' :
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
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
            if key_1=='20A' or key_1=='32A' or key_1=='40A' :
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p),App.Rotation(App.Vector(0,1,0),-s0))
            else:
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p),App.Rotation(App.Vector(0,1,0),-s0))
            wface=Part.Face(cutProfile)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.fuse(pipe)
            p3=Base.Vector(0,0,l)
            p5=Base.Vector(0,0,-2*p)
            c11 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p5)),Base.Vector(0,0,1))
            c00=c00.cut(c11)
            c12 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p3)),Base.Vector(0,0,1))
            c00=c00.cut(c12)
        def male_thread3(self):#R平行おねじ　ねじあり　軸用
            global c00
            sa=ThreadStl_data.screws[key_1]
            p=float(sa[0])
            h=float(sa[1])
            r=float(sa[2])
            D0=float(sa[3])/2 #外径
            d1=float(sa[5])/2 #谷径
            a=float(sa[6])
            t=float(sa[9])
            A2=float(sa[11])/2
            sa=ThreadStl_data.socket_p[key_1]
            l=float(sa[1])
            d0=A2-t+0.001
            s=0
            s0=math.degrees(s)
            d10=d1-a*math.tan(s)
            d11=d10-p*math.tan(s)
            d20=d10+l*math.tan(s)
            d21=d20+p*math.tan(s)
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
            pface = Part.Face(pwire)
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
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
            if key_1=='20A' or key_1=='32A' or key_1=='40A':
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p/2),App.Rotation(App.Vector(0,1,0),-s0))
            else:
                cutProfile.Placement=App.Placement(App.Vector(d11+h-r,0,-p),App.Rotation(App.Vector(0,1,0),-s0))
            wface=Part.Face(cutProfile)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            c00=c00.fuse(pipe)
            p3=Base.Vector(0,0,l)
            p5=Base.Vector(0,0,-2*p)
            c11 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p5)),Base.Vector(0,0,1))
            c00=c00.cut(c11)
            c12 = Part.makeCylinder(2.5*D0,2*p,Base.Vector((p3)),Base.Vector(0,0,1))
            c00=c00.cut(c12)
        def hexagon(self):
            global c00
            sa1=ThreadStl_data.tubes[key_1]
            d2=float(sa1[0])/2
            t=sa1[3]
            d0=d2-t
            if key=='11':
                sa=ThreadStl_data.bushs_d[dia]
                L00=sa[0]
                sa = ThreadStl_data.nipples[key_1]
            else:
                sa = ThreadStl_data.nipples[key_1]
                L00=sa[0]
            L=L00
            E=sa[1]
            n=sa[2]
            B=sa[3]/2
            dk=float(sa[4])/2
            if key=='11':
                H=L-E
            else:
                H=L-2*E
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
            c1=wface.extrude(Base.Vector(0,0,H))
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),90))
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
            c00=c1.cut(c2)
        def hexagon2(self):
            global c00
            sa = ThreadStl_data.nipples_h[key_1]
            L=sa[0]
            E1=sa[1]
            E2=sa[2]
            d0=sa[3]
            n=sa[6]
            B=sa[7]/2
            sa=ThreadStl_data.nipples[key_1]
            dk=float(sa[4])/2
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
            c00=c1.cut(c2)
        def hexagon3(self):#メートルネジ　ナット
            global c00
            doc=App.ActiveDocument
            V=FreeCAD.Vector
            sa = ThreadStl_data.regular[key_1]
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
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1+1,H)
            c2=c2.cut(c3)
        if key=='00':
            key_1=dia
            if st=='JIS5k':
                sa = ThreadStl_data.JIS5k[key_1]
            elif st=='JIS10k':
                sa = ThreadStl_data.JIS10k[key_1]
            Flange(self)
            c1=c00
            if Thread==True:
                male_thread(self)
                c2=c00
                c1=c1.cut(c2)
            else:
                cutter_01(self)
                c2=c00
                c1=c1.cut(c2)
                pass
        elif key=='01':
            if st=='45L' or st=='90L':
                key_1=dia
                sa=ThreadStl_data.elbows[key_1]
                A=sa[0]
                A45=sa[1]
                B=sa[2]
                sa1=ThreadStl_data.screws[key_1]
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.cut(c2)
                    
            elif st=='90SL':
                sa=ThreadStl_data.elbows_sl[key_1]
                A=sa[0]
                B=sa[1]
                sa1=ThreadStl_data.screws[key_1]
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
                if Thread==True:
                    s0=45
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread2(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c1=c1.cut(c2)
                    cutter_01(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                    
            elif st=='90RL':
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                sa=ThreadStl_data.elbows_rl[dia]
                A=sa[0]
                B=sa[1]
                c0=sa[2]
                sa1=ThreadStl_data.screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L01=float(sa1[7])
                sa1=ThreadStl_data.screws[key_2]
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
                c11=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c11.Placement=App.Placement(App.Vector(0,0,m-m1),App.Rotation(App.Vector(0,0,1),0))
                c21 = Part.makeCylinder(d02+0.001,L2,Base.Vector((p9)),Base.Vector(1,0,0))#枝管
                c21.Placement=App.Placement(App.Vector(-L2,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.cut(c21)
                c1=c1.cut(c11)
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L2,0,A),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),0))
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    
            elif st=='90RSL':
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                sa=ThreadStl_data.elbows_rsl[dia]
                A=sa[0]
                B=sa[1]
                xi=dia.find('x')
                key_1=dia[:xi]
                key_2=dia[xi+1:]
                sa1=ThreadStl_data.screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L01=float(sa1[7])
                sa1=ThreadStl_data.screws[key_2]
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
                c2 = Part.makeCylinder(d2,B-L02,Base.Vector((p10)),Base.Vector(1,0,0))#枝管
                c2.Placement=App.Placement(App.Vector(-B,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.fuse(c2)
                #内径
                edge1 = Part.makeLine(p5,p6)
                edge2 = Part.makeLine(p6,p7)
                edge3 = Part.makeCircle(d01, Base.Vector(p8), Base.Vector(0,1,0),270,0)
                edge4 = Part.makeLine(p11,p5)
                aWire = Part.Wire([edge1,edge2,edge3,edge4])
                pface = Part.Face(aWire)
                c11=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
                c11.Placement=App.Placement(App.Vector(0,0,m-m1),App.Rotation(App.Vector(0,0,1),0))
                c21 = Part.makeCylinder(d02,L2,Base.Vector((p9)),Base.Vector(1,0,0))#枝管
                c21.Placement=App.Placement(App.Vector(-L2,0,0),App.Rotation(App.Vector(1,0,0),0))
                c1=c1.cut(c21)
                c1=c1.cut(c11)
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L01),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread2(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(B+0.001,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),0))
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_01(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(B,0,A),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                   
        elif key=='02':
            key_1=dia
            sa1=ThreadStl_data.screws[key_1]
            A1=float(sa1[10])/2
            A2=float(sa1[11])/2
            L=float(sa1[7])
            LL=float(sa1[8])
            sa=ThreadStl_data.tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            D0=A1-t
            if st[:2]=='45':
                s0=22.5
                sa=ThreadStl_data.bends_d[key_1]
                La=sa[0]
                r=sa[1]
            elif st[:2]=='90':
                s0=45
                sa=ThreadStl_data.bends_d[key_1]
                La=sa[2]
                if dia=='50A' or dia=='10A':
                    r=float(sa[3])*0.9
                else:
                    r=sa[3]
            a=1.8*L
            b=a
            d0=A2-t
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),2*s0))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.cut(c2)
                #c1=c1.cut(c22)
                    return
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
                c4 = Part.makeCylinder(2*d0,LL,Base.Vector((p1)),Base.Vector(0,0,1))
                c4.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                c1=c1.cut(c4)
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread2(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.fuse(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c1=c1.cut(c2)
                    cutter_01(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p5),App.Rotation(App.Vector(0,1,0),180+2*s0))
                    c1=c1.fuse(c2)
                #c1=c1.cut(c23)
                    return
        elif key=='04':
            key_1=dia[:3]
            key_2=dia[-3:]
            sa1=ThreadStl_data.screws[key_1]
            A1=float(sa1[10])/2
            A2=float(sa1[11])/2
            L=float(sa1[7])
            LL=float(sa1[8])
            sa1=ThreadStl_data.screws[key_2]
            A10=float(sa1[10])/2
            A20=float(sa1[11])/2
            L0=float(sa1[7])
            LL0=float(sa1[8])
            sa=ThreadStl_data.tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            D0=A1-t
            sa=ThreadStl_data.tubes[key_2]
            d20=float(sa[0])/2
            t0=sa[3]
            D00=A10-t0
            if st=='45Y':
                s0=22.5
                sa=ThreadStl_data.Ys_d[key_1]
                A=sa[0]
                B=sa[1]
            elif st=='90Y':
                s0=45
                sa=ThreadStl_data.Ys_d[key_1]
                A=sa[2]
                B=sa[3]
            elif st=='90RY':
                s0=45
                sa=ThreadStl_data.RYs_d[dia]
                A=sa[0]
                B=sa[1]
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    if st=='45Y':
                        male_thread(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,0,A+B-L),App.Rotation(App.Vector(0,1,0),0))
                        c1=c1.cut(c2)
                    elif st=='90Y':
                        male_thread(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(p9),App.Rotation(App.Vector(0,1,0),315))
                        c1=c1.cut(c2)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p6),App.Rotation(App.Vector(0,1,0),45))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)#(1)
                    c2=c00
                    c1=c1.cut(c2)
                    if st=='45Y':
                        cutter_011(self)#(4)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(p3),App.Rotation(App.Vector(0,1,0),180))
                        c1=c1.cut(c2)
                    elif st=='90Y':
                        cutter_011(self)#(7)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                        c1=c1.cut(c2)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                    c1=c1.cut(c2)
                    c1=c1.cut(c21)
                    
            elif st=='90RY':
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
                c1 = Part.makeCylinder(A2,A,Base.Vector(p1),Base.Vector(0,0,1))
                c11 = Part.makeCylinder(d0,A,Base.Vector(p1),Base.Vector(0,0,1))
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,L),App.Rotation(App.Vector(0,1,0),180))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p9),App.Rotation(App.Vector(0,1,0),315))
                    c1=c1.cut(c2)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p6),App.Rotation(App.Vector(0,1,0),45))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)#(1)
                    c2=c00
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)#(7)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p7),App.Rotation(App.Vector(0,1,0),135))
                    c1=c1.cut(c2)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(p4),App.Rotation(App.Vector(0,1,0),-135))
                    c1=c1.cut(c2)
                c1=c1.cut(c21)
                c1=c1.cut(c22)
                    
        elif key=='03' or key=='05':
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='T' or st=='Cr':
                sa=ThreadStl_data.tees_e[key_1]
                A=sa[0]
                sa1=ThreadStl_data.screws[key_1]
                t=sa1[9]
                d1=float(sa1[10])/2
                L=float(sa1[7])
                d0=d1-t
                if st=='T':
                    x=0
                else:
                    x=A
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-A+L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c21=c00
                    c21.Placement=App.Placement(App.Vector(A-L,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c21)
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,A-L,0),App.Rotation(App.Vector(1,0,0),270))
                    if st=='Cr':
                        male_thread(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,-A+L,0),App.Rotation(App.Vector(1,0,0),90))
                        c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-A,0,0),App.Rotation(App.Vector(0,1,0),90))
                    cutter_011(self)
                    c21=c00
                    c21.Placement=App.Placement(App.Vector(A,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,A,0),App.Rotation(App.Vector(1,0,0),90))
                    if st=='Cr':
                        cutter_011(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,-A,0),App.Rotation(App.Vector(1,0,0),270))
                        c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    
            elif st=='RT'or st=='RCr':
                if st=='RT':
                    sa=ThreadStl_data.tees_d[dia]
                    A=sa[0]
                    B=sa[1]

                elif st=='RCr':
                    sa=ThreadStl_data.cross_d[dia]
                    A=sa[0]
                    B=sa[1]
                sa1=ThreadStl_data.screws[key_1]
                t1=sa1[9]
                d1=float(sa1[10])/2
                L1=float(sa1[7])
                d01=d1-t1
                sa1=ThreadStl_data.screws[key_2]
                t2=sa1[9]
                d2=float(sa1[10])/2
                L2=float(sa1[7])
                d02=d2-t2
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-A+L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c21=c00
                    c21.Placement=App.Placement(App.Vector(A-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c21)
                    key_1=key_2
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,B-L2,0),App.Rotation(App.Vector(1,0,0),270))
                    c1=c1.cut(c2)
                    if st=='RCr':
                        male_thread(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,-(B-L2),0),App.Rotation(App.Vector(1,0,0),90))
                        c1=c1.cut(c21)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-A,0,0),App.Rotation(App.Vector(0,1,0),90))
                    cutter_011(self)
                    c21=c00
                    c21.Placement=App.Placement(App.Vector(A,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,B,0),App.Rotation(App.Vector(1,0,0),90))
                    c1=c1.cut(c2)
                    if st=='RCr':
                        cutter_011(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,-B,0),App.Rotation(App.Vector(1,0,0),270))
                        c1=c1.cut(c21)
                    
        elif key=='06':
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='Nipple'or st=='Reducing_nipple':
                if st=='Nipple':
                    sa=ThreadStl_data.nipples[key_1]
                    L=sa[0]
                    E1=sa[1]
                    n=sa[2]
                    B=sa[3]
                    dk=sa[4]
                    sa1=ThreadStl_data.screws[key_1]
                    L1=sa1[8]
                    A1=float(sa1[11])/2
                    sa2=ThreadStl_data.tubes[key_1]
                    d1=float(sa2[0])/2
                    t1=sa2[3]
                    x1=E1-L1
                    d01=d1-t1
                    H=L-2*E1
                elif st=='Reducing_nipple':
                    sa=ThreadStl_data.nipples_d[dia]
                    L=sa[0]
                    E1=sa[1]
                    E2=sa[2]
                    H=L-(E1+E2)
                    sa=ThreadStl_data.nipples[key_1]
                    n=sa[2]
                    B=float(sa[3])/2
                    dk=float(sa[4])/2
                    sa1=ThreadStl_data.screws[key_1]
                    L1=sa1[8]
                    A1=float(sa1[11])/2
                    sa1=ThreadStl_data.screws[key_2]
                    L2=sa1[8]
                    A2=float(sa1[11])/2
                    sa2=ThreadStl_data.tubes[key_1]
                    d1=float(sa2[0])/2
                    t1=sa2[3]
                    x1=E1-L1
                    d01=d1-t1
                    sa2=ThreadStl_data.tubes[key_2]
                    d2=float(sa2[0])/2
                    t2=sa2[3]
                    x2=E2-L2
                    d02=d2-t2
                hexagon(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c11 = Part.makeCylinder(A1,x1,Base.Vector((-x1,0,0)),Base.Vector(1,0,0))
                c12 = Part.makeCylinder(d01,x1,Base.Vector((-x1,0,0)),Base.Vector(1,0,0))
                c11=c11.cut(c12)
                c1=c1.fuse(c11)
                if st=='Nipple':
                    E2=E1
                    A2=A1
                    d02=d01
                    x2=x1
                c11 = Part.makeCylinder(A2,x2,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c12 = Part.makeCylinder(d02,x2,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c11=c11.cut(c12)
                c1=c1.fuse(c11)
                #ナット部穴
                p1=(0,0,0)
                p2=(0,0,d01)
                p3=(H,0,d02)
                p4=(H,0,0)
                plist=[p1,p2,p3,p4,p1]
                pwire=Part.makePolygon(plist)
                pface = Part.Face(pwire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c1=c1.cut(c2)
                if Thread==True:
                    male_thread2(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-E1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    key_1=key_2
                    male_thread2(self)
                    c2=c00
                    if st=='Nipple':
                        E2=E1
                    c2.Placement=App.Placement(App.Vector(H+E2,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_01(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(-E1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    key_1=key_2
                    cutter_01(self)
                    c21=c00
                    if st=='Nipple':
                        E2=E1
                    c21.Placement=App.Placement(App.Vector(H+E2,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c2=c2.fuse(c21)
                    c1=c1.fuse(c21)
                    
            elif st=='Hose_nipple':
                sa1=ThreadStl_data.screws[key_1]
                LL1=sa1[8]
                A1=float(sa1[11])/2
                sa=ThreadStl_data.nipples_h[key_1]
                L=sa[0]
                E1=sa[1]
                E2=sa[2]
                d0=sa[3]/2
                d1=sa[4]/2
                D=sa[5]/2
                sa=ThreadStl_data.tubes[key_1]
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
                c2=c00
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
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c2.Placement=App.Placement(App.Vector(E1,0,0),App.Rotation(App.Vector(0,0,1),0))
                c1=c1.cut(c2)
                if Thread==True:
                    male_thread2(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c2)
                else:
                    cutter_01(self)
                    c21=c00
                    c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.fuse(c21)
                    
            elif st=='Piece_nipple' or st=='Both_nipple':
                sa=ThreadStl_data.screws[key_1]
                a=sa[6]
                f=sa[13]
                L1=a+f
                sa=ThreadStl_data.tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d0=d2-t
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                if st=='Piece_nipple':
                    c1 = Part.makeCylinder(d2,L-L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c20 = Part.makeCylinder(d0,L+L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    if Thread==True:
                        male_thread2(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c2)
                    else:
                        cutter_01a(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c21)
                    c1=c1.cut(c20)
                        
                elif st=='Both_nipple':
                    c1 = Part.makeCylinder(d2,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                    c20 = Part.makeCylinder(d0,L+2*L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    if Thread==True:
                        male_thread2(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c2)
                        male_thread2(self)
                        c2=c00
                        c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                        c1=c1.fuse(c2)
                    else:
                        cutter_01a(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                        c1=c1.fuse(c21)
                        cutter_01a(self)
                        c21=c00
                        c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                        c1=c1.fuse(c21)
                    c1=c1.cut(c20)
                       
        elif key=='07':
            global w10
            key_1=dia
            sa=ThreadStl_data.unions_d[key_1]
            b1=sa[0]
            d1=sa[2]/2
            n=sa[3]
            B1=sa[4]/2
            B2=sa[5]/2
            dk=sa[6]/2*2.0
            H=sa[7]
            L1=b1-H/2
            sa=ThreadStl_data.screws[key_1]
            l=sa[7]
            #ナット8角
            if n==8:
                s=float(math.radians(45))/2
                e0=B1/math.cos(s)
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
                    w10=Part.makePolygon(plist)
                    return
                plst8(self)
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
                    plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p1]
                    w10=Part.makePolygon(plist)
                    return
                plst10(self)
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
            wface=Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c1.cut(c2)
            if Thread==True:
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(l,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(b1*2-l,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                c2 = Part.makeCylinder(d1,b1*2-2*l,Base.Vector(l,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
            else:
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(b1*2,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                c2 = Part.makeCylinder(d1,b1*2-2*l,Base.Vector(l,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                
        elif key=='08':
            if st=='Socket_parrallel':
                key_1=dia
                sa=ThreadStl_data.screws[key_1]
                D0=sa[3]/2
                sa=ThreadStl_data.socket_p[key_1]
                D=sa[0]/2
                L=sa[1]
                c1 = Part.makeCylinder(D,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                if Thread==True:
                    male_thread3(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                else:
                   #c2 = Part.makeCylinder(D0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                   #c1=c1.cut(c2)
                   return
            elif st=='Socket_taper':
                key_1=dia
                sa=ThreadStl_data.screws[key_1]
                D0=sa[3]/2
                sa=ThreadStl_data.screws[key_1]
                L1=sa[7]
                sa=ThreadStl_data.tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d0=d2-t
                sa=ThreadStl_data.socket_p[key_1]
                D=sa[2]/2
                L=sa[3]
                c1 = Part.makeCylinder(D,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c2 = Part.makeCylinder(d0,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    
            elif st=='Socket_difference':
                key_1=dia[:3]
                key_2=dia[-3:]
                sa=ThreadStl_data.screws[key_1]
                L1=sa[7]
                sa=ThreadStl_data.screws[key_2]
                L2=sa[7]
                sa=ThreadStl_data.tubes[key_1]
                d2=sa[0]/2
                t=sa[3]
                d01=d2-t
                sa=ThreadStl_data.tubes[key_2]
                d2=sa[0]/2
                t=sa[3]
                d02=d2-t
                sa=ThreadStl_data.sockets_d[dia]
                La=sa[0]
                L12=L1*1.1
                L22=L2*1.1
                Lb=La-(L12+L22)
                sa=ThreadStl_data.socket_p[key_1]
                D1=sa[0]/2
                sa=ThreadStl_data.socket_p[key_2]
                D2=sa[0]/2
                edge1 = Part.makeCircle(D1, Base.Vector(0,0,0), Base.Vector(1,0,0), 0, 360)
                edge2 = Part.makeCircle(D1, Base.Vector(L12,0,0), Base.Vector(1,0,0), 0, 360)
                edge3 = Part.makeCircle(D2, Base.Vector(L12+Lb,0,0), Base.Vector(1,0,0), 0, 360)
                edge4 = Part.makeCircle(D2, Base.Vector(La,0,0), Base.Vector(1,0,0), 0, 360)
                edge5 = Part.makeCircle(d01, Base.Vector(L1,0,0), Base.Vector(1,0,0), 0, 360)
                edge6 = Part.makeCircle(d02, Base.Vector(La-L2,0,0), Base.Vector(1,0,0), 0, 360)
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
                if Thread==True:
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    key_1=key_2
                    male_thread(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(La-L2,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                else:
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.cut(c2)
                    key_1=key_2
                    cutter_011(self)
                    c2=c00
                    c2.Placement=App.Placement(App.Vector(La,0,0),App.Rotation(App.Vector(0,1,0),270))
                    c1=c1.cut(c2)
                    
        if key=='09' :
            key_1=dia
            sa=ThreadStl_data.tubes[key_1]
            t=float(sa[3])
            sa=ThreadStl_data.caps_d[key_1]
            d2=float(sa[0])/2
            H=float(sa[1])-t
            sa=ThreadStl_data.screws[key_1]
            l=sa[7]
            d0=d2-t
            D=2*d0
            R0=D
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
            if Thread==True:
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,l,0),App.Rotation(App.Vector(1,0,0),90))
                c1=c1.cut(c2)
            else:
                #cutter_011(self)
                #c2=c00
                #c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),270))
                #c1=c1.cut(c2)
                return
        if key=='10' :
            key_1=dia
            sa=ThreadStl_data.screws[key_1]
            l=sa[8]
            sa=ThreadStl_data.tubes[key_1]
            d2=float(sa[0])/2
            t=sa[3]
            d0=d2-t
            sa=ThreadStl_data.plugs_d[key_1]
            L=float(sa[0])
            B=float(sa[1])
            b=float(sa[2])
            c1=Part.makeBox(b,B,B,Base.Vector((0,-B/2,-B/2)),Base.Vector(0,0,1))
            c3 = Part.makeCylinder(B,b,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c4 = Part.makeCylinder(1.3*B/2,b,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c3=c3.cut(c4)
            c1=c1.cut(c3)
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),45))
            if Thread==True:
                male_thread2(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(l+b,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
            else:
                cutter_01(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(l+b,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                
            if float(key_1[:2])>=25:
                c2 = Part.makeCylinder(0.8*B/2,1.3*b,Base.Vector(0.3*b,0,0),Base.Vector(1,0,0))
                c3 = Part.makeCylinder(0.8*d0,L-1.3*b,Base.Vector(1.3*b,0,0),Base.Vector(1,0,0))
                c2=c2.fuse(c3)
                c1=c1.cut(c2)
        elif key=='11':
            key_1=dia[:3]
            key_2=dia[-3:]
            sa=ThreadStl_data.bushs_d[dia]
            L=sa[0]
            E=sa[1]
            n=sa[2]
            B=sa[3]
            H=L-E
            sa=ThreadStl_data.nipples[key_1]
            dk=float(sa[4])/2
            sa1=ThreadStl_data.screws[key_1]
            L1=sa1[8]
            A1=float(sa1[11])/2
            sa1=ThreadStl_data.screws[key_2]
            L2=sa1[7]
            A2=float(sa1[11])/2
            sa2=ThreadStl_data.tubes[key_1]
            d1=float(sa2[0])/2
            t1=sa2[3]
            x1=E-L1
            d01=d1-t1
            sa2=ThreadStl_data.tubes[key_2]
            d2=float(sa2[0])/2
            t2=sa2[3]
            x2=E-L2
            d02=d2-t2
            hexagon(self)
            c1=c00
            c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            if E-L1>0:
                c2 = Part.makeCylinder(A1,E-L1,Base.Vector(H,0,0),Base.Vector(1,0,0))
                c1=c1.fuse(c2)
            if Thread==True:
                male_thread2(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(E+H,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                key_1=key_2
                male_thread2(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L2,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
            else:
                cutter_01(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(E+H,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                key_1=key_2
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
            c2 = Part.makeCylinder(d01,L-L2,Base.Vector(L2,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
                
        elif key=='12':
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='JIS5k':
                sa=ThreadStl_data.globes_5k[key_1]
            elif st=='JIS10k':
                sa=ThreadStl_data.globes_10k[key_1]
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
            sa=ThreadStl_data.screws[key_1]
            L1=float(sa[7])
            A1=float(sa[10])/2
            x1=L/2-1.1*L1
            s=math.asin(x1/d1)
            y1=d1-s1
            d10=0.9*2*s2+2*1.0*a
            d11=0.9*2*s2
            H=0.7*L1
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
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
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
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #スポーク
            for i in range(3):
                c2 = Part.makeCylinder(0.5*d3,D1-2*d3,Base.Vector(d3,0,y1+0.7*d3),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                c1=c1.fuse(c2)
            #ナット
            key_2=d41
            sa = ThreadStl_data.regular[key_2]
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
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1,H)
            c2=c2.cut(c3)
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-hm),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            if Thread==True:
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
            else:
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                
        elif key=='13':
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='JIS5k':
                sa=ThreadStl_data.gates_5k[key_1]
            elif st=='JIS10k':
                sa=ThreadStl_data.gates_10k[key_1]
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
            sa=ThreadStl_data.screws[key_1]
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
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p1]
            w10=Part.makePolygon(plist)
            wface = Part.Face(w10)
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
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
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
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
            c2=wface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            #スポーク
            for i in range(3):
                c2 = Part.makeCylinder(0.5*d3,D1-2*d3,Base.Vector(d3,0,y1+0.7*d3),Base.Vector(1,0,0))
                c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                c1=c1.fuse(c2)
            #ナット
            key_2=d41
            sa = ThreadStl_data.regular[key_2]
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
            H=m
            c2=wface.extrude(Base.Vector(0,0,H))
            c3=Part.makeCylinder(D1,H)
            c2=c2.cut(c3)
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-hm),App.Rotation(App.Vector(1,0,0),0))
            c1=c1.fuse(c2)
            if Thread==True:
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
            else:
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                
        elif key=='14':
            key_1=dia[:3]
            key_2=dia[-3:]
            sa=ThreadStl_data.checks_10k[key_1]
            d=float(sa[0])/2
            L=float(sa[1])
            H0=float(sa[2])
            a=float(sa[3])
            d1=float(sa[4])
            s1=float(sa[5])/2
            s2=float(sa[6])/2
            sa=ThreadStl_data.screws[key_1]
            L1=float(sa[7])
            A1=float(sa[10])/2
            t=float(sa[9])
            d0=A1-t
            x1=L/2-1.1*L1
            s=math.asin(x1/d1)
            y1=2*A1
            d10=2*s2+2*a
            d11=2*s2
            H=0.7*L1
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
            pface=Part.Face(aWire)
            c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c2.Placement=App.Placement(App.Vector(L/2,0,0),App.Rotation(App.Vector(1,0,0),0))
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
            if Thread==True:
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L1,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                #key_1=key_2
                male_thread(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
            else:
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.cut(c2)
                cutter_011(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.cut(c2)
                
        elif key=='15':
            key_1=dia[:3]
            sa=ThreadStl_data.screws[key_1]
            p=sa[0]
            h=sa[1]
            r=sa[2]
            D0=sa[3]
            d1=sa[5]
            a=sa[6]
            l=sa[7]
            A2=sa[11]/2
            f=sa[13]
            L1=a+f
            sa=ThreadStl_data.tubes[key_1]
            A20=sa[0]/2
            d2=sa[0]/2
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
            L=App.ActiveDocument.getObject(label).L
            L=float(L) 
            d0=d2-t
            c1 = Part.makeCylinder(d2,L-2*L1,Base.Vector(0,0,0),Base.Vector(1,0,0))
            #Part.show(c1)
            c20 = Part.makeCylinder(d0,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
            #Part.show(c20)
            if Thread==True:
                male_thread2(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
                male_thread2(self)
                c2=c00
                c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
                c1=c1.fuse(c2)
                c2 = Part.makeCylinder(d0,L+L1,Base.Vector(-L1/2,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c2)
            else:
                c1 = Part.makeCylinder(d2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                c1=c1.cut(c20)  
                
        obj.Shape=c1        




