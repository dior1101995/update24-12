
import os
from re import T
import subprocess
import sys
from threading import Thread, Lock, Event
import wmi
import win32gui,win32ui,win32con

from _congfig_bot import Setting_Bot
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QSettings
from PyQt5.QtWidgets import QMessageBox

from numpy import frombuffer, shape , ascontiguousarray
import time

from New_Data_Image import *
from _controller import  controller
from _read_lic import Lic_info
from datetime import datetime

from Bot_Chuc_Nang import Bot_ChucNang
from SQL_DB import SQLite
import configparser

from datetime import timedelta,datetime

Exit_Event = Event()


def SaveTime():
    print("Saves Time")
    now = datetime.utcnow()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    with open('New_Data\DiAnMo\log.as', 'w') as FileLic:
        FileLic.write(dt_string)





class showtime(QtCore.QThread):
    '''Show Time Lên Gui'''
    thoigian_run = [0, 0, 0]
    thoigian_tong = [0, 0, 0]
    thoigian_1acc = [0, 0, 0]

    Start_Time_ChucNang = False

    Running_ChucNang = True
    

    Time_GMT = datetime.utcnow()
    Lience_HetHanSuDung = QtCore.pyqtSignal()
    Lable_Time_GMT = QtCore.pyqtSignal(str)
    Lable_TimeTong = QtCore.pyqtSignal(str)
    Lable_Time_1Acc = QtCore.pyqtSignal(str)
    Lable_Time_1ChucNang = QtCore.pyqtSignal(str)
    Lable_Time_HanSuDung = QtCore.pyqtSignal(str)
    Reset_File_Data_Running = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


    def show(self):

    # Xác Định Time GMT
        self.Time_GMT = datetime.utcnow()

    # Reset lúc 23:59:59
        if self.Time_GMT.hour == 23 and self.Time_GMT.minute == 59 and self.Time_GMT.second >= 59:
            print("Reset File Running")
            self.Reset_File_Data_Running.emit()


    # Xác Định Hạn Sử Dụng 
        self.Han_Su_Dung = Get_Hansudung - self.Time_GMT

        # Lic  Hết Hạn Sử Dụng
        if Get_Hansudung < self.Time_GMT:
            self.Lience_HetHanSuDung.emit()
            self.Han_Su_Dung = "0 day, 00:00:00"

        # Đọc File Log.as
        with open('New_Data\DiAnMo\log.as', 'r') as File_log_as:
            Log_as_Time = File_log_as.read()

        # Conver Log.as
        Data_Time_Log_as_Time = datetime.strptime(Log_as_Time,"%d-%m-%Y %H:%M:%S")

        # Time_GMT < Log.as => Stop   
        if  self.Time_GMT < Data_Time_Log_as_Time :
            self.Lience_HetHanSuDung.emit()
            self.Han_Su_Dung = "0 day, 00:00:00"


        if  self.Start_Time_ChucNang:

            if self.Running_ChucNang:
                # Time 1 Chuc Nang
                self.thoigian_run[2] += 1
                if self.thoigian_run[2] >= 60: self.thoigian_run[1] += 1; self.thoigian_run[2] = 0
                if self.thoigian_run[1] >= 60: self.thoigian_run[0] += 1; self.thoigian_run[1] = 0; self.thoigian_run[2] = 0

                # Time 1 Acc
                self.thoigian_1acc[2] += 1
                if self.thoigian_1acc[2] >= 60: self.thoigian_1acc[1] += 1; self.thoigian_1acc[2] = 0
                if self.thoigian_1acc[1] >= 60: self.thoigian_1acc[0] += 1; self.thoigian_1acc[1] = 0; self.thoigian_1acc[2] = 0

                # Time Tong
                self.thoigian_tong[2] += 1
                if self.thoigian_tong[2] >= 60: self.thoigian_tong[1] += 1; self.thoigian_tong[2] = 0
                if self.thoigian_tong[1] >= 60: self.thoigian_tong[0] += 1; self.thoigian_tong[1] = 0; self.thoigian_tong[2] = 0


            timeString =  f"{self.thoigian_run[0]:02d}:{self.thoigian_run[1]:02d}:{self.thoigian_run[2]:02d}"
            timeString_1acc = f"{self.thoigian_1acc[0]:02d}:{self.thoigian_1acc[1]:02d}:{self.thoigian_1acc[2]:02d}"
            timetong_String = f"{self.thoigian_tong[0]:02d}:{self.thoigian_tong[1]:02d}:{self.thoigian_tong[2]:02d}"
        else:
            timeString = "   "
            timeString_1acc = "   "
            timetong_String = "   "



    #Show Gui

        # Show Time GMT    
        self.Lable_Time_GMT.emit(str(self.Time_GMT.strftime("%H:%M:%S")))

        # Show Han Su Dung
        self.Lable_Time_HanSuDung.emit(str(self.Han_Su_Dung).split('.', 2)[0])

        # Show Time Run
        self.Lable_TimeTong.emit(timetong_String)
        self.Lable_Time_1Acc.emit(timeString_1acc)
        self.Lable_Time_1ChucNang.emit(timeString)

    def Start(self):
        """Start Show Time"""
        self.Start_Time_ChucNang = True


    def Stop(self):
        """Stop Show Time"""
        self.thoigian_run = [0, 0, 0]
        self.thoigian_tong = [0, 0, 0]
        self.thoigian_1acc = [0, 0, 0]
        self.Start_Time_ChucNang = False
        self.Running_ChucNang = False


    def Pause(self):
        """Pause Show Time"""
        self.Running_ChucNang = False

    def Continue(self):
        """Continue Show Time"""
        self.Running_ChucNang = True

    def Reset_Time_Run_Chuc_Nang(self):
        """Reset Time Run Chuc Nang """
        SaveTime()
        self.stopped_time_run = [0, 0, 0]

    def Reset_Time_Run_1_Acc(self):
        """Reset Time Run 1 Acc """
        self.thoigian_1acc = [0, 0, 0]

        
    def Reset_Time_Run_Tong(self):
        self.thoigian_tong = [0, 0, 0]





class Languge:
    

    def __init__(self):
        File_config = configparser.ConfigParser()
        File_config.read('/DataText/ConfigAuto.ini')

        if File_config.get('ChucNang', 'language') == "English":
            pass

        else:




        


    




