import FreeCADGui as Gui
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App

from . import WeldStl_data
class welded_p:
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
        #print(st)
        dia=App.ActiveDocument.getObject(label).dia
        #print(dia)
        key_1=App.ActiveDocument.getObject(label).dia
        def flange(self):#00
            global c00
            global k00
            if material=='Carbon steel':
                C0=0
                if st=='JIS2k' or st[-5:]=='JIS2k':
                    sa = WeldStl_data.JIS2k[key_1]
                elif st=='JIS5k':
                        sa = WeldStl_data.JIS5k[key_1]
                elif st=='JIS7.5k' or st[-7:]=='JIS7.5k':
                        sa = WeldStl_data.JIS75k[key_1]
                elif st=='JIS10k' or st[-6:]=='JIS10k':
                        sa = WeldStl_data.JIS10k[key_1]

                elif st=='JIS16k' or st[-6:]=='JIS16k':
                        sa = WeldStl_data.JIS16k[key_1]
                elif st=='JIS20k' or st[-6:]=='JIS20k':
                        sa = WeldStl_data.JIS20k[key_1]        

                elif st=='JIS10k_Loose' or st[-12:]=='JIS10k_Loose':
                        sa = WeldStl_data.JIS10k[key_1]

            elif material=='Stainless steel':
                C0=0
                if st=='JIS5k' or st[-5:]=='JIS5k':
                    sa = WeldStl_data.JIS5k[key_1]
                elif st=='JIS7.5k' or st[-7:]=='JIS7.5k':
                    sa = WeldStl_data.JIS75k[key_1]
                elif st=='JIS10k' or st[-6:]=='JIS10k':
                    sa = WeldStl_data.JIS10k[key_1]
                elif st=='JIS10k_Loose' or st[-12:]=='JIS10k_Loose':
                    sa = WeldStl_data.JIS5k[key_1]
                    C0=sa[11]
                    sa = WeldStl_data.JIS10k[key_1]
                elif st=='JIS5k_Loose' or st[-11:]=='JIS5k_Loose':
                    sa = WeldStl_data.JIS5k[key_1]
                    C0=sa[11]
            if key=='11' or key=='12' or key=='14' or key=='15' or  key=='16':
                if key=='11' or key=='12' or  key=='14' or key=='15':
                    sa = WeldStl_data.JIS10k[key_1]
                elif  key=='16':
                    sa = WeldStl_data.JIS75k[key_1]    

            d0=sa[0]
            d2=sa[1]
            d4=sa[2]
            d5=sa[3]
            k0=sa[4]
            k00=k0
            E0=sa[5]
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
            c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
            c01=Part.makeCylinder(d2/2,k0)
            c00=c00.cut(c01)
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
                   c00=c00.cut(c3)
               else:
                   c00=c00.cut(c3)
        def flange2(self):
           global c00
           #key_1=self.comboBox_dia.currentText()
           #print(st)
           if material=='Carbon steel':
               if st=='JIS7.5k' or st[-7:]=='JIS7.5k':
                   sa = WeldStl_data.JIS75k[key_1]
               elif st=='JIS10k' or st[-6:]=='JIS10k':
                   sa = WeldStl_data.JIS10k[key_1]
           elif material=='Stainless steel':
               if st=='JIS7.5k' or st[-7:]=='JIS7.5k':
                   sa = WeldStl_data.JIS75k[key_1]
               elif st=='JIS10k' or st[-6:]=='JIS10k':
                   sa = WeldStl_data.JIS5k[key_1]
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
           c00=pface.revolve(Base.Vector(0,0,0),Base.Vector(0,0,1),360)
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
                   c00=c00.cut(c3)
               else:
                   c00=c00.cut(c3)

        def straight_p(self):#05
            global c00

            sa = WeldStl_data.str_tube[key_1]
            if st[:3]=='SGP':
                t=float(sa[1])
            if st[:5]=='Sch20':
                t=float(sa[2])
            if st[:5]=='Sch40':
                t=float(sa[3])
            if st[:5]=='Sch80':
                t=float(sa[5])
            if st[:6]=='Sch10S':
                t=float(sa[7])
            if st[:6]=='Sch20S':
                t=float(sa[8])
            d2=float(sa[0])/2
            d0=d2-t
           
            L=App.ActiveDocument.getObject(label).L
            try:
                L=float(L)
            except:
                return    

            if key=='05':
                Lx = L
            elif key=='06':
                Lx = L-int(t)
            elif key=='07':
                Lx = L-int(2*t)    

            c1 = Part.makeCylinder(d2,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c2 = Part.makeCylinder(d0,Lx,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c00=c1.cut(c2)

        if key=='00':#フランジ
            flange(self)
            c1=c00
            #obj.Shape=c1
        elif key=='01':    
            sa = WeldStl_data.elbo[key_1]
            sa1 = WeldStl_data.str_tube[key_1]
            #print(st[-3:])
            d2=float(sa[0])/2
            if st[4:8]=='Long' or st[4:9]=='Large':
                r=float(sa[1])
            if st[4:9]=='Short':
                r=float(sa[2])
            if st[-3:]=='SGP':
                #print(st[-3:])
                t=sa1[1]
            if st[-5:]=='Sch40':
                t=float(sa1[3])
            if st[-5:]=='Sch80':
                t=float(sa1[5])
            if st[-6:]=='Sch10S':
                t=float(sa1[6])
            if st[-6:]=='Sch20S':
                t=float(sa1[7])
            if st[:3]=='045':
                s=22.5
            if st[:3]=='090':
                s=45
            if st[:3]=='180':
                s=90
            d0=d2-t
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
            #obj.Shape=c1

        elif key=='02':
            sa = WeldStl_data.tees[key_1]
            d1=float(sa[0])/2
            d2=float(sa[1])/2
            C=float(sa[2])
            M=float(sa[3])
            key_2=dia[:3]
            key_3=dia[4:7]
            sa1=WeldStl_data.str_tube[key_2]
            sa2=WeldStl_data.str_tube[key_3]
            if st=='SGP' or st=='Large':
                t1=float(sa1[1])
                t2=float(sa2[1])
            elif st=='Sch40':
                t1=float(sa1[3])
                t2=float(sa2[3])
            elif st=='Sch80':
                t1=float(sa1[5])
                t2=float(sa2[5])
            elif st=='Sch10S':
                t1=float(sa1[7])
                t2=float(sa2[7])
            elif st=='Sch20S':
                t1=float(sa1[8])
                t2=float(sa2[8])
            d01=d1-t1
            d02=d2-t2
            c1 = Part.makeCylinder(d1,2*C,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01 = Part.makeCylinder(d01,2*C,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c2 = Part.makeCylinder(d2,M,Base.Vector(C,0,0),Base.Vector(0,1,0))
            c02 = Part.makeCylinder(d02,M,Base.Vector(C,0,0),Base.Vector(0,1,0))
            c1=c1.fuse(c2)
            c1=c1.cut(c01)
            c1=c1.cut(c02)  
            #obj.Shape=c1  
        elif key=='03':
            sa = WeldStl_data.reducs[key_1]
            d1=float(sa[0])/2
            d2=float(sa[1])/2
            H=float(sa[2])
            key_2=dia[:3]
            key_3=dia[4:7]
            sa1=WeldStl_data.str_tube[key_2]
            sa2=WeldStl_data.str_tube[key_3]
            if st=='SGP' or st=='Large':
                t1=float(sa1[1])
                t2=float(sa2[1])
            elif st=='Sch40':
                t1=float(sa1[3])
                t2=float(sa2[3])
            elif st=='Sch80':
                t1=float(sa1[5])
                t2=float(sa2[5])
            elif st=='Sch10S':
                t1=float(sa1[7])
                t2=float(sa2[7])
            elif st=='Sch20S':
                t1=float(sa1[8])
                t2=float(sa2[8])
            d01=d1-t1#大径
            d02=d2-t2#小径
            x=0.1*H
            p1=(0,d02,0)
            p2=(0,d2,0)
            p3=(x,d2,0)
            p4=(H-x,d1,0)
            p5=(H,d1,0)
            p6=(H,d01,0)
            p7=(H-x,d01,0)
            p8=(x,d02,0)
            plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
            pwire=Part.makePolygon(plist)
            pface = Part.Face(pwire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
        elif key=='04':
            sa = WeldStl_data.reducs[key_1]
            d1=float(sa[0])/2
            d2=float(sa[1])/2
            H=float(sa[2])
            key_2=dia[:3]
            key_3=dia[4:7]
            sa1=WeldStl_data.str_tube[key_2]
            sa2=WeldStl_data.str_tube[key_3]
            if st=='SGP' or st=='Large':
                t1=float(sa1[4])
                t2=float(sa2[5])
            elif st=='Sch40':
                t1=float(sa1[6])
                t2=float(sa2[7])
            elif st=='Sch80':
                t1=float(sa1[8])
                t2=float(sa2[9])
            elif st=='Sch10S':
                t1=float(sa1[7])
                t2=float(sa2[7])
            elif st=='Sch20S':
                t1=float(sa1[8])
                t2=float(sa2[8])
            d01=d1-t1#大径
            d02=d2-t2#小径
            p1=(0,0,0)
            p2=(0.1*H,0,0)
            p3=(0.9*H,0,d1-d2)
            p4=(H,0,d1-d2)
            line_1=Part.makeLine(p1,p2)
            line_2=Part.makeLine(p2,p3)
            line_3=Part.makeLine(p3,p4)
            edge2 = Part.makeCircle(d2, Base.Vector(0,0,0), Base.Vector(1,0,0),0, 360)
            edge3 = Part.makeCircle(d2, Base.Vector(.1*H,0,0), Base.Vector(1,0,0),0, 360)
            edge4 = Part.makeCircle(d1, Base.Vector(0.9*H,0,d1-d2), Base.Vector(1,0,0),0, 360)
            edge5 = Part.makeCircle(d1, Base.Vector(H,0,d1-d2), Base.Vector(1,0,0),0, 360)
            edge02 = Part.makeCircle(d02, Base.Vector(0,0,0), Base.Vector(1,0,0),0, 360)
            edge03 = Part.makeCircle(d02, Base.Vector(.1*H,0,0), Base.Vector(1,0,0),0, 360)
            edge04 = Part.makeCircle(d01, Base.Vector(0.9*H,0,d1-d2), Base.Vector(1,0,0),0, 360)
            edge05 = Part.makeCircle(d01, Base.Vector(H,0,d1-d2), Base.Vector(1,0,0),0, 360)
            Solid=True
            ruled=False
            closed=False
            maxDegree=5
            profile1=Part.Wire(edge2)
            profile2=Part.Wire(edge3)
            profile3=Part.Wire(edge4)
            profile4=Part.Wire(edge5)
            profile01=Part.Wire(edge02)
            profile02=Part.Wire(edge03)
            profile03=Part.Wire(edge04)
            profile04=Part.Wire(edge05)
            c1= Part.makeLoft([profile1,profile2,profile3,profile4],Solid,ruled,closed,maxDegree)
            c01= Part.makeLoft([profile01,profile02,profile03,profile04],Solid,ruled,closed,maxDegree)
            c1= c1.cut(c01)
        elif key=='05':#直管
            straight_p(self)
            try:
                c1=c00
            except:
                return    

            obj.Shape=c1
        elif key=='06' or key=='07':#1F短管
            sa = WeldStl_data.str_tube[key_1]
            #print(sa)
            #print(st)
            if st=='SGP':
                t=float(sa[1])
            if st=='Sch20':
                t=float(sa[2])
            if st=='Sch40':
                t=float(sa[3])
            if st=='Sch80':
                t=float(sa[5])
            if st=='Sch10S':
                t=float(sa[7])
            if st=='Sch20S':
                t=float(sa[8])
            if key=='06':
                st=App.ActiveDocument.getObject(label).standard2
                flange(self)
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                st=App.ActiveDocument.getObject(label).standard
                straight_p(self)
                c2=c00
                #print(t)
                c2.Placement=App.Placement(App.Vector((t),0,0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2)
                
            elif key=='07':
                st=App.ActiveDocument.getObject(label).standard2
                flange(self)
                #k0=sa[4]
                c1=c00
                c1.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
                st=App.ActiveDocument.getObject(label).standard
                straight_p(self)
                a=int(t)
                #print(a)
                c2=c00
                c2.Placement=App.Placement(App.Vector(a,0,0),App.Rotation(App.Vector(0,1,0),0))
                c1=c1.fuse(c2)
                st=App.ActiveDocument.getObject(label).standard2
                flange(self)
                c2=c00
                L=App.ActiveDocument.getObject(label).L
                L=float(L)
                #k0=sa[4]
                c2.Placement=App.Placement(App.Vector(L-k00,0,0),App.Rotation(App.Vector(0,1,0),90))
                #c2.Placement=App.Placement(App.Vector(L-k0,0,0),App.Rotation(App.Vector(0,1,0),90))
                c1=c1.fuse(c2)
                
        elif key=='08':
            sa=WeldStl_data.str_tube[key_1]
            if st=='SGP':
                t=float(sa[1])
            elif st=='Sch20':
                t=float(sa[2])
            elif st=='Sch40':
                t=float(sa[3])
            elif st=='Sch80':
                t=float(sa[5])
            elif st=='Sch10S':
                t=float(sa[7])
            elif st=='Sch20S':
                t=float(sa[8])
            d2=float(sa[0])/2
            H=float(sa[10])
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
        elif key=='09':
            if material=='Carbon steel':
                if st=='JIS2k':
                    sa = WeldStl_data.JIS2k[key_1]
                elif st=='JIS5k' :
                    sa = WeldStl_data.JIS5k[key_1]
                elif st=='JIS7.5k':
                    sa = WeldStl_data.JIS75k[key_1]
                elif st=='JIS10k':
                    sa = WeldStl_data.JIS10k[key_1]
                elif st=='JIS16k':
                    sa =WeldStl_data. JIS16k[key_1]
                elif st=='JIS20k':
                    sa =WeldStl_data. JIS20k[key_1]    
                elif st=='JIS10k_Loose':
                    sa = WeldStl_data.JIS10k[key_1]
            elif material=='Stainless steel':
                if st=='JIS5k' :
                    sa = WeldStl_data.JIS5k[key_1]
                elif st=='JIS7.5k':
                    sa = WeldStl_data.JIS75k[key_1]
                elif st=='JIS10k':
                    sa = WeldStl_data.JIS5k[key_1]
            d4=float(sa[2])/2
            d5=float(sa[3])/2
            t=float(sa[4])
            E0=float(sa[5])/2
            n0=sa[6]
            c1 = Part.makeCylinder(d5,t,Base.Vector(0,0,0),Base.Vector(0,0,1))
            ks=0
            for i in range(n0):
                k=2*math.pi/n0
                r=d4
                if i==0:
                    x=r*math.cos(k/2)
                    y=r*math.sin(k/2)
                else:
                    ks=i*k+k/2
                    x=r*math.cos(ks)
                    y=r*math.sin(ks)
                c3 = Part.makeCylinder(E0,t,Base.Vector(x,y,0),Base.Vector(0,0,1))
                if i==0:
                    c1=c1.cut(c3)
                else:
                    c1=c1.cut(c3)

        elif key=='10':
            sa=WeldStl_data.raps[key_1]
            d3=float(sa[0])/2
            T=sa[1]
            F=sa[4]
            R=sa[5]
            if st=='JIS5k':
                G=float(sa[2])/2
            elif st=='JIS10k':
                G=float(sa[3])/2
            d0=d3-T
            p1=(0,d0,0)
            p2=(0,G,0)
            p3=(T,G,0)
            p4=(T,d3+R,0)
            p5=(T+R,d3+R,0)
            p6=(T+R,d3,0)
            p7=(F,d3,0)
            p8=(F,d0,0)
            edge1=Part.makeLine(p1,p2)
            edge2=Part.makeLine(p2,p3)
            edge3=Part.makeLine(p3,p4)
            edge4=Part.makeCircle(R, Base.Vector(T+R,d3+R,0), Base.Vector(0,0,1),180, 270)
            edge5=Part.makeLine(p6,p7)
            edge6=Part.makeLine(p7,p8)
            edge7=Part.makeLine(p8,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,])
            pface = Part.Face(aWire)
            c1=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
        elif key=='11' or key=='12' :
            
            sa=WeldStl_data.JIS10k[key_1]
            d2=float(sa[1])
            M=float(sa[4])
            #print(M)
            
            if material=='Carbon steel':
                sa1=WeldStl_data.gates_10k_cast[key_1]
            elif material=='Stainless steel':
                sa1=WeldStl_data.gates_10k_SUS[key_1]
            L=sa1[0]
            H1=sa1[1]
            H2=sa1[2]
            w=sa1[3]
            a1=sa1[4]
            flange(self)
            c01=c00
            flange(self)
            c02=c00
            c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c02.Placement=App.Placement(App.Vector(L-M,0,0),App.Rotation(App.Vector(0,1,0),90))
            c01=c01.fuse(c02)

            H=H1
            x2=0.4
            L1=L
            d21=d2+2*a1
            if key_1<='100':
                x3=0.25
            elif key_1<='200':
                x3=0.35
            else:
                x3=0.35
            w0=x2*L
            h0=d21+20
            LL=(L1-w0)/2
            p1=(0,d21/2,0)
            p2=(10,h0/2,0)
            p3=(10,d21/2,0)
            p4=(w0-10,h0/2,0)
            p5=(w0,d21/2,0)
            p6=(w0,-d21/2,0)
            p7=(w0,-d21/2,0)
            p8=(w0-10,-h0/2,0)
            p9=(w0-10,-d21/2,0)
            p10=(10,-h0/2,0)
            p11=(0,-d21/2,0)
            p12=(10,0,0)
            p13=(w0,0,0)
            p14=(0,0,0)
            edge1 = Part.makeCircle(10, Base.Vector(10,d21/2,0), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p4)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,d21/2,0), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p5,p7)
            edge5 = Part.makeCircle(10, Base.Vector(w0-10,-d21/2,0), Base.Vector(0,0,1), 270, 360)
            edge6 = Part.makeLine(p8,p10)
            edge7 = Part.makeCircle(10, Base.Vector(10,-d21/2,0), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p11,p1)
            aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface = Part.Face(aWire)
            wface.Placement=App.Placement(App.Vector(LL,0,0),App.Rotation(App.Vector(1,0,0),0))
            wface_k=wface
            c02=wface.extrude(Base.Vector(0,0,x3*H+2*0.7*M+3))#角柱下
            c01=c01.fuse(c02)
            edge1 = Part.makeCircle(10, Base.Vector(10,-d21/2,0), Base.Vector(0,0,1), 180, 270)
            edge2 = Part.makeLine(p10,p8)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,-d21/2,0), Base.Vector(0,0,1), 270, 360)
            edge4 = Part.makeLine(p11,p7)
            edge5 = Part.makeLine(p13,p7)
            edge6 = Part.makeLine(p13,p4)
            edge7 = Part.makeLine(p11,p14)
            edge8 = Part.makeLine(p13,p14)
            aWire1=Part.Wire([edge1,edge2,edge3,edge5,edge7,edge8])
            aWire11=Part.Wire([edge1,edge2,edge3,edge5,edge7,edge8])
            wface1 = Part.Face(aWire1)
            wface1.Placement=App.Placement(App.Vector(LL,0,0),App.Rotation(App.Vector(1,0,0),0))
            c03=wface1.revolve(Base.Vector(0,0.0,0.0),Base.Vector(1,0,0),180)
            c01=c01.fuse(c03)
            #フランジ
            zz=40
            x=(w0+zz)/2
            y=(h0+zz)/2
            p1=(0,d21/2,0)
            p2=(zz-10,y,0)
            p3=(2*x-zz+10,y,0)
            p4=(2*x,d21/2,0)
            p5=(2*x,-d21/2,0)
            p6=(2*x-zz+10,-y,0)
            p7=(zz-10,-y,0)
            p8=(0,-d21/2,0)
            p9=(zz-10,d21/2,0)
            p10=(2*x-zz+10,d21/2,0)
            p11=(zz-10,-d21/2,0)
            p12=(2*x-zz+10,-d21/2,0)
            edge1 = Part.makeCircle(zz-10, Base.Vector(p9), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeCircle(zz-10, Base.Vector(p10), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p4,p5)
            edge5 = Part.makeCircle(zz-10, Base.Vector(p12), Base.Vector(0,0,1), 270, 360)
            edge6 = Part.makeLine(p6,p7)
            edge7 = Part.makeCircle(zz-10, Base.Vector(p11), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p8,p1)
            aWire2=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface2 = Part.Face(aWire2)
            wface2.Placement=App.Placement(App.Vector(LL-zz/2,0,x3*H),App.Rotation(App.Vector(0,0,1),0))
            c04=wface2.extrude(Base.Vector(0,0,0.7*M))#フランジ下
            c01=c01.fuse(c04)
            aWire3=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface3 = Part.Face(aWire3)
            wface3.Placement=App.Placement(App.Vector(LL-zz/2,0,x3*H+0.7*M+3),App.Rotation(App.Vector(0,0,1),0))
            c05=wface3.extrude(Base.Vector(0,0,0.7*M))#フランジ上
            c01=c01.fuse(c05)
            wface4 = Part.Face(aWire11)
            wface4.Placement=App.Placement(App.Vector(LL,0,x3*H+2*0.7*M+3),App.Rotation(App.Vector(0,0,1),0))
            c06=wface4.revolve(Base.Vector(0,0,x3*H+2*0.7*M+3),Base.Vector(1,0,0),-180)
            c01=c01.fuse(c06)
            L0=h0-40
            if key_1<='075':
                L0=1.0*L0
                z1=x3*H+2*0.7*M+3+h0/2+10
            elif key_1<='200':
                L0=0.9*L0
                z1=x3*H+2*0.7*M+3+h0/2+10
            elif key_1<='250':
                L0=0.8*L0
                z1=x3*H+2*0.7*M+3+h0/2+20
            elif key_1<='300':
                L0=0.7*L0
                z1=x3*H+2*0.7*M+3+h0/2+50
            elif key_1<='500':
                L0=0.7*L0
                z1=x3*H+2*0.75*M+3+h0/2+60
            else:
                L0=0.5*L0
                z1=x3*H+2*0.7*M+3+h0/2+60
            w0=w0-0.1
            w1=w0-20
            h1=L0-20
            p1=(0,h1/2,0)
            p2=(10,L0/2,0)
            p3=(w0-10,L0/2,0)
            p4=(w0,h1/2,0)
            p5=(w0,-h1/2,0)
            p6=(w0-10,-L0/2,0)
            p7=(10,-L0/2,0)
            p8=(0,-h1/2,0)
            p9=(10,h1/2,0)
            p10=(w0-10,h1/2,0)
            p11=(w0-10,-h1/2,0)
            p12=(10,-h1/2,0)
            edge1 = Part.makeCircle(10, Base.Vector(10,h1/2,0), Base.Vector(0,0,1), 90, 180)
            edge2 = Part.makeLine(p2,p3)
            edge3 = Part.makeCircle(10, Base.Vector(w0-10,h1/2,0), Base.Vector(0,0,1), 0, 90)
            edge4 = Part.makeLine(p4,p5)
            edge5 = Part.makeCircle(10, Base.Vector(w0-10,-h1/2,0), Base.Vector(0,0,1), 270, 0)
            edge6 = Part.makeLine(p6,p7)
            edge7 = Part.makeCircle(10, Base.Vector(10,-h1/2,0), Base.Vector(0,0,1), 180, 270)
            edge8 = Part.makeLine(p8,p1)
            aWire5=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
            wface5 = Part.Face(aWire5)
            wface5.Placement=App.Placement(App.Vector((L1-w0)/2,0,0),App.Rotation(App.Vector(0,0,1),0))
            if key=='11':
                c07=wface5.extrude(Base.Vector(0,0,z1))#z1角柱
            elif key=='12':
                c07=wface5.extrude(Base.Vector(0,0,z1))#z1角柱
            c01=c01.fuse(c07)
            wface6 = Part.Face(aWire5)
            wface6.Placement=App.Placement(App.Vector((L1-w0)/2,0,z1+1),App.Rotation(App.Vector(0,0,1),0))
            if key=='11':
                c08=wface6.extrude(Base.Vector(0,0,0.7*M))
            elif key=='12':
                wface_k.Placement=App.Placement(App.Vector((L1-w0)/2,0,z1+1),App.Rotation(App.Vector(0,0,1),0))
                c08=wface6.extrude(Base.Vector(0,0,0.7*M))
            c01=c01.fuse(c08)
            c13= Part.makeCylinder(d21/2,L-2*M,Base.Vector(M,0,0),Base.Vector(1,0,0))
            c01=c01.fuse(c13)
            c14= Part.makeCylinder(d2/2,L-2*M,Base.Vector(M,0,0),Base.Vector(1,0,0))
            c01=c01.cut(c14)
            if key=='11':
                if key_1<='100':
                    Lb=20
                    B=20
                    C=16
                elif key_1<='150':
                    Lb=35
                    B=20
                    C=16
                elif key_1<='200':
                    Lb=40
                    B=25
                    C=20
                elif key_1<='250':
                    Lb=42
                    B=35
                    C=24
                elif key_1<='300':
                    Lb=45
                    B=35
                    C=24
                elif key_1<='400':
                    Lb=70
                    B=35
                    C=24
                elif key_1<='500':
                    Lb=100
                    B=35
                    C=24
                H=H1
                H0=H
                z10=x3*H+2*2*0.7*M+3
                c10= Part.makeCylinder(1.2*B/2,H-z10-30,Base.Vector(L1/2,0,z10),Base.Vector(0,0,1))
                c01=c01.fuse(c10)
                c12= Part.makeCylinder(C/2,35+C,Base.Vector(L1/2,0,H-30),Base.Vector(0,0,1))
                c01=c01.fuse(c12)
                #ハンドル
                boss= Part.makeCylinder(2*B/2,30,Base.Vector(L1/2,0,H-30),Base.Vector(0,0,1))
                boss_1= Part.makeCylinder(C/2,30,Base.Vector(L1/2,0,H-30),Base.Vector(0,0,1))
                boss=boss.cut(boss_1)
                torus=Part.makeTorus(w/2,10,Base.Vector(L1/2,0,H-15))
                c01=c01.fuse(torus)
                c01=c01.fuse(boss)
                #スポーク
                for i in range(3):
                    c2 = Part.makeCylinder(7.5,(w-10)/2,Base.Vector(10/2,0,H0-15),Base.Vector(1,0,0))
                    c2.Placement=App.Placement(App.Vector(L1/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                    c01=c01.fuse(c2)
                #ナット
                key_2='M'+str(C)
                sa = WeldStl_data.regular[key_2]
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
                c2.Placement=App.Placement(App.Vector(L1/2,0,H0),App.Rotation(App.Vector(1,0,0),0))
                c1=c01.fuse(c2)

            elif key=='12':
                H=H2
                w=sa1[3]
                if key_1<='100':
                    Lb1=40
                    Lb2=40
                    B1=20
                    C=10
                elif key_1<='200':
                    Lb1=40
                    Lb2=50
                    B1=30
                    C=15
                elif key_1<='250':
                    Lb1=40
                    Lb2=50
                    B1=40
                    C=15
                elif key_1<='300':
                    Lb1=50
                    Lb2=50
                    B1=40
                    C=15
                elif key_1<='500':
                    Lb1=50
                    Lb2=50
                    B1=40
                    C=15
                R=10
                t1=5
                z1=z1+1+0.7*M
                z2=z1+t1
                z3=H-d2*2
                z4=z3-Lb1
                z5=z4-(1+Lb2)
                Lb3=z5-z1
                #シャフト
                cc1= Part.makeCylinder(C,(H-z1),Base.Vector(L1/2,0,z1),Base.Vector(0,0,1))
                cc2= Part.makeCylinder(B1,Lb1,Base.Vector(L1/2,0,z4+2*R),Base.Vector(0,0,1))
                cc3= Part.makeCylinder(B1,Lb2,Base.Vector(L1/2,0,z5+2*R),Base.Vector(0,0,1))
                cc1=cc1.fuse(cc2)
                cc1=cc1.fuse(cc3)
                c01=c01.fuse(cc1)
                #サポート
                h0=0.8*h0
                if key_1<='200':
                    y3=z5+2*R+Lb2/2-z1+2*M
                else:
                    y3=z5+2*R+Lb2/2-z1+1.5*M
                y4=z1+M
                y5=y4+y3
                p1=(0,-h0/2+R,y4)
                p2=(0,-h0/2,y4+R)
                p3=(0,-h0/2,y5-R)
                p4=(0,-h0/2+R,y5)
                p5=(0,h0/2-R,y5)
                p6=(0,h0/2,y5-R)
                p7=(0,h0/2,y4+R)
                p8=(0,h0/2-R,y4)
                p9=(0,-h0/2+R,y5-R)
                p10=(0,-h0/2+R,y4+R)
                p11=(0,h0/2-R,y5-R)
                p12=(0,h0/2-R,y4+R)
                edge1 = Part.makeCircle(10, Base.Vector(p10), Base.Vector(1,0,0), 180, 270)
                edge2 = Part.makeLine(p2,p3)
                edge3 = Part.makeCircle(10, Base.Vector(p9), Base.Vector(1,0,0), 90, 180)
                edge4 = Part.makeLine(p4,p5)
                edge5 = Part.makeCircle(10, Base.Vector(p11), Base.Vector(1,0,0), 0, 90)
                edge6 = Part.makeLine(p6,p7)
                edge7 = Part.makeCircle(10, Base.Vector(p12), Base.Vector(1,0,0), 270, 360)
                edge8 = Part.makeLine(p8,p1)
                aWire=Part.Wire([edge1,edge2,edge3,edge4,edge5,edge6,edge7,edge8])
                #プロファイル
                t=3.0
                p1=(-0.8*B1,-h0/2,z1+M+R)
                p2=(-0.8*B1,-h0/2-t,z1+M+R)
                p3=(-t/2,-h0/2-t,z1+M+R)
                p4=(-t/2,-h0/2-B1,z1+M+R)
                p5=(t/2,-h0/2-B1,z1+M+R)
                p6=(t/2,-h0/2-t,z1+M+R)
                p7=(0.8*B1,-h0/2-t,z1+M+R)
                p8=(0.8*B1,-h0/2,z1+M+R)
                plist=[p1,p2,p3,p4,p5,p6,p7,p8,p1]
                w10=Part.makePolygon(plist)
                makeSolid=True
                isFrenet=True
                cb3 = Part.Wire(aWire).makePipeShell([w10],makeSolid,isFrenet)#サポート
                cb3.Placement=App.Placement(App.Vector(L1/2,0,-3.5*M),App.Rotation(App.Vector(1,0,0),0))
                c01=c01.fuse(cb3)
                #ハンドル
                torus=Part.makeTorus(w/2,12.5,Base.Vector(L1/2,0,z4+Lb1))
                c01=c01.fuse(cc1)
                c01=c01.fuse(torus)
                #スポーク
                for i in range(3):
                    c2 = Part.makeCylinder(7.5,(w-10)/2,Base.Vector(10/2,0,z4+Lb1),Base.Vector(1,0,0))
                    c2.Placement=App.Placement(App.Vector(L1/2,0,0),App.Rotation(App.Vector(0,0,1),i*120))
                    c01=c01.fuse(c2)
                c1=c01
        elif key=='13':
            key_1=dia[:3]
            key_2=dia[-3:]
            if st=='JIS7.5k':
                sa=WeldStl_data.checks_75k_cast[key_1]
            elif st=='JIS10k':
                sa=WeldStl_data.checks_10k_cast[key_1]
            d=sa[0]/2
            L=float(sa[1])
            H0=float(sa[2])
            a=float(sa[3])
            d1=float(sa[4])
            R=float(sa[5])
            #self.label_l.setText(QtGui.QApplication.translate("Dialog", str(d), None))
            if st=='JIS10k':
                sa=WeldStl_data.JIS10k[key_1]
            elif st=='JIS7.5k':    
                sa=WeldStl_data.JIS75k[key_1]

            L1=float(sa[4])
            d2=float(sa[1])/2
            D1=float(sa[3])/2
            x2=L/2-2*L1
            s=math.acos(x2/(R+a))
            a1=a*math.sin(s)

            flange(self)
            c01=c00
            c01.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,1,0),90))
            flange(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(L-L1,0,0),App.Rotation(App.Vector(0,1,0),90))
            c01=c01.fuse(c2)

            flange(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-2*L1),App.Rotation(App.Vector(0,0,1),0))
            c01=c01.fuse(c2)

            if key_1>='150':
                ma=1.00
            else:
                ma=0.85

            p1=(L1,0,-d2)
            p2=(0,0,-D1)
            p3=(L1,0,-D1)
            p4=(L1,0,-(d2+a))
            p5=(2*L1,0,-(d2+a))
            p6=(L/2,0,-ma*D1)
            p7=(L-2*L1,0,-(d2+a))
            p8=(L-L1,0,-(d2+a))
            p9=(L-L1,0,-D1)
            p10=(L,0,-D1)
            p11=(L-L1,0,-d2)
            p12=(L-(2*L1+a1),0,-d2)
            p13=(L/2,0,-ma*D1+a)
            p14=(2*L1+a1,0,-d2)
            p15=(L-L1,0,0)
            p16=(L1,0,0)
            edge1 = Part.makeLine(p16,p4)
            edge4 = Part.makeLine(p4,p5)
            edge5=Part.Arc(Base.Vector(p5),Base.Vector(p6),Base.Vector(p7)).toShape()
            edge6 = Part.makeLine(p7,p8)
            edge7 = Part.makeLine(p8,p15)
            edge10 = Part.makeLine(p15,p16)
            edge11 = Part.makeLine(p16,p1)
            edge12 = Part.makeLine(p1,p14)
            edge13=Part.Arc(Base.Vector(p14),Base.Vector(p13),Base.Vector(p12)).toShape()
            edge14 = Part.makeLine(p12,p11)
            edge15 = Part.makeLine(p11,p15)
            #本体
            aWire=Part.Wire([edge1,edge4,edge5,edge6,edge7,edge10])
            aWire2=Part.Wire([edge11,edge12,edge13,edge14,edge15,edge10])
            pface=Part.Face(aWire)
            pface2=Part.Face(aWire2)
            c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c01=c01.fuse(c2)
            c3 = Part.makeCylinder(d2+2*a,H0-2*L1,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c4 = Part.makeCylinder(d2+1*a,2*H0,Base.Vector(L/2,0,0),Base.Vector(0,0,1))
            c01=c01.fuse(c3)
            c01=c01.cut(c4)
            c20=pface2.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c01=c01.cut(c20)

            #弁体仕切り
            wface=Part.makePlane(6*d2,a,Base.Vector(3*L1,-3*d2,-3*d2),Base.Vector(0,1,0))
            c2=wface.extrude(Base.Vector(0,6*d2,0))
            #Part.show(c2)
            #流路
            c22 = Part.makeCylinder(d,L/2,Base.Vector(3*L1,0,0),Base.Vector(1,0,0))
            c2=c2.cut(c22)
            if key_1>='25A':
                c2.Placement=App.Placement(App.Vector(a,0,-1.5*a),App.Rotation(App.Vector(0,1,0),-8))
            else:
                c2.Placement=App.Placement(App.Vector(a,0,-0.8*a),App.Rotation(App.Vector(0,1,0),-8))
            c3=c2.common(c20)
            c01=c01.fuse(c3)
            #弁体
            c2 = Part.makeCylinder(1.1*d,a,Base.Vector(3*L1+a,0,0),Base.Vector(1,0,0))
            if key_1>='25A':
                c2.Placement=App.Placement(App.Vector(a,0,-1.5*a),App.Rotation(App.Vector(0,1,0),-8))
            else:
                c2.Placement=App.Placement(App.Vector(a,0,-0.8*a),App.Rotation(App.Vector(0,1,0),-8))
            c01=c01.fuse(c2)

            flange2(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(L/2,0,H0-1*L1+1),App.Rotation(App.Vector(0,0,1),0))
            c1=c01.fuse(c2)

        elif key=='14' or key=='16':
            if st=='20mm':
                sa=WeldStl_data.exp_20mm[key_1]
                n=int(1)
            elif st=='50mm':
                sa=WeldStl_data.exp_50mm[key_1]
                n=int(2)
            elif st=='100mm':
                sa=WeldStl_data.exp_100mm[key_1]
                n=int(3)
            elif st=='200mm':
                sa=WeldStl_data.exp_200mm[key_1]
                n=int(4)
            d0=float(key_1)
            d1=float(sa[0])
            d2=float(sa[1])
            c=float(sa[4])
            f=float(sa[5])
            R=float(sa[6])
            l=float(sa[2])
            l1=float(sa[3])
            c01 = Part.makeCylinder(d1/2,l-2*c,Base.Vector(c,0,0),Base.Vector(1,0,0))
            c2 = Part.makeCylinder(d2/2,c,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01=c01.fuse(c2)
            c2= Part.makeCylinder(d2/2,c,Base.Vector(l-c,0,0),Base.Vector(1,0,0))
            c01=c01.fuse(c2)

            flange(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(c,0,0),App.Rotation(App.Vector(0,1,0),90))
            c01=c01.fuse(c2)
            flange(self)
            c2=c00
            if key=='14':
                sa = WeldStl_data.JIS10k[key_1]
            elif key=='16':
                sa = WeldStl_data.JIS75k[key_1]    

            k0=sa[4]
            c2.Placement=App.Placement(App.Vector(c+l1-k0,0,0),App.Rotation(App.Vector(0,1,0),90))

            c01=c01.fuse(c2)
            c2 = Part.makeCylinder(d0/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01=c01.cut(c2)
            #c1=c01
            
            for i in range(n):
                p1=(0,f,0)
                p2=(R,f+R,0)
                p3=(2*R,f,0)
                edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
                edge2 = Part.makeLine(p1,p3)
                aWire=Part.Wire([edge1,edge2])
                pface=Part.Face(aWire)
                c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
                c2.Placement=App.Placement(App.Vector((i+1)*l/(n+1)-R,0,0),App.Rotation(App.Vector(1,0,0),0))
                c01=c01.fuse(c2)
                #c1=c01.fuse(c2)
            c1=c01
        if key=='15':
            sa=WeldStl_data.exp_50mm[key_1]
            d0=float(key_1)
            d1=float(sa[0])
            d2=float(sa[1])
            c=3.0
            f=float(sa[5])
            R=float(sa[8])
            l=float(sa[7])
            l1=l-2*c

            t=14.0
            c01 = Part.makeCylinder(d1/2,l-2*c,Base.Vector(c,0,0),Base.Vector(1,0,0))
            c2 = Part.makeCylinder(d2/2,c,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01=c01.fuse(c2)
            c2= Part.makeCylinder(d2/2,c,Base.Vector(l-c,0,0),Base.Vector(1,0,0))
            c01=c01.fuse(c2)

            flange(self)
            c2=c00
            c2.Placement=App.Placement(App.Vector(c,0,0),App.Rotation(App.Vector(0,1,0),90))
            c01=c01.fuse(c2)
            flange(self)
            c2=c00
            sa = WeldStl_data.JIS10k[key_1]
            k0=sa[4]
            c2.Placement=App.Placement(App.Vector(c+l1-k0,0,0),App.Rotation(App.Vector(0,1,0),90))
            c01=c01.fuse(c2)
            c2 = Part.makeCylinder(d0/2,l,Base.Vector(0,0,0),Base.Vector(1,0,0))
            c01=c01.cut(c2)

            p1=(c+t,d1/2,0)
            p2=(l/2,1.2*d1/2,0)
            p3=(l-(c+t),d1/2,0)
            edge1=Part.Arc(Base.Vector(p1),Base.Vector(p2),Base.Vector(p3)).toShape()
            edge2 = Part.makeLine(p1,p3)
            aWire=Part.Wire([edge1,edge2])
            pface=Part.Face(aWire)
            c2=pface.revolve(Base.Vector(0,0,0),Base.Vector(1,0,0),360)
            c1=c01.fuse(c2)
        doc=App.ActiveDocument
        #Gui.Selection.addSelection(doc.Name,obj.Name)
        #Gui.runCommand('Draft_Move',0)  
        try:     
            obj.Shape=c1
        except:
            pass
