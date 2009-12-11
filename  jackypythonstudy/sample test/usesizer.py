import wx

# usesizer.py
class MyFrame(wx.Frame):
   def __init__(self, parent, ID, title):
      wx.Frame.__init__(self, parent, ID, title, size=(600, 250))
      notebook = wx.Notebook(self, -1, size=(450,300))
      
      panel1 = wx.Panel(notebook,-1, style=wx.SUNKEN_BORDER)
      panel2 = wx.Panel(notebook,-1, style=wx.SUNKEN_BORDER)

      panel1.SetBackgroundColour("BLUE")
      panel2.SetBackgroundColour("RED")
      panel1_sizer = wx.BoxSizer(wx.VERTICAL)
      text = wx.TextCtrl(panel1, -1, "Hi!", size=(400,90), style=wx.TE_MULTILINE)
      button1 = wx.Button(panel1, -1, "I only resize horizontally...")
      panel1_sizer.Add(text, 1, wx.EXPAND|wx.ALL, 10)
      buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
      buttonsizer.Add(button1,0,wx.ALIGN_CENTER,10)
      panel1_sizer.Add(buttonsizer, 0, wx.ALIGN_BOTTOM|wx.ALL, 10)
      panel1.SetSizer(panel1_sizer)
      
      notebook.AddPage(panel1, "Panel 1")
      notebook.AddPage(panel2, "Panel 2")

      box = wx.BoxSizer(wx.VERTICAL)
      box.Add(notebook, 2, wx.EXPAND)
      #box.Add(panel2, 0, wx.EXPAND)
      

      self.SetAutoLayout(True)
      self.SetSizer(box)
      self.Layout()


app = wx.PySimpleApp()
frame = MyFrame(None, -1, "Sizer Test")
frame.Show()
app.MainLoop()