class Gui_Farm_Info(QtWidgets.QMainWindow):
    '''Gui Farm Info'''
    data_ccombo_sodao = ["2", "3", "4", "5", "6"]
    data_loamo = ["1", "2", "3", "4"]
    data_mainacc = ("False", "True")
    data_combo_capmo = ["2","3","4","5","6","7"]
    click = 0

    def __init__(self,main_Window,parent = None):
        super(Gui_Farm_Info, self).__init__(parent)
        self.main_Window = main_Window

        self.ui = uic.loadUi('Gui/Gui_Farm_Info.ui', self)
        self.setObjectName("Farm Info")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.load_data()

        self.tableWidget.setColumnWidth(0, 270)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 70)
        self.tableWidget.setColumnWidth(3, 70)
        self.tableWidget.setColumnWidth(4, 70)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setColumnWidth(6, 70)
        self.tableWidget.setColumnWidth(7, 70)


        self.comboBox_sodao.addItems(self.data_ccombo_sodao)
        self.comboBox_sodao.setCurrentIndex(3)
        # loại Mỏ
        self.comboBox_loaimo.addItems(self.data_loamo)
        self.comboBox_loaimo.setCurrentIndex(2)
        # Cấp Mỏ
        self.comboBox_loaimo_2.addItems(self.data_combo_capmo)
        self.comboBox_loaimo_2.setCurrentIndex(4)
        
        


        self.spinBox_2_ttanhhung.setRange(1, 9)
        self.spinBox_somoxay.setRange(6, 9)
        self.spinBox_3_mainacc.setRange(0, 3)

        self.Delete.clicked.connect(self.delete_data)
        self.pushButton.clicked.connect(self.add_data)
        self.Clear.clicked.connect(self.clear_add)
        self.deleteall.clicked.connect(self.Delete_all_data)
        self.ResetAuto.clicked.connect(self.reset_auto_main)
        self.Edit.clicked.connect(self.edit_data)

        self.tableWidget.viewport().installEventFilter(self)

    def eventFilter(self, source, event):

        if (event.type() == QtCore.QEvent.MouseButtonDblClick and
                event.buttons() == QtCore.Qt.LeftButton and
                source is self.tableWidget.viewport()):

            self.clear_add()
            self.Edit.setDisabled(False)
            self.pushButton.setDisabled(True)
            self.Clear.setDisabled(True)
            self.Delete.setDisabled(True)

            with SQLite('DataText/Farm_Info.db') as cur:
                content = "SELECT * FROM Farm_Info"
                res = cur.execute(content)
                for row in enumerate(res):
                    if row[0] == self.tableWidget.currentRow():
                        self.RoW_edit = row[0]
                        data = row[1]
                        Email = data[0]
                        self.lineEdit_email.setText(Email)
                        Password1 = data[1]
                        self.lineEdit_password.setText(Password1)
                        SoDao = data[2]
                        self.comboBox_sodao.setCurrentIndex(self.data_ccombo_sodao.index(str(SoDao)))
                        LoaiMo = data[3]
                        self.comboBox_loaimo.setCurrentIndex(self.data_combo_capmo.index(str(LoaiMo + 1)))
                        CapMo = data[4]
                        self.comboBox_loaimo_2.setCurrentIndex(self.data_combo_capmo.index(str(CapMo)))
                        NangCapAH = data[5]
                        XayNha = data[6]
                        MainAcc = data[7]


        return super().eventFilter(source, event)

    def load_data(self):

        with SQLite('DataText/Farm_Info.db') as cur:
            query = "SELECT * FROM Farm_Info"
            result = cur.execute(query)
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for colum_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

        self.label_8.setText("Total User :" + str(self.tableWidget.rowCount()))
        

    def add_data(self):
        #Quá 36 Acc
        soacc = self.tableWidget.rowCount()
        if int(soacc) >= 37:
            choice = QtWidgets.QMessageBox.question(self, 'Warning', " 'Limit Farm Account'?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                return False

            if choice == QMessageBox.No:
                return False



        Email = self.lineEdit_email.text()
        Password = self.lineEdit_password.text()
        so_dao = self.comboBox_sodao.currentText()
        loaimo = self.comboBox_loaimo.currentText()
        tt_anhhung = self.spinBox_2_ttanhhung.value()
        xay_nha = self.spinBox_somoxay.value()
        main_acc = self.spinBox_3_mainacc.value()
        cap_mo = self.comboBox_loaimo_2.currentText()

        with SQLite('DataText/Farm_Info.db') as cur:
            cur.execute("""INSERT INTO Farm_Info 
                    ( Email , Password , SoDao , LoaiMo ,CapMo, NangCapAH , XayNha , MainAcc ) 
                        VALUES 
                        (?, ? ,?, ?, ?, ? ,?,?)""", (Email, Password, so_dao, loaimo,cap_mo,tt_anhhung,xay_nha, main_acc))

        self.load_data()

    def clear_add(self):
        self.lineEdit_email.clear()
        self.lineEdit_password.clear()

    def delete_data(self):
        with SQLite('DataText/Farm_Info.db') as cur:
            content = "SELECT * FROM Farm_Info"
            res = cur.execute(content)
            for row in enumerate(res):
                if row[0] == self.tableWidget.currentRow():
                    print(row[0])
                    data = row[1]
                    Email = data[0]
  
                    Password1 = data[1]

                    SoDao = data[2]

                    LoaiMo = data[3]

                    CapMo = data[4]

                    NangCapAH = data[5]
                    XayNha = data[6]
                    MainAcc = data[7]

                    cur.execute(
                        "DELETE FROM Farm_Info WHERE Email=? AND Password=? AND SoDao=? AND LoaiMo=? AND NangCapAH=? AND XayNha=? AND MainAcc=? AND CapMo = ?",
                        (Email, Password1, SoDao, LoaiMo, NangCapAH, XayNha, MainAcc,CapMo))
        self.load_data()

    def edit_data(self):

        print("edit")
        self.delete_data()
        self.add_data()
        self.clear_add()
        self.Edit.setDisabled(True)
        self.pushButton.setDisabled(False)
        self.Clear.setDisabled(False)
        self.Delete.setDisabled(False)
        self.load_data()

    def Delete_all_data(self):
        choice = QtWidgets.QMessageBox.question(self, 'Farm Info', " 'Xóa Tất Cả Dữ Liệu Farm Account'?",
                                                QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            with SQLite('DataText/Farm_Info.db') as cur:
                cur.execute("""DELETE FROM Farm_Info""")
            self.load_data()

            return False
        if choice == QMessageBox.No:
            return False

    def closeEvent(self, event):
        try:
            self.main_Window.Window_Farm_Info = None
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
        except:
            pass

 
    def reset_auto_main(self, ):
        try:
            os.execl(sys.executable, sys.executable, *sys.argv)
        except:
            pass


class Gui_buys(QtWidgets.QMainWindow):
    def __init__(self,main_Window ,parent = None):
        super(Gui_buys, self).__init__(parent)
        self.main_Window = main_Window

        self.ui = uic.loadUi('Gui/Buys.ui', self)
        self.setObjectName("Buys Info")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.pushButton.clicked.connect( lambda: self.GetKey())

    def GetKey(self):
        c = wmi.WMI()
        Get_seri_hhd_number = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
        print(Get_seri_hhd_number)
        self.lineEdit.clear()
        self.lineEdit.setText(Get_seri_hhd_number)

    def closeEvent(self, event):
        try:
            self.main_Window.Window_Buys = None
            
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
        except:
            pass


class Gui_Auto(QtWidgets.QMainWindow):
    id_device = None
    Nox_Name = None

    #Info Farm Account
    List_Email_Farm_Acount = []
    List_Password_Farm_Account = []
    List_So_Dao = []
    List_Loai_Mo = []
    List_CapMo = []
    List_NangCapAnhHung = []
    List_XayNha = []
    List_MainAcc= []



    List_NgonNgu = ["VietNam","English"]
    List_Time_Nhan_NhiemVu = ["16:00","17:00","18:00","19:00","20:00","21:00"]
    Time_NhanNhiemVu = 21
    List_Time_DeLay = ["60","70","80","90","100","110"]
    List_Time_Delay_Load_Anh = ["3","4","5"]
    list_ComBoBox_MoTaiNguyen = ["Gems","Rice","Wood","Metal","Silver"]
    List_Quai = ["1","2", "3","4","5","6","7","8","9", "10","11","12","13","14","15", "16","17","18","19","20", "21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40"]
    List_Khien = ["8h","24h","3Day"]


    List_TuAcc = ["1","2","3","4","5","6"]
    List_DenAcc = ["1","2","3","4","5","6"]

    def __init__(self ):
      #  super(Gui_Auto, self).__init__(parent)
        super().__init__()
        self.ui = uic.loadUi('Gui/New_Gui_Auto.ui', self)
    # Set Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.Window_Farm_Info =None
        self.Window_Buys = None

    # Tab Widget Danh Quai Vat
        self.tableWidget.setColumnWidth(1, 15)
        self.tableWidget.setColumnWidth(2, 15)

        self.tableWidget.setColumnWidth(0, 89)
        self.tableWidget.setColumnWidth(1, 89)

    # Tạo Thư Mục Lưu Config  \HKEY_CURRENT_USER\Software\Auto_Rise\Config
        self.Config = QSettings('Auto_Rise','Config')

    # Đọc Và Tạo Data Farm Account
        self.Doc_Va_Tao_Data_Farm()

# Thread MainBot
        self.Main_Bot = Main_Bot(self)
        self.Main_Bot.ThongBaoNox.connect(self.Thread_Main_Bot_ThongBaoLoiNox)
        self.Main_Bot.Update_ComBoBox_ChonAcc.connect(self.Thread_Main_bot_Update_ComBobox_ChonAcc)
        self.Main_Bot.Update_KhoangCach_DanhQuai.connect(self.Thread_Main_bot_Update_KhoangCach_DanhQuai)

#Thread Show_Time
        # Show Time
        self.timer = QTimer(self)
        self.Show_Time = showtime()
        self.timer.timeout.connect(self.Show_Time.show)
        self.Show_Time.Lable_Time_GMT.connect(self.Lable_Time_GMT)
        self.Show_Time.Lable_TimeTong.connect(self.Lable_TimeTong)
        self.Show_Time.Lable_Time_1Acc.connect(self.Lable_Time_1Acc)
        self.Show_Time.Lable_Time_1ChucNang.connect(self.Lable_Time_1ChucNang)
        self.Show_Time.Lable_Time_HanSuDung.connect(self.Lable_Time_HanSuDung)
        self.Show_Time.Reset_File_Data_Running.connect(self.Reset_File_Data_Running)
        self.Show_Time.Lience_HetHanSuDung.connect(self.Lience_HetHanSuDung)
        self.timer.start(1000)





# Set Value ComBoBox
    # Setting
        # Delay
        self.CBBox_Delay.addItems(self.List_Time_DeLay)
        self.CBBox_Delay.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBBox_Delay,"Delay"))
        self.Set_Delay()

        # ComBobox Set Title Nox 
        self.CBBox_ChonTitle.addItems(self.Get_Title_Nox())
        self.CBBox_ChonTitle.currentTextChanged.connect(lambda: self.Combobox_SetTitlets())

        # ComBobox Set Email Farm Account
        self.CBbox_Chon_Acc.addItems(self.List_Email_Farm_Acount)

    # Tab Develoop
        # ComBobox Set Languge
        self.CBbox_Ngon_Ngu.addItems(self.List_NgonNgu)
        self.CBbox_Ngon_Ngu.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBbox_Ngon_Ngu,"Language"))

        # ComBobox Set Time Nhận Nhiêm Vụ
        self.CBbox_Time_NhiemVu.addItems(self.List_Time_Nhan_NhiemVu)
        self.CBbox_Time_NhiemVu.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBbox_Time_NhiemVu,"Time_Nhan_NhiemVu"))
        
        # ComBobox Set Delay Load image
        self.CBBox_Delay_2.addItems(self.List_Time_Delay_Load_Anh)
        self.CBBox_Delay_2.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBBox_Delay_2,"Delay_Load_Image"))

    # Tab Event
        # ComBobox Set Mở Loại Tài Nguyên
        self.CBbox_MoTaiNguyen.addItems(self.list_ComBoBox_MoTaiNguyen)

        # ComBobox Set Loại Khiên
        self.CBbox_MoTaiNguyen_4.addItems(self.List_Khien)

    # Tab Main Acc
        # ComBobox Set Cấp Quái Vật
        self.CBbox_MoTaiNguyen_3.addItems(self.List_Quai)
        self.CBbox_MoTaiNguyen_3.setCurrentIndex(29)

        self.CBbox_MoTaiNguyen_2.addItems(self.List_Quai)
        self.CBbox_MoTaiNguyen_2.setCurrentIndex(39)

        # ComBoBox GomRss
        self.CBBox_ChonTitle_2.addItems(self.List_TuAcc)
        self.CBBox_ChonTitle_2.setCurrentIndex(0)

        self.CBBox_ChonTitle_3.addItems(self.List_TuAcc)
        self.CBBox_ChonTitle_3.setCurrentIndex(5)

        self.lineEdit.setText("100")

    # Load Language
        try:
            self.CBbox_Ngon_Ngu.setCurrentIndex(self.List_NgonNgu.index(self.Config.value("Language")))
            self.CBBox_Delay.setCurrentIndex(self.List_Time_DeLay.index(self.Config.value("Delay")))
            self.CBBox_Delay_2.setCurrentIndex(self.List_Time_Delay_Load_Anh.index(self.Config.value("Delay_Load_Image")))
            self.CBbox_Time_NhiemVu.setCurrentIndex(self.List_Time_Nhan_NhiemVu.index(self.Config.value("Time_Nhan_NhiemVu")))

            if self.Config.value("Language") == "English":

            # Tab Event


                
                
            # Set Language running
                # Tab Event
                

                # Tab Farm

                
  
        # Language Tiếng Việt
            else:

