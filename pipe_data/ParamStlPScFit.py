from FreeCAD import Base
import FreeCADGui as Gui   
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import StlPScFit

class StraightPipe:
    def __init__(self, obj):
        self.Type = ''
        obj.Proxy = self
        App.activeDocument().recompute(None,True,True)
    def execute(self, obj):
        label=obj.Name
        key=App.ActiveDocument.getObject(label).key
        t=App.ActiveDocument.getObject(label).t
        d1=App.ActiveDocument.getObject(label).d1
        d2=App.ActiveDocument.getObject(label).d2
        a=App.ActiveDocument.getObject(label).a
        f=App.ActiveDocument.getObject(label).f
        L=App.ActiveDocument.getObject(label).L
        l=App.ActiveDocument.getObject(label).l
        D0=App.ActiveDocument.getObject(label).D0/2
        p=App.ActiveDocument.getObject(label).p
        h=App.ActiveDocument.getObject(label).h
        r=App.ActiveDocument.getObject(label).r
        A20=App.ActiveDocument.getObject(label).A20/2
        A2=App.ActiveDocument.getObject(label).A2/2
        IsChecked=App.ActiveDocument.getObject(label).IsChecked
        def Thread(self):#おねじ　ねじあり カッター用
            global c00
            global c10
            s=math.atan(0.5/16)
            d10=d1-a*math.tan(s)
            d20=d10+l*math.tan(s)
            p1=Base.Vector(0,0,0)
            p2=Base.Vector(d10/2,0,0)
            p3=Base.Vector(d20/2,0,L1)
            p4=Base.Vector(0,0,L1)
            plist=[p1,p2,p3,p4,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c10=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            cb1= Part.makeCylinder(d10/2,p,Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c10=c10.fuse(cb1)
            #ねじ断面
            c0=0
            x0=d10/2+(h-r)
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
            helix=Part.makeHelix(p,l,d10,s0,False)
            #Part.show(helix)
            cutProfile = Part.Wire([edge1,edge2,edge3,edge4])
            cutProfile.Placement=App.Placement(App.Vector(-x0,0,p/2),App.Rotation(App.Vector(0,1,0),s0))
            wface=Part.Face(cutProfile)
            #Part.show(wface)
            makeSolid=True
            isFrenet=True
            pipe = Part.Wire(helix).makePipeShell([cutProfile],makeSolid,isFrenet)
            #pipe.Placement=App.Placement(App.Vector(0,0,p),App.Rotation(App.Vector(1,0,0),0))
            #Part.show(pipe)
            c10=c10.fuse(pipe)
        def cutter_01A(self): #おねじ　ねじなし 管用
            global c00
            global c10
            global pipe
            l=a+f
            s=math.atan(0.5/16)
            d10=D0-a*math.tan(s)
            d20=d10+l*math.tan(s)
            d0=A20-t
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

        d0=D0-t
        L1=a+f
        c1 = Part.makeCylinder(D0,L-2*L1,Base.Vector(L1,0,0),Base.Vector(1,0,0))
        c2 = Part.makeCylinder(d0,L,Base.Vector(L1,0,0),Base.Vector(1,0,0))
        c1=c1.cut(c2)
        if IsChecked==True:
            #return
            Thread(self)
            c2=c10
            c2.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c2)
            c2 = Part.makeCylinder(D0+10, L1, Base.Vector(-L1,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
            #Part.show(c2)
            Thread(self)
            c2=c10
            c2.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
            c1=c1.fuse(c2)
            c2 = Part.makeCylinder(d0,L+L1,Base.Vector(-L1/2,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
            c2 = Part.makeCylinder(D0+10, L1, Base.Vector(L,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2)
            

        else:
            cutter_01A(self)
            c21=c10
            c21.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c1=c1.fuse(c21)
            cutter_01A(self)
            c21=c10
            c21.Placement=App.Placement(App.Vector(L,0,0),App.Rotation(App.Vector(0,1,0),270))
            c1=c1.fuse(c21)  
            c2 = Part.makeCylinder(d0,L+L1,Base.Vector(-L1/2,0,0),Base.Vector(1,0,0))
            c1=c1.cut(c2) 
        doc=App.ActiveDocument
        Gui.Selection.addSelection(doc.Name,obj.Name)
        Gui.runCommand('Draft_Move',0)   
        obj.Shape=c1   