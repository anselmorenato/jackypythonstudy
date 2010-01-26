# _*_ coding: utf-8 _*_
# Copyright (C)  2009 Takakazu Ishikura

import sys, os
import wx
import wx.lib.customtreectrl as CT
import exception
import molformat
import system
import molview

#-------------------------------------------------------------------------------

class SystemError(exception.NagaraException): pass


class SystemView(wx.Panel):

    """
    Class to show or operate the bio system information using GUI.
    """

    def __init__(self, parent, id, position, size, style, log=None):
        """Constructor."""
        wx.Panel.__init__(self, parent, -1)

        self.log = log

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.tree = SystemTreeCtrl(self, log=log)
        self.tree = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS)

        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.initView()

        self.styledata = dir(CT)

        self.system = None

        # self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelChanged, id=1)

    def initView(self):
        tree = self.tree
        self.root = tree.AddRoot('Systems')

    def onInitProject(self, evt):
        self.initProject()

    def _addItems_all_dict(self, parent, tree_list):
        """ add all dict items to parent
        root = {A:a, B:b, C:c, D:d}
        A = {name=a, items=a_items}
        B = {name=b, items=b_items}
        C = {name=c, items=c_items}
        D = {name=d, items=d_items}
        """
        for item in tree_list:
            branch = self.AppendItem(parent, item['name'])

            if isinstance(item['items'], list):
                for leaf in item['items']:
                    self.AppendItem(branch, leaf)

            elif isinstance(item['items'], dict):
                _addItems(self, branch, )

            else:
                raise ParseTreeError(item=item)
                
    def addItems(self, parent, tree_list):
        """ add all dict items to parent
        """
        br1 = self.tree.AppendItem(parent, tree_list['name'])
        for item in tree_list['items']:

            if isinstance(item, str):
                if self.log: print(item)
                self.tree.AppendItem(br1, item)

            elif isinstance(item, dict):
                if self.log: print(item['items'])
                self.addItems(br1, item)

            else:
                raise ParseTreeError(item=item)
            
    def onAddGroup(self, evt): pass

    def loadSystem(self, system):
        """Load the biosystem into the system view."""
        self.system = system
        tree = self.tree
        top = tree.AppendItem(self.root, system.getName())

        # Atom group
        atom_item = tree.AppendItem(top, 'Atoms')
        for atom in system.getAtoms():
            label = '%d : %s' % (atom.id, atom.name)
            self.tree.AppendItem(atom_item, label)

        # Other group
        for name, grps in system.groups.items():
            item = tree.AppendItem(top, name)
            if self.log:
                self.log.write('Appending...: %s' % name)
            for grp in grps:
                self.appendGroup(item, grp)

    def appendGroup(self, parent, group):
        """Append the group under the parent item, recursively."""
        label = '%d : %s' % (group.id, group.getName())
        grp_item = self.tree.AppendItem(parent, label)
        if not group.getChildGrps():
            self.appendAtoms(grp_item, group)
        else:
            for cgrp in group.getChildGrps():
                if self.log:
                    self.log.write('Appending... : %s' % label)
                self.appendGroup(grp_item, cgrp)

    def appendAtoms(self, parent, group):
        """Append the atoms under the parent item."""
        for atom in group.getAtoms():
            label = '%d : %s' % (atom.id, atom.name)
            self.tree.AppendItem(parent, label)

    def OnSetSystemName(self, newname):
        """Do rename of the system."""
        self.system.setName(newname)

    def readMolecule(self, filename):
        """Read a pdb formatted data file."""
        self.system = molformat.PDB(filename).read()

    def matToTree(self, material): pass

    def renameItem(self, id, label):
        """ rename item name of the tree id 
        """
        can_rename_items = self.__flattenProject() 
        if id in can_rename_items:
            self.SetItemText(id, label)
        else:
            raise TreeRenameError(id=id)

    def deleteItem(self): pass

    def __flattenProject(self):
        flat_list = []
        for p in self.project:
            flat_list.append(p)
        return flat_list

class SystemTreeCtrl(CT.CustomTreeCtrl):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize,
                 style=wx.SUNKEN_BORDER | CT.TR_HAS_BUTTONS |
                 CT.TR_HAS_VARIABLE_ROW_HEIGHT | wx.WANTS_CHARS, log=None
                ):
        """Constructor."""
        CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log



class MyFrame(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, size=(450,350))

        self.splitter = wx.SplitterWindow(self, -1)
        self.systemview =  SystemView(self.splitter, 1,
                                           wx.DefaultPosition, (-1,-1),
                                           style=wx.SUNKEN_BORDER)

        self.nb = wx.Notebook(self.splitter, -1, wx.DefaultPosition,
                              (-1,-1), style=wx.NB_BOTTOM)
        self.molview = molview.MoleculeView(self.nb, -1)
        self.nb.AddPage(self.molview, 'Molecule View')

        self.splitter.SplitVertically(self.systemview, self.nb)
        self.Center()
        self.Show()

def main():
    logfile = __name__ + "_error.log"
    app = wx.App(redirect=False, filename=logfile)

    pdbfile = 'user-dir/1AG2.pdb'
    system = molformat.PDB(pdbfile).read()
    # for res in system.getGroups('Residues'):
    #     print(res.id, res.name)
    #     for atom in res.getAtoms():
    #         print(atom.id, atom.name)

    # molformat.PDB('user-dir/test.pdb').write(system)

    frame = MyFrame(None, -1, "ProjectFrame")
    frame.systemview.loadSystem(system)

    frame.Show()

    try:
        app.MainLoop()
    except:
        app.RedirectStdio()

if __name__ == '__main__':
    main()