"

                # Text Event
                
    # Load Config Check Box
            self.CB_Login.setChecked(True)
            self.CB_RssTrongThanh.setChecked(True)
            self.CB_QuaBenCang.setChecked(True)

            self.CB_Diem_Danh.setChecked(self.Config.value("DiemDanh"))
            self.CB_Choi_Xuc_Xac.setChecked(self.Config.value("ChoiXucXac"))
            self.CB_DAnh_Ai_Rong.setChecked(self.Config.value("DanhAiRong"))
            self.CB_Tri_Thuong.setChecked(self.Config.value("TriThuong"))
            self.CB_An_4_Mo.setChecked(self.Config.value("An4Mo"))
            self.CB_Thay_Phap.setChecked(self.Config.value("ThayPhap"))
            self.CB_Cong_Hien_LM.setChecked(self.Config.value("CongHienLM"))
            self.Cb_Nap_Rong.setChecked(self.Config.value("NapRong"))
            self.CB_Luyen_Linh.setChecked(self.Config.value("LuyenLinh"))
            self.CB_Doi_Hc.setChecked(self.Config.value("DoiH.C"))
            self.CB_Gui_Da_Quy.setChecked(self.Config.value("GuiDaQuy"))
            self.CB_Nang_Cap_AH.setChecked(self.Config.value("NangCapA.H"))
            self.CB_Tai_Thiet.setChecked(self.Config.value("TaiThiet"))
            self.CB_Uoc.setChecked(self.Config.value("Uoc"))

            self.CB_DapLua.setChecked(self.Config.value("DapLua"))
            self.CB_XayDung.setChecked(self.Config.value("XayDung"))
            self.CB_Chieu_Mo_AH.setChecked(self.Config.value("ChieuMoA.H"))
            self.CB_Bua_San_Luong.setChecked(self.Config.value("BuaSanLuong"))
        #    self.CB_Kiem_Tra_Vip.setChecked(self.Config.value("KiemTraVip"))
            self.CB_Nghien_Cuu.setChecked(self.Config.value("NghienCuu"))
            self.CB_Skill_Lanh_Chua.setChecked(self.Config.value("SkillLanhChua"))
            self.CB_Di_Thu_Mo.setChecked(self.Config.value("DiThuMo"))
            self.CB_Khien_Nc.setChecked(self.Config.value("KhienN.C"))

            self.CB_May_Ban_Da.setChecked(self.Config.value("MayBanDa"))
            self.CB_Kho_Bau_Bi_An.setChecked(self.Config.value("KHoBauBiAn"))
            self.CB_Thu_Thap_Kiet_Xuat.setChecked(self.Config.value("ThuThapKietXuat"))
            self.Cb_Ruong_KVK.setChecked(self.Config.value("RuongKVK"))
            self.Cb_Ruong_Ba_Chu.setChecked(self.Config.value("RuongBaChu"))
            self.Cb_Gac_Lau_Kho_Bau.setChecked(self.Config.value("GacLauKhoBau"))
       
        except:
             pass

    # Set Config Check Box
        self.CB_Diem_Danh.clicked.connect(lambda: self.Set_Config(self.CB_Diem_Danh,"DiemDanh"))
        self.CB_Choi_Xuc_Xac.clicked.connect(lambda: self.Set_Config(self.CB_Choi_Xuc_Xac,"ChoiXucXac"))
        self.CB_DAnh_Ai_Rong.clicked.connect(lambda: self.Set_Config(self.CB_DAnh_Ai_Rong,"DanhAiRong"))
        self.CB_Tri_Thuong.clicked.connect(lambda: self.Set_Config(self.CB_Tri_Thuong,"TriThuong"))
        self.CB_An_4_Mo.clicked.connect(lambda: self.Set_Config(self.CB_An_4_Mo,"An4Mo"))
        self.CB_Thay_Phap.clicked.connect(lambda: self.Set_Config(self.CB_Thay_Phap,"ThayPhap"))
        self.CB_Cong_Hien_LM.clicked.connect(lambda: self.Set_Config(self.CB_Cong_Hien_LM,"CongHienLM"))
        self.Cb_Nap_Rong.clicked.connect(lambda: self.Set_Config(self.Cb_Nap_Rong,"NapRong"))
        self.CB_Luyen_Linh.clicked.connect(lambda: self.Set_Config(self.CB_Luyen_Linh,"LuyenLinh"))
        self.CB_Doi_Hc.clicked.connect(lambda: self.Set_Config(self.CB_Doi_Hc,"DoiH.C"))
        self.CB_Gui_Da_Quy.clicked.connect(lambda: self.Set_Config(self.CB_Gui_Da_Quy,"GuiDaQuy"))
        self.CB_Nang_Cap_AH.clicked.connect(lambda: self.Set_Config(self.CB_Nang_Cap_AH,"NangCapA.H"))
        self.CB_Tai_Thiet.clicked.connect(lambda: self.Set_Config(self.CB_Tai_Thiet,"TaiThiet"))
        self.CB_Uoc.clicked.connect(lambda: self.Set_Config(self.CB_Uoc,"Uoc"))

        self.CB_DapLua.clicked.connect(lambda: self.Set_Config(self.CB_DapLua,"DapLua"))
        self.CB_XayDung.clicked.connect(lambda: self.Set_Config(self.CB_XayDung,"XayDung"))
        self.CB_Chieu_Mo_AH.clicked.connect(lambda: self.Set_Config(self.CB_Chieu_Mo_AH,"ChieuMoA.H"))
        self.CB_Bua_San_Luong.clicked.connect(lambda: self.Set_Config(self.CB_Bua_San_Luong,"BuaSanLuong"))
 
        self.CB_Nghien_Cuu.clicked.connect(lambda: self.Set_Config(self.CB_Nghien_Cuu,"NghienCuu"))
        self.CB_Skill_Lanh_Chua.clicked.connect(lambda: self.Set_Config(self.CB_Skill_Lanh_Chua,"SkillLanhChua"))
        self.CB_Di_Thu_Mo.clicked.connect(lambda: self.Set_Config(self.CB_Di_Thu_Mo,"DiThuMo"))
        self.CB_Khien_Nc.clicked.connect(lambda: self.Set_Config(self.CB_Khien_Nc,"KhienN.C"))

        self.CB_May_Ban_Da.clicked.connect(lambda: self.Set_Config(self.CB_May_Ban_Da,"MayBanDa"))
        self.CB_Kho_Bau_Bi_An.clicked.connect(lambda: self.Set_Config(self.CB_Kho_Bau_Bi_An,"KHoBauBiAn"))
        self.CB_Thu_Thap_Kiet_Xuat.clicked.connect(lambda: self.Set_Config(self.CB_Thu_Thap_Kiet_Xuat,"ThuThapKietXuat"))
        self.Cb_Ruong_KVK.clicked.connect(lambda: self.Set_Config(self.Cb_Ruong_KVK,"RuongKVK"))
        self.Cb_Ruong_Ba_Chu.clicked.connect(lambda: self.Set_Config(self.Cb_Ruong_Ba_Chu,"RuongBaChu"))
        self.Cb_Gac_Lau_Kho_Bau.clicked.connect(lambda: self.Set_Config(self.Cb_Gac_Lau_Kho_Bau,"GacLauKhoBau"))

