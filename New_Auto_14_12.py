
import os
import subprocess
import sys
from threading import Thread, Lock, Event
import wmi
import win32gui,win32ui,win32con

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QSettings
from PyQt5.QtWidgets import QMessageBox

from numpy import frombuffer, shape , ascontiguousarray
import time

from New_Data_Image import *


from datetime import datetime

from New_BotChucNang_14_12 import Bot_ChucNang, controller
from SQL_DB import SQLite
import configparser

from datetime import timedelta,datetime
import wmi
from cryptography.fernet import Fernet

class Lic_info:
    # Tạo mẫu Khóa
    # with open('filekey.key', 'wb') as filekey:
    #     filekey.write(key)

    Mau_Khoa = None
    Key_MauKhoa =None
    ThoiGian_HienTai = None
    HanSuDung = None


    def __init__(self):
        # Nếu Mẫu khóa Tồn Tại
        
        # Tạo Mẫu Khóa
        # try:
        #     with open('filekey.key', 'rb') as filekey:
        #         self.Mau_Khoa  = filekey.read()
        #     self.Key_MauKhoa = Fernet(self.Mau_Khoa)

        # except:
        #   pass

        # Mẫu Khóa
        self.Key_MauKhoa = Fernet(b'gvSG8sgM-k-Pc3yrJGHGcc_IiqBrZnXTE6ORhaDlb6c=')

        # Thời Gian Bây Giờ
        self.Time_now = datetime.utcnow()
        self.String_Time_Now = self.Time_now.strftime("%d-%m-%Y %H:%M:%S")




    def Tao_Lic(self,Seri_hhd,  Han_SuDung : int ):
        """Nhập Seri HHd - Hạn Sử Dụng (Ngày)"""
        # Nhập Seri HHD

        # Thêm Ngày Sử Dụng
        Ngay_HetHan = self.Time_now + timedelta(days= Han_SuDung)

        # Fomat Time
        String_Ngay_HetHan = Ngay_HetHan.strftime("%d-%m-%Y %H:%M:%S")
        Str_Key = str(str('@') + str('SeriHhd') + str('@') + str(Seri_hhd) + str('@')+ str("NgayCap") + str('@') + str(self.String_Time_Now) + str('@')+ str("HanSuDung") + str('@')+ str(String_Ngay_HetHan) + str('@') + str("Farme"))
        print(Str_Key)

        #  Mã Hóa
        info_key = bytes(Str_Key.encode())
        Key_Ma_Hoa = self.Key_MauKhoa.encrypt(info_key)

        #Tạo File Lience
        with open('licence.lience', 'wb') as FileLic:
            FileLic.write(Key_Ma_Hoa)
        print(Key_Ma_Hoa)


    def Farm_DocLic(self):
        """Nhập Seri HHd"""
                
        #Get Seri hhd
        try:
            c = wmi.WMI()
            Seri_hhd_number = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
    
            # Mở File Lience
            with open('licence.lience', 'rb') as FileLic:
                Doc_Licence = FileLic.read()

            # Đọc Key
            Key_info = self.Key_MauKhoa.decrypt(Doc_Licence)

            #Chuyển Key_info To String
            Key_info =str(Key_info)

            # Tách Chuỗi Key_info
            List_key = Key_info.split('@')

            # Set
            Lic_Seri_Hhd = List_key[2]
            Lic_NgayCap = List_key[4]
            Lic_HanSuDung = List_key[6]

            print("Lience :",List_key)
            print("Seri Hhd Trong Máy :",Seri_hhd_number)
            
            # So Sánh Seri hhd Với List_Key:
            print("Seri Hhd Trong File Lience:",Lic_Seri_Hhd)
            if Lic_Seri_Hhd == Seri_hhd_number:
                print("Ngày Cấp :", Lic_NgayCap)
                print("Hạn Sử Dụng :",Lic_HanSuDung)
                
                self.HanSuDung = datetime.strptime(Lic_HanSuDung,"%d-%m-%Y %H:%M:%S")

                hansudung = datetime.strptime(Lic_HanSuDung,"%d-%m-%Y %H:%M:%S")
                hientai = datetime.strptime(Lic_NgayCap,"%d-%m-%Y %H:%M:%S")

                print("Hết Hạn Sau :" ,hansudung - hientai )
                return self.HanSuDung

            else:
                print("Lience Lỗi Không Khớp Seri Hhd")
                if self.HanSuDung == None:
                    self.HanSuDung = datetime.strptime(self.String_Time_Now,"%d-%m-%Y %H:%M:%S")
                    print(self.HanSuDung)
                    return self.HanSuDung
                    
        except:
            print("Lience Lỗi")
            self.HanSuDung = datetime.strptime(self.String_Time_Now,"%d-%m-%Y %H:%M:%S")
            print(self.HanSuDung)
            return self.HanSuDung 


Exit_Event = Event()

File_config = configparser.ConfigParser()
File_config.read('DataText/ConfigAuto.ini')

if  File_config.get('ChucNang', 'language') == "English":
    # Main Acc
    Text_Login_Next = "Login Next"
    Text_ThanhDiaLienMinh = "Alliance Sanctuary"
    Text_HoatDongLienMinh = "Alliance Activities"
    # Tab MainAcc
    Text_Level_Min= "Level Min :"
    Text_Level_MAx= "Level Max :"
    Text_BuaNgauNhien= "Rdm Teleport Spell"
    Text_TheLuc= "Stamina"
    Text_TuAcc= "From Acc :"
    Text_DenAcc= "To Acc :"
    Text_SoLan ="Times :"
    Text_DaDanh ="Complete :"
    Text_Grupbox_DiQuanXamLuoc = "The Outsider Has Come"
    Text_Grupbox_QuaiVatVienCo = "Dreadlord's Arrival"

    #FarmAcc
    Text_GropBox_Chay1Lan = "Run 1 Time"
    Text_GropBox_ChaytheoVongLap = "Run In The Loop"
    Text_DangNhap = "Login"
    Text_NhanQua_BenCang = "Port Cargo"
    Text_DiemDanh = "Receive Attendance Gift"
    Text_ChoiXucXac = "Yanna en'Marth"
    Text_DanhAiRong = "Dragon's Challenge"
    Text_TriThuong = "Healing"
    Text_An4Mo = "Collect 4 Types"
    Text_DapLua = " Put Out Fires"
    Text_GuiDaQuy = "Bank Deposit"
    Text_ThayPhap = "Drunken Wizard"
    Text_CongHien = "Alliance Donation"
    Text_NapRong = "D.Port Of The Void"
    Text_LuyenLinh = "Soldier Training"
    Text_DoiHuyChuong = "Changing Medals"
    Text_NangCapAnhHung = "Hero Upgrade"
    Text_TaiThiet = "Reset Equipment"
    Text_Uoc = "Wish 20 Times"
    Text_AnRssTrongThanh = "Rss In City"
    Text_XayDung = "Building Uppgrade"
    Text_ChieuMoAnhHung = "Hero Summons"
    Text_BuaSanLuong = "Farm Boost"
    Text_KiemTraVip = "Check Vip"
    Text_NghienCuu = "Technology Research"
    Text_SkillLanhChua ="Lord Skill"
    Text_DiThuMo = "Go Collect Rss"
    Text_KhienNoiChien = "Civil War Shield"

    # Event Hàng Ngày
    Text_MayBanDa = "Catapult: Discount"
    Text_KhobauBian = "Mysterious Treasure"
    Text_ThuThapKietXuat = "Green Thumb"
    Text_RuongKVK = "Chest of Kvk"
    Text_RuongBaChu = "Treasure Chest"
    Text_Gac_Lau_Kho_Bau = "Loft Of Treasures"
    Text_DoiCanhBauTroi = "Sky Wings"
    Text_NhanNhiemVu = "Get Daily Quests"

    #Tab Farm Event
    Text_GropBox_MoTaiNguyen = "Open Resources"
    Text_GropBox_EpKhien = "Force Shield"
    Text_GropBox_Docthu = "Open Messages"
    Text_MoDa_quy = " Open Gems"
    Text_MoTinNhan = "Open Messages"
    Text_LoaiKhien = "Shield Type"
    Text_TuMua = "Self-Buy" 

    # Load Data Running
    Text_LoadData = "Reset Data Runnning Farm Account"



    #famr info
    Farm_Text_SoDao = " Corps Number :"
    Farm_Text_LoaiMo = "Mine Type Rss :"
    Farm_Text_CapMo = "Mine Level Rss :"
    Farm_Text_NangCapAnhHung = "Hero Upgrade :"
    Farm_Text_So_Mo_XayDung = "Construction Mines: "

    Farm_Tab_Text_SoDao = " Corps Number"
    Farm_Tab_Text_LoaiMo = "Mine Type Rss"
    Farm_Tab_Text_CapMo = "Mine Level Rss"
    Farm_Tab_Text_NangCapAnhHung = "Hero Upgrade"
    Farm_Tab_Text_So_Mo_XayDung = "Construction Mines"

    #TopTip
    Text_TopTip_ComBobox_Black = "Use KeyEvent Or Click Back Button (If Game Hangs Game Logo Use Click Back Button Then Restart Game And Program)"

    Text_TopTip_ComBoBox_Delay_Load_Image = "After(s) Skip Function Or Event If No Matching Image Found"

    Text_TopTip_ComBoBox_NhanNhiemVu = "Get Daily Quests Later (h)"

    Farm_Info_Text_SoLuongXuatQuan = "Number of Troops That Can Collect Farm Resources ( Vip10 = 6 , Vip < Vip10 = 5)"

    Farm_Info_Text_CapDoMo = "Mine Level Wants Farm To Collect"

    Farm_Info_Text_LoaiMo = "1 = Rice ; 2 = Wood ;3 = Metal ; 4 = Silve"


