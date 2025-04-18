import globalPluginHandler
import gui
import wx
import api
import ui
from scriptHandler import script
from .functions import tampilkan_info_sistem,check_top_processes, check_ram, check_cpu, check_usb_devices, checkInternet, check_disk_usage, check_battery_status, check_windows_update, nvdaVersion 
# Variabel global untuk menyimpan dialog yang aktif
showDialog = None

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
        self.open = self.toolsMenu.Append(wx.ID_ANY, _("Monitoring"), _("Monitoring"))
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.run, self.open)

    @script(
        description=_("Check Network"),
        category=_("Monitoring"),
        gesture="kb:"
    )
    def script_checkInternet(self, gesture):
        checkInternet()

    @script(
        description=_("Check Battery"),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+2"
    )
    def script_checkBattery(self, gesture):
        check_battery_status()

    @script(
        description=_("Check storage"),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+3"
    )
    def script_checkStorage(self, gesture):
        check_disk_usage()

    @script(
        description=_("Check Memory "),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+4"
    )
    def script_checkRAM(self, gesture):
        check_ram()

    @script(
        description=_("Check CPU"),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+5"
    )
    def script_checkCPU(self, gesture):
        check_cpu()

    @script(
        description=_("Background Process"),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+6"
    )
    def script_Process(self, gesture):
        check_top_processes()

    @script(
        description=_("Check USB "),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+7"
    )
    def script_checkUSB(self, gesture):
        check_usb_devices()

    @script(
        description=_("Check windows Update "),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+8"
    )
    def script_checkUpdate(self, gesture):
        check_windows_update()

    @script(
        description=_("Check info system "),
        category=_("Monitoring"),
        gesture="kb:nvda+shift+9"
    )
    def script_infoSistem(self, gesture):
        tampilkan_info_sistem()
    
    @script(
        description=_("Show monitoring menu"),
        category=_("Monitoring"),
        gesture="kb:nvda+i"
    )
    def script_show_dialog(self, gesture):
        global showDialog
        if not showDialog:  # Jika dialog belum ada, buat dialog baru
            showDialog = InteractiveDialog(gui.mainFrame)
            showDialog.Show()
            showDialog.Raise()
            showDialog.Bind(wx.EVT_CLOSE, self.on_dialog_close)
        else:  # Jika dialog sudah ada, cukup angkat dialog ke atas
            showDialog.Raise()
            showDialog.listBox.SetFocus()

    def on_dialog_close(self, event):
        global showDialog
        showDialog = None  # Hapus referensi dialog saat ditutup
        event.Skip()

    def run(self, event):
        self.script_show_dialog(None)

    def terminate(self):
        try:
            self.toolsMenu.Remove(self.open)
        except:
            pass


class InteractiveDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title=_("Device Monitoring"), size=(400, 250))

        # Panel utama untuk elemen dialog
        self.Center()
        panel = wx.Panel(self)

        # Label instruksi
        wx.StaticText(panel, label=_("MENU"), pos=(20, 20))

        # ListBox untuk pilihan fitur
        self.listBox = wx.ListBox(panel, choices=[
            _("Jaringan"),
                        _("Baterai"),
            _("Penyimpanan"),
            _("RAM"),
            _("CPU"),
            _("Proses"),
            _("USB"),
                        _("Periksa Update"),
                        _("Info Sistem"), 
                        _("Versi NVDA")
        ], pos=(20, 50), size=(350, 100), style=wx.LB_SINGLE)

        # Tombol batal
        cancel_button = wx.Button(panel, label=_("Batal"), pos=(200, 170))
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Menangani event keyboard global
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_cancel(self, event):
        self.Destroy()

    def on_key_press(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_RETURN or key_code == wx.WXK_SPACE:
            self.run_selected_function()
        elif key_code == wx.WXK_ESCAPE:
            self.on_cancel(event)
        else:
            event.Skip()

    def run_selected_function(self):
        selection = self.listBox.GetSelection()
        if selection == 0:
            checkInternet()
        elif selection == 1:
            check_battery_status()
        elif selection == 2:
            check_disk_usage()
        elif selection == 3:
            check_ram()
        elif selection == 4:
            check_cpu()
        elif selection == 5:
            check_top_processes()
        elif selection == 6:
            check_usb_devices()
        elif selection == 7:
         check_windows_update()
        elif selection == 8:
         tampilkan_info_sistem()
        elif selection == 9:
         nvdaVersion()
            
            