# Set Click Button
    # Setting
        self.pushButton.clicked.connect(lambda: self.Button_Caidat_Adb())
        self.Btn_Open_Farm_Info.clicked.connect(lambda: self.Click_Button_Open_Farm_InFo())
        self.Btn_Login_Next.clicked.connect(lambda: self.Click_Button_Login_Next())

    # Tab Farm Acc
        self.pushButton_4.clicked.connect(lambda: self.Click_Button_Start())
        self.pushButton_5.clicked.connect(lambda: self.Click_Button_Stop())
        self.Btn_Mua.clicked.connect(lambda : self.Show_Buys())
        
    # Tab Event
        self.Btn_MoTaiNguyen.clicked.connect(lambda: self.Click_Button_Start_MoDa_Quy())
        self.Btn_MoTaiNguyen_5.clicked.connect(lambda: self.Click_Button_Start_MoTinNhan())
        self.Btn_MoTaiNguyen_4.clicked.connect(lambda: self.Click_Button_Start_EpKhien())

    # Tab MainAcc
        self.Btn_Start_DanhQuaiVat.clicked.connect(lambda: self.Click_Button_Start_DanhQuaiVat())
        self.Btn_Start_DanhQuaiVat_2.clicked.connect(lambda: self.Click_Button_Start_DanhVienCo())
        self.Btn_Start_DanhQuaiVat_3.clicked.connect(lambda: self.Click_Button_Start_GomRss())
    

    # Show Gui
        self.show()