else:
    #MainAcc
    Text_Login_Next = "Login Next"
    Text_ThanhDiaLienMinh = "Thánh Địa Liên Minh"
    Text_HoatDongLienMinh = "Hoạt Động Liên Minh"
    # Tab MainAcc
    Text_Level_Min= "Cấp Min :"
    Text_Level_MAx= "Cấp Max :"
    Text_BuaNgauNhien= "Bùa Ngẫu Nhiên"
    Text_TheLuc= "Sử Dụng thể Lực"
    Text_TuAcc= "Từ Acc :"
    Text_DenAcc= "Đến Acc :"
    Text_SoLan ="Số Lần :"
    Text_DaDanh ="Đã Đánh :"
    Text_Grupbox_DiQuanXamLuoc = "Dị Quân Xâm Lược"
    Text_Grupbox_QuaiVatVienCo = "Quái Vật Viễn Cổ"

    #FarmAcc
    Text_GropBox_Chay1Lan = "Chạy 1 Lần"
    Text_GropBox_ChaytheoVongLap = "Chạy Theo Vòng Lặp"
    Text_DangNhap = "Đăng Nhập"

    Text_NhanQua_BenCang = "Quà Bến Cảng"
    Text_DiemDanh = "Quà Điểm Danh"
    Text_ChoiXucXac = "Trò Chơi Xúc Xắc"
    Text_DanhAiRong = "Khiêu Chiến Rồng"
    Text_TriThuong = "Trị Thương"
    Text_An4Mo = "Ăn 4 Loại Mỏ"
    Text_DapLua = "Dập Lửa"
    Text_GuiDaQuy = "Gửi Đá Quý"
    Text_ThayPhap = "Mua Hàng Thầy Pháp"
    Text_CongHien = "Cống Hiến Liên Minh"
    Text_NapRong = "Nạp Cánh Cửa"
    Text_LuyenLinh = "Luyện Lính"
    Text_DoiHuyChuong = "Đổi Huy Chương"
    Text_NangCapAnhHung = "Nâng Cấp Anh Hùng"
    Text_TaiThiet = "Tái Thiết"
    Text_Uoc = "Ước 20 Lần"
    Text_AnRssTrongThanh = "Rss Trong Thành"
    Text_XayDung = "Nhiệm Vụ Xây Dựng"
    Text_ChieuMoAnhHung = "Chiêu Mộ Anh Hùng"
    Text_BuaSanLuong = "Bùa Sản Lượng "
    Text_KiemTraVip = "Check Vip"
    Text_NghienCuu = "Nghiên Cứu"
    Text_SkillLanhChua ="Skill Lãnh Chúa"
    Text_DiThuMo = "Đi Thu Mỏ"
    Text_KhienNoiChien = "Khiên Nội Chiến"

    #Event Hàng Ngày
    Text_MayBanDa = "Máy Bắn Đá"
    Text_KhobauBian = "Kho Bắu Bí Ẩn"
    Text_ThuThapKietXuat = "Thu Thập Kiệt Xuất"
    Text_RuongKVK = "Rương KVK"
    Text_RuongBaChu = "Rương Bá Chủ"
    Text_Gac_Lau_Kho_Bau = "Gác Lầu Kho Báu"
    Text_DoiCanhBauTroi = "Đôi Cánh Bầu Trời"
    Text_NhanNhiemVu = " Nhận Nhiệm Vụ"
        
    #Tab Farm Event
    Text_GropBox_MoTaiNguyen = "Mở Tài Nguyên"
    Text_GropBox_EpKhien = "Ép Khiên"
    Text_GropBox_Docthu = "Mở Thư"
    Text_LoaiKhien = "Loại Khiên"
    Text_TuMua = "Tự Mua" 
    Text_MoDa_quy = " Mở Tài Nguyên"
    Text_MoTinNhan = " Đọc Thư"

    # Load Data Running
    Text_LoadData = "Reset Data Runnning Farm Account"



    #Famr Info
    Farm_Text_SoDao = "Số Đạo :"
    Farm_Text_LoaiMo = "Loại Mỏ :"
    Farm_Text_CapMo = "Cấp Mỏ :"
    Farm_Text_NangCapAnhHung = "Nâng Cấp Anh Hùng :"
    Farm_Text_So_Mo_XayDung = "Số Mỏ Xây Dựng :"

    Farm_Tab_Text_SoDao = "Số Đạo"
    Farm_Tab_Text_LoaiMo = "Loại Mỏ"
    Farm_Tab_Text_CapMo = "Cấp Mỏ"
    Farm_Tab_Text_NangCapAnhHung = "Nâng Cấp Anh Hùng"
    Farm_Tab_Text_So_Mo_XayDung = "Mỏ Xây Dựng"

    #TopTip
    Text_TopTip_ComBobox_Black = "Sử Dụng KeyEvent Hoặc Click Nút Trở Lại (Nếu Trò Chơi Treo Logo Game Sử Dụng Click Nút Trở Lại Sau Đó Khởi Động Lại Trò Chơi Và Chương Trình)"
    
    Text_TopTip_ComBoBox_Delay_Load_Image = "Sau (s) Bỏ Qua Chức Năng Hoặc Sự Kiện Nếu Không Tìm Thấy Hình Ảnh Phù Hợp"

    Text_TopTip_ComBoBox_NhanNhiemVu = "Nhận Nhiệm Vụ Hàng Ngày Sau (h)"

    Farm_Info_Text_SoLuongXuatQuan = "Số Đạo Quân Trang Trại Có Thể Xuất Đi Nhặt Mỏ ( Vip10 = 6 , Vip < Vip10 = 5)"

    Farm_Info_Text_CapDoMo = "Cấp Độ Mỏ Muốn Đi Thập"

    Farm_Info_Text_LoaiMo = "1 = Lúa ; 2 = Gỗ ; 3 = Kim Loại ; 4 = Bạc"

