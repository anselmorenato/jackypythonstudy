# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takeshi Ishikawa

import os, sys
import wx
from wx import glcanvas
import math
# from OpenGL.GLUT import *
from OpenGL.GLU  import *
from OpenGL.GL   import *
import iCppExtention

#-------------------------------------------------------------------------------

class myGLCanvas(glcanvas.GLCanvas):

  center_point_rotate=iCppExtention.Dvector3D()
  center_point_view=iCppExtention.Dvector3D()

  eye_fovy=60
  eye_znear=0.1
  eye_zfar=300.0

  mouse_left=0
  mouse_right=0
  mouse_start_x=0.0
  mouse_start_y=0.0
  mouse_scale_angle=0.5
  mouse_scale_dist=0.03

  default_atom_view_color=[]
  default_atom_view_radius=[]

  def __init__(self, parent):
    # glutInit("") # glut function
    glcanvas.GLCanvas.__init__(self, parent, -1)
    # initialize
    self.center_point_rotate.set_x(0.0)
    self.center_point_rotate.set_y(0.0)
    self.center_point_rotate.set_z(0.0)
    self.center_point_view.set_x(0.0)
    self.center_point_view.set_y(0.0)
    self.center_point_view.set_z(0.0)
    self.SetDefault()

    ########################################
    #090304 ishikura added these variables #
    ########################################
    self.molecule    = iCppExtention.Molecule()
    self.eye         = iCppExtention.Eye()
    self.enable_draw = True
    #090304 end of variables added         #
    ########################################

    # envet define
    self.Bind(wx.EVT_PAINT,self.OnPaint)
    self.Bind(wx.EVT_IDLE,self.OnIdle)
    self.Bind(wx.EVT_SIZE,self.OnSize)
    self.Bind(wx.EVT_MOTION,self.OnMotion)
    self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)
    self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    self.Bind(wx.EVT_RIGHT_UP,self.OnRightUp)
    self.Bind(wx.EVT_CHAR,self.OnChar)
    #090326 ishikura added
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBG)
    return

  def SetDefault(self):
    
    w_radius = 0.6/0.5291

    self.default_atom_view_color=[ [  1.00 ,  1.00 ,  1.00 ] #  Dmmy
                                 , [  1.00 ,  1.00 ,  1.00 ] #     H
                                 , [  0.85 ,  1.00 ,  1.00 ] #    He
                                 , [  0.80 ,  0.50 ,  1.00 ] #    Li
                                 , [  0.76 ,  1.00 ,  0.00 ] #    Be
                                 , [  1.00 ,  0.71 ,  0.71 ] #     B
                                 , [  0.56 ,  0.56 ,  0.56 ] #     C
                                 , [  0.19 ,  0.31 ,  0.97 ] #     N
                                 , [  1.00 ,  0.05 ,  0.05 ] #     O
                                 , [  0.56 ,  0.88 ,  0.31 ] #     F
                                 , [  0.70 ,  0.89 ,  0.96 ] #    Ne
                                 , [  0.67 ,  0.36 ,  0.95 ] #    Na
                                 , [  0.54 ,  1.00 ,  0.00 ] #    Mg
                                 , [  0.75 ,  0.65 ,  0.65 ] #    Al
                                 , [  0.94 ,  0.78 ,  0.63 ] #    Si
                                 , [  1.00 ,  0.50 ,  0.00 ] #     P
                                 , [  1.00 ,  1.00 ,  0.19 ] #     S
                                 , [  0.12 ,  0.94 ,  0.12 ] #    Cl
                                 , [  0.50 ,  0.82 ,  0.89 ] #    Ar
                                 , [  0.56 ,  0.25 ,  0.83 ] #     K
                                 , [  0.24 ,  1.00 ,  0.00 ] #    Ca
                                 , [  0.90 ,  0.90 ,  0.90 ] #    Sc
                                 , [  0.75 ,  0.76 ,  0.78 ] #    Ti
                                 , [  0.65 ,  0.65 ,  0.67 ] #     V
                                 , [  0.54 ,  0.60 ,  0.78 ] #    Cr
                                 , [  0.61 ,  0.48 ,  0.78 ] #    Mn
                                 , [  0.88 ,  0.40 ,  0.20 ] #    Fe
                                 , [  0.94 ,  0.56 ,  0.63 ] #    Co
                                 , [  0.31 ,  0.82 ,  0.31 ] #    Ni
                                 , [  0.78 ,  0.50 ,  0.20 ] #    Cu
                                 , [  0.49 ,  0.50 ,  0.69 ] #    Zn
                                 , [  0.76 ,  0.56 ,  0.56 ] #    Ga
                                 , [  0.40 ,  0.56 ,  0.56 ] #    Ge
                                 , [  0.74 ,  0.50 ,  0.89 ] #    As
                                 , [  1.00 ,  0.63 ,  0.00 ] #    Se
                                 , [  0.65 ,  0.16 ,  0.16 ] #    Br
                                 , [  0.36 ,  0.72 ,  0.82 ] #    Kr
                                 , [  0.44 ,  0.18 ,  0.69 ] #    Rb
                                 , [  0.00 ,  1.00 ,  0.00 ] #    Sr
                                 , [  0.58 ,  1.00 ,  1.00 ] #     Y
                                 , [  0.58 ,  0.88 ,  0.88 ] #    Zr
                                 , [  0.45 ,  0.76 ,  0.79 ] #    Nb
                                 , [  0.33 ,  0.71 ,  0.71 ] #    Mo
                                 , [  0.23 ,  0.62 ,  0.62 ] #    Tc
                                 , [  0.14 ,  0.56 ,  0.56 ] #    Ru
                                 , [  0.04 ,  0.49 ,  0.55 ] #    Rh
                                 , [  0.00 ,  0.41 ,  0.52 ] #    Pd
                                 , [  0.75 ,  0.75 ,  0.75 ] #    Ag
                                 , [  1.00 ,  0.85 ,  0.56 ] #    Cd
                                 , [  0.65 ,  0.46 ,  0.45 ] #    In
                                 , [  0.40 ,  0.50 ,  0.50 ] #    Sn
                                 , [  0.62 ,  0.39 ,  0.71 ] #    Sb
                                 , [  0.83 ,  0.48 ,  0.00 ] #    Te
                                 , [  0.58 ,  0.00 ,  0.58 ] #     I
                                 , [  0.26 ,  0.62 ,  0.69 ] #    Xe
                                 , [  0.34 ,  0.09 ,  0.56 ] #    Cs
                                 , [  0.00 ,  0.79 ,  0.00 ] #    Ba
                                 , [  0.44 ,  0.83 ,  1.00 ] #    La
                                 , [  1.00 ,  1.00 ,  0.78 ] #    Ce
                                 , [  0.85 ,  1.00 ,  0.78 ] #    Pr
                                 , [  0.78 ,  1.00 ,  0.78 ] #    Nd
                                 , [  0.64 ,  1.00 ,  0.78 ] #    Pm
                                 , [  0.56 ,  1.00 ,  0.78 ] #    Sm
                                 , [  0.38 ,  1.00 ,  0.78 ] #    Eu
                                 , [  0.27 ,  1.00 ,  0.78 ] #    Gd
                                 , [  0.19 ,  1.00 ,  0.78 ] #    Tb
                                 , [  0.12 ,  1.00 ,  0.78 ] #    Dy
                                 , [  0.00 ,  1.00 ,  0.61 ] #    Ho
                                 , [  0.00 ,  0.90 ,  0.46 ] #    Er
                                 , [  0.00 ,  0.83 ,  0.32 ] #    Tm
                                 , [  0.00 ,  0.75 ,  0.22 ] #    Yb
                                 , [  0.00 ,  0.67 ,  0.14 ] #    Lu
                                 , [  0.30 ,  0.76 ,  1.00 ] #    Hf
                                 , [  0.30 ,  0.65 ,  1.00 ] #    Ta
                                 , [  0.13 ,  0.58 ,  0.84 ] #     W
                                 , [  0.15 ,  0.49 ,  0.67 ] #    Re
                                 , [  0.15 ,  0.40 ,  0.59 ] #    Os
                                 , [  0.09 ,  0.33 ,  0.53 ] #    Ir
                                 , [  0.82 ,  0.82 ,  0.88 ] #    Pt
                                 , [  1.00 ,  0.82 ,  0.14 ] #    Au
                                 , [  0.72 ,  0.72 ,  0.82 ] #    Hg
                                 , [  0.65 ,  0.33 ,  0.30 ] #    Tl
                                 , [  0.34 ,  0.35 ,  0.38 ] #    Pb
                                 , [  0.62 ,  0.31 ,  0.71 ] #    Bi
                                 , [  0.67 ,  0.36 ,  0.00 ] #    Po
                                 , [  0.46 ,  0.31 ,  0.27 ] #    At
                                 , [  0.26 ,  0.51 ,  0.59 ] #    Rn
                                 , [  0.26 ,  0.00 ,  0.40 ] #    Fr
                                 , [  0.00 ,  0.49 ,  0.00 ] #    Ra
                                 , [  0.44 ,  0.67 ,  0.98 ] #    Ac
                                 , [  0.00 ,  0.73 ,  1.00 ] #    Th
                                 , [  0.00 ,  0.63 ,  1.00 ] #    Pa
                                 , [  0.00 ,  0.56 ,  1.00 ] #     U
                                 , [  0.00 ,  0.50 ,  1.00 ] #    Np
                                 , [  0.00 ,  0.42 ,  1.00 ] #    Pu
                                 , [  0.33 ,  0.36 ,  0.95 ] #    Am
                                 , [  0.47 ,  0.36 ,  0.89 ] #    Cm
                                 , [  0.54 ,  0.31 ,  0.89 ] #    Bk
                                 , [  0.63 ,  0.21 ,  0.83 ] #    Cf
                                 , [  0.70 ,  0.12 ,  0.83 ] #    Es
                                 , [  0.70 ,  0.12 ,  0.73 ] #    Fm
                                 , [  0.70 ,  0.05 ,  0.65 ] #    Md
                                 , [  0.74 ,  0.05 ,  0.53 ] #    No
                                 , [  0.78 ,  0.00 ,  0.40 ] #    Lr
                                 , [  0.80 ,  0.00 ,  0.35 ] #    Rf
                                 , [  0.82 ,  0.00 ,  0.31 ] #    Db
                                 , [  0.85 ,  0.00 ,  0.27 ] #    Sg
                                 , [  0.88 ,  0.00 ,  0.22 ] #    Bh
                                 , [  0.90 ,  0.00 ,  0.18 ] #    Hs
                                 , [  0.92 ,  0.00 ,  0.15 ] #    Mt
                                 ]
    default_atom_view_radius=[ 1.0000 * w_radius  #    Xx
                             , 0.3500 * w_radius  #     H
                             , 0.3500 * w_radius  #    He
                             , 1.2300 * w_radius  #    Li
                             , 0.8870 * w_radius  #    Be
                             , 0.8220 * w_radius  #     B
                             , 0.7720 * w_radius  #     C
                             , 0.7500 * w_radius  #     N
                             , 0.7300 * w_radius  #     O
                             , 0.7200 * w_radius  #     F
                             , 0.7100 * w_radius  #    Ne
                             , 1.5390 * w_radius  #    Na
                             , 1.3730 * w_radius  #    Mg
                             , 1.1800 * w_radius  #    Al
                             , 1.1690 * w_radius  #    Si
                             , 1.1070 * w_radius  #     P
                             , 1.0490 * w_radius  #     S
                             , 0.9940 * w_radius  #    Cl
                             , 0.9800 * w_radius  #    Ar
                             , 1.9620 * w_radius  #     K
                             , 1.7400 * w_radius  #    Ca
                             , 1.4400 * w_radius  #    Sc
                             , 1.3200 * w_radius  #    Ti
                             , 1.2200 * w_radius  #     V
                             , 1.1800 * w_radius  #    Cr
                             , 1.1700 * w_radius  #    Mn
                             , 1.1700 * w_radius  #    Fe
                             , 1.1600 * w_radius  #    Co
                             , 1.1500 * w_radius  #    Ni
                             , 1.1700 * w_radius  #    Cu
                             , 1.2500 * w_radius  #    Zn
                             , 1.2560 * w_radius  #    Ga
                             , 1.2230 * w_radius  #    Ge
                             , 1.1940 * w_radius  #    As
                             , 1.1670 * w_radius  #    Se
                             , 1.1420 * w_radius  #    Br
                             , 1.8900 * w_radius  #    Kr
                             ]

  def OnSize(self,event):
    self.size = self.GetClientSize()
    s=self.size
    if self.GetContext():
      self.SetCurrent()
      glViewport(0,0,s.width,s.height)
    event.Skip()

  def OnIdle(self, event):
    self.Refresh(False)
    return

  def OnMotion(self,event):
    if self.mouse_left==1:
      pos=event.GetPosition()
      angx=-1.0*(pos.x-self.mouse_start_x)*self.mouse_scale_angle*3.141592/180.0
      angy=-1.0*(pos.y-self.mouse_start_y)*self.mouse_scale_angle*3.141592/180.0
      self.RotateEye('y',angx)
      self.RotateEye('x',angy)
      self.mouse_start_x=pos.x
      self.mouse_start_y=pos.y
      return
    if self.mouse_right==1:
      pos=event.GetPosition()
      angz=-1.0*(pos.x-self.mouse_start_x)*self.mouse_scale_angle*3.141592/180.0
      dist=-1.0*(pos.y-self.mouse_start_y)*self.mouse_scale_dist
      self.MoveEye(1,'z',dist)
      self.mouse_start_x=pos.x
      self.mouse_start_y=pos.y
      return

  def OnLeftDown(self,event):
    self.mouse_left=1
    pos=event.GetPosition()
    self.mouse_start_x=pos.x
    self.mouse_start_y=pos.y

  def OnLeftUp(self,event):
    self.mouse_left=0

  def OnRightDown(self,event):
    self.mouse_right=1
    pos=event.GetPosition()
    self.mouse_start_x=pos.x
    self.mouse_start_y=pos.y

  def OnRightUp(self,event):
    self.mouse_right=0

  def OnChar(self,event):
    c=event.GetKeyCode()
    if   c==ord('a'):
         return
    elif c==ord('b'):
         self.MoveEye(1,'z',-0.5)
         return
    elif c==ord('c'):
         return
    elif c==ord('d'):
         return
    elif c==ord('e'):
         return
    elif c==ord('f'):
         self.MoveEye(1,'z',0.5)
         event.Skip()
    elif c==ord('g'):
         return
    elif c==ord('h'):
         return
    elif c==ord('i'):
         return
    elif c==ord('j'):
         return
    elif c==ord('k'):
         return
    elif c==ord('l'):
         return
    elif c==ord('m'):
         return
    elif c==ord('n'):
         return
    elif c==ord('o'):
         return
    elif c==ord('p'):
         return
    elif c==ord('q'):
         return
    elif c==ord('r'):
         return
    elif c==ord('s'):
         return
    elif c==ord('t'):
         return
    elif c==ord('u'):
         return
    elif c==ord('v'):
         return
    elif c==ord('w'):
         return
    elif c==ord('x'):
         self.RotateEye('x',(5.0*3.141592/180.0))
         return
    elif c==ord('y'):
         self.RotateEye('y',(5.0*3.141592/180.0))
         return
    elif c==ord('z'):
         return

  def OnPaint(self, event):
    self.SetCurrent()
    self.Draw()
    return

  def SetDefaultPointView(self):
    self.center_point_view.copy(iCppExtention.Dvector3D(self.molecule.get_center_of_mass()))
    return

  def SetDefaultPointRotate(self):
    self.center_point_rotate.copy(iCppExtention.Dvector3D(self.molecule.get_center_of_mass()))
    return

  def SetAtomDefault(self):
    natom=self.molecule.get_natom()
    va=iCppExtention.ViewAtom()
    for i in range(natom):
      atomic=self.molecule.get_atom(i).get_atomic_number()
      va.set_color_R(self.default_atom_view_color[atomic][0])
      va.set_color_G(self.default_atom_view_color[atomic][1])
      va.set_color_B(self.default_atom_view_color[atomic][2])
      iCppExtention.py_Molecule_ViewAtom_copy(self.molecule,va,i)

  def SetBondDefault(self):
    nbond=self.molecule.get_nbond()
    vb=iCppExtention.ViewBond()
    for i in range(nbond):
      a1=self.molecule.get_bond(i).get_iatom1()
      a2=self.molecule.get_bond(i).get_iatom2()
      atomic1=self.molecule.get_atom(a1).get_atomic_number()
      atomic2=self.molecule.get_atom(a2).get_atomic_number()
      vb.view_on()
      vb.set_dist_ratio_1(self.molecule.get_atom(a1).get_bond_distance())
      vb.set_dist_ratio_2(self.molecule.get_atom(a2).get_bond_distance())
      vb.set_color_R1(self.default_atom_view_color[atomic1][0])
      vb.set_color_G1(self.default_atom_view_color[atomic1][1])
      vb.set_color_B1(self.default_atom_view_color[atomic1][2])
      vb.set_color_R2(self.default_atom_view_color[atomic2][0])
      vb.set_color_G2(self.default_atom_view_color[atomic2][1])
      vb.set_color_B2(self.default_atom_view_color[atomic2][2])
      iCppExtention.py_Molecule_ViewBond_copy(self.molecule,vb,i)

  def DrawBond(self):
    iCppExtention.py_draw_bond_all(self.molecule)
    return

  def DrawTeapot(self,size,color):
    glColor3d(color[0],color[1],color[2])
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glutWireTeapot(size)
    glPopMatrix()

  def ViewReset(self):
    self.SetDefaultPointRotate()
    self.SetDefaultPointView()
    cx=self.center_point_view.get_x()
    cy=self.center_point_view.get_y()
    cz=self.center_point_view.get_z()+200.0
    self.eye.set_R(iCppExtention.Dvector3D(cx,cy,cz))
    self.eye.set_eyeAxis_x(iCppExtention.Dvector3D(1.00, 0.00,  0.00))
    self.eye.set_eyeAxis_y(iCppExtention.Dvector3D(0.00, 1.00,  0.00))
    self.eye.set_eyeAxis_z(iCppExtention.Dvector3D(0.00, 0.00, -1.00))

  def RotateEye(self,axis,angle):
    chk=self.DisableDraw()
    if   axis=='x':
         self.eye.rotate_eyeAxis_fixed_view_x(angle,self.center_point_rotate,self.center_point_view)
    elif axis=='y':
         self.eye.rotate_eyeAxis_fixed_view_y(angle,self.center_point_rotate,self.center_point_view)
    elif axis=='z':
         self.eye.rotate_eyeAxis_fixed_view_z(angle,self.center_point_rotate,self.center_point_view)
    self.EnableDraw(chk)

  def MoveEye(self,eye_fix,axis,dist):
    chk=self.DisableDraw()
    r1_x=self.eye.get_R().get_x()
    r1_y=self.eye.get_R().get_y()
    r1_z=self.eye.get_R().get_z()
    if   eye_fix==0:
         if   axis=='x':
              self.eye.translate_eyeAxis_x(dist)
         elif axis=='y':
              self.eye.translate_eyeAxis_y(dist)
         elif axis=='z':
              self.eye.translate_eyeAxis_z(dist)
         dr_x=self.eye.get_R().get_x()-r1_x
         dr_y=self.eye.get_R().get_y()-r1_y
         dr_z=self.eye.get_R().get_z()-r1_z
         self.center_point_view.set_x(self.center_point_view.get_x()+dr_x)
         self.center_point_view.set_y(self.center_point_view.get_y()+dr_y)
         self.center_point_view.set_z(self.center_point_view.get_z()+dr_z)
         self.center_point_rotate.set_x(self.center_point_rotate.get_x()+dr_x)
         self.center_point_rotate.set_y(self.center_point_rotate.get_y()+dr_y)
         self.center_point_rotate.set_z(self.center_point_rotate.get_z()+dr_z)
    elif eye_fix==1:
         e=iCppExtention.Eye(self.eye)
         e_x=e.get_R().get_x()
         e_y=e.get_R().get_y()
         e_z=e.get_R().get_z()
         c_x=self.center_point_view.get_x()
         c_y=self.center_point_view.get_y()
         c_z=self.center_point_view.get_z()
         l2=(e_x-c_x)*(e_x-c_x)+(e_y-c_y)*(e_y-c_y)+(e_z-c_z)*(e_z-c_z)
         l1=pow(l2,1.0/2.0) 
         if   axis=='x':
              e.translate_eyeAxis_fixed_view_x(dist,self.center_point_view)
         elif axis=='y':
              e.translate_eyeAxis_fixed_view_y(dist,self.center_point_view)
         elif axis=='z':
              if (l1-dist)<1.0:
                return
              e.translate_eyeAxis_fixed_view_z(dist,self.center_point_view)
         e_x=e.get_R().get_x()
         e_y=e.get_R().get_y()
         e_z=e.get_R().get_z()
         l4=(e_x-c_x)*(e_x-c_x)+(e_y-c_y)*(e_y-c_y)+(e_z-c_z)*(e_z-c_z)
         if l4 > l2 :
           self.eye.copy(e)
           return
         if l4 > 1.0:
           self.eye.copy(e)
           return
    self.EnableDraw(chk)

  def SetEye(self):
    zAxis=iCppExtention.Dvector3D(0.0,0.0,1.0)
    ex=self.eye.get_R().get_x()
    ey=self.eye.get_R().get_y()
    ez=self.eye.get_R().get_z()
    cx=self.eye.eyeR_to_R(zAxis).get_x()
    cy=self.eye.eyeR_to_R(zAxis).get_y()
    cz=self.eye.eyeR_to_R(zAxis).get_z()
    ux=self.eye.get_eyeAxis_y().get_x() 
    uy=self.eye.get_eyeAxis_y().get_y() 
    uz=self.eye.get_eyeAxis_y().get_z() 
    glMatrixMode(GL_PROJECTION)
    gluPerspective((self.eye_fovy),((1.0*self.size.width)/(1.0*self.size.height)),(self.eye_znear),(self.eye_zfar))
    gluLookAt(ex,ey,ez,cx,cy,cz,ux,uy,uz)

  def Draw(self):
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0,0.0,0.0,1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    self.SetEye()
    self.DrawBond()
    self.SwapBuffers()

  ######################################
  #090304 ishikura added these methods #
  ######################################
  def SetMolecule(self, ans, crd):
      for an, pos in zip(ans, crd):
          x, y, z = [ p/0.52921 for p in pos ]
          self.molecule.add_atom(an, x, y, z)
      self.molecule.add_bond_auto()

  def DisableDraw(self):
      if not self.enable_draw:
          return False
      if self.enable_draw:
          self.enable_draw = False
          return True
    
  def EnableDraw(self, chk):
      if chk:
          self.enable_draw = True
  #090304 end of methods added         #
  ######################################

  #090326 ishikura added
  def OnEraseBG(self, event):
      """Process the erase background event."""
      pass # Do nothing, to avoid flashing on MSWin