# CLick Button
    # Tab Farm Acc
    def Click_Button_Start(self):
        '''Button Start'''
        
        if self.Combobox_SetTitlets():
            self.Btn_Login_Next.setDisabled(True)
            text = self.pushButton_4.text()
       #     get_Time()

            if Get_Hansudung > showtime.Time_GMT:
                if text == "Start":
                    print(self.Nox_Name, "__", self.id_device)
                    print("_____Start_____")
                    self.pushButton_4.setText("Pause")

                    # Show Time
                    showtime.Start()

                    # Start Bot
                    
                    self.Main_Bot.Start_MainBot_ChucNang()



                if text == "Pause":
                    print("_____Pause_____")
                    self.pushButton_4.setText("Continue")

                    # Show Time
                    showtime.Pause()

                    #Pause Bot
                    self.Main_Bot.Pause()


                if text == "Continue":
                    print("_____Continue_____")
                    self.stopped_time = True
                    self.pushButton_4.setText("Pause")

                    # Show Time
                    showtime.Continue()

                    #Continue Bot
                    self.Main_Bot.Continue()

            else:
                choice = QtWidgets.QMessageBox.question(self, 'Lỗi',
                                                        " 'Vui Lòng Liên Hệ Nhà Cung Cấp Để Thêm Thời Gian Sử Dụng'?",
                                                        QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    # subprocess.call(['notepad.exe', 'DataText/Adb.txt'])
                    return False
                if choice == QMessageBox.No:
                    return False

    def Click_Button_Stop(self):
        """Button Stop"""
        print("_____Stop_____")
        self.Btn_Login_Next.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.pushButton_4.setText("Start")
        
        try:
            # show_time
            showtime.Stop()
            
            #Stop MainBot
            self.Main_Bot.Stop()
            self.LB_Running.setText("      ")
             
        except:
            pass

    def Click_Button_Login_Next(self):
        if self.Combobox_SetTitlets():
            self.pushButton_4.setDisabled(True)
            self.Btn_Login_Next.setDisabled(True)

            self.Main_Bot.Start_Login_Next()


    #Tab MainAcc
    def Click_Button_Start_DanhVienCo(self):


        text = self.Btn_Start_DanhQuaiVat_2.text()
        if self.Combobox_SetTitlets():
           if Get_Hansudung > showtime.Time_GMT:
    
            if text == "Start":
                print(self.Nox_Name, "__", self.id_device)
                print("_____Start_____")
                self.Btn_Start_DanhQuaiVat_2.setText("Stop")
                self.Main_Bot.Start_Danh_VienCo()


            if text == "Stop":

                print("_____Stop_____")
                self.Btn_Start_DanhQuaiVat_2.setText("Start")

                self.Main_Bot.Stop()


        else:
            choice = QtWidgets.QMessageBox.question(self, 'Lỗi',
                                                        " 'Vui Lòng Liên Hệ Nhà Cung Cấp Để Thêm Thời Gian Sử Dụng'?",
                                                        QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                    # subprocess.call(['notepad.exe', 'DataText/Adb.txt'])
                return False
            if choice == QMessageBox.No:
                return False

    def Click_Button_Start_GomRss(self):


        text = self.Btn_Start_DanhQuaiVat_3.text()
        if self.Combobox_SetTitlets():
           if Get_Hansudung > showtime.Time_GMT:
    
            if text == "Start":
                print(self.Nox_Name, "__", self.id_device)
                print("_____Start_____")
                self.Btn_Start_DanhQuaiVat_3.setText("Stop")
                self.Main_Bot.Start_GomRss()


            if text == "Stop":

                print("_____Stop_____")
                self.Btn_Start_DanhQuaiVat_3.setText("Start")

                self.Main_Bot.Stop()


        else:
            choice = QtWidgets.QMessageBox.question(self, 'Lỗi',
                                                        " 'Vui Lòng Liên Hệ Nhà Cung Cấp Để Thêm Thời Gian Sử Dụng'?",
                                                        QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                    # subprocess.call(['notepad.exe', 'DataText/Adb.txt'])
                return False
            if choice == QMessageBox.No:
                return False

    def Tao_Tab_Leve_Monter(self):
        self.QuaiVatMin = self.CBbox_MoTaiNguyen_3.currentText()
        self.QuaiVatMax = self.CBbox_MoTaiNguyen_2.currentText()
        list_ChonQuai = list(range(int(self.QuaiVatMin) ,int(self.QuaiVatMax)+1, +1))

        self.tableWidget.setRowCount(int(len(list_ChonQuai)))

        for a in range(0,int(len(list_ChonQuai))):
            capquai = list_ChonQuai[a]
            self.tableWidget.setItem(a, 0, QtWidgets.QTableWidgetItem(str(capquai)))

    def Click_Button_Start_DanhQuaiVat(self):

        text = self.Btn_Start_DanhQuaiVat.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > showtime.Time_GMT:
                if text == "Start":
                    print(self.Nox_Name, "__", self.id_device)
                    print("_____Start_____")
                    self.Btn_Start_DanhQuaiVat.setText("Stop")
                    self.Tao_Tab_Leve_Monter()
                    
                    self.Main_Bot.Start_Danh_QuaiVat()

             
                else:

                    print("_____Stop_____")
                    self.Btn_Start_DanhQuaiVat.setText("Start")
                    self.tableWidget.setRowCount(0)
                    self.Main_Bot.Stop()


            else:
                choice = QtWidgets.QMessageBox.question(self, 'Lỗi',
                                                            " 'Vui Lòng Liên Hệ Nhà Cung Cấp Để Thêm Thời Gian Sử Dụng'?",
                                                            QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                        # subprocess.call(['notepad.exe', 'DataText/Adb.txt'])
                    return False
                if choice == QMessageBox.No:
                    return False

    #Tab Event
    def Click_Button_Start_MoDa_Quy(self):
        """Button Mở Đá Quý"""

        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen.text()
            if text == "Start":
                self.Btn_MoTaiNguyen.setText("Stop")
                showtime.Start()
                self.Main_Bot.Start_MoTaiNguyen()

            else:
                self.Btn_MoTaiNguyen.setText("Start")
                self.Main_Bot.Stop()
                showtime.Stop()

    def Click_Button_Start_MoTinNhan(self):
        print(self.Text_MoTinNhan)

        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen_5.text()
            if text == "Start":
                self.Btn_MoTaiNguyen_5.setText("Stop")
                showtime.Start()
                self.Main_Bot.Start_MoTinNhan()

            else:
                self.Btn_MoTaiNguyen_5.setText("Start")
                self.Main_Bot.Stop()
                showtime.Stop()

    def Click_Button_Start_EpKhien(self):
        print(self.Text_KhienNoiChien)

        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen_4.text()
            if text == "Start":
                self.Btn_MoTaiNguyen_4.setText("Stop")
                showtime.Start()
                self.Main_Bot.Start_EpKhien()

            else:
                self.Btn_MoTaiNguyen_4.setText("Start")
                self.Main_Bot.Stop()
                showtime.Stop()

    # Setting 
    def Button_Caidat_Adb(self):
        '''Nút Mở Cài Đặt Adb'''
        subprocess.call(['notepad.exe', 'DataText/Adb.txt'])

    def Click_Button_Open_Farm_InFo(self):
        if self.Window_Farm_Info == None:
            self.Window_Farm_Info = Gui_Farm_Info(self)
            self.Window_Farm_Info.show()

        else:
            self.Window_Farm_Info.close()
            self.Window_Farm_Info = None

    def Show_Buys(self):

        if self.Window_Buys == None:
            self.Window_Buys = Gui_buys(self)
            self.Window_Buys.show()
        else:
            self.Window_Buys.close()
            self.Window_Buys = None

    def Set_Delay(self):
        Get_Time_Delay = self.CBBox_Delay.currentText()
        Setting_Bot.Delay = 0.05
 

        if Get_Time_Delay == "60":
            Setting_Bot.Delay_CLick = 0.16

        if Get_Time_Delay == "70":
            Setting_Bot.Delay_CLick = 0.14

        if Get_Time_Delay == "80":
            Setting_Bot.Delay_CLick = 0.12

        if Get_Time_Delay == "90":
            Setting_Bot.Delay_CLick = 0.1

        if Get_Time_Delay == "100":
            Setting_Bot.Delay_CLick = 0.08

        if Get_Time_Delay == "110":
            Setting_Bot.Delay_CLick = 0.05

        print("Delay While, Seach image :",Setting_Bot.Delay)
        print("Delay Click :",Setting_Bot.Delay_CLick )

    def closeEvent(self, event):
        """Event Close"""
        SaveTime()

        try:
            print("Exit Application")

            # Stop Thow Time
            self.timer.stop()
            # Close Gui Bot
            self.close()
            #Stop Main Bot
            self.Main_Bot.Stop()


            # Close Của Sổ Farm Info
            self.Window_Farm_Info.close()
            

            sys.stdout = sys.__stdout__
            sys.exit()

        except:
            pass
    
# Func
    def Set_Config(self,bunton,Key):
        '''Set Config'''
        bunton.isChecked()
        if bunton.isChecked():
            self.Config.setValue(Key,1)
        else:
            self.Config.setValue(Key,0)

    def Set_Config_ComBoBox(self,ComBobox,Key):
        '''Set Config ComboBox'''
        self.Config.setValue(Key,ComBobox.currentText())
        if Key == "Delay":
            self.Set_Delay()


        if Key == "Delay_Load_Image":
            Setting_Bot.Delay_Load_Image = int(ComBobox.currentText())
            print( Setting_Bot.Delay_Load_Image )

    def Doc_Va_Tao_Data_Farm(self):
        """Đọc File Data Farm Account, Tạo File Running Farm Account"""

        with SQLite('DataText/Farm_Info.db') as cur:
            cur.execute("SELECT Email , Password , SoDao , LoaiMo ,CapMo, NangCapAH , XayNha , MainAcc from Farm_Info")
            data = cur.fetchall()
            for row in data:
                self.List_Email_Farm_Acount.append(row[0])
                self.List_Password_Farm_Account.append(row[1])
                self.List_So_Dao.append(row[2])
                self.List_Loai_Mo.append(row[3])
                self.List_CapMo.append(row[4])
                self.List_NangCapAnhHung.append(row[5])
                self.List_XayNha.append(row[6])
                self.List_MainAcc.append(row[7])
            

        with SQLite('DataText/running.db') as cur:
            cur.execute("""DELETE FROM running""")
            for i in self.List_Email_Farm_Acount:
                cur.execute("""INSERT INTO running 
                (Email, DiemDanh, KhieuChienRong, ChoixucXac, DoiHuyChuong, CongHienLienMinh,\
                Naprong, Taithiet, LuyenLinh, NangCapAnhHung, BuaSanLuongMo, Uoc, TriThuong, ThayPhap, GuiDaQuy, XayDung, HoatDongLienMinh, DiemDanhDienDan) 
                VALUES 
                (?, ? ,?, ?, ?, ? ,?, ?, ?, ? ,?, ?,?,?,?,?,?,?)""", (str(i), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0))

    def Get_Title_Nox(self):
        '''Combobox Get titles'''
        # Set Button Start Nếu Của sổ Thứ 2 mở Lên
        titles2 = set()
        def gethwnd2(hwnd, nouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles2.add(win32gui.GetWindowText(win32gui.FindWindow("Qt5152QWindowIcon", win32gui.GetWindowText(hwnd))))

        win32gui.EnumWindows(gethwnd2, 0)
        titlet2 = [t for t in titles2 if t]
        titlet2.sort()
        # Get Seri hhd
        c = wmi.WMI()
        Seri_hhd_number = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
        if 'RiseOfTheKing_Bot' in titlet2:
            # Admin
            if Seri_hhd_number == "0025_3854_0140_0908.":
                pass
            else:
                self.pushButton_4.setDisabled(True)

        titles = set()

        def gethwnd(hwnd, nouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles.add(win32gui.GetWindowText(win32gui.FindWindow("Qt5QWindowIcon", win32gui.GetWindowText(hwnd))))

        win32gui.EnumWindows(gethwnd, 0)
        titlet = [t for t in titles if t]
        titlet.sort()
        print(titlet)


        if 'Garena - Trò chơi' in titlet:
            titlet.remove('Garena - Trò chơi')

        if 'Tin Nhắn Hệ Thống' in titlet:
            titlet.remove('Tin Nhắn Hệ Thống')

        if 'Hệ Thống Xử Phạt' in titlet:
            titlet.remove('Hệ Thống Xử Phạt')
 
        return titlet

    def Combobox_SetTitlets(self):
        '''Combobox Set Titles, Trả lại Địa chỉ Adb'''

        self.Nox_Name = str(self.CBBox_ChonTitle.currentText())
        try:
            dladb = [line.rstrip()
                     for line in open("DataText/Adb.txt", "r")]
            sttadb = dladb.index(self.Nox_Name)
            if sttadb == 0:
                self.id_device = dladb[1]

            if sttadb == 2:
                self.id_device = dladb[3]

            if sttadb == 4:
                self.id_device = dladb[5]

            if sttadb == 6:
                self.id_device = dladb[7]

            if sttadb == 8:
                self.id_device = dladb[9]

        except:
            self.label_2.setText("Error  Adb Address ")

            choice = QtWidgets.QMessageBox.question(self, 'Lỗi', " 'Kiểm Tra Lại ADB và Reset Auto'?",
                                                    QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                subprocess.call(['notepad.exe', 'DataText/Adb.txt'])
                return False
            if choice == QMessageBox.No:
                return False

        self.label_2.setText(self.id_device)

        # self.Nox_Name= adbhientai
        Main_Bot.c_name = self.Nox_Name
        controller.c_id_device = self.id_device
        controller.c_name = self.Nox_Name

        hwnd = win32gui.FindWindow(None, self.Nox_Name)
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        win32gui.MoveWindow(hwnd, x0, y0, 383, 708, True)
        return True

# Signal MainBot
    def Thread_Main_bot_Update_ComBobox_ChonAcc(self,email_set_combobox):
        self.CBbox_Chon_Acc.setCurrentIndex(self.List_Email_Farm_Acount.index(email_set_combobox))
        
    def Thread_Main_Bot_ThongBaoLoiNox(self):
        choice = QtWidgets.QMessageBox.question(self, 'Lỗi', " 'Cửa Sổ NoxPlay Không Tồn Tại'?",
                                                    QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            return True
        if choice == QMessageBox.No:
            return False

    def Thread_Main_bot_Update_KhoangCach_DanhQuai(self,capquai : int, khoangcach :int):
        str_khoangcach = "0x"
        if khoangcach == 10:
            str_khoangcach = "10x"
        if khoangcach == 20:
            str_khoangcach = "20x"
        if khoangcach == 30:
            str_khoangcach = "30x"
        if khoangcach == 40:
            str_khoangcach = "40x"
        if khoangcach == 50:
            str_khoangcach = "50x"
        if khoangcach == 60:
            str_khoangcach = "60x" 
        if khoangcach == 70:
            str_khoangcach = "70x"
        if khoangcach == 80:
            str_khoangcach = "80x"
        if khoangcach == 90:
            str_khoangcach = "90x"
        if khoangcach == 100:
            str_khoangcach = "100x"  

        self.QuaiVatMin = self.CBbox_MoTaiNguyen_3.currentText()
        self.QuaiVatMax = self.CBbox_MoTaiNguyen_2.currentText()

        list_ChonQuai = list(range(int(self.QuaiVatMin) ,int(self.QuaiVatMax)+1, +1))
        Vitri_quai = list_ChonQuai.index(capquai)

        self.tableWidget.setItem(Vitri_quai, 1, QtWidgets.QTableWidgetItem(str_khoangcach))

# Signal ShowTime
    # Lable Time
    def Lable_Time_GMT(self,Str_Time):
        self.LB_Time_GMT.setText(str(Str_Time))
  
    def Lable_TimeTong(self,Str_Time):
        self.LB_Time_Run_1_Vong.setText(str(Str_Time))

    def Lable_Time_1Acc(self,Str_Time):
        self.LB_Time_Run_1_Acc.setText(str(Str_Time))

    def Lable_Time_1ChucNang(self,Str_Time):
        self.LB_Time_Run_Chuc_Nang.setText(str(Str_Time))

    def Lable_Time_HanSuDung(self,Str_Time):
        self.LB_Han_Su_Dung.setText(str(Str_Time))

    def Reset_File_Data_Running(self):
        with SQLite('DataText/running.db') as cur:
            cur.execute("""DELETE FROM running""")
            for i in self.List_Email_Farm_Acount:
                cur.execute("""INSERT INTO running 
                (Email, DiemDanh, KhieuChienRong, ChoixucXac, DoiHuyChuong, CongHienLienMinh,\
                Naprong, Taithiet, LuyenLinh, NangCapAnhHung, BuaSanLuongMo, Uoc, TriThuong, ThayPhap, GuiDaQuy, XayDung, HoatDongLienMinh, DiemDanhDienDan) 
                VALUES 
                (?, ? ,?, ?, ?, ? ,?, ?, ?, ? ,?, ?,?,?,?,?,?,?)""", (str(i), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0))

    def Lience_HetHanSuDung(self):
        Exit_Event.set()

#Signal Edit_Running

    def Edit_Running(self,Text):   
        self.LB_Running.setText(Text)
        showtime.Reset_Time_Run_Chuc_Nang()




class Main_Bot(QtCore.QThread):

    lock = None
    Thread_1 = None
    Thread_2 = None
    Thread_3 = None
    Sleep_Running = 0.1

    Running = False

    screenshot = None

    w = 0
    h = 0
    hwnd = None
    ThongBaoNox = QtCore.pyqtSignal()
    Update_ComBoBox_ChonAcc = QtCore.pyqtSignal(str)
    Update_KhoangCach_DanhQuai = QtCore.pyqtSignal(int ,int)
  
    def __init__(self,main_Window, parent=None):
        self.main_Window = main_Window


        super().__init__(parent)
        self.lock = Lock()
        
        
    def Main_Bot_Danh_QuaiVat(self):
        """Main_Bot Đánh Quái Vật"""
        self.main_Window.Edit_Running("Kill Monter")
        

        QuaiVatMin = self.main_Window.CBbox_MoTaiNguyen_3.currentText()
        QuaiVatMax = self.main_Window.CBbox_MoTaiNguyen_2.currentText()
        list_ChonQuai = []
        for i in range(int(QuaiVatMin),int(QuaiVatMax)+1):
         #   print(str(i))
            list_ChonQuai.append(str(i))
                

        
        print(list_ChonQuai)
        print(len(list_ChonQuai))
        print(list_ChonQuai[0])
        Quai_LV = 0
        Set_Dao = 2
        KhoangCachXa = 0
        DungBuaNgauNhien = True
        print("Start")
        Tang = False
        Giam = True
        # while True:
        #     if self.MainBot_Stoped: return
        #     if Bot_ChucNang.out_MHchinh():
        #         print("0")

        while True:
            if Exit_Event.wait(timeout=Setting_Bot.Delay) : 
                return
                
            # Danh het Quai Trong List
            print("List Quai con Lai :", list_ChonQuai)
            print(":: Do Dai:",len(list_ChonQuai), "Vi Tri Quai Trong List :", Quai_LV)
            if Quai_LV>= len(list_ChonQuai):
                Quai_LV = 0

            if list_ChonQuai == []:
                if self.main_Window.checkBox.isChecked():
                    Bot_ChucNang.SuDung_BuaNgauNhien()
                    print("DungBuaNgauNhien")


                if Giam:
                        
                    list_ChonQuai = list(range(int(QuaiVatMax) -1 ,int(QuaiVatMin)-1,-1))
                    print("Giảm", list_ChonQuai )
                    Giam = False

                else:
                        
                    list_ChonQuai = list(range(int(QuaiVatMin) ,int(QuaiVatMax)+1, +1))
                    print("Tăng", list_ChonQuai )
                    Giam = True


                # if DungBuaNgauNhien:
                #         print("DungBuaNgauNhien00000000000000000000000000000")

                #     print(list_ChonQuai)
                #     Quai_LV = 0
                #     continue
                    
            # Set Dao >= 5
            if Set_Dao>= 6: 
                Set_Dao =2

            # Kill Quai Vat
            print("Danh Quai :",list_ChonQuai[Quai_LV] )
            Bot_ChucNang.DanhQuai_KVK(CapQuai = list_ChonQuai[Quai_LV],Set_Dao = Set_Dao)

            KhoangCach = Bot_ChucNang.DoKhoangCach()

            self.Update_KhoangCach_DanhQuai.emit(int(list_ChonQuai[Quai_LV]),int(KhoangCach))

            #self.main_Window.Add_KhoangCach(int(list_ChonQuai[Quai_LV]),KhoangCach)

            if KhoangCach <= 10:
                print("Khoang Cach <= 10. Tiep Tuc Danh Quai : ",list_ChonQuai[Quai_LV] )
                Set_Dao +=1
                continue

            if KhoangCach >= 20:
                # KhoangCachXa += 1
                # if KhoangCachXa >
                print("Khoang Cach >= 30. Xoa Quai: ",list_ChonQuai[Quai_LV] ," Khoi List",)
                    

                list_ChonQuai.pop(Quai_LV)
                Set_Dao +=1
                if Quai_LV == 0:
                    continue
                if Quai_LV >= 1:
                    Quai_LV = Quai_LV -1
                    continue

            Set_Dao +=1
            Quai_LV += 1


    def Main_Bot_Run_ChucNang(self):
        
        """Main_Bot_Chức_Năng"""

        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)


        while True:
            if  not Exit_Event.is_set():
                self.main_Window.label_6.setText(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
  
                Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]
                So_Dao_Run = self.main_Window.List_So_Dao[Index_Email_Select]
                Loai_Mo_Run = self.main_Window.List_Loai_Mo[Index_Email_Select]
                Cap_Mo_Run = self.main_Window.List_CapMo[Index_Email_Select]
                NangCap_AnhHung_Run = self.main_Window.List_NangCapAnhHung[Index_Email_Select]
                Xay_Nha_Run =self.main_Window.List_XayNha[Index_Email_Select]
                MainAcc_Run = self.main_Window.List_MainAcc[Index_Email_Select]



    
            # Đăng Nhập 
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Login.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_DangNhap)
                        Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)

                if  not Exit_Event.is_set():
                    if self.main_Window.CB_DapLua.isChecked():
                    #    main_Window.Edit_Running(main_Window.Text_DapLua)
                        Bot_ChucNang.SuaThanhDapLua()
 

            # Nhận Quà Bến Cảng -- 
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_QuaBenCang.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_NhanQuaBenCang)
                        if Bot_ChucNang.NhanQua_BenCang():
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Diem_Danh.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "DiemDanh") == [0]:
                                        self.main_Window.Edit_Running(self.main_Window.Text_DiemDanh)
                                        Bot_ChucNang.Nhan_Qua_DangNhap(Email_Run)


            # Chơi Xúc Xắc
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Choi_Xuc_Xac.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "ChoixucXac") == [0]:
                                        self.main_Window.Edit_Running(self.main_Window.Text_ChoiXucXac)
                                        Bot_ChucNang.Kho_Tang(Email_Run)


            # Khiêu Chiến Rồng
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_DAnh_Ai_Rong.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "KhieuChienRong") == [0]:
                                        self.main_Window.Edit_Running(self.main_Window.Tex_DanhAiRong)
                                        Bot_ChucNang.KhieuChienRong(Email_Run)


            # Chiêu Mộ Anh Hùng --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Chieu_Mo_AH.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_ChieuMoAnhHung)
                        Bot_ChucNang.ChieuMo_AnhHung()
                        if  not Exit_Event.is_set():
                            if self.main_Window.CB_Thay_Phap.isChecked():
                                if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "ThayPhap") == [0]:
                                    self.main_Window.Edit_Running(self.main_Window.Text_ThayPhap)
                                    Bot_ChucNang.Thay_Phap(Email_Run)
    

            # Gửi Đá Quý    
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Gui_Da_Quy.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "GuiDaQuy") ==[0]:
                                        self.main_Window.Edit_Running(self.main_Window.Text_GuiDaQuy)
                                        Bot_ChucNang.Gui_Da_Quy(Email_Run)


            # Hiến Tặng Liên Minh --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Cong_Hien_LM.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "CongHienLienMinh") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_CongHien)
                            Bot_ChucNang.HienTang_LienMinh(Email_Run)


            # Ước Free --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Uoc.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "Uoc") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_Uoc)
                            Bot_ChucNang.Uoc_Free(Email_Run)
 

            # Trị Thương --- Chạy 1 lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Tri_Thuong.isChecked():

                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "TriThuong") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_TriThuong)
                            Bot_ChucNang.Tri_Thuong(Email_Run)


            # Tái Thiết --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Tai_Thiet.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "Taithiet") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_TaiThiet)
                            Bot_ChucNang.Tai_Thiet(Email_Run)


            # Skill Lãnh Chúa --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Skill_Lanh_Chua.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_SkillLanhChua)
                        Bot_ChucNang.Skill_LanhChua()


            # Bùa Sản Lượng Trong Thành --- Theo Vòng Lặp            
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Bua_San_Luong.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_BuaSanLuong)
                        Bot_ChucNang.BuaSanLuong_TrongThanh()


            # RSS Trong Thành --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_RssTrongThanh.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_AnRssTrongThanh)
                        Bot_ChucNang.AnRss_TrongThanh()


            # Xây Dựng
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_XayDung.isChecked():
                        #Đỏi Lại ?Get Chuc nang
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "XayDung") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_XayDung)
                            Bot_ChucNang.NhiemVu_XayDung(Email_Run)


            # Nâng Cấp Anh Hùng --- Chạy 1 lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Nang_Cap_AH.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "NangCapAnhHung") == [0]:
                            self.main_Window.Edit_Running(self.main_Window.Text_NangCapAnhHung)
                            Bot_ChucNang.NangCapAnhHung(Email = Email_Run, vitrianhhung = NangCap_AnhHung_Run)


            # MainAcc

                if  not Exit_Event.is_set():
                    if MainAcc_Run == float(3):
                            self.main_Window.Edit_Running(self.main_Window.Text_ThanhDiaLienMinh)
                            Bot_ChucNang.NhanQua_ThanhDiaLienMinh_MainAcc()
                            
                            if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "HoatDongLienMinh") == [0]:
                                self.main_Window.Edit_Running(self.main_Window.Text_HoatDongLienMinh)
                                Bot_ChucNang.NhanQua_HoaDongLienMinh_MainAcc(Email_Run)
                            Bot_ChucNang.HienTang_LienMinh(Email_Run)


            # Đi Ăn Mỏ RSS --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Di_Thu_Mo.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_DiThuMo)
                        Bot_ChucNang.Di_AnMo(Email_Run,Loai_Mo_Run,Cap_Mo_Run,So_Dao_Run)


            # Khiên Nội Chiến
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Khien_Nc.isChecked():
                        self.main_Window.Edit_Running(self.main_Window.Text_KhienNoiChien)
                        Bot_ChucNang.Khien_Farm(Email_Run,)
                

            # Lấy Và So Sánh Time GMT Với Time Nhận Nhiệm Vụ
                if  not Exit_Event.is_set():
                    print("Time Nhận Nhiệm Vụ :","TimeGMT =",int(showtime.Time_GMT.hour),"Time Set =",int(self.main_Window.CBbox_Time_NhiemVu.currentText().split(':')[0]))
                    if int(showtime.Time_GMT.hour) >= int(self.main_Window.CBbox_Time_NhiemVu.currentText().split(':')[0]):
                        self.main_Window.Edit_Running(self.main_Window.Text_NhanNhiemVu)
                        Bot_ChucNang.Nhan_NhiemVu()


            # Event
                if  not Exit_Event.is_set():
                    if self.main_Window.Cb_Gac_Lau_Kho_Bau.isChecked():
                        self.main_Window.Edit_Running("Đôi Cánh Bầu Trời")
                        Bot_ChucNang.Event_DoiCanhBauTroi()


                if  not Exit_Event.is_set():
                    if self.main_Window.CB_May_Ban_Da.isChecked():
                        self.main_Window.Edit_Running("Máy Bắn Đá")
                        Bot_ChucNang.Event_MayBan_Da()

                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Thu_Thap_Kiet_Xuat.isChecked():
                        self.main_Window.Edit_Running("Thu Thap Kiet Xuat")
                        Bot_ChucNang.Event_ThuThapKietXuat()



                if  not Exit_Event.is_set():
                    if self.main_Window.Cb_Ruong_KVK.isChecked():
                        self.main_Window.Edit_Running("Get The Chest KvK")
                        Bot_ChucNang.Event_RuongKVK()


                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Kho_Bau_Bi_An.isChecked():
                        self.main_Window.Edit_Running("Mysterious Treasure")
                        Bot_ChucNang.Event_KhoBauBiAn()



                if  not Exit_Event.is_set():
                    Index_Email_Select = Index_Email_Select + 1
                    # So sánh Vị Trí hiện tại đến tổng Email
                    if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                        Index_Email_Select = 0
                        showtime.Reset_Time_Run_Tong()
                    

            # Viết File Log
                if  not Exit_Event.is_set():
                    with open("DataText/log.txt","a+",encoding="utf-8") as f:
                        f.write(str(showtime.Time_GMT)+'\n')

            # Set email tiếp theo vào Combobox chọn Account
                if  not Exit_Event.is_set():
                    showtime.Reset_Time_Run_1_Acc()
                    email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                    self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))

                else:
                    return


            else:
                time.sleep(self.Sleep_Running)


    def Main_Bot_Update_Screenshot(self):
        """Main Update Screenshot"""
        loop_time = time.time()

        
        while True:

            if  Exit_Event.is_set():
                return

            if  self.Running:
                #time.sleep(Setting_Bot.Delay)
                if Exit_Event.wait(timeout=Setting_Bot.Delay):
                    return

                #time.sleep(0.06)
                # print("Delay Click = ",Setting_Bot.Delay,end="\r")
                # print(end="\n")

                self.screenshot = self.get_screenshot(self.main_Window.Nox_Name)
                if self.screenshot is None:
                    self.ThongBaoNox.emit()

                    self.Stop()
                    return



                self.lock.acquire()

                Bot_ChucNang.Update_Screenshot(self.screenshot)

                self.lock.release()
                # print('FPS {}'.format(1 / (time.time() - loop_time)))
                # loop_time = time.time()

            else:
                time.sleep(self.Sleep_Running)


    def Main_Bot_Login_Next(self):
        """Main_bot_Login_Next"""
        self.main_Window.Edit_Running(self.main_Window.Text_Login_Next)
        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account + Them 1
        print(self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select))
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select) + int(1)

        self.main_Window.label_6.setText(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))

    
        if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
            Index_Email_Select = 0
        #Set Email Vào ComBoBox


        Email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
        self.Update_ComBoBox_ChonAcc.emit(str(Email_set_combobox))
        



        Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
        Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]
        
        Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)


        self.main_Window.pushButton_4.setDisabled(False)
        self.main_Window.Btn_Login_Next.setDisabled(False)

        # Stop MainBot
        self.Stop()
        return


    # Tab Event
    def Main_Bot_MoTaiNguyen(self):
        """Main_Bot Mở Tài Nguyên """


        self.main_Window.Edit_Running(self.main_Window.Text_MoDa_quy)

        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)


        while True:
            if Exit_Event.is_set() : 
                return
            self.main_Window.label_6.setText(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            

            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
            Bot_ChucNang.MoDa_Quy(self.main_Window.CBbox_MoTaiNguyen.currentText())

            if not Exit_Event.is_set():
                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    showtime.Reset_Time_Run_Tong()
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen.setText("Start")
                    self.Stop()
                    return
                    
                
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))
            else:
                return

    def Main_Bot_MoTinNhan(self):
        """Main_Bot Mở Tin Nhan """

        

        self.main_Window.Edit_Running(self.main_Window.Text_MoTinNhan)

        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)


        while True:
            if Exit_Event.is_set(): 
                return

            self.main_Window.label_6.setText(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            

            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
            Bot_ChucNang.DocThu()

            if not Exit_Event.is_set(): 

                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    showtime.Reset_Time_Run_Tong()
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen_5.setText("Start")
                    self.Stop()
                    return
                    
                
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))

            else:
                return

    def Main_Bot_EpKhien(self):
        """Main_Bot Ep khien """


        self.main_Window.Edit_Running(self.main_Window.Text_KhienNoiChien)

        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)

        Loai_Khien = self.main_Window.CBbox_MoTaiNguyen_4.currentText()
        if Loai_Khien =="8h":
            int_LoaiKhien = 1

        if Loai_Khien =="24h":
            int_LoaiKhien = 2

        if Loai_Khien =="3Day":
            int_LoaiKhien = 3
        while True:
            if Exit_Event.is_set() : 
                return
            self.main_Window.label_6.setText(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            

            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)

            Bot_ChucNang.Khien_Farm(Email = Email_Run,Ep_Khien= True,loaikhien= int_LoaiKhien )

            if not Exit_Event.is_set():
                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    showtime.Reset_Time_Run_Tong()
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen.setText("Start")
                    self.Stop()
                    return
                    
                
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))
            else:
                return



    

