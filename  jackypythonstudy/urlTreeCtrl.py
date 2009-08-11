import wx



rooturl=['http://www.54snapple.org/flash/54snapple/register.asp',
         'http://www.54snapple.org/flash/wwwnet/list.asp',
         'http://www.54snapple.org/index.asp',
         'http://www.54snapple.org/flash/member.asp',
         'http://www.54snapple.org/note/image/addnote.asp',
         'http://www.54snapple.org/note/news/addnote.asp']

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="simple tree", size=(800,500))
       
        self.tree = wx.TreeCtrl(self)
      
        root = self.tree.AddRoot("www.54snapple.org")
        tt=self.getChildren(self.tree,root)
        print self.tree.GetItemText(root)
        print "this is a test!"
        for url in rooturl:
            url=url.split("/")
            url=url[3:]
            print url
            self.format(root,url)

        self.tree.Expand(root)
       
    def getChildren(self,tree, parent):
        result = []
        item, cookie = tree.GetFirstChild(parent)
        while item:
            result.append(tree.GetItemText(item))
            item, cookie = tree.GetNextChild(parent, cookie)
           
        return result
    def format(self,parent,url):
        if url==[]:
            return False
        else:
            item=parent

            result=self.getChildren(self.tree,item)
            tturl=url
            ss=url.pop(0)

            if ss in result:
                item=self.getThisNode(item,ss)
                self.format(item,url)
            else:
                item=self.tree.AppendItem(item,ss)
                self.add(item,tturl)
                self.format(item,url)
    def getThisNode(self,parent,ss):
        item,cookie=self.tree.GetFirstChild(parent)
        while item:
            sz=self.tree.GetItemText(item)
            if ss==sz:
                node=item
                break
            else:
                item,cookie=self.tree.GetNextChild(parent,cookie)
        return node
    def add(self,item,url):
        if url!=[]:
            item=self.tree.AppendItem(item,url.pop(0))
            newitem=self.add(item,url)
            
app = wx.App()

frame = MyFrame()
frame.Show()
app.MainLoop()