#-------------------------------------------------------------------------------

class MoleculeView(wx.Panel):

    """
    """

    def __init__(self, parent, id, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SUNKEN_BORDER, log=None):
        """Constructor."""
        wx.Panel.__init__(self, parent, -1)
        self.canvas = myGLCanvas(self)

#-------------------------------------------------------------------------------

class FrameSingle(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 
                          title='Drug Discovery software \"NAGARA\" : SCREEN',
                          pos=wx.DefaultPosition, size=(700,700))

        self.canvas = myGLCanvas(self)
        # self.canvas = MoleculeView(self, -1)
        self.Center()
        self.Show()

#-------------------------------------------------------------------------------

class FrameSeparate(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title='Test Frame',
                          pos=wx.DefaultPosition, size=(450,350))

        self.Center()
        self.Show()

        self.frame_gl=wx.Frame(self,-1,'DRAG DISCAVARY SOFTWARE \"NAGARA\" : SCREEN',pos=(16,32),size=(700,700))
        self.canvas=myGLCanvas(self.frame_gl)
        self.frame_gl.Show()

#-------------------------------------------------------------------------------

class FrameNotebook(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title='Test Frame',
                          pos=wx.DefaultPosition, size=(450,350))

        self.nb = wx.Notebook(self, -1, wx.DefaultPosition,
                              (-1,-1), style=wx.NB_BOTTOM)

        self.canvas = myGLCanvas(self.nb)
        self.panel = wx.Panel(self.nb, -1)
        self.nb.AddPage(self.canvas, 'Molecule View')
        self.nb.AddPage(self.panel, 'tests panel')

        self.Center()
        self.Show()