#Tab MainAcc       

    def Main_Bot_GomRss(self):
        """Main_Bot Gom Rss"""
        self.main_Window.Edit_Running("Gom Rss")
        self.main_Window.lineEdit_2.setText("0")
        

        TuAcc = self.main_Window.CBBox_ChonTitle_2.currentText()
        DenAcc = self.main_Window.CBBox_ChonTitle_3.currentText()
        List_GomRss = list(range(int(TuAcc) ,int(DenAcc)+1))
        if List_GomRss == []:
            self.Stop()
            return

        Set_TuAcc = int(TuAcc) - 1

        LuotAcc = 0 
        Set_Dao = 2
        SoLan_DaDanh = 0
        Saikhac = 0
        Solan_CanDanh = self.main_Window.lineEdit.text()
        while True:
            if Exit_Event.wait(timeout=Setting_Bot.Delay):
                return
            

            if LuotAcc >= len(List_GomRss):
                self.main_Window.Btn_Start_DanhQuaiVat_3.setText("Start")
                self.Stop()
                return

            if Saikhac >= 3:
                self.main_Window.Btn_Start_DanhQuaiVat_3.setText("Start")
                self.Stop()
                return

            Acc_Dang_Danh = List_GomRss[int(LuotAcc)]


            if Bot_ChucNang.GomRss(Vi_Tri_Acc= int(Acc_Dang_Danh), Set_Dao = Set_Dao):
                SoLan_DaDanh +=1
                print("Da Danh",SoLan_DaDanh)
                self.main_Window.lineEdit_2.setText(str(SoLan_DaDanh))
                Set_Dao += 1
                if Set_Dao >= 3:
                    Set_Dao = 2
            else:
                Saikhac +=1
                continue

            if SoLan_DaDanh >= int(Solan_CanDanh):
                SoLan_DaDanh = 0

                 
                Set_TuAcc +=1
                self.main_Window.CBBox_ChonTitle_2.setCurrentIndex(Set_TuAcc )
                LuotAcc +=1
                

    def Main_Bot_Danh_VienCo(self):
        """Main_Bot Đánh Quái Vật"""
        self.main_Window.Edit_Running("Dreadlord's Arrival")


        while True:
            if  Exit_Event.is_set():
                return
            if self.screenshot is None: continue
            Bot_ChucNang.Danh_VienCo()


