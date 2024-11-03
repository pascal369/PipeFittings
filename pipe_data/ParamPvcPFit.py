from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import PvcPFit

class pvc_p:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        k_index=App.ActiveDocument.getObject(label).k_index
        key=App.ActiveDocument.getObject(label).key
        st=App.ActiveDocument.getObject(label).st
        dia=App.ActiveDocument.getObject(label).dia
        
        def Flange10(self):
            global c01
            C0=0
            if st[-2:]=='5k':
                print(st[:-2])
                sa = PvcPFit.JIS5k_2[dia]
            elif st[-3:]=='10k' :
                sa = PvcPFit.JIS10k_2[dia]
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

        if key[:2]=='00' or key[:2]=='01':
            if k_index==0:#直管
                L=App.ActiveDocument.getObject(label).L
                sa=PvcPFit.strt_dia[dia]
                D=sa[0]
                if st[:3]=='VP ' or st[:3]=='VU ' or st[:3]=='VPW':
                    if st[:3]=='VP ' :
                        t=float(sa[1])
                    elif st[:3]=='VU ' :
                        t=float(sa[3])
                    elif st[:3]=='VPW' :
                        t=float(sa[5])
                    d=D-2*t
                if st[4:8]=='Both':
                    c1=Part.makeCylinder(D/2,L-2*t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                    c2=Part.makeCylinder(d/2,L-2*t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2)
                    Flange10(self)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),-90))
                    c1=c1.fuse(c2)
                elif st[4:10]=='Single' :
                    c1=Part.makeCylinder(D/2,L-t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                    c2=Part.makeCylinder(d/2,L-t,Base.Vector(t,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2)
                    Flange10(self)
                    c2=c01
                    c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                    c1=c1.fuse(c2)
                else:
                    c1=Part.makeCylinder(D/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    c2=Part.makeCylinder(d/2,L,Base.Vector(0,0,0),Base.Vector(1,0,0))
                    c1=c1.cut(c2) 
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        Gui.runCommand('Draft_Move',0)                
        obj.Shape=c1