#-------------------------------------------------------------------------------

class FrameSplitter(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title='Test Frame',
                          pos=wx.DefaultPosition, size=(700,700))

        self.splitter = wx.SplitterWindow(self, -1)
        import systemview
        self.systemview =  systemview.SystemView(self.splitter, 1,
                                           wx.DefaultPosition, (-1,-1),
                                           style=wx.SUNKEN_BORDER)

        self.canvas = myGLCanvas(self.splitter)

        self.splitter.SplitVertically(self.systemview, self.canvas)
        self.Center()
        self.Show()

#-------------------------------------------------------------------------------

def main():

    import exception
    import molformat
    import systemview

    logfile = __name__ + '_error.log'
    # app = wx.App(redirect=False, filename=logfile)
    app = wx.App(redirect=False)

    frame = FrameSingle(None, -1)

    pdbfile = '../user-dir/1AG2.pdb'
    system = molformat.PDB(pdbfile).read()

    crd = system.getCrds()
    ans = [ atom.getAtmNum() for atom in system.getAtoms() ]

    frame.canvas.SetMolecule(ans, crd)
    chk = frame.canvas.DisableDraw()
    frame.canvas.SetAtomDefault()
    frame.canvas.SetBondDefault()
    frame.canvas.ViewReset()
    frame.canvas.EnableDraw(chk)

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()