def SaveTime():
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
    Text_Lience = QtCore.pyqtSignal(str)
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



        if self.Han_Su_Dung == "0 day, 00:00:00":
            self.Text_Lience.emit("Demo")

        else:
            self.Text_Lience.emit("Licence")


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
        self.Running_ChucNang = True


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
        self.thoigian_run = [0, 0, 0]

    def Reset_Time_Run_1_Acc(self):
        """Reset Time Run 1 Acc """

        self.thoigian_1acc = [0, 0, 0]

        
    def Reset_Time_Run_Tong(self):
        self.thoigian_tong = [0, 0, 0]


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
        # config languge
        self.label_3.setText(Farm_Text_SoDao)
        self.label_4.setText(Farm_Text_LoaiMo)
        self.label_9.setText(Farm_Text_CapMo)
        self.label_5.setText(Farm_Text_NangCapAnhHung)
        self.label_6.setText(Farm_Text_So_Mo_XayDung)

        #  = "Cấp Độ Mỏ Muốn Đi Thập"

        # Farm_Info_Text_LoaiMo = "1 = Lúa ; 2 = Gỗ ;3 = Kim Loại ; 4 = Bạc"


        self.comboBox_sodao.setToolTip(Farm_Info_Text_SoLuongXuatQuan)
        self.comboBox_loaimo.setToolTip(Farm_Info_Text_LoaiMo)
        self.comboBox_loaimo_2.setToolTip(Farm_Info_Text_CapDoMo)


        self.load_data()



        self.tableWidget.setHorizontalHeaderLabels(["Email ", "Password", Farm_Tab_Text_SoDao, Farm_Tab_Text_LoaiMo ,Farm_Tab_Text_CapMo ,Farm_Tab_Text_NangCapAnhHung,Farm_Tab_Text_So_Mo_XayDung ,"MainAcc"])
        self.tableWidget.setColumnWidth(0, 270)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 130)
        self.tableWidget.setColumnWidth(3, 130)
        self.tableWidget.setColumnWidth(4, 130)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setColumnWidth(6, 130)
        self.tableWidget.setColumnWidth(7, 130)


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
        c = wmi.WMI()
        Seri_hhd_number = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
        if Seri_hhd_number == "0025_3854_0140_0908.":
            pass
        
        else:
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

    #Setting
    List_Time_DeLay = ["0.16","0.14","0.12","0.10","0.08","0.05","3.5"]
    List_Time_Delay_Load_Anh = ["3","4","5"]

    #Farm Acc
    List_Email_Farm_Acount = []
    List_Password_Farm_Account = []
    List_So_Dao = []
    List_Loai_Mo = []
    List_CapMo = []
    List_NangCapAnhHung = []
    List_XayNha = []
    List_MainAcc= []

    #Event
    list_ComBoBox_MoTaiNguyen = ["Gems","Rice","Wood","Metal","Silver"]
    List_Khien = ["8h","24h","3Day"]

    #MainAcc
    List_Quai = ["1","2", "3","4","5","6","7","8","9", "10","11","12","13","14","15", "16","17","18","19","20", "21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40"]
    List_TuAcc = ["1","2","3","4","5","6"]
    List_DenAcc = ["1","2","3","4","5","6"]
    List_VienTro = ["Lua","Go","KimLoai","Bac"]

    #Develoop
    List_Black = ["Key","Click"]
    List_NgonNgu = ["VietNam","English"]
    List_Time_Nhan_NhiemVu = ["18","19","20","21"]

    c = wmi.WMI()
    Seri_hhd_number = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()


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

    #TODO: Thread MainBot
        self.Main_Bot = Main_Bot(self)
        self.Main_Bot.ThongBaoNox.connect(self.Thread_Main_Bot_ThongBaoLoiNox)
        self.Main_Bot.Update_ComBoBox_ChonAcc.connect(self.Thread_Main_bot_Update_ComBobox_ChonAcc)
        self.Main_Bot.Update_KhoangCach_DanhQuai.connect(self.Thread_Main_bot_Update_KhoangCach_DanhQuai)
        self.Main_Bot.Update_Lable_Email.connect(self.EditLable_Email)
        self.Main_Bot.Update_Running.connect(self.Edit_Running)

    #TODO: Thread ShowTime

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
        self.Show_Time.Text_Lience.connect(self.Lable_Text_licence)
        self.timer.start(1000)
   
    #TODO: ComBobox Tab Develoop, Setting 
        # Language
        self.CBbox_Ngon_Ngu.addItems(self.List_NgonNgu)
        self.CBbox_Ngon_Ngu.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBbox_Ngon_Ngu,"Language"))
        self.CBbox_Ngon_Ngu.setCurrentIndex(self.List_NgonNgu.index(File_config.get('ChucNang', 'Language')))

        # Delay Click
        self.CBBox_Delay.addItems(self.List_Time_DeLay) 
        self.CBBox_Delay.currentIndexChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBBox_Delay,"delay_click"))
        self.CBBox_Delay.setCurrentIndex(self.List_Time_DeLay.index(File_config.get('ChucNang', 'delay_click')))
        self.CBBox_Delay.setToolTip("Delay Click (s)")

        # Delay Load Imgae Sai Khac
        self.CBBox_Delay_2.addItems(self.List_Time_Delay_Load_Anh) # Time Load Image
        self.CBBox_Delay_2.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBBox_Delay_2,"delay_load_image"))
        self.CBBox_Delay_2.setCurrentIndex(self.List_Time_Delay_Load_Anh.index(File_config.get('ChucNang', 'delay_load_image')))
        self.CBBox_Delay_2.setToolTip(Text_TopTip_ComBoBox_Delay_Load_Image)

        #Time Nhan Nhiem Vu
        self.CBbox_Time_NhiemVu.addItems(self.List_Time_Nhan_NhiemVu) # Time Nhận Nhiệm Vụ
        self.CBbox_Time_NhiemVu.setCurrentIndex(self.List_Time_Nhan_NhiemVu.index(File_config.get('ChucNang', 'Time_Nhan_NhiemVu')))
        self.CBbox_Time_NhiemVu.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBbox_Time_NhiemVu,"Time_Nhan_NhiemVu"))
        self.CBbox_Time_NhiemVu.setToolTip(Text_TopTip_ComBoBox_NhanNhiemVu)

        # Key Black
        self.CBBox_Delay_3.addItems(self.List_Black)
        self.CBBox_Delay_3.setToolTip(Text_TopTip_ComBobox_Black)
        self.CBBox_Delay_3.setCurrentIndex(self.List_Black.index(File_config.get('ChucNang', 'black')))
        self.CBBox_Delay_3.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBBox_Delay_3,"black"))


        self.comboBox.addItems(self.List_VienTro) # Time Nhận Nhiệm Vụ
     #   self.comboBox.setCurrentIndex(self.List_Time_Nhan_NhiemVu.index(File_config.get('ChucNang', 'Time_Nhan_NhiemVu')))
     #   self.comboBox.currentTextChanged.connect(lambda: self.Set_Config_ComBoBox(self.CBbox_Time_NhiemVu,"Time_Nhan_NhiemVu"))
        


        #Titlet NoxPlay
        self.CBBox_ChonTitle.addItems(self.Get_Title_Nox()) 
        self.CBBox_ChonTitle.currentTextChanged.connect(lambda: self.Combobox_SetTitlets())

        #Tab FarmAcc
        self.Doc_Va_Tao_Data_Farm()
        self.CBbox_Chon_Acc.addItems(self.List_Email_Farm_Acount)

        # Tab Event
        self.CBbox_MoTaiNguyen.addItems(self.list_ComBoBox_MoTaiNguyen)
        self.CBbox_MoTaiNguyen_4.addItems(self.List_Khien)

        # Tab Main Acc
        self.CBbox_MoTaiNguyen_3.addItems(self.List_Quai)
        self.CBbox_MoTaiNguyen_3.setCurrentIndex(29)
        self.CBbox_MoTaiNguyen_2.addItems(self.List_Quai)
        self.CBbox_MoTaiNguyen_2.setCurrentIndex(39)
 
        self.CBBox_ChonTitle_2.addItems(self.List_TuAcc)
        self.CBBox_ChonTitle_2.setCurrentIndex(0)
        self.CBBox_ChonTitle_3.addItems(self.List_TuAcc)
        self.CBBox_ChonTitle_3.setCurrentIndex(5)
        self.lineEdit.setText("100")
        self.lineEdit_3.setText(str(30))

        #TODO: Load Language CheckButton
        # Tab Event

        self.groupBox_3.setTitle(Text_GropBox_MoTaiNguyen)
        self.groupBox_5.setTitle(Text_GropBox_EpKhien)
        self.CB_Choi_Xuc_Xac_2.setText(Text_TuMua)
        self.label_16.setText(Text_LoaiKhien)
        self.groupBox_7.setTitle(Text_GropBox_Docthu)

        #Tab Farm
        self.groupBox.setTitle(Text_GropBox_Chay1Lan)
        self.groupBox_2.setTitle(Text_GropBox_ChaytheoVongLap)
        self.CB_Login.setText(Text_DangNhap)
        self.CB_Diem_Danh.setText(Text_DiemDanh)
        self.CB_Choi_Xuc_Xac.setText(Text_ChoiXucXac)
        self.CB_DAnh_Ai_Rong.setText(Text_DanhAiRong)
        self.CB_Tri_Thuong.setText(Text_TriThuong)
        self.CB_An_4_Mo.setText(Text_An4Mo)
        self.CB_Thay_Phap.setText(Text_ThayPhap)
        self.CB_Cong_Hien_LM.setText(Text_CongHien)
        self.Cb_Nap_Rong.setText(Text_NapRong)
        self.CB_Luyen_Linh.setText(Text_LuyenLinh)
        self.CB_Doi_Hc.setText(Text_DoiHuyChuong)
        self.CB_Gui_Da_Quy.setText(Text_GuiDaQuy)
        self.CB_Nang_Cap_AH.setText(Text_NangCapAnhHung)
        self.CB_Tai_Thiet.setText(Text_TaiThiet)
        self.CB_Uoc.setText(Text_Uoc)
        self.CB_XayDung.setText(Text_XayDung)
        self.CB_Chieu_Mo_AH.setText(Text_ChieuMoAnhHung)
        self.CB_Bua_San_Luong.setText(Text_BuaSanLuong)
        self.CB_DapLua.setText(Text_DapLua)
        self.CB_Nghien_Cuu.setText(Text_NghienCuu)
        self.CB_Skill_Lanh_Chua.setText(Text_SkillLanhChua)
        self.CB_Di_Thu_Mo.setText(Text_DiThuMo)
        self.CB_Khien_Nc.setText(Text_KhienNoiChien)
        self.CB_May_Ban_Da.setText(Text_MayBanDa)
        self.CB_Kho_Bau_Bi_An.setText(Text_KhobauBian)
        self.CB_Thu_Thap_Kiet_Xuat.setText(Text_ThuThapKietXuat)
        self.Cb_Ruong_KVK.setText(Text_RuongKVK)
        self.Cb_Ruong_Ba_Chu.setText(Text_RuongBaChu)
        self.Cb_Gac_Lau_Kho_Bau.setText(Text_Gac_Lau_Kho_Bau)

        # Tab MainAcc
        self.label_17.setText(Text_Level_Min)
        self.label_18.setText(Text_Level_MAx)
        self.checkBox.setText(Text_BuaNgauNhien)
        self.checkBox_2.setText(Text_TheLuc)
        self.LB_TotalTime_4.setText(Text_TuAcc)
        self.LB_TotalTime_3.setText(Text_DenAcc)
        self.LB_TotalTime_5.setText(Text_SoLan)
        self.LB_TotalTime_6.setText(Text_DaDanh)
        self.groupBox_9.setTitle(Text_Grupbox_DiQuanXamLuoc)
        
        # Tab Develoop
        self.CB_QuaBenCang.setText(Text_NhanQua_BenCang)
        self.CB_RssTrongThanh.setText(Text_AnRssTrongThanh)

    #TODO: Load Config CheckBox
            #Tab Develoop
        self.CB_Login.setChecked(True)
        self.CB_RssTrongThanh.setChecked(True)
        self.CB_QuaBenCang.setChecked(True)

        self.CB_Diem_Danh.setChecked(File_config.getboolean('ChucNang', 'DiemDanh'))
        self.CB_Diem_Danh.clicked.connect(lambda: self.Set_Config(self.CB_Diem_Danh,"DiemDanh"))

            #Tab FarmAcc  
        self.CB_Choi_Xuc_Xac.setChecked(File_config.getboolean('ChucNang', 'ChoiXucXac'))
        self.CB_Choi_Xuc_Xac.clicked.connect(lambda: self.Set_Config(self.CB_Choi_Xuc_Xac,"ChoiXucXac"))

        self.CB_Tri_Thuong.setChecked(File_config.getboolean('ChucNang', 'TriThuong'))
        self.CB_Tri_Thuong.clicked.connect(lambda: self.Set_Config(self.CB_Tri_Thuong,"TriThuong"))

        self.CB_DAnh_Ai_Rong.setChecked(File_config.getboolean('ChucNang', 'DanhAiRong'))
        self.CB_DAnh_Ai_Rong.clicked.connect(lambda: self.Set_Config(self.CB_DAnh_Ai_Rong,"DanhAiRong"))

        self.CB_An_4_Mo.setChecked(File_config.getboolean('ChucNang', 'An4Mo'))
        self.CB_An_4_Mo.clicked.connect(lambda: self.Set_Config(self.CB_An_4_Mo,"An4Mo"))

        self.CB_Thay_Phap.setChecked(File_config.getboolean('ChucNang', 'ThayPhap'))
        self.CB_Thay_Phap.clicked.connect(lambda: self.Set_Config(self.CB_Thay_Phap,"ThayPhap"))

        self.CB_Cong_Hien_LM.setChecked(File_config.getboolean('ChucNang', 'CongHienLM'))
        self.CB_Cong_Hien_LM.clicked.connect(lambda: self.Set_Config(self.CB_Cong_Hien_LM,"CongHienLM"))

        self.Cb_Nap_Rong.setChecked(File_config.getboolean('ChucNang', 'NapRong'))
        self.Cb_Nap_Rong.clicked.connect(lambda: self.Set_Config(self.Cb_Nap_Rong,"NapRong"))

        self.CB_Luyen_Linh.setChecked(File_config.getboolean('ChucNang', 'LuyenLinh'))
        self.CB_Luyen_Linh.clicked.connect(lambda: self.Set_Config(self.CB_Luyen_Linh,"LuyenLinh"))

        self.CB_Doi_Hc.setChecked(File_config.getboolean('ChucNang', 'DoiH.C'))
        self.CB_Doi_Hc.clicked.connect(lambda: self.Set_Config(self.CB_Doi_Hc,"DoiH.C"))

        self.CB_Gui_Da_Quy.setChecked(File_config.getboolean('ChucNang', 'GuiDaQuy'))
        self.CB_Gui_Da_Quy.clicked.connect(lambda: self.Set_Config(self.CB_Gui_Da_Quy,"GuiDaQuy"))

        self.CB_Nang_Cap_AH.setChecked(File_config.getboolean('ChucNang', 'NangCapA.H'))
        self.CB_Nang_Cap_AH.clicked.connect(lambda: self.Set_Config(self.CB_Nang_Cap_AH,"NangCapA.H"))

        self.CB_Tai_Thiet.setChecked(File_config.getboolean('ChucNang', 'TaiThiet'))
        self.CB_Tai_Thiet.clicked.connect(lambda: self.Set_Config(self.CB_Tai_Thiet,"TaiThiet"))

        self.CB_Uoc.setChecked(File_config.getboolean('ChucNang', 'Uoc'))
        self.CB_Uoc.clicked.connect(lambda: self.Set_Config(self.CB_Uoc,"Uoc"))

        self.CB_DapLua.setChecked(File_config.getboolean('ChucNang', 'DapLua'))
        self.CB_DapLua.clicked.connect(lambda: self.Set_Config(self.CB_DapLua,"DapLua"))

        self.CB_XayDung.setChecked(File_config.getboolean('ChucNang', 'XayDung'))
        self.CB_XayDung.clicked.connect(lambda: self.Set_Config(self.CB_XayDung,"XayDung"))

        self.CB_Chieu_Mo_AH.setChecked(File_config.getboolean('ChucNang', 'ChieuMoA.H'))
        self.CB_Chieu_Mo_AH.clicked.connect(lambda: self.Set_Config(self.CB_Chieu_Mo_AH,"ChieuMoA.H"))

        self.CB_Bua_San_Luong.setChecked(File_config.getboolean('ChucNang', 'BuaSanLuong'))
        self.CB_Bua_San_Luong.clicked.connect(lambda: self.Set_Config(self.CB_Bua_San_Luong,"BuaSanLuong"))

        self.CB_Nghien_Cuu.setChecked(File_config.getboolean('ChucNang', 'NghienCuu'))
        self.CB_Nghien_Cuu.clicked.connect(lambda: self.Set_Config(self.CB_Nghien_Cuu,"NghienCuu"))

        self.CB_Skill_Lanh_Chua.setChecked(File_config.getboolean('ChucNang', 'SkillLanhChua'))
        self.CB_Skill_Lanh_Chua.clicked.connect(lambda: self.Set_Config(self.CB_Skill_Lanh_Chua,"SkillLanhChua"))

        self.CB_Di_Thu_Mo.setChecked(File_config.getboolean('ChucNang', 'DiThuMo'))
        self.CB_Di_Thu_Mo.clicked.connect(lambda: self.Set_Config(self.CB_Di_Thu_Mo,"DiThuMo"))

        self.CB_Khien_Nc.setChecked(File_config.getboolean('ChucNang', 'KhienN.C'))
        self.CB_Khien_Nc.clicked.connect(lambda: self.Set_Config(self.CB_Khien_Nc,"KhienN.C"))

            #Event
        self.CB_May_Ban_Da.setChecked(File_config.getboolean('ChucNang', 'MayBanDa'))
        self.CB_May_Ban_Da.clicked.connect(lambda: self.Set_Config(self.CB_May_Ban_Da,"MayBanDa"))

        self.CB_Kho_Bau_Bi_An.setChecked(File_config.getboolean('ChucNang', 'KhoBauBiAn'))
        self.CB_Kho_Bau_Bi_An.clicked.connect(lambda: self.Set_Config(self.CB_Kho_Bau_Bi_An,"KHoBauBiAn"))

        self.CB_Thu_Thap_Kiet_Xuat.setChecked(File_config.getboolean('ChucNang', 'ThuThapKietXuat'))
        self.CB_Thu_Thap_Kiet_Xuat.clicked.connect(lambda: self.Set_Config(self.CB_Thu_Thap_Kiet_Xuat,"ThuThapKietXuat"))

        self.Cb_Ruong_KVK.setChecked(File_config.getboolean('ChucNang', 'RuongKVK'))
        self.Cb_Ruong_KVK.clicked.connect(lambda: self.Set_Config(self.Cb_Ruong_KVK,"RuongKVK"))

        self.Cb_Ruong_Ba_Chu.setChecked(File_config.getboolean('ChucNang', 'RuongBaChu'))
        self.Cb_Ruong_Ba_Chu.clicked.connect(lambda: self.Set_Config(self.Cb_Ruong_Ba_Chu,"RuongBaChu"))

        self.Cb_Gac_Lau_Kho_Bau.setChecked(File_config.getboolean('ChucNang', 'GacLauKhoBau'))
        self.Cb_Gac_Lau_Kho_Bau.clicked.connect(lambda: self.Set_Config(self.Cb_Gac_Lau_Kho_Bau,'GacLauKhoBau'))

    #TODO:  Click Button Connect 
        # Setting 
        self.pushButton.clicked.connect(lambda: self.button_caidat_adb())
        self.Btn_Open_Farm_Info.clicked.connect(lambda: self.click_button_open_farm_info())

        #Tab Farm Acc 
        self.pushButton_4.clicked.connect(lambda: self.Click_Button_Start())
        self.pushButton_5.clicked.connect(lambda: self.Click_Button_Stop())
        self.Btn_Login_Next.clicked.connect(lambda: self.Click_Button_Login_Next())
        self.Btn_Mua.clicked.connect(lambda : self.show_buys())
        
        #Tab Event 
        self.Btn_MoTaiNguyen.clicked.connect(lambda: self.Click_Button_Start_MoDa_Quy())
        self.Btn_MoTaiNguyen_5.clicked.connect(lambda: self.Click_Button_Start_MoTinNhan())
        self.Btn_MoTaiNguyen_4.clicked.connect(lambda: self.Click_Button_Start_EpKhien())

        #Tab MainAcc 
        self.Btn_Start_DanhQuaiVat.clicked.connect(lambda: self.Click_Button_Start_DanhQuaiVat())
        self.Btn_Start_DanhQuaiVat_2.clicked.connect(lambda: self.Click_Button_Start_DanhVienCo())
        self.Btn_Start_DanhQuaiVat_3.clicked.connect(lambda: self.Click_Button_Start_GomRss())
        self.Btn_Start_DanhQuaiVat_4.clicked.connect(lambda: self.Click_Button_Start_DiQuanXamLuoc())
        self.Btn_Start_DanhQuaiVat_5.clicked.connect(lambda: self.Click_Button_Start_PK_Titan())
        self.pushButton_2.clicked.connect(lambda: self.Click_Button_Start_VienTro_TaiNguyen())



        #Tab Ad
        self.Btn_Login_Next_2.clicked.connect(lambda: self.Click_Button_Show_ID())
        self.Btn_Login_Next_3.clicked.connect(lambda: self.Create())


        if self.Seri_hhd_number == "0025_3854_0140_0908.":
            print("Hello Admin")
            self.Btn_Login_Next_3.hide()
            self.label_21.hide()
            self.lineEdit_6.hide()
            self.lineEdit_7.hide()

            
        
        else:
            # XoaTab Ad

            self.tabWidget.removeTab(4)
            self.Btn_Login_Next_2.hide()
            self.Btn_Login_Next_3.hide()
            # Hide Button PK_Titan
            self.Btn_Start_DanhQuaiVat_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_5.hide()

        print(controller.Delay_Click)
        print( Bot_ChucNang.Delay_Load_Image)
        self.load_data_running()
        self.show()

    #TODO:AdButton

    def Click_Button_Show_ID(self):
        
        if self.lineEdit_5.text() == "dior1101995@gmail.com":
            if self.lineEdit_8.text() == "ngacuong1":
                self.Btn_Login_Next_3.show()
                self.label_21.show()
                self.lineEdit_6.show()
                self.lineEdit_7.show()
            else:
                self.tabWidget.removeTab(4)
                print("SaiMatKhau")

        else:
            self.tabWidget.removeTab(4)
            print("SaiMatKhau")

    def Create(self):
        seri = self.lineEdit_6.text()
        hansudung = self.lineEdit_7.text()
        Lic_info().Tao_Lic(str(seri),int(hansudung))



    #TODO: Click Button
    #Setting
 

    def button_caidat_adb(self):
        '''Nút Mở Cài Đặt Adb'''
        subprocess.call(['notepad.exe', 'DataText/Adb.txt'])

    def click_button_open_farm_info(self):
        if self.Window_Farm_Info == None:
            self.Window_Farm_Info = Gui_Farm_Info(self)
            self.Window_Farm_Info.show()

        else:
            self.Window_Farm_Info.close()
            self.Window_Farm_Info = None

    def show_buys(self):
        if self.Window_Buys == None:
            self.Window_Buys = Gui_buys(self)
            self.Window_Buys.show()
        else:
            self.Window_Buys.close()
            self.Window_Buys = None

    def load_data_running(self):
        choice = QtWidgets.QMessageBox.question(self, 'Warning', str(Text_LoadData) + "?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.Reset_File_Data_Running()
            return False

        if choice == QMessageBox.No:
            return False

    def Set_Config_ComBoBox(self,ComBobox,Key):
        '''Set Config ComboBox'''



        File_config.set('ChucNang', Key, ComBobox.currentText())

        with open('DataText/ConfigAuto.ini', 'w') as configfile:
            File_config.write(configfile)
        

        if Key == "delay_click":
            controller.Delay_Click = ComBobox.currentText()

        if Key == "delay_load_image":
            Bot_ChucNang.Delay_Load_Image = ComBobox.currentText()

        if Key == "black":
            black = ComBobox.currentText()
            if black == "Click":
                Bot_ChucNang.Click_Black = True
            else:
                Bot_ChucNang.Click_Black = False



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

        if 'RiseOfTheKing_Bot' in titlet2:
            # Admin
            if self.Seri_hhd_number == "0025_3854_0140_0908.":

                pass
            else:
                # Hide Buton Start Cua So Thu 2 Bat Len
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
               
    def Set_Config(self,bunton,Key):
        '''Set Config'''

        bunton.isChecked()
        if bunton.isChecked():
            
            File_config.set('ChucNang', Key, "True")
        else:
            File_config.set('ChucNang', Key, "False")

 
        with open('DataText/ConfigAuto.ini', 'w') as configfile:
            File_config.write(configfile) 

    def VuiLongLienHeNhaCungCap(self):
        choice = QtWidgets.QMessageBox.question(self, 'Lỗi',
                                                        " 'Vui Lòng Liên Hệ Nhà Cung Cấp Để Thêm Thời Gian Sử Dụng'?",
                                                        QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            return False
        if choice == QMessageBox.No:
            return False

    def closeEvent(self, event):
        """Event Close"""
        SaveTime()
        try:
            print("Exit Application")
            # Stop Thow Time
            self.timer.stop()
            if self.Window_Farm_Info is not None:
                self.Window_Farm_Info.close()

            if self.Window_Buys is not None:
                self.Window_Buys.close()

            #Stop Main Bot
            self.Main_Bot.Stop()

            self.close()
            sys.stdout = sys.__stdout__
            sys.exit()

        except:
            pass
   
    def Disable_Button(self,Button):
        if Button == "Start_Login_Next":
            #self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_ChucNang":
            self.Btn_Login_Next.setDisabled(True)
            #self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_MoTaiNguyen":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            #self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_EpKhien":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            #self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_DocThu":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            #self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_DanhQuaiVat":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            #self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_DanhVienCo":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            #self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)


        if Button == "Start_GomRss":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            #self.Btn_Start_DanhQuaiVat_3.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_4.setDisabled(True)

        if Button == "Start_DiQuanXamLuoc":
            self.Btn_Login_Next.setDisabled(True)
            self.pushButton_4.setDisabled(True)
            self.Btn_MoTaiNguyen.setDisabled(True)
            self.Btn_MoTaiNguyen_4.setDisabled(True)
            self.Btn_MoTaiNguyen_5.setDisabled(True)
            self.Btn_Start_DanhQuaiVat.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_2.setDisabled(True)
            self.Btn_Start_DanhQuaiVat_3.setDisabled(True)

    def Enable_Button(self):
        self.Btn_Login_Next.setDisabled(False)
        self.pushButton_4.setDisabled(False)
        self.Btn_MoTaiNguyen.setDisabled(False)
        self.Btn_MoTaiNguyen_4.setDisabled(False)
        self.Btn_MoTaiNguyen_5.setDisabled(False)
        self.Btn_Start_DanhQuaiVat.setDisabled(False)
        self.Btn_Start_DanhQuaiVat_2.setDisabled(False)
        self.Btn_Start_DanhQuaiVat_3.setDisabled(False)
        self.Btn_Start_DanhQuaiVat_4.setDisabled(False)

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
            

        # with SQLite('DataText/running.db') as cur:
        #     cur.execute("""DELETE FROM running""")
        #     for i in self.List_Email_Farm_Acount:
        #         cur.execute("""INSERT INTO running 
        #         (Email, DiemDanh, KhieuChienRong, ChoixucXac, DoiHuyChuong, CongHienLienMinh,\
        #         Naprong, Taithiet, LuyenLinh, NangCapAnhHung, BuaSanLuongMo, Uoc, TriThuong, ThayPhap, GuiDaQuy, XayDung, HoatDongLienMinh, DiemDanhDienDan) 
        #         VALUES 
        #         (?, ? ,?, ?, ?, ? ,?, ?, ?, ? ,?, ?,?,?,?,?,?,?)""", (str(i), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0))


    #Tab Farm Acc
    def Click_Button_Start(self):
        '''Button Start'''
        if self.Combobox_SetTitlets():
            text = self.pushButton_4.text()
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":

                    print("_____Start_____")
                    self.pushButton_4.setText("Pause")
                    self.Disable_Button(Button = "Start_ChucNang")

                    # # Show Time
                    self.Show_Time.Start()
                    print(controller.Delay_Click)
                    print( Bot_ChucNang.Delay_Load_Image)

                    # # Start Bot
                    self.Main_Bot.Start_MainBot_ChucNang()



                if text == "Pause":
                    print("_____Pause_____")
                    self.pushButton_4.setText("Continue")

                    # # Show Time
                    self.Show_Time.Pause()

                    # #Pause Bot
                    self.Main_Bot.Pause()


                if text == "Continue":
                    print("_____Continue_____")
                    self.stopped_time = True
                    self.pushButton_4.setText("Pause")

                    # # Show Time
                    self.Show_Time.Continue()

                    # #Continue Bot
                    self.Main_Bot.Continue()

            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Stop(self):
        """Button Stop"""
        print("_____Stop_____")
        self.pushButton_4.setText("Start")
        
        try:
            # show_time
            self.Show_Time.Stop()
            #Stop MainBot
            self.Main_Bot.Stop()
            self.Enable_Button()
            self.LB_Running.setText("      ")
             
        except:
            pass

    def Click_Button_Login_Next(self):
        if self.Combobox_SetTitlets():
            self.Disable_Button(Button = "Start_Login_Next")
            self.Main_Bot.Start_Login_Next()

    #Tab Event
    def Click_Button_Start_MoDa_Quy(self):
        """Button Mở Đá Quý"""

        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen.text()
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    self.Disable_Button(Button = "Start_MoTaiNguyen")
                    self.Btn_MoTaiNguyen.setText("Stop")
                    self.Main_Bot.Start_MoTaiNguyen()

                else:
                    self.Btn_MoTaiNguyen.setText("Start")
                    self.Main_Bot.Stop()
                    self.Enable_Button()
            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Start_MoTinNhan(self):
        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen_5.text()
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    self.Disable_Button(Button = "Start_DocThu")
                    self.Btn_MoTaiNguyen_5.setText("Stop")
                    self.Main_Bot.Start_MoTinNhan()

                else:
                    self.Btn_MoTaiNguyen_5.setText("Start")
                    self.Main_Bot.Stop()
                    self.Enable_Button()
            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Start_EpKhien(self):
        if self.Combobox_SetTitlets():
            text = self.Btn_MoTaiNguyen_4.text()
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    self.Disable_Button(Button = "Start_EpKhien")
                    self.Btn_MoTaiNguyen_4.setText("Stop")
                    self.Main_Bot.Start_EpKhien()

                else:
                    
                    self.Btn_MoTaiNguyen_4.setText("Start")
                    self.Main_Bot.Stop()
                    self.Enable_Button()
            else:
                self.VuiLongLienHeNhaCungCap()
                return

    #Tab MainAcc
    def Click_Button_Start_DanhVienCo(self):
        text = self.Btn_Start_DanhQuaiVat_2.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                   self.Disable_Button(Button = "Start_DanhVienCo")
                   self.Btn_Start_DanhQuaiVat_2.setText("Stop")
                   self.Main_Bot.Start_Danh_VienCo()

                if text == "Stop":
                    self.Btn_Start_DanhQuaiVat_2.setText("Start")
                    self.Main_Bot.Stop()
                    self.Enable_Button()
            else:
                self.VuiLongLienHeNhaCungCap()
                return
            
    def Click_Button_Start_GomRss(self):
        text = self.Btn_Start_DanhQuaiVat_3.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > self.Show_Time.Time_GMT:
    
                if text == "Start":
                    self.Disable_Button(Button = "Start_GomRss")

                    self.Btn_Start_DanhQuaiVat_3.setText("Stop")
                    self.Main_Bot.Start_GomRss()


                if text == "Stop":
                    self.Btn_Start_DanhQuaiVat_3.setText("Start")
                    self.Main_Bot.Stop()
                    self.Enable_Button()

            else:
                self.VuiLongLienHeNhaCungCap()
                return

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
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    self.Disable_Button(Button = "Start_DanhQuaiVat")
                    self.Btn_Start_DanhQuaiVat.setText("Stop")
                    self.Tao_Tab_Leve_Monter()
                    self.Main_Bot.Start_Danh_QuaiVat()

                else:
                    self.Btn_Start_DanhQuaiVat.setText("Start")
                    self.tableWidget.setRowCount(0)
                    self.Main_Bot.Stop()
                    self.Enable_Button()

            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Start_DiQuanXamLuoc(self):
        
        text = self.Btn_Start_DanhQuaiVat_4.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    self.Disable_Button(Button = "Start_DiQuanXamLuoc")
                    self.Btn_Start_DanhQuaiVat_4.setText("Stop")
                    self.Main_Bot.Start_DiQuanXamLuoc()

             
                else:
                    self.Btn_Start_DanhQuaiVat_4.setText("Start")
                    self.lineEdit_4.setText(str(0))
                    self.Main_Bot.Stop()
                    self.Enable_Button()


            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Start_PK_Titan(self):
        text = self.Btn_Start_DanhQuaiVat_5.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start PK_Titan":
                    #self.Disable_Button(Button = "Start_DiQuanXamLuoc")
                    self.Btn_Start_DanhQuaiVat_5.setText("Stop PK_Titan")
                    self.Main_Bot.Start_PK_Titan()

             
                else:
                    self.Btn_Start_DanhQuaiVat_5.setText("Start PK_Titan")
                    self.lineEdit_4.setText(str(0))
                    self.Main_Bot.Stop()
                    self.Enable_Button()

            else:
                self.VuiLongLienHeNhaCungCap()
                return

    def Click_Button_Start_VienTro_TaiNguyen(self):
        
        text = self.pushButton_2.text()
        if self.Combobox_SetTitlets():
            if Get_Hansudung > self.Show_Time.Time_GMT:
                if text == "Start":
                    #self.Disable_Button(Button = "Start_DiQuanXamLuoc")
                    self.pushButton_2.setText("Stop")
                    self.Main_Bot.Start_VienTroTaiNguyen()

             
                else:
                    self.pushButton_2.setText("Start")
                    self.lineEdit_10.setText(str(0))
                    self.Main_Bot.Stop()
                    self.Enable_Button()

            else:
                self.VuiLongLienHeNhaCungCap()
                return














#     # Tab Widget Danh Quai Vat
#         self.tableWidget.setColumnWidth(1, 15)
#         self.tableWidget.setColumnWidth(2, 15)

#         self.tableWidget.setColumnWidth(0, 89)
#         self.tableWidget.setColumnWidth(1, 89)




    #TODO:  Signal ShowTime
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

    def Lable_Text_licence(self,str_lic):
        self.LB_Demo.setText(str(str_lic))

    def Reset_File_Data_Running(self):
        print("Reset Data Runnning Farm Account")

        with SQLite('DataText/running.db') as cur:
            cur.execute("""DELETE FROM running""")
            for i in self.List_Email_Farm_Acount:
                cur.execute("""INSERT INTO running 
                (Email, DiemDanh, KhieuChienRong, ChoixucXac, DoiHuyChuong, CongHienLienMinh,\
                Naprong, Taithiet, LuyenLinh, NangCapAnhHung, BuaSanLuongMo, Uoc, TriThuong, ThayPhap, GuiDaQuy, XayDung, HoatDongLienMinh, DiemDanhDienDan) 
                VALUES 
                (?, ? ,?, ?, ?, ? ,?, ?, ?, ? ,?, ?,?,?,?,?,?,?)""", (str(i), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0))

    def Lience_HetHanSuDung(self):
        self.Click_Button_Stop()
        
        Exit_Event.set()

        
    #TODO:  Signal MainBot
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

    def Edit_Running(self,Text):   
        self.LB_Running.setText(str(Text))
        self.Show_Time.Reset_Time_Run_Chuc_Nang()
    
    def EditLable_Email(self,Text):
        self.label_6.setText(str(Text))





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
    Update_Running = QtCore.pyqtSignal(str)
    Update_Lable_Email = QtCore.pyqtSignal(str)
    ThongBaoNox = QtCore.pyqtSignal()
    Update_ComBoBox_ChonAcc = QtCore.pyqtSignal(str)
    Update_KhoangCach_DanhQuai = QtCore.pyqtSignal(int ,int)

    def __init__(self,main_Window, parent=None):
        self.main_Window = main_Window
        
        super().__init__(parent)
        self.lock = Lock()
 
        
        
    def Main_Bot_Danh_QuaiVat(self):
        """Main_Bot Đánh Quái Vật"""
        self.Update_Running.emit("Kill Monter")
        

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
        if self.main_Window.checkBox_3.isChecked():
            DanhTitan = True

        else:
            DanhTitan = False

        while True:
            if Exit_Event.wait(timeout=0.05) : 
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
            Bot_ChucNang.DanhQuai_KVK(CapQuai = list_ChonQuai[Quai_LV],Set_Dao = Set_Dao, DanhTitan = DanhTitan)

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

                #
                self.Update_Lable_Email.emit(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
  
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
                        self.Update_Running.emit(Text_DangNhap)
                        Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)

                if  not Exit_Event.is_set():
                    if self.main_Window.CB_DapLua.isChecked():
                        self.Update_Running.emit(Text_DapLua)
                        Bot_ChucNang.SuaThanhDapLua()
 

            # Nhận Quà Bến Cảng -- 
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_QuaBenCang.isChecked():
                        self.Update_Running.emit(Text_NhanQua_BenCang)
                        if Bot_ChucNang.NhanQua_BenCang():
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Diem_Danh.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "DiemDanh") == [0]:
                                        self.Update_Running.emit(Text_DiemDanh)
                                        Bot_ChucNang.Nhan_Qua_DangNhap(Email_Run)


            # Chơi Xúc Xắc
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Choi_Xuc_Xac.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "ChoixucXac") == [0]:
                                        self.Update_Running.emit(Text_ChoiXucXac)
                                        Bot_ChucNang.Kho_Tang(Email_Run)


            # Khiêu Chiến Rồng
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_DAnh_Ai_Rong.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "KhieuChienRong") == [0]:
                                        self.Update_Running.emit(Text_DanhAiRong)
                                        Bot_ChucNang.KhieuChienRong(Email_Run)


            # Chiêu Mộ Anh Hùng --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Chieu_Mo_AH.isChecked():
                        self.Update_Running.emit(Text_ChieuMoAnhHung)
                        Bot_ChucNang.ChieuMo_AnhHung()
                        if  not Exit_Event.is_set():
                            if self.main_Window.CB_Thay_Phap.isChecked():
                                if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "ThayPhap") == [0]:
                                    self.Update_Running.emit(Text_ThayPhap)
                                    Bot_ChucNang.Thay_Phap(Email_Run)
    

            # Gửi Đá Quý    
                            if  not Exit_Event.is_set():
                                if self.main_Window.CB_Gui_Da_Quy.isChecked():
                                    if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "GuiDaQuy") ==[0]:
                                        self.Update_Running.emit(Text_GuiDaQuy)
                                        Bot_ChucNang.Gui_Da_Quy(Email_Run)


            # Hiến Tặng Liên Minh --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Cong_Hien_LM.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "CongHienLienMinh") == [0]:
                            self.Update_Running.emit(Text_CongHien)
                            Bot_ChucNang.HienTang_LienMinh(Email_Run)


            # Ước Free --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Uoc.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "Uoc") == [0]:
                            self.Update_Running.emit(Text_Uoc)
                            Bot_ChucNang.Uoc_Free(Email_Run)
 

            # Trị Thương --- Chạy 1 lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Tri_Thuong.isChecked():

                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "TriThuong") == [0]:
                            self.Update_Running.emit(Text_TriThuong)
                            Bot_ChucNang.Tri_Thuong(Email_Run)


            # Tái Thiết --- Chạy 1 Lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Tai_Thiet.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "Taithiet") == [0]:
                            self.Update_Running.emit(Text_TaiThiet)
                            Bot_ChucNang.Tai_Thiet(Email_Run)


            # Skill Lãnh Chúa --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Skill_Lanh_Chua.isChecked():
                        self.Update_Running.emit(Text_SkillLanhChua)
                        Bot_ChucNang.Skill_LanhChua()


            # Bùa Sản Lượng Trong Thành --- Theo Vòng Lặp            
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Bua_San_Luong.isChecked():
                        self.Update_Running.emit(Text_BuaSanLuong)
                        Bot_ChucNang.BuaSanLuong_TrongThanh()


            # RSS Trong Thành --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_RssTrongThanh.isChecked():
                        self.Update_Running.emit(Text_AnRssTrongThanh)
                        Bot_ChucNang.AnRss_TrongThanh()


            # Xây Dựng
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_XayDung.isChecked():
                        #Đỏi Lại ?Get Chuc nang
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "XayDung") == [0]:
                            self.Update_Running.emit(Text_XayDung)
                            Bot_ChucNang.NhiemVu_XayDung(Email_Run)


            # Nâng Cấp Anh Hùng --- Chạy 1 lần
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Nang_Cap_AH.isChecked():
                        if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "NangCapAnhHung") == [0]:
                            self.Update_Running.emit(Text_NangCapAnhHung)
                            Bot_ChucNang.NangCapAnhHung(Email = Email_Run, vitrianhhung = NangCap_AnhHung_Run)


            # MainAcc

                if  not Exit_Event.is_set():
                    if MainAcc_Run == float(3):
                            self.Update_Running.emit(Text_ThanhDiaLienMinh)
                            Bot_ChucNang.NhanQua_ThanhDiaLienMinh_MainAcc()
                            
                            if Bot_ChucNang.Get_Database_Running(email = Email_Run,chucnang = "HoatDongLienMinh") == [0]:
                                self.Update_Running.emit(Text_HoatDongLienMinh)
                                Bot_ChucNang.NhanQua_HoaDongLienMinh_MainAcc(Email_Run)
                            Bot_ChucNang.HienTang_LienMinh(Email_Run)


            # Đi Ăn Mỏ RSS --- Theo Vòng Lặp
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Di_Thu_Mo.isChecked():
                        self.Update_Running.emit(Text_DiThuMo)
                        Bot_ChucNang.Di_AnMo(Email_Run,Loai_Mo_Run,Cap_Mo_Run,So_Dao_Run)


            # Khiên Nội Chiến
                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Khien_Nc.isChecked():
                        self.Update_Running.emit(Text_KhienNoiChien)
                        Bot_ChucNang.Khien_Farm(Email_Run,)
                

            # Lấy Và So Sánh Time GMT Với Time Nhận Nhiệm Vụ
                if  not Exit_Event.is_set():
                    print("Time Nhận Nhiệm Vụ :","TimeGMT =",int(self.main_Window.Show_Time.Time_GMT.hour),"Time Set =",int(self.main_Window.CBbox_Time_NhiemVu.currentText().split(':')[0]))
                    if int(showtime().Time_GMT.hour) >= int(self.main_Window.CBbox_Time_NhiemVu.currentText().split(':')[0]):
                        self.Update_Running.emit(Text_NhanNhiemVu)
                        Bot_ChucNang.Nhan_NhiemVu()


            # Event
                if  not Exit_Event.is_set():
                    if self.main_Window.Cb_Gac_Lau_Kho_Bau.isChecked():
                        self.Update_Running.emit(Text_DoiCanhBauTroi)
                        Bot_ChucNang.Event_DoiCanhBauTroi()


                if  not Exit_Event.is_set():
                    if self.main_Window.CB_May_Ban_Da.isChecked():
                        self.Update_Running.emit(Text_MayBanDa)
                        Bot_ChucNang.Event_MayBan_Da()

                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Thu_Thap_Kiet_Xuat.isChecked():
                        self.Update_Running.emit(Text_ThuThapKietXuat)
                        Bot_ChucNang.Event_ThuThapKietXuat()



                if  not Exit_Event.is_set():
                    if self.main_Window.Cb_Ruong_KVK.isChecked():
                        self.Update_Running.emit(Text_RuongKVK)
                        Bot_ChucNang.Event_RuongKVK()


                if  not Exit_Event.is_set():
                    if self.main_Window.CB_Kho_Bau_Bi_An.isChecked():
                        self.Update_Running.emit(Text_KhobauBian)
                        Bot_ChucNang.Event_KhoBauBiAn()



                if  not Exit_Event.is_set():
                    Index_Email_Select = Index_Email_Select + 1
                    # So sánh Vị Trí hiện tại đến tổng Email
                    if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                        Index_Email_Select = 0
                        self.main_Window.Show_Time.Reset_Time_Run_Tong()
                    

            # Viết File Log
                if  not Exit_Event.is_set():
                    with open("DataText/log.txt","a+",encoding="utf-8") as f:
                        f.write(str(self.main_Window.Show_Time.Time_GMT)+'\n')

            # Set email tiếp theo vào Combobox chọn Account
                if  not Exit_Event.is_set():
                    self.main_Window.Show_Time.Reset_Time_Run_1_Acc()
                    email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                    self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))



            else:
                while True: 
                    if self.Running == False: return
                    if Exit_Event.wait(timeout= 0.05):
                        return 



    def Main_Bot_Login_Next(self):
        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account + Them 1
        print(self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select))
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select) + int(1)

        self.Update_Lable_Email.emit(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
        if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
            Index_Email_Select = 0
        #Set Email Vào ComBoBox

        Email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
        self.Update_ComBoBox_ChonAcc.emit(str(Email_set_combobox))
        Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
        Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

        Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
        self.main_Window.Enable_Button()

        self.Stop()
        return


    #TODO: MainBot Event
    def Main_Bot_MoTaiNguyen(self):

        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)


        while True:
            if Exit_Event.is_set() : 
                return
            #
            self.Update_Lable_Email.emit(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            

            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
            Bot_ChucNang.MoDa_Quy(self.main_Window.CBbox_MoTaiNguyen.currentText())

            if not Exit_Event.is_set():
                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    self.main_Window.Show_Time.Reset_Time_Run_Tong()
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen.setText("Start")
                    self.Stop()
                    self.main_Window.Enable_Button()
                    return
                    
                
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))


    def Main_Bot_MoTinNhan(self):
        # Lấy Email Chọn Trong CoBobox
        ComBoBox_Email_Select= self.main_Window.CBbox_Chon_Acc.currentText()

        # lấy vị trí email trong Combobox Chọn Account 
        Index_Email_Select = self.main_Window.List_Email_Farm_Acount.index(ComBoBox_Email_Select)


        while True:
            if Exit_Event.is_set(): return
            self.Update_Lable_Email.emit(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            
            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
            Bot_ChucNang.DocThu()

            if not Exit_Event.is_set(): 

                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen_5.setText("Start")
                    self.Stop()
                    self.main_Window.Enable_Button()
                    return
                    
                
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))



    def Main_Bot_EpKhien(self):
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
            if Exit_Event.is_set() : return

            self.Update_Lable_Email.emit(str(Index_Email_Select + 1)+"/"+ str(len(self.main_Window.List_Email_Farm_Acount)))
            Email_Run = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
            Password_Run = self.main_Window.List_Password_Farm_Account[Index_Email_Select]

            Bot_ChucNang.DangNhap(Email = Email_Run,Password = Password_Run)
            Bot_ChucNang.Khien_Farm(Email = Email_Run,Ep_Khien= True,loaikhien= int_LoaiKhien )

            if not Exit_Event.is_set():
                Index_Email_Select = Index_Email_Select + 1
                # So sánh Vị Trí hiện tại đến tổng Email
                if Index_Email_Select >= len(self.main_Window.List_Email_Farm_Acount):
                    Index_Email_Select = 0
                    print("Mở xong")
                    self.main_Window.Btn_MoTaiNguyen_4.setText("Start")
                    self.Stop()
                    self.main_Window.Enable_Button()
                    return
                    
                # Set email tiếp theo vào Combobox chọn Account
                email_set_combobox = self.main_Window.List_Email_Farm_Acount[Index_Email_Select]
                self.Update_ComBoBox_ChonAcc.emit(str(email_set_combobox))

    #TODO: MainBot MainAcc
    def Main_Bot_Pk_Titan(self):
        while True:
            if Exit_Event.is_set(): return
            Bot_ChucNang.Pk_Titan()

    def Main_Bot_GomRss(self):
        """Main_Bot Gom Rss"""

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
            if Exit_Event.is_set(): return
            
            if LuotAcc >= len(List_GomRss):
                self.main_Window.Btn_Start_DanhQuaiVat_3.setText("Start")
                self.Stop()
                self.main_Window.Enable_Button()
                return

            if Saikhac >= 3:
                self.main_Window.Btn_Start_DanhQuaiVat_3.setText("Start")
                self.Stop()
                self.main_Window.Enable_Button()
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
        while True:
            if  Exit_Event.is_set(): return
            if self.screenshot is None: continue
            Bot_ChucNang.Danh_VienCo()

    def Main_Bot_DiQuanXamLuoc(self):
        SoQuaiDaChon = self.main_Window.lineEdit_3.text()
        for i in range(0,int(SoQuaiDaChon)):
            Bot_ChucNang.DiQuan_XamLuoc()
            if  Exit_Event.is_set(): return
            self.main_Window.lineEdit_4.setText(str(i+1))


        self.Stop()
        self.main_Window.Btn_Start_DanhQuaiVat_4.setText("Start")
        self.main_Window.Enable_Button()

    def Main_Bot_VienTroTaiNguyen(self):
        SoLanDaChon = self.main_Window.lineEdit_9.text()
        for i in range(0,int(SoLanDaChon)):
            Bot_ChucNang.VienTro_TaiNguyen(LoaiTaiNguyen = int(self.main_Window.comboBox.currentText()))
            if  Exit_Event.is_set(): return
            self.main_Window.lineEdit_10.setText(str(i+1))


        self.Stop()
        self.main_Window.pushButton_2.setText("Start VienTro")
        self.main_Window.Enable_Button()


    #TODO: MainBot Start
    def Start_VienTroTaiNguyen(self):
        self.Update_Running.emit("VienTroTaiNguyen")
        self.Start()

        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_VienTroTaiNguyen [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_VienTroTaiNguyen, daemon=True)
            self.Thread_1.start()

    def Start_MoTinNhan(self):
        self.Update_Running.emit(Text_GropBox_Docthu)
        self.Start()

        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_MoTinNhan [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_MoTinNhan, daemon=True)
            self.Thread_1.start()

    def Start_EpKhien(self):
        self.Update_Running.emit(Text_GropBox_EpKhien)
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_Epkhien [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_EpKhien, daemon=True)
            self.Thread_1.start()

    def Start_Login_Next(self):
        self.Start()
        self.Update_Running.emit("Login Next")
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_LoginNext [" + str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Login_Next, daemon=True)
            self.Thread_1.start()

    def Start_PK_Titan(self):
        self.Update_Running.emit("PK Titan")
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_PK_Titan [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Pk_Titan, daemon=True)
            self.Thread_1.start()

    def Start_DiQuanXamLuoc(self):
        self.Update_Running.emit(Text_Grupbox_DiQuanXamLuoc)
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_DiQuanXamLuoc [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_DiQuanXamLuoc, daemon=True)
            self.Thread_1.start()

    def Start_Danh_VienCo(self):

        self.Update_Running.emit(Text_Grupbox_QuaiVatVienCo)
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_DanhVienCo [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Danh_VienCo, daemon=True)
            self.Thread_1.start()

    def Start_GomRss(self):
        self.Update_Running.emit("Gom Tai Nguyen")
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_GomRss [" +str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_GomRss, daemon=True)
            self.Thread_1.start()

    def Start_MoTaiNguyen(self):
        self.Update_Running.emit(Text_GropBox_MoTaiNguyen)
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_MoTaiNguyen [" + str(self.main_Window.Nox_Name)+ "]", target=self.Main_Bot_MoTaiNguyen, daemon=True)
            self.Thread_1.start()

    def Start_Danh_QuaiVat(self):
        self.Update_Running.emit("Kill Monters")
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_DanhQuaiKVK [" + str(self.main_Window.Nox_Name) + "]", target=self.Main_Bot_Danh_QuaiVat, daemon=True)
            self.Thread_1.start()

    def Start_MainBot_ChucNang(self):
        '''MainBot Chuc Nang'''
        self.Start()
        if self.Thread_1 == None:
            self.Thread_1 = Thread(name="Running_Bot_ChucNang [" + str(self.main_Window.Nox_Name) + "]", target= self.Main_Bot_Run_ChucNang, daemon=True)
            self.Thread_1.start()

    #TODO: MainBot Controller
    def Start(self):
        print("[...Start_MainBot...]")
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
        self.Update_Lable_Email.emit('Email :')
        self.Running = False
        Exit_Event.set()

        self.Thread_1 = None
        self.Thread_2 = None
        self.Thread_3 = None

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

    def Main_Bot_Update_Screenshot(self):
        """Main Update Screenshot"""
    
        while True:
            if  Exit_Event.is_set():
                return

            if  self.Running:
                if Exit_Event.wait(timeout=0.05):
                    return

                self.screenshot = self.get_screenshot(self.main_Window.Nox_Name)
                if self.screenshot is None:
                    self.ThongBaoNox.emit()

                    self.Stop()
                    return

                self.lock.acquire()

                Bot_ChucNang.Update_Screenshot(self.screenshot)

                self.lock.release()

            else:
                while not self.Running: 
                    if Exit_Event.wait(timeout= 0.05):
                        return 
                Start = time.time()


      



if __name__ == "__main__":
 
    # Đọc Thông Tin Lic
    Get_Hansudung = Lic_info().Farm_DocLic()

    print(Get_Hansudung)
    Bot_ChucNang = Bot_ChucNang()


    app = QtWidgets.QApplication(sys.argv)


    # Set Style

#    \ app.setStyle("QtCurve")

    tmain_Window = Gui_Auto()

    sys.exit(app.exec_())