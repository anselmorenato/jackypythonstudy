#  -*- encoding: utf-8 -*-
import os, sys


# nagara modules
nagara_path = os.environ['NAGARA_PATH']
sys.path.append( os.path.join(nagara_path, 'src') )

from  dialog  import *

# shower API

class Shower(object):

    def __init__(self):
        pass

    def get_project(self):
        pass

    def get_file(self):
        pass

    def show_aboutinfo(self):
        """Show the dialog of About information."""
        import core.copyright as c
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('nagara.ico', wx.BITMAP_TYPE_ICO))
        info.SetName(c.NAME)
        info.SetVersion(c.VERSION)
        info.SetDescription(c.DESCRIPTION)
        info.SetCopyright(c.COPYRIGHT)
        info.SetWebSite(c.WEBSITE)
        # info.SetLicence(c.LICENCE)
        for d in c.DEVELOPERS:
            info.AddDeveloper(d)
        # info.AddDocWriter('jan bodnar')
        # info.AddArtist('The Tango crew')
        # info.AddTranslator('jan bodnar')
        wx.AboutBox(info)

    def get_help(self, help_word):
        pass

    def get_molecule(self):
        """Show the open molecule dialog and get a molecule."""

        dirpath = "C:\Home_Ishikura\docs\Nagara\src\user-dir"
        message = ""
        extension = "|".join(
            ["Protein Data Bank File ( *.pdb )|*.pdb",
             "Sybyl Mol2 File ( *.mol2 )|*.mol2"]
        )

        dialog = wx.FileDialog(
            self, "Please choose pdb file",
            defaultDir=dirpath, wildcard=extension
        )
        answer = dialog.ShowModal()

        # filename = dialog.GetFilename()
        filename  = dialog.GetPath()
        dirpath = dialog.GetDirectory()
        dialog.Destroy()
        
        # read the pdb file and store to the system
        import molformat
        # self.nagara.system = molformat.PDB(filename).read()
        system = molformat.PDB(filename).read()
        project = wx.GetApp().getCurPrj()
        project.appendSystem(system)
        systemview = self._panels['SystemView']
        systemview.loadSystem(system)
        if __debug__:
            for atom in system.getAtoms():
                self.getLog().write(atom.getAtmNum())

        crd = system.getCrds()
        ans = [ atom.getAtmNum() for atom in system.getAtoms() ]

        if self.molview:
            self.molview.SetMolecule(ans, crd)
            chk = self.molview.DisableDraw()
            self.molview.SetAtomDefault()
            self.molview.SetBondDefault()
            self.molview.ViewReset()
            self.molview.EnableDraw(chk)

        # for res in system.getGroups('Residues'):
        #     print(res.id, res.name)
        #     for atom in res.getAtoms():
        #         print(atom.id, atom.name)

        # molformat.PDB('user-dir/test.pdb').write(system)

        # frame = MyFrame(None, -1, "ProjectFrame")
        # frame.systemview.loadSystem(system)

    def onConfigDlg(self, event):
        dlg = ConfigDlg(None, "simpledialog.py")
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def show_amber_dialog(self, event):
        import amberpanel
        dlg = wx.Dialog(None, -1, title='Amber Dialog', size=(480, 570))
        amberpanel.AmberPanel(dlg, -1, 'amber', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def show_paics_dialog(self, event):
        import paicspanel
        dlg = wx.Dialog(None, -1, title='Paics Dialog', size=(390, 340))
        paicspanel.PaicsPanel(dlg, -1, 'paics', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def show_marvin_dialog(self, event):
        import marvinpanel
        dlg = wx.Dialog(None, -1, title='Marvin Dialog', size=(562, 500))
        marvinpanel.MarvinPanel(dlg, -1, 'marvin', log=self.getLog())
        dlg.ShowModal()
        dlg.Destroy()
        return True

    def onProjectDlg(self, event):
        # In this case we include a "New directory" button. 
        dlg = wx.DirDialog(self, "Choose a nagara project directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.configs['project_root'] = dlg.GetPath()
            project = wx.GetApp().getCurPrj()
            project.setRoot(dlg.GetPath())
            self.log('set the project directory: '+ str(dlg.GetPath()))

        dlg.Destroy()

    def onRemoteRootDlg(self, event):
        dlg = wx.TextEntryDialog(
                self, 'Put a remote working directory.',
                'RemoteRootDlg', '/home/ishikura/Nagara/projects')

        dlg.SetValue('/home/ishikura/Nagara/projects')

        if dlg.ShowModal() == wx.ID_OK:
            configs = wx.GetApp().getConfigs()
            configs['remote_root'] = dlg.GetValue()

        dlg.Destroy()