#Start
    def Start_MoTinNhan(self):
        """Mo Tin Nhan"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_MoTinNhan, daemon=True)
            self.Thread_1.start()


    def Start_EpKhien(self):
        """Ep Khien"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_EpKhien, daemon=True)
            self.Thread_1.start()



    def Start_Login_Next(self):
        """Login Next"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" + str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Login_Next, daemon=True)
            self.Thread_1.start()

#  Start Tab MainAcc
    def Start_Danh_VienCo(self):
        """Danh Vien Co"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Danh_VienCo, daemon=True)
            self.Thread_1.start()

    def Start_GomRss(self):
        """Gom Rss"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_GomRss, daemon=True)
            self.Thread_1.start()



    def Start_MoTaiNguyen(self):
        """Mo Tai Nguyen"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" + str(self.main_Window.Nox_Name)+ "]", target=self.Main_Bot_MoTaiNguyen, daemon=True)
            self.Thread_1.start()


    def Start_Danh_QuaiVat(self):
        """Kill Monter KVK"""
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" + str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Danh_QuaiVat, daemon=True)
            self.Thread_1.start()


    def Start_MainBot_ChucNang(self):
        '''MainBot Chuc Nang'''
        self.Start()
        print(self.Thread_1)
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" + str(self.main_Window.Nox_Name) + "]", target= self.Main_Bot_Run_ChucNang, daemon=True)
            self.Thread_1.start()

        else:
            print("asdas")







# Controller



    def Start(self):
        print("[...Start_MainBot...]")
        time.sleep(0.2)
        Exit_Event.clear()

        self.Running = True

        Bot_ChucNang.Start()


        if self.Thread_2 == None:
            self.Thread_2 = Thread(name="Update_Screenshot [" + str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Update_Screenshot, daemon=True)
            self.Thread_2.start()



        if self.Thread_3 == None:
            self.Thread_3 = Thread(name="Running_Close_QuangCao[" + str(self.main_Window.Nox_Name) + "]", target=Bot_ChucNang.Close_QuangCao, daemon=True)
            self.Thread_3.start()



    def Pause(self):
        print("[...Pause_MainBot...]")
        Bot_ChucNang.Pause()
        self.Running = False
        


        
        
    def Continue(self):
        print("[...Continue_MainBot...]")
        Bot_ChucNang.Continue()
        self.Running = True

        
  
    def Stop(self):
        print("[...Stop_MainBot...]")
        Bot_ChucNang.Stop()
        self.main_Window.label_6.setText("Email :")
        
        self.Running = False
        Exit_Event.set()

        
        self.Thread_1 = None
        self.Thread_2 = None
        self.Thread_3 = None
        time.sleep(0.2)

    def get_screenshot(self,hwnd):
        """"ScreenShot"""
        try:
            self.hwnd = win32gui.FindWindow(None, hwnd)#self.c_name)

            (left, top, right, bottom) = win32gui.GetWindowRect(self.hwnd)
            self.w = right - left
            self.h = bottom - top

            # get the window image data
            wDC = win32gui.GetWindowDC(self.hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            if cDC == 0:
                print('saveDC = ', cDC)
                return None
            dataBitMap = win32ui.CreateBitmap()

            dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

            signedIntsArray = dataBitMap.GetBitmapBits(True)
          #  img = np.fromstring(signedIntsArray, dtype='uint8')
            img = frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (self.h, self.w, 4)

            # free resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            img = img[..., :3]
            img = img[:, :, ::3]

            img = ascontiguousarray(img)
            # trả về  cv2 . cvtColor ( img ,  cv2 . COLOR_BGRA2RGB )

            return img

        except:
            print('Exception')
            return None

      


if __name__ == "__main__":
 
    # Đọc Thông Tin Lic
    Get_Hansudung = Lic_info().Farm_DocLic()

    print(Get_Hansudung)


    #showtime = showtime()

    Bot_ChucNang = Bot_ChucNang()


    app = QtWidgets.QApplication(sys.argv)


    # Set Style

#    \ app.setStyle("QtCurve")

    tmain_Window = Gui_Auto()

    sys.exit(app.exec_())