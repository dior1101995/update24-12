"""Bot Chức Năng"""




from pickle import TRUE
import re
from threading import  Lock, Event
from cv2 import CLAHE, TermCriteria_COUNT, copyTo, ellipse2Poly, matchTemplate , imread,  minMaxLoc, TM_CCORR_NORMED ,TM_CCOEFF_NORMED
from numpy import linspace
import imutils
import time

from win32api import Sleep
from New_Data_Image import *
from _congfig_bot import Setting_Bot
from _controller import  controller
from SQL_DB import SQLite



Exit_Event = Event()




class Bot_ChucNang:
    # Trạng Thái

    Running = False

    Sleep_Swipe = 0.9
    Sleep_Swipe_Event = 0.3

    lock = None
    screenshot = None
    TimeLoad = (0,100)

    # Close Quảng Cáo
    Thay_QuangCao = False
    Ckeck_NgayMayMan_XayDung = True
    Ckeck_NgayMayMan_HuanLuyen = True
    Ckeck_NgayMayMan_NghienCuu = True
    Ckeck_TrungTamPhucLoi = True

    
    # DeBug
    Debug = Setting_Bot.Debug
    def __init__(self):
        self.lock = Lock()


# Func Controller  
    def Docfiletext(self, duongdan):
        file_path = open("New_Data/%s.txt" % (duongdan), "r")
        f = file_path.readline()
        file_path.close()
        return f

    def Time_Check(self,Start_Time,Stop_Time = 0):
        print("                                                 ", f'{time.time() - int(Start_Time):.2f}' ,end="\r")

        if Stop_Time == 0:

            if time.time() - int(Start_Time) >= Setting_Bot.Delay_Load_Image:
                return True 
            else:
                return False

        else:            
            if time.time() - int(Start_Time) >= Stop_Time:
                return True 
            else:
                return False
        
        return False
            

    def Update_Database_Running(self, email, chucnang, giatri):
        with SQLite('DataText/running.db') as cur:
            cur.execute("Update running set " + str(chucnang) + " = ? where Email = ?", (giatri, email,))

    def Get_Database_Running(self, email, chucnang):
        DiemDanh = []
        KhieuChienRong = []
        ChoixucXac = []
        DoiHuyChuong = []
        CongHienLienMinh = []
        Naprong = []
        Taithiet = []
        LuyenLinh = []
        NangCapAnhHung = []
        BuaSanLuongMo = []
        Uoc = []
        TriThuong = []
        ThayPhap =[]
        GuiDaQuy = []
        XayDung = []
        HoatDongLienMinh = []
        false = [1]
        with SQLite('DataText/running.db') as cur:
            cur.execute("""select * from running where email = ?""", (email,))
            data = cur.fetchall()
            for row in data:
                DiemDanh.append(row[1])
                KhieuChienRong.append(row[2])
                ChoixucXac.append(row[3])
                DoiHuyChuong.append(row[4])
                CongHienLienMinh.append(row[5])
                Naprong.append(row[6])
                Taithiet.append(row[7])
                LuyenLinh.append(row[8])
                NangCapAnhHung.append(row[9])
                BuaSanLuongMo.append(row[10])
                Uoc.append(row[11])
                TriThuong.append(row[12])
                ThayPhap.append(row[13])
                GuiDaQuy.append(row[14])
                XayDung.append(row[15])
                HoatDongLienMinh.append(row[16])

            if chucnang == "DiemDanh":
                print("Runing________DiemDanh")
                return DiemDanh

            elif chucnang == "KhieuChienRong":
                print("Runing________KhieuChienRong")
                return KhieuChienRong

            elif chucnang == "ChoixucXac":
                print("Runing________ChoixucXac")
                return ChoixucXac

            elif chucnang == "DoiHuyChuong":
                print("Runing________DoiHuyChuong")
                return DoiHuyChuong

            elif chucnang == "CongHienLienMinh":
                print("Runing________CongHienLienMinh")
                return CongHienLienMinh

            elif chucnang == "Naprong":
                print("Runing________Naprong")
                return Naprong

            elif chucnang == "Taithiet":
                print("Runing________Taithiet")
                return Taithiet

            elif chucnang == "LuyenLinh":
                print("Runing________LuyenLinh")
                return LuyenLinh

            elif chucnang == "NangCapAnhHung":
                print("Runing________NangCapAnhHung")
                return NangCapAnhHung

            elif chucnang == "BuaSanLuongMo":
                print("Runing________BuaSanLuongMo")
                return BuaSanLuongMo

            elif chucnang == "Uoc":
                print("Runing________Uoc")
                return Uoc

            if chucnang == "TriThuong":
                print("Running______TriThuong")
                return TriThuong

            if chucnang == "ThayPhap":
                print("Running______ThayPhap")
                return ThayPhap

            if chucnang == "GuiDaQuy":
                print("Running______GuiDaQuy")
                return GuiDaQuy

            if chucnang == "XayDung":
                print("Running______XayDung")
                return XayDung

            if chucnang == "HoatDongLienMinh":
                return HoatDongLienMinh


            else:
                print("Sai Chuc Nang")
                return false

    def Check_QuangCao(self, anhnho, khoang_x=1, khoang_y=1, Click_Khac=False, khac_x=0, khac_y=0, Click=False,
                       Key_Event=False, sleep=0.1):
        

        result = matchTemplate(self.screenshot, anhnho.anh(), TM_CCORR_NORMED)
        (minVal, maxVal, minLoc, (x, y)) = minMaxLoc(result)

        if maxVal >= 0.9:

            if x + khoang_x >= int(anhnho.toado()[0]) >= x - khoang_x and y + khoang_y >= int(
                    anhnho.toado()[1]) >= y - khoang_y:

                self.Pause()

                if self.Debug: print(anhnho.name())

                if Click:
                    controller().Click(x + anhnho.x(), y + anhnho.y())

                if Click_Khac:
                    controller().Click(khac_x, khac_y)

                if Key_Event:
                    controller().KeyEvent("4")

                if Exit_Event.wait(timeout = 0.08):
                    return


                self.Continue()
                return True
            else:
                if Exit_Event.wait(timeout = Setting_Bot.Delay):
                    return False
                return False

        else:

            if Exit_Event.wait(timeout = Setting_Bot.Delay):
                return False

            return False

    def Check(self, anhnho, sleep= 0, Click=False, khoang_x=1, khoang_y=1, them_x=0, them_y=0, Click_Khac=False,
              khac_x=0, khac_y=0,threshold = 0.8 ):
        """ Check ảnh trong khoảng :x1,y1
        Click Vào Ví Trí Thay Đổi Liên Quan Đến x ,y: cod_x, cod_y
        Click Vào Vị Trí Khác khac_x,khac_y """

        
 
        result = matchTemplate(self.screenshot, anhnho.anh(), TM_CCORR_NORMED)     
        (minVal, maxVal, minLoc, (x, y)) = minMaxLoc(result)

        if maxVal >= threshold:

            if x + khoang_x >= int(anhnho.toado()[0]) >= x - khoang_x and y + khoang_y >= int(
                    anhnho.toado()[1]) >= y - khoang_y:
                if self.Debug: print(anhnho.name())
                if self.Running:
                    
                    if Click: controller().Click(x + anhnho.x() + them_x, y + anhnho.y() + them_y)

                    if Click_Khac: controller().Click(khac_x, khac_y)
                    
                    if sleep == 0:
                        if Exit_Event.wait(timeout= Setting_Bot.Delay_CLick): return False
                        return True

                    else:
                        if Exit_Event.wait(timeout=sleep): return False
                        return True

                else: 
                    if Exit_Event.wait(timeout=Setting_Bot.Delay): return False

            else:
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return False
                return False

        else:
            if Exit_Event.wait(timeout=Setting_Bot.Delay): return False
            return False

    def Check_Monter(self,anhnho,Click = False,sleep = 0):

        result = matchTemplate(self.screenshot, anhnho.anh(), TM_CCORR_NORMED)
        (minVal, maxVal, minLoc, (x, y)) = minMaxLoc(result)

        if maxVal >= 0.9:

            if x + 1 >= int(anhnho.toado()[0]) >= x - 1 and y + 1 >= int(anhnho.toado()[1]) >= y - 1:

                if self.Running:
                    if self.Debug: print(anhnho.name())

                    if Click:
                        controller().Click(x + anhnho.x() , y + anhnho.y() )

                    if sleep == 0:
                        if Exit_Event.wait(timeout= Setting_Bot.Delay_CLick):return False
                        return True

                    else:
                        if Exit_Event.wait(timeout=sleep):return False
                        return True

                else: return False

            else: return False

        return False

    def out_MHchinh(self,NgayMayMan_XayDung = True, NgayMayMan_HuanLuyen= True, NgayMayMan_NghienCuu = True, TrungTamPhucLoi = True):

        #CK Xây Dựng
        if NgayMayMan_XayDung:
            self.Ckeck_NgayMayMan_XayDung = True
        else:
            self.Ckeck_NgayMayMan_XayDung = False

        # CK Huấn Luyện
        if NgayMayMan_HuanLuyen:
            self.Ckeck_NgayMayMan_HuanLuyen = True
        else:
            self.Ckeck_NgayMayMan_HuanLuyen = False

        # CK Nghiên Cứu
        if NgayMayMan_NghienCuu:
            self.Ckeck_NgayMayMan_NghienCuu = True
        else:
            self.Ckeck_NgayMayMan_NghienCuu = False

        # CK TrungTaam Phúc Lợi
        if TrungTamPhucLoi:
            self.Ckeck_TrungTamPhucLoi = True
        else:
            self.Ckeck_TrungTamPhucLoi = False

        Start = time.time()
        for i in range(0,1000):
            print("       Out MH")
            if Exit_Event.wait(timeout=Setting_Bot.Delay):
                return 

            if  self.Running:

                if self.screenshot is None: continue


                if self.Check(image_SkillLanhChua.MoSach,) and self.Check(image_DangNhap.ThanhBenTrong) and self.Check(image_TongQuan.Mo_TongQuan) or self.Check(image_TongQuan.Mo_TongQuan) and self.Check(image_DangNhap.ThanhBenNgoai) and self.Check(image_SkillLanhChua.MoSach,) :
                    return True


                elif self.Check(image_TongQuan.Dong_TongQuan, Click=True):
                    Start = time.time()
                    continue

                elif self.Check(image_close_QuangCao.Onemt):
                    Exit_Event.wait(0.5)
                    Start = time.time()
                    continue

                elif self.Check(image_close_QuangCao.Wellcome_game):
                    Exit_Event.wait(0.5)
                    Start = time.time()
                    continue

                elif self.Check(image_close_QuangCao.Open_game):
                    Exit_Event.wait(0.5)
                    Start = time.time()
                    continue


                else:
                    if  self.Running:
                        if self.Check(image_close_QuangCao.Keyblack, Click=True,sleep = 0.1) or  self.Check(image_close_QuangCao.Keyblack2, Click=True,sleep = 0.1):
                            Start = time.time()
                            continue

                        if self.Check(image_close_QuangCao.ThoatGame):
                            Exit_Event.wait(0.5)
                            Start = time.time()
                            return

                            
                        if self.Check(image_TongQuan.Dong_TongQuan, Click=True,sleep =0.08):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,2):
                                controller().KeyEvent("4")
                                Start = time.time()
                                

                    else:
                        while not self.Running: 
                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                        Start = time.time()


            else:
                while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()


        if not Exit_Event.is_set() and self.Running == True:
            controller().ResetGame()
        
    def Check_Mutil_zoom(self, anhnho, sleep=0.3, Click=False):

        for scale in linspace(0.2, 1.0, 20)[::-1]:
            if Exit_Event.is_set():
                return

            if self.Running:
                if scale <= 0.4:
                    break

                resized = imutils.resize(anhnho.anh(), width=int(anhnho.needle_w * scale))
                w, h = resized.shape[::-1]
                res = matchTemplate(self.screenshot, resized, TM_CCORR_NORMED)
                (minVal, maxVal, minLoc, (x, y)) = minMaxLoc(res)

                if maxVal >= 0.8:
                    if x + 200 >= int(anhnho.toado()[0]) >= x - 200 and y + 200 >= int(anhnho.toado()[1]) >= y - 200:
                        if Click:
                            Exit_Event.wait(timeout= 0.1)
                            controller().Click(x + anhnho.x(), y + anhnho.y())
                            Exit_Event.wait(timeout= 0.1)

                        return True
        return False



    def Close_QuangCao(self):

 

        while True:

            if Exit_Event.wait(timeout=Setting_Bot.Delay):
                return

            if self.screenshot is None: continue

            if self.Check_QuangCao(image_close_QuangCao.TroGiupLienMinh,Click=True):
                pass


            if self.Check_QuangCao(image_close_QuangCao.Loi_Mang, Click_Khac=True, khac_x=182, khac_y=418):
                pass

            if self.Check_QuangCao(image_close_QuangCao.ChieuMoChiaSeLienMinh,Click_Khac=True,khac_x = 106 ,khac_y=654 ):
                pass

            if self.Check_QuangCao(image_close_QuangCao.Oops_ThuLai, khoang_x=15, Click_Khac=True, khac_x=173, khac_y=419):
                pass

            if self.Check_QuangCao(image_close_QuangCao.Oops_ThuLai2, Click=True):
                pass
            if self.Check_QuangCao(image_close_QuangCao.ThoatGame, Click_Khac=True,khac_x = 29,khac_y = 51):

                pass


            if self.Check_QuangCao(image_close_QuangCao.DangNhapNoiKhac,Click_Khac=True,sleep = 0.5,khac_x=186,khac_y = 422):
                pass


            if self.Check_QuangCao(image_close_QuangCao.Close_1, Click=True):
                pass

            if self.Check_QuangCao(image_close_QuangCao.Open_game, Click=True,sleep=0.2):
                pass

            if self.Check_QuangCao(image_close_QuangCao.Opps_Het_Time_DangNhap, Click_Khac=True, khac_x=173,
                                       khac_y=419, sleep=0.2):
                pass

            if self.Check_QuangCao(image_close_QuangCao.NgayMayMan, Click=True):
                pass
            if self.Check_QuangCao(image_close_QuangCao.NapTien, Key_Event=True):
                pass
    



            if self.Check_QuangCao(image_close_QuangCao.ThoatGame, Click_Khac=True,khac_x = 29,khac_y = 51):

                pass



            if self.Ckeck_NgayMayMan_XayDung == True:
                if self.Check_QuangCao(image_close_QuangCao.CK_NgayMayMan_NangCap,Key_Event =True):
                    continue

            if self.Ckeck_NgayMayMan_HuanLuyen == True:
                if self.Check_QuangCao(image_close_QuangCao.CK_NgayMayMan_HuanLuyen,Key_Event =True):
                    continue

            if self.Ckeck_NgayMayMan_NghienCuu == True:
                if self.Check_QuangCao(image_close_QuangCao.CK_NgayMayMan_HocVien,Key_Event =True):
                    continue

            if self.Ckeck_TrungTamPhucLoi == True:
                if self.Check_QuangCao(image_close_QuangCao.TrungTamPhucLoi,Key_Event =True):
                    continue



# Chuc Nang

    def Kick_Hoat_Vip(self):
        '''Kich Hoat Vip'''
        print("Kích Hoạt Vip")

        for i in range(self.TimeLoad[0],self.TimeLoad[1]):
            if Exit_Event.wait(timeout=Setting_Bot.Delay): return

 
            if self.Running:
                if self.screenshot is None: continue
                if self.Check(image_KickHoat_Vip.CK_KickHoatVip,Click_Khac=True ,khac_x =181, khac_y =419):
                    Start = time.time()
                    for i in range(self.TimeLoad[0],self.TimeLoad[1]):

                        if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                        if self.Running:
                            if self.screenshot is None: continue

                            if self.Check(image_KickHoat_Vip.SuDung_Vip,Click=True):
                                return True
                            if self.Check(image_KickHoat_Vip.Vip_30Day,Click=True):
                                Start = time.time()
                                continue

                            elif self.Check(image_KickHoat_Vip.Vip_Thuong,Click=True):
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    self.out_MHchinh()
                                    return False


                        else:
                            while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()

                    self.out_MHchinh()
                    return False   
                    
                
                elif self.Check(image_KickHoat_Vip.KickHoatVip,Click_Khac=True ,khac_x =181, khac_y =419):
                    Start = time.time()
                    continue

                elif self.Check(image_KickHoat_Vip.TrungTam_KickHoatVip,Click=True):
                    Start = time.time()
                    continue
                else:
                    if self.Time_Check(Start):
                        return False
            else:
                while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()

        self.out_MHchinh()
        return False       


    def DangNhap(self, Email, Password):
        '''Dang Nhap Email'''

        print("Đăng Nhập")
        Ck_VuiLongNhapDiaChiEmail = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(1,300):

                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if  self.Running:
                        
                    if self.screenshot is None: continue

                    if Ck_VuiLongNhapDiaChiEmail:

                        if self.Check(image_DangNhap.VuiLongNhapDiaChiEmail, Click=True, them_x=-100, sleep=0.5,):
                            if not Exit_Event.is_set():
                                controller().SendText(Email)
                            if not Exit_Event.is_set():
                                controller().KeyEvent("20")
                            if not Exit_Event.is_set():
                                controller().SendText(Password)

                            Start = time.time()
                            for i in range(1,300):

                                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                                if  self.Running:

                                    if self.screenshot is None: continue

                                    if self.Check(image_DangNhap.ThanhBenTrong) or self.Check(image_DangNhap.ThanhBenNgoai):
                                        return

                                    elif self.Check(image_DangNhap.DaDangNhapHopThu):
                                        if not Exit_Event.is_set():
                                            controller().KeyEvent("4")
                                        if not Exit_Event.is_set():
                                            controller().KeyEvent("4")
                                        self.out_MHchinh()

                                    elif self.Check(image_DangNhap.DangNhap2, Click=True):
                                        pass

                                    elif self.Check(image_close_QuangCao.Wellcome_game,sleep=0.3):
                                        Start = time.time()
                                    else:
                                        if self.Time_Check(Start,10):
                                            return

                                else:
                                    while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()

                            self.out_MHchinh()
                            return 


                    elif self.Check(image_DangNhap.ChuyenDoiTaiKhoan, Click=True):
                        Start = time.time()
                        Ck_VuiLongNhapDiaChiEmail = True
                        continue

                    elif self.Check(image_DangNhap.TaiKhoan, Click=True):
                        Start = time.time()
                        continue

                    elif self.Check(image_DangNhap.CaiDat, Click=True):
                        Start = time.time()
                        continue

                    elif self.Check(image_DangNhap.ThanhBenTrong, Click=True, them_y=-600) or self.Check(image_DangNhap.ThanhBenNgoai, Click=True, them_y=-600):
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()


                else:
                    while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()

        self.out_MHchinh()
        return   


    def NhanQua_BenCang(self):
        """Nhận Quà BẾn Cảng"""

        print("Nhận Quà Bến Cảng")
        SwipeBenCang = self.Docfiletext("TongQuan/Swipebencang")
        saikhac2 = 0

        Click_Dohang = False
        Mo_TongQuan = True
        Check_TongQuan = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):

                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                # Check Map Bên Ngoài
                    if self.Check(image_DangNhap.ThanhBenNgoai, Click=True):
                        continue

                # Check Tổng Quan
                    if Check_TongQuan:

                        if self.Check(image_TongQuan.CK_TongQuan):
                            if self.Check(image_TongQuan.PhaiLamHangNgay, Click=True, sleep=0.3) or self.Check(
                                    image_TongQuan.PhaiLamHangNgay2, Click=True, sleep=0.3):

                                controller().Swipe(SwipeBenCang)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)
                                Start = time.time()

                                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                                    if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                                    if self.Running:

                                        if self.screenshot is None: continue

                                    # Click Quá 3 lần
                                        if saikhac2 == 3:
                                            return False

                                    # Click Dỡ Hàng
                                        if self.Check(image_TongQuan.DoHang, khoang_y=300, Click=True, them_x=200):
                                            saikhac2 = saikhac2 + 1
                                            Click_Dohang = True
                                            Start = time.time()
                                            continue

                                    # Check Bến Cảng
                                        if Click_Dohang == True:
                                            print("CK Bến Cảng")
                                            if self.Check(image_BenCang.YeuCau_BenCang, Click=True,sleep =0.3):
                                                return True

                                            elif self.Check(image_BenCang.CK_BenCang):
                                                Start = time.time()
                                            
                                                if self.Check(image_BenCang.BenCang,Click=True):
                                                    Start = time.time()
                                                    continue

                                                if self.Check(image_TongQuan.TroGiupLienMinh,Click=True):
                                                    continue

                                                else:
                                                    if self.Time_Check(Start):
                                                        return False

                                            else:
                                                if self.Time_Check(Start):
                                                    return False

                                        else:
                                            if self.Time_Check(Start):
                                                return False

                                    else:
                                        while not self.Running: 
                                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                                return 
                                        Start = time.time()


                                return False

                            else:
                                if self.Time_Check(Start):
                                    return False


                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Mo_TongQuan = True
                                Check_TongQuan = False
                                Start = time.time()

                # Click Tổng Quan
                    if Mo_TongQuan:
                        if self.Check(image_TongQuan.Mo_TongQuan,Click=True):
                            Mo_TongQuan = False
                            Check_TongQuan = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Start = time.time()
                    

                else:
                    while not self.Running: Exit_Event.wait(timeout= Setting_Bot.Delay) ; Start = time.time()
            return False


    def Nhan_Qua_DangNhap(self, Email):
        """"Nhận Quà Đăng Nhập, Điểm Danh"""

        nhan1quadangnhap = False
        def Qua_DangNhap(self):
            nonlocal nhan1quadangnhap
            print("Nhận Quà Đăng Nhập")

            Check_TrungTamPhucLoi = False
            Check_BenCang = True

            if self.out_MHchinh(TrungTamPhucLoi = False):
                Start = time.time()

                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                    if Exit_Event.wait(timeout=Setting_Bot.Delay):
                        return
                    if self.Running:
                        if self.screenshot is None: continue

                    # Check Trung Tâm Phúc Lợi
                        if Check_TrungTamPhucLoi:
                            if self.Check(image_Qua_DangNhap.CK_TrungTamPhucLoi):
                                if self.Check(image_Qua_DangNhap.DaNhan_DangNhap, khoang_x=3,Click_Khac = True,khac_x=32 ,khac_y =54,sleep = 0.1):
                                    return True

                                elif self.Check(image_Qua_DangNhap.YeuCau_DangNhap, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return False
                            else:
                                if self.Time_Check(Start):
                                    return False

                    # Check Bến Cảng
                        if Check_BenCang:
                            if self.Check(image_BenCang.CK_BenCang):
                                if self.Check(image_Qua_DangNhap.DangNhap_1,Click=True):
                                    Check_TrungTamPhucLoi = True
                                    Check_BenCang = False
                                    nhan1quadangnhap = True
                                    Start = time.time()


                                if self.Check(image_Qua_DangNhap.DangNhap, khoang_y=30, khoang_x=30, Click=True):
                                    Check_TrungTamPhucLoi = True
                                    Check_BenCang = False
                                    Start = time.time()
                                    continue

                                elif self.Check(image_Qua_DangNhap.KhinhKhiCau, khoang_y=5, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return False

                            else:
                                if self.Time_Check(Start):
                                    return False

                        else:
                            if self.Time_Check(Start):
                                return False

                    else:
                        while not self.Running: 
                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                        Start = time.time()


                return False

        def Qua_DiemDanh(self):
            print("Nhận Quà Điểm Danh")
            Check_TrungTamPhucLoi = False
            Check_BenCang = True

            if self.out_MHchinh(TrungTamPhucLoi = False):
                Start = time.time()
                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                    if Exit_Event.wait(timeout=Setting_Bot.Delay):
                        return
                    if self.Running:

                        if self.screenshot is None: continue

                        if nhan1quadangnhap == True:
                            return True

                    # Check Trung Tâm Phúc Lợi
                        if Check_TrungTamPhucLoi :
                            if self.Check(image_Qua_DangNhap.CK_TrungTamPhucLoi, ):
                                if self.Check(image_Qua_DangNhap.DaNhan_ThangDiemDanh,Click_Khac=True,khac_x =32 ,khac_y =54,sleep = 0.1):
                                    return True

                                elif self.Check(image_Qua_DangNhap.ThangDiemDanh_DangNhap, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return False
                            else:
                                if self.Time_Check(Start):
                                    return False


                    # Check Bến Cảng
                        if Check_BenCang:
                            if self.Check(image_BenCang.CK_BenCang):
                                if self.Check(image_Qua_DangNhap.ThangDiemDanh, khoang_y=30, khoang_x=30, Click=True):
                                    Check_TrungTamPhucLoi = True
                                    Check_BenCang = False
                                    Start = time.time()
                                    continue

                                elif self.Check(image_Qua_DangNhap.KhinhKhiCau, khoang_y=5, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return False
                            
                            else:
                                if self.Time_Check(Start):
                                    return False

                        else:
                            if self.Time_Check(Start):
                                return False

                    else:
                        while not self.Running: 
                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                        Start = time.time()

                return False

        if Qua_DangNhap(self):
            if Qua_DiemDanh(self):
                self.Update_Database_Running(email=Email, chucnang="DiemDanh", giatri=1)


    def KhieuChienRong(self,Email):
        """"Khiêu Chiến Rồng"""
        print("Khiêu Chiến Rồng")
        Nha_ThuThachRong =True
        Vao_ThuThachRong = False
        Check_ThuThachRong = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay):
                    return

                if self.Running:
                    if self.screenshot is None: continue

                # Check Thử Thách Rồng
                    if Check_ThuThachRong:
                        if self.Check(image_KhoTang_TTrong.Close_CheDoNhanh,Click=True) or self.Check(image_KhoTang_TTrong.OK_CheDoNhanh,Click=True):
                            self.Update_Database_Running(email=Email, chucnang="KhieuChienRong", giatri=1)
                            return

                        elif self.Check(image_KhoTang_TTrong.CK_ThuThachRong):
                            if self.Check(image_KhoTang_TTrong.CheDoNhanh,Click=True,sleep = 0.1):
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Time_Check(Start):
                                return

                # Check Vào Thử Thách Rồng
                    elif Vao_ThuThachRong:
                        if self.Check(image_KhoTang_TTrong.ThuThachRong,Click=True,khoang_x =90,khoang_y =20):# or self.Check(image_KhoTang_TTrong.KhoTang2,Click=True):
                            Start = time.time()
                            Vao_ThuThachRong = False
                            Check_ThuThachRong = True
                            continue

                        else:
                            if self.Time_Check(Start,2):
                                return
                            
                # Check Nhà Event Thử Thách Rồng
                    elif Nha_ThuThachRong:
                        if self.Check(image_KhoTang_TTrong.CK_Vao_ThuThachRong):
                            if self.Check(image_KhoTang_TTrong.NhaEvent_2,Click=True):
                                Vao_ThuThachRong = True
                                Nha_ThuThachRong = False
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start):
                                    return
                            
                        else:
                            if self.Time_Check(Start):
                                return

                    else:
                        if self.Time_Check(Start):
                            return

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                    Start = time.time()

            return


    def Kho_Tang(self,Email):
        """"Xúc Xắc Kho Tàng"""
        print("Xúc Xắc Kho Tàng")

        daquay_khancap = False
        chothoat = False
        CK_MoKhoTang = False
        Quay_KhoTang = False
        CK_KhoTang = False
        CK_BenCang = True

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:
                    if self.screenshot is None: continue

                # Ckeck Quay Kho Tàng
                    if Quay_KhoTang:
                    # Hết Vip Hoặc Dưới Vip 6
                        if self.Check(image_KhoTang_TTrong.DuoiVip6):
                            self.Update_Database_Running(email=Email, chucnang="ChoixucXac", giatri=1)
                            return
                    #Check Kho Tàng
                        if self.Check(image_KhoTang_TTrong.CK_Quay_KhoTang):

                            if self.Check(image_KhoTang_TTrong.KetThuc,Click=True):
                                Start = time.time()
                        # Nếu Đã Quay Miễn Phí
                                if daquay_khancap == True:
                                    chothoat = True
                                    continue

                        # Quay Miễn Phí
                            elif self.Check(image_KhoTang_TTrong.KhanCap_MienPhi,Click=True):
                                Start = time.time()
                                continue

                            if chothoat == True:
                                if self.Check(image_KhoTang_TTrong.KhanCap10):
                                    self.Update_Database_Running(email=Email, chucnang="ChoixucXac", giatri=1)
                                    return
                            else:
                        # Quay Khẩn Cấp 10 Xu
                                if self.Check(image_KhoTang_TTrong.KhanCap10,Click=True):
                                    daquay_khancap =True
                                    Start = time.time()
                                    continue
                        
                        else:
                            if self.Time_Check(Start):
                                return

                # Check Lượt Miễn Phí Màn Kho Tàng
                    elif  CK_KhoTang:            
                        if self.Check(image_KhoTang_TTrong.CK_KhoTang):
                            if self.Check(image_KhoTang_TTrong.MienPhi,Click=True):
                                CK_KhoTang = False
                                Quay_KhoTang = True
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,1):
                                    print("Không Thấy Miễn Phí")
                                    self.Update_Database_Running(email=Email, chucnang="ChoixucXac", giatri=1)
                                    return
                        else:
                            if self.Time_Check(Start):
                                return

                # Check Vào Kho Tàng
                    elif CK_MoKhoTang:
                        if self.Check(image_KhoTang_TTrong.KhoTang,Click=True) or self.Check(image_KhoTang_TTrong.KhoTang2,Click=True):
                            CK_MoKhoTang = False
                            CK_KhoTang = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                return

                # Check Bến Cảng
                    elif CK_BenCang:
                        if self.Check(image_BenCang.CK_BenCang):
                            if self.Check(image_KhoTang_TTrong.NhaEvent,Click=True):
                                CK_BenCang = False
                                CK_MoKhoTang = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Time_Check(Start):
                                return
                    else:
                        if self.Time_Check(Start):
                            return

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

            return


    def ChieuMo_AnhHung(self):
        print("Chiêu Mộ Anh Hùng")

        Swipe_CongXuong = self.Docfiletext("TongQuan/Swipe_CongXuong")
        CK_CongXuong = False
        Mo_TongQuan = True
        CK_TongQuan = False
        VaoChieuMoAnhHung = False
        Ok_ChieuMoXong = False
        Chieu_Mo = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                

                if self.Running:

                    if self.screenshot is None: continue

                # Check Thành Bên ngoài
                    if self.Check(image_DangNhap.ThanhBenNgoai,Click=True):
                            continue

                # Check Mở Tổng Quan
                    if CK_TongQuan:
                        if self.Check(image_TongQuan.CK_TongQuan):
                            if self.Check(image_TongQuan.PhaiLamHangNgay, Click=True, sleep=0.3) or self.Check(
                                    image_TongQuan.PhaiLamHangNgay2, Click=True, sleep=0.3):
                                controller().Swipe(Swipe_CongXuong)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)
                                Start = time.time()
                                for i in range(self.TimeLoad[0],self.TimeLoad[1]):

                                    if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                

                                    if self.Running:

                                        if self.screenshot is None: continue


                                    # Vào Chiêu Mộ anh Hùng
                                        if VaoChieuMoAnhHung:
                                            # Chiêu Mộ
                                            if Chieu_Mo:
                                                if self.Check(image_ChieuMoAnhHung.CK_ChieuMoAnhHung):
                                                    if self.Check(image_ChieuMoAnhHung.MienPhi_Vang,Click=True,sleep = 0.3):
                                                        Ok_ChieuMoXong = True
                                                        Chieu_Mo = False
                                                        Start = time.time()
                                                        continue
                                                                    
                                                    elif self.Check(image_ChieuMoAnhHung.MienPhi_Thuong,Click=True,sleep = 0.3):
                                                        Ok_ChieuMoXong = True
                                                        Chieu_Mo =False
                                                        Start = time.time()
                                                        continue

                                                    else:
                                                        if self.Time_Check(Start):
                                                            return

                                                else:
                                                    if self.Time_Check(Start):
                                                        return

                                            # Chiêu Mộ Xong
                                            if Ok_ChieuMoXong:
                                                if self.Check(image_ChieuMoAnhHung.Ok_ChieuMoXong,Click=True):
                                                    return
                                                elif self.Check(image_ChieuMoAnhHung.OK_RaAnhHung,Click=True):
                                                    Start = time.time()
                                                    continue
                                                else:
                                                    if self.Time_Check(Start):
                                                        return  

                                            else:
                                                if self.Time_Check(Start):
                                                    return                                                  


                                    # Check Công Xưởng
                                        if CK_CongXuong:
                                            if self.Check(image_TongQuan.CK_CongXuong):
                                                if self.Check(image_ChieuMoAnhHung.VaoChieuMoAnhHung,Click=True):
                                                    VaoChieuMoAnhHung = True
                                                    Chieu_Mo = True
                                                    CK_CongXuong = False
                                                    Start = time.time()
                                                    continue

                                                else:
                                                    if self.Time_Check(Start):
                                                        return
                                            else:
                                                if self.Time_Check(Start):
                                                    return

                                    # Mở công Xưởng
                                        elif self.Check(image_TongQuan.CongXuong, khoang_y=300, Click=True, them_x=200):
                                            CK_CongXuong = True
                                            Start = time.time()
                                            continue
                                        else:
                                            if self.Time_Check(Start):
                                                return
                                        
                                    else:
                                        while not self.Running: 
                                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                                return 
                                        Start = time.time()

                                
                                return

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Mo_TongQuan = True
                                CK_TongQuan = False
                                Start = time.time()
                # Mở Tổng Quan
                    if Mo_TongQuan:
                        if self.Check(image_TongQuan.Mo_TongQuan,Click=True):
                            Start = time.time()
                            Mo_TongQuan = False
                            CK_TongQuan = True
                            continue


                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Start = time.time()

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()



    def Thay_Phap(self,Email):
        print("Thầy Pháp")
        CK_CongXuong = True
        CK_ThayPhap = False

        Da_Click_Mua = False
        Ok_LamMoi = False

        Thay_Mua = True
        Lam_Moi =False

        Da_LamMoi20 = False

        if self. out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if CK_ThayPhap:

                        if self.Check(image_close_QuangCao.HetDaQuy):
                            self.Update_Database_Running(email=Email, chucnang="ThayPhap", giatri=1)
                            self.out_MHchinh()
                            return

                        if self.Check(image_UocFree.DungDaQuy, Click=True):
                                Start = time.time()
                                continue

                        if self.Check(image_ThayPhap.DayLaMonHangQuy_TiepTucLamMoi,Click_Khac = True,khac_x = 29,khac_y = 51):
                            Start = time.time()
                            continue

                        if Ok_LamMoi:
                            if self.Check(image_ThayPhap.OK_LamMoi,Click=True):
                                Ok_LamMoi = False
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return

                        if Da_Click_Mua:
                            print("VaoDAyu")
                            if self.Check(image_ThayPhap.Mua_1Da,Click=True,them_y= 28):
                                Start = time.time()
                                Da_Click_Mua = False
                                continue

                            if self.Check(image_ThayPhap.BanKhongDuNguonLuc,Click_Khac=True,khac_x= 29, khac_y= 51):
                                self.Update_Database_Running(email=Email, chucnang="ThayPhap", giatri=1)
                                return

                            if self.Check(image_close_QuangCao.HetDaQuy):
                                self.Update_Database_Running(email=Email, chucnang="ThayPhap", giatri=1)
                                return

                            else:
                                if self.Time_Check(Start):
                                    return

                        if self.Check(image_ThayPhap.CK_ThayPhap,sleep=0.2):
                            
                            if Thay_Mua:
                                if self.Check(image_ThayPhap.Mua_Mon_HangQuy,Click =True,khoang_y= 300,them_y= 20):
                                    Da_Click_Mua = True
                                    Start = time.time()
                                    continue

                                elif self.Check(image_ThayPhap.Mua_Bac_1,Click=True,khoang_y =300,) or self.Check(image_ThayPhap.Mua_KL_1,Click=True,khoang_y =300) or self.Check(image_ThayPhap.Mua_Go_1,Click=True,khoang_y =300) or self.Check(image_ThayPhap.Mua_Lua_1,Click=True,khoang_y =300):
                                    Exit_Event.wait(timeout= 0.1)
                                    Da_Click_Mua = True
                                    Start = time.time()
                                    continue

                                else:
                                    if Da_LamMoi20:
                                        self.Update_Database_Running(email=Email, chucnang="ThayPhap", giatri=1)
                                        self.out_MHchinh()
                                        return

                                    if self.Time_Check(Start,1):
                                        Thay_Mua = False
                                        Lam_Moi = True

                            if Lam_Moi:
                                if self.Check(image_ThayPhap.LamMoi_MienPhi,Click=True):
                                    Da_Click_Mua = False
                                    Lam_Moi = False
                                    Thay_Mua = True
                                    Start = time.time()
                                    continue

                                if self.Check(image_ThayPhap.LamMoi_20Da):
                                    Da_LamMoi20 = True
                                    Lam_Moi = False
                                    Thay_Mua = True
                                    continue

                                if self.Check(image_ThayPhap.LamMoi_5Da,Click=True):
                                    Lam_Moi = False
                                    Thay_Mua = True

                                    Ok_LamMoi = True
                                    Da_Click_Mua = False
                                    Start = time.time()


                                elif self.Check(image_ThayPhap.LamMoi_10Da,Click=True):
                                    Lam_Moi = False
                                    Thay_Mua = True
                                    Ok_LamMoi = True
                                    Da_Click_Mua = False
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return

                        else:
                            if self.Time_Check(Start):
                                return

                # Check Công Xưởng
                    if CK_CongXuong:
                        if self.Check(image_TongQuan.CK_CongXuong):
                            if self.Check(image_ThayPhap.VaoThayPhap,Click=True):
                                CK_ThayPhap = True
                                CK_CongXuong = False
                                Start = time.time()

                            else:
                                if self.Time_Check(Start):
                                    return
                        else:
                            if self.Time_Check(Start):
                                return

                    else:
                        if self.Time_Check(Start):
                            return
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                             return 
                    Start = time.time()

            return


    def Skill_LanhChua(self):
        print("Sử Dụng Skill Lãnh Chúa")

        def skill_muagat():
            Da_MoSach = False
            Check_KyNangLanhChua = False
            Start = time.time()
            if self.out_MHchinh():
                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                    if Exit_Event.wait(timeout=Setting_Bot.Delay):
                        return 

                    if self.Running:

                        if self.screenshot is None: continue

                    # Sau Khi Click Kỹ Năng Lãnh Chúa 
                        if Check_KyNangLanhChua == True:
                            if self.Check(image_SkillLanhChua.CK_KyNangLanhChua,):

                                if self.Check(image_SkillLanhChua.Tang_SanLuong_DangNguoi,Click_Khac= True, khac_x =31 ,khac_y=52,sleep = 0.05):
                                    controller().Click(31,52)
                                    return

                                if self.Check(image_SkillLanhChua.SuDung_Skill, Click=True,sleep = 0.3):
                                    return

                                elif self.Check(image_SkillLanhChua.Skill_MuaGat, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start,1): 
                                        controller().Click(31,52)
                                        Exit_Event.wait(timeout=Setting_Bot.Delay_CLick)
                                        controller().Click(31,52)
                                        Exit_Event.wait(timeout=Setting_Bot.Delay_CLick)
                                        return
                            
                            else:
                                if self.Time_Check(Start):
                                    return

                    # Sau Khi Mở Sách
                        if Da_MoSach == True:
                            if self.Check(image_SkillLanhChua.KyNangLanhChua, Click=True):
                                Check_KyNangLanhChua = True
                                Da_MoSach = False
                                Start = time.time()
                                continue

                          
                            else:
                                if self.Time_Check(Start):
                                    Da_MoSach = False
                                    self.out_MHchinh()
                                    Start = time.time()
                                    continue

                    # Mở Sách
                        elif self.Check(image_SkillLanhChua.MoSach, Click=True, threshold =0.9,sleep = 0.1):
                            Da_MoSach = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Start = time.time()

                    else:
                        while not self.Running: 
                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                        Start = time.time()


                return
        def skill_thuthap():
            Da_MoSach = False
            Check_KyNangLanhChua = False
            Start = time.time()

            if self.out_MHchinh():
                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                    if Exit_Event.wait(timeout=Setting_Bot.Delay):
                        return 

                    if self.Running:

                        if self.screenshot is None: continue

                    # Sau Khi Click Kỹ Năng Lãnh Chúa
                        if Check_KyNangLanhChua:

                            if self.Check(image_SkillLanhChua.CK_KyNangLanhChua, ):
                                
                                if self.Check(image_SkillLanhChua.ThuThap_DangNguoi,Click_Khac= True, khac_x =31 ,khac_y=52,sleep = 0.05):
                                    controller().Click(31,52)
                                    return

                                if self.Check(image_SkillLanhChua.ThuThap_DangduyTri,Click_Khac= True, khac_x =31 ,khac_y=52,sleep = 0.05):
                                    controller().Click(31,52)
                                    return

                                if self.Check(image_SkillLanhChua.SuDung_Skill, Click=True,sleep=0.3):
                                    return

                                elif self.Check(image_SkillLanhChua.Skill_ThuThap, Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start,1):
                                        controller().Click(31,52)
                                        Exit_Event.wait(timeout=Setting_Bot.Delay_CLick)
                                        controller().Click(31,52) 
                                        Exit_Event.wait(timeout=Setting_Bot.Delay_CLick)
                                        return

                            else:
                                if self.Time_Check(Start):

                                    return

                    # Sau Mở Sách
                        if Da_MoSach:
                            if self.Check(image_SkillLanhChua.KyNangLanhChua, Click=True):
                                Check_KyNangLanhChua = True
                                Da_MoSach = False
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    self.out_MHchinh()
                                    Da_MoSach = False
                                    Start = time.time()
                                    continue
                            
                    # Mở Sách
                        elif self.Check(image_SkillLanhChua.MoSach, Click=True, threshold =0.9,sleep=0.1):
                            Da_MoSach = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Start = time.time()

                    else:
                        while not self.Running: 
                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                return 
                        Start = time.time()

                return
        skill_muagat()
        skill_thuthap()


    def NangCapAnhHung(self,Email,vitrianhhung : int):
        """Nâng Cấp Anh Hùng"""
        print("Nâng Cấp Anh Hùng")
        CK_TongQuan_AnhHung = False
        CK_ChiTiet_AnhHung = False
        CK_NangCap = False
        DaNangCap = 0

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:

                    if self.screenshot is None: continue

                    if CK_NangCap:
                        if DaNangCap>=2:
                            self.Update_Database_Running(email=Email, chucnang="NangCapAnhHung", giatri=1)
                            return

                        if self.Check(image_NangCapAnhHung.KinhNghiem300,Click=True):
                            DaNangCap +=1
                            Start = time.time()
                            continue

                        
                        else:
                            if self.Time_Check(Start):
                                return





                    if CK_ChiTiet_AnhHung:
                        if self.Check(image_NangCapAnhHung.NangCap,Click=True):
                            CK_NangCap = True
                            CK_ChiTiet_AnhHung = False
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                return





                # Check Tổng Quan Anh hùng
                    if CK_TongQuan_AnhHung:
                        if self.Check(image_NangCapAnhHung.TongQuan_AnhHung,sleep = 0.1):
                            if vitrianhhung == 1:
                                controller().Click(65, 298)
                            if vitrianhhung == 2:
                                controller().Click(152, 298)
                            if vitrianhhung == 3:
                                controller().Click(234, 298)                    
                            if vitrianhhung == 4:
                                controller().Click(330, 298)

                            if vitrianhhung == 5:
                                controller().Click(65, 421)
                            if vitrianhhung == 6:
                                controller().Click(152, 421)
                            if vitrianhhung == 7:
                                controller().Click(234, 421)
                            if vitrianhhung == 8:
                                controller().Click(330, 421)  


                            if vitrianhhung == 9:
                                controller().Click(65, 560)
                            if vitrianhhung == 10:
                                controller().Click(152, 560)
                            if vitrianhhung == 11:
                                controller().Click(234, 560)              
                            if vitrianhhung == 12:
                                controller().Click(330,560)



                            CK_TongQuan_AnhHung =False
                            CK_ChiTiet_AnhHung = True
                            Start = time.time()

                            
                        else:
                            if self.Check(image_NangCapAnhHung.CK_KyNangAnhHung,Click_Khac=True, khac_x = 14, khac_y= 43,sleep = 0.2):
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return


                # Vào Anh Hùng
                    elif self.Check(image_NangCapAnhHung.AnhHung,Click=True):
                        Start = time.time()
                        CK_TongQuan_AnhHung = True
                        continue

                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            Start = time.time()


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                             return 
                    Start = time.time()

            return


    def Tri_Thuong(self, Email):
        """"Trị Thương"""
        print("Trị Thương")
        SwipeDieuTri = self.Docfiletext("TongQuan/SwipeDieuTri")
        saikhac1 = 0
        Mo_TongQuan = True
        Check_TongQuan = False
        Click_DieuTri = False

        if self.out_MHchinh():
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                # Check Bên Ngoài
                    if self.Check(image_DangNhap.ThanhBenNgoai, Click=True):
                        continue

                # Check Tổng Quan
                    if Check_TongQuan:
                        if self.Check(image_TongQuan.CK_TongQuan):
                            if self.Check(image_TongQuan.QuanSu, Click=True, sleep=0.3) or self.Check(
                                    image_TongQuan.QuanSu_2, Click=True, sleep=0.3):
                                controller().Swipe(SwipeDieuTri)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)

                                Start = time.time()
                                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                                    if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                                    if self.Running:

                                        if self.screenshot is None: continue

                                    # Click Điều Trị 3 Lần
                                        if saikhac1 == 3:
                                            self.Update_Database_Running(email=Email, chucnang="TriThuong", giatri=1)
                                            self.out_MHchinh()
                                            return

                                    # Sau Click Điều Trị
                                        if Click_DieuTri:
                                            if self.Check(image_DieuTri.DieuTri_BenhVien, Click=True):
                                                self.out_MHchinh()
                                                self.Update_Database_Running(email=Email, chucnang="TriThuong", giatri=1)
                                                return

                                            else:
                                                if self.Time_Check(Start):
                                                    return

                                    # Click Điều Trị
                                        if self.Check(image_TongQuan.DieuTri, khoang_y=300, Click=True, them_x=200):
                                            saikhac1 += 1
                                            Click_DieuTri = True
                                            Start = time.time()

                                        else:
                                            if self.Time_Check(Start):
                                                return

                                    else:
                                        while not self.Running: 
                                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                                return 
                                        Start = time.time()


                                return

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Mo_TongQuan = True
                                Check_TongQuan = False
                                Start = time.time()

                # Mở Tổng Quan
                    if Mo_TongQuan:
                        if self.Check(image_TongQuan.Mo_TongQuan,Click=True,):
                            Mo_TongQuan = False
                            Check_TongQuan = True
                            Start = time.time()
                            continue

                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            Mo_TongQuan = True
                            Check_TongQuan = False
                            Start = time.time()

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

            return


    def Gui_Da_Quy(self,Email):
        print(" Gửi Đá Quý")
        CK_CongXuong = True
        CK_NganHang = False
        Gui3Ngay = True
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
                
                # Check Ngân Hàng
                    if CK_NganHang:
                        if self.Check( image_GuiDaQuy.XacNhanRut,Click=True):
                            self.Update_Database_Running(email=Email, chucnang="GuiDaQuy", giatri=1)
                            return

                        elif self.Check(image_GuiDaQuy.CK_NganHang):
                            if self.Check(image_GuiDaQuy.RutKhongLoiTuc,Click=True):
                                Start = time.time()

                                continue

                            elif self.Check(image_GuiDaQuy.TrongCung1ThoiGian):
                                self.Update_Database_Running(email=Email, chucnang="GuiDaQuy", giatri=1)
                                return

                            elif Gui3Ngay:
                                if self.Check(image_GuiDaQuy.Gui3Ngay,Click=True):
                                    Start = time.time()
                                    Gui3Ngay = False
                                    continue
                                else:
                                    Gui3Ngay = False


                            elif Gui3Ngay == False:
                                if self.Check(image_GuiDaQuy.Gui_DaQuy2,Click=True):
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start,3):
                                        self.Update_Database_Running(email=Email, chucnang="GuiDaQuy", giatri=1)
                                        return



                            elif self.Check(image_GuiDaQuy.Rut_Da_Quy,Click=True):
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Time_Check(Start):
                                return

                # Check Công Xưởng
                    elif CK_CongXuong:
                        if self.Check(image_TongQuan.CK_CongXuong):
                            if self.Check(image_GuiDaQuy.GuiDaQuy,Click=True):
                                CK_NganHang = True
                                CK_CongXuong = False
                                continue
                            else:
                                if self.Time_Check(Start):
                                    return
                        else:
                            if self.Time_Check(Start):
                                return
      
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()


            return


    def HienTang_LienMinh(self,Email):
        """Hiến Tặng Liên Minh"""

        print("Hiến Tặng Liên Minh")
        SwipeBenCang = self.Docfiletext("TongQuan/Swipebencang")

        Mo_TongQuan = True
        Check_TongQuan = False
        Vao_HienTang = True

        Click_HienTang = False
        Click_DeNghi = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                # Check Bên Ngoài
                    if self.Check(image_DangNhap.ThanhBenNgoai, Click=True):
                        continue

                # Check Tổng Quan
                    if Check_TongQuan:
                        if self.Check(image_TongQuan.CK_TongQuan):
                            if self.Check(image_TongQuan.PhaiLamHangNgay, Click=True, sleep=0.3) or self.Check(
                                    image_TongQuan.PhaiLamHangNgay2, Click=True, sleep=0.3):

                                controller().Swipe(SwipeBenCang)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)
                                Start = time.time()
                                for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                                    if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                                    if self.Running:


                                        if self.screenshot is None: continue
                                    # Click Đề Nghị
                                        if Click_DeNghi:
                                            if self.Check(image_UocFree.DungDaQuy):
                                                self.out_MHchinh()
                                                self.Update_Database_Running(email=Email, chucnang="CongHienLienMinh",giatri=1)
                                                return

                                            if self.Check(image_HienTangLienMinh.CongHienXong ):
                                                self.Update_Database_Running(email=Email, chucnang="CongHienLienMinh",giatri=1)
                                                controller().Click(29, 60)
                                                controller().Click(29, 60)
                                                controller().Click(29, 60)

                                                return

                                            elif self.Check(image_HienTangLienMinh.CK_Close_Tang):

                                                if self.Check(image_HienTangLienMinh.CongHien_Go3,Click=True) or self.Check(image_HienTangLienMinh.CongHien_Lua3,Click=True):
                                                    Start = time.time()
                                                    continue

                                                if self.Check(image_HienTangLienMinh.CongHien_Go2,Click=True) or self.Check(image_HienTangLienMinh.CongHien_Lua2,Click=True):
                                                    Start = time.time()
                                                    continue

                                                if self.Check(image_HienTangLienMinh.CongHien_Go1,Click=True) or self.Check(image_HienTangLienMinh.CongHien_Lua1,Click=True):
                                                    Start = time.time()
                                                    continue

                                                else:
                                                    if self.Time_Check(Start,2):
                                                        controller().Click(29, 60)
                                                        return

                                            else:
                                                if self.Time_Check(Start,2):
                                                    
                                                    # Cống Hiến Full
                                                    self.Update_Database_Running(email=Email, chucnang="CongHienLienMinh",giatri=1)
                                                    controller().Click(29, 60)
                                                    return

                                    # Check Hiến Tặng
                                        elif Click_HienTang:
                                            if self.Check(image_HienTangLienMinh.CK_KyThuatLienMinh):
                                                if  self.Check(image_HienTangLienMinh.DeNghi,khoang_y =300,Click=True) or self.Check(image_HienTangLienMinh.Cap,khoang_y =300,khoang_x=20,Click=True) :
                                                    Click_HienTang = False
                                                    Click_DeNghi = True
                                                    Start = time.time()
                                                    continue

                                                else:
                                                    return
 
                                            else:
                                                if self.Time_Check(Start):
                                                    return
                                                

                                    # Vào Click Hiến Tặng
                                        elif Vao_HienTang:
                                            if self.Check(image_HienTangLienMinh.HienTangLienMinh,Click=True,khoang_y =300, them_x=220):
                                                Click_HienTang = True
                                                Vao_HienTang = False
                                                Start = time.time()
                                            
                                            else:
                                                if self.Time_Check(Start):
                                                    return

                                        else:
                                            if self.Time_Check(Start):
                                                return

                                    else:
                                        while not self.Running: 
                                            if Exit_Event.wait(timeout= Setting_Bot.Delay):
                                                return 
                                        Start = time.time()

                                return


                            else:
                                if self.Time_Check(Start):
                                    return
                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Mo_TongQuan = True
                                Check_TongQuan = False
                                Start = time.time()
                
                # Mở Tổng Quan
                    if Mo_TongQuan:
                        if self.Check(image_TongQuan.Mo_TongQuan,Click=True):
                            Mo_TongQuan = False
                            Check_TongQuan = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Start = time.time()
  
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return


    def Su_DungBuaFarm(self):
        """"Sử Dụng Bùa Farm"""
        print("Sư Dụng Bùa Farm")

        CK_ThuongThanhPho = False
        CK_BuaChuNguonLuc = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
                    
                    if CK_BuaChuNguonLuc:
                        if self.Check(image_ThuongThanhPho.CK_BuaChuNguonLuc):
                            if self.Check(image_ThuongThanhPho.CheckBua):
                                if self.Check(image_ThuongThanhPho.SuDung_BuaNguonLuc, Click=True):
                                    return

                                else:
                                    return
                            else:
                                return

                        else:
                            if self.Time_Check(Start):
                                return



                    if CK_ThuongThanhPho:
                        if self.Check(image_ThuongThanhPho.CK_ThuongThanhPho):

                            if self.Check(image_ThuongThanhPho.BuaChuNguonLuc, Click=True, threshold=0.9,khoang_y = 300):
                                CK_ThuongThanhPho = False
                                CK_BuaChuNguonLuc = True
                                Start = time.time()
                                continue

                            elif self.Check(image_ThuongThanhPho.TongHop, Click=True):
                                Start = time.time()
                                continue


                            else:
                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Time_Check(Start):
                                return



                    if self.Check(image_SkillLanhChua.MoSach, Click=True, them_y=-50 ):
                        CK_ThuongThanhPho = True
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            Start = time.time()




                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

            return


    def Tai_Thiet(self,Email):
        """"Tái Thiết"""
        print("Tái Thiết")
        solan = 0
        Click_Avatar = True
        Start_TaiThiet = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:

                    if self.screenshot is None: continue

                    if  Start_TaiThiet:
                        if self.Check(image_TaiThiet.HetDa_TaiThiet):
                            self.Update_Database_Running(email=Email, chucnang="Taithiet", giatri=1)
                            self.out_MHchinh()
                            return

                        if solan >=5:
                            self.Update_Database_Running(email=Email, chucnang="Taithiet", giatri=1)

                            return

                        if self.Check(image_TaiThiet.CaiDatMienPhi,Click=True,sleep=0.2):
                            Start = time.time()
                            continue

                        if self.Check(image_TaiThiet.CK_TaiThiet):
                            if self.Check(image_TaiThiet.Cai_DatLai,Click=True,sleep = 0.7):
                                Start = time.time()
                                solan +=1

                        elif self.Check(image_TaiThiet.CK_TrangBi):
                            if self.Check(image_TaiThiet.TaiThiet,Click=True,khoang_y = 200):
                                Start = time.time()
                                continue
                        
                        elif self.Check(image_TaiThiet.ThamLoRen,Click=True, sleep = 0.2):
                            Start = time.time()
                            continue

                        elif self.Check(image_TaiThiet.TrangBi1,Click=True,them_x= -200):
                            Start = time.time()
                            continue

                        elif self.Check(image_TaiThiet.CK_TrangSuc):
                            controller().Click(21,51)
                            Start = time.time()
                            continue


                        else:
                            if self.Time_Check(Start):
                                Start_TaiThiet = False
                                Click_Avatar = True
                                self.out_MHchinh()
                                Start = time.time()
                    


                    elif Click_Avatar:
                        if self.Check(image_DangNhap.ThanhBenTrong, Click=True,them_y = -600):
                            Click_Avatar = False
                            Start_TaiThiet = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Click_Avatar = True

                                

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return


    def BuaSanLuong_TrongThanh(self):
        """Sử Dụng Bùa Tăng Sản Lượng"""
        print("Sử Dụng Bùa Sản Lượng")

        BuaBac = True
        BuaKimLoai = False
        BuaGo = False
        BuaLua = False

        Click_BuaBac = 0
        Click_BuaKimLoai = 0
        Click_BuaLua = 0
        Click_BuaGo = 0

        CK_SuDung= False
        Click_Tui = True
        Click_Tui_Khac = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if Click_Tui_Khac:

                        if BuaBac:
                            if CK_SuDung:

                                if self.Check(image_Tui.Dung_Xong_Bua,khoang_y = 2,sleep=2):
                                    CK_SuDung = False
                                    BuaBac = False
                                    BuaKimLoai = True
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Check(image_Tui.OK_SuDung,Click=True,sleep = 0.05):
                                        CK_SuDung = False
                                        Start = time.time()
                                        continue

                                    if self.Time_Check(Start,2):
                                        CK_SuDung = False
                                        BuaBac = False
                                        BuaKimLoai = True
                                        Start = time.time()
                                        continue


                            # Check Bùa Bạc Tồn Tại Hay Không
                            elif self.Check(image_Tui.Bua_Bac,khoang_x = 300, khoang_y = 150,Click=True, threshold =0.925):
                                Click_BuaBac +=1
                                if self.Check(image_Tui.SuDung_Bua,khoang_y=300,Click=True,sleep = 0.05):
                                    Click_BuaBac = 0
                                    CK_SuDung = True
                                    Start = time.time()
                                    continue


                                else :
                                    if Click_BuaBac >= 5:
                                        print("Buabac = False")
                                        BuaBac = False
                                        BuaKimLoai = True
                                        Click_Tui_Khac = False
                                        Click_Tui= True
                                        self.out_MHchinh()
                                        Start = time.time()
                                        continue

                                    if self.Time_Check(Start,2):
                                        BuaBac = False
                                        BuaKimLoai = True
                                        Start = time.time()
                                        continue

                            else:
                                if self.Time_Check(Start,2):
                                    BuaBac = False
                                    BuaKimLoai = True
                                    Start = time.time()
                                    continue

                        if BuaKimLoai:

                            if CK_SuDung:
                                if self.Check(image_Tui.Dung_Xong_Bua,khoang_y = 2,sleep =2):
                                    CK_SuDung = False
                                    BuaLua = True
                                    BuaKimLoai = False
                                    Start = time.time()

                                else:
                                    if self.Check(image_Tui.OK_SuDung,Click=True,sleep = 0.05):
                                        CK_SuDung = False
                                        Start = time.time()
                                        continue

                                    if self.Time_Check(Start,2):
                                        CK_SuDung = False
                                        BuaLua = True
                                        BuaKimLoai = False
                                        Start = time.time()


                            # Check Bùa KimLoai tồn Tại Hay Không
                            elif self.Check(image_Tui.Bua_KimLoai,khoang_x = 300, khoang_y = 150,Click=True, threshold =0.925):
                                Click_BuaKimLoai +=1
                                if self.Check(image_Tui.SuDung_Bua,khoang_y=300,Click=True):
                                    Click_BuaKimLoai = 0
                                    CK_SuDung = True
                                    Start = time.time()
                                    continue

                                else :

                                    if Click_BuaKimLoai >= 5:
                                        BuaKimLoai = False
                                        BuaLua = True
                                        Click_Tui_Khac = False
                                        Click_Tui= True
                                        self.out_MHchinh()
                                        Start = time.time()
                                        continue


                                    if self.Time_Check(Start,2):
                                        BuaKimLoai = False
                                        BuaLua = True
                                        Start = time.time()
                                        continue

                            else:
                                if self.Time_Check(Start,2):
                                    BuaKimLoai = False
                                    BuaLua = True
                                    Start = time.time()
                                    continue

                        if BuaLua:

                            if CK_SuDung:
                                if self.Check(image_Tui.Dung_Xong_Bua,khoang_y = 2,sleep=2):
                                    CK_SuDung = False
                                    BuaGo = True
                                    BuaLua = False
                                    Start = time.time()
                                    continue



                                else:
                                    if self.Check(image_Tui.OK_SuDung,Click=True,sleep = 0.05):
                                        CK_SuDung = False
                                        Start = time.time()
                                        continue

                                    if self.Time_Check(Start,2):
                                        CK_SuDung = False
                                        BuaGo = True
                                        BuaLua = False
                                        Start = time.time()


                            # Check Bùa KimLoai tồn Tại Hay Không
                            elif self.Check(image_Tui.Bua_Lua,khoang_x = 300, khoang_y = 150,Click=True, threshold =0.925):
                                Click_BuaLua +=1
                                if self.Check(image_Tui.SuDung_Bua,khoang_y=300,Click=True):
                                    Click_BuaLua = 0
                                    CK_SuDung = True
                                    Start = time.time()
                                    continue

                                else :

                                    if Click_BuaLua >= 5:
                                        BuaLua = False
                                        BuaGo = True
                                        Click_Tui_Khac = False
                                        Click_Tui= True
                                        self.out_MHchinh()
                                        Start = time.time()
                                        continue



                                    if self.Time_Check(Start,2):
                                        BuaLua = False
                                        BuaGo = True
                                        Start = time.time()
                                        continue

                            else:
                                if self.Time_Check(Start,2):
                                    BuaLua = False
                                    BuaGo = True
                                    continue

                        if BuaGo:
                            if CK_SuDung:
                                if self.Check(image_Tui.Dung_Xong_Bua,khoang_y = 2,):
                                    return


                                else:
                                    if self.Check(image_Tui.OK_SuDung,Click=True):
                                        CK_SuDung = False
                                        Start = time.time()
                                        continue

                                    if self.Time_Check(Start,2):
                                        return



                            # Check Bùa KimLoai tồn Tại Hay Không
                            elif self.Check(image_Tui.Bua_Go,khoang_x = 300, khoang_y = 150,Click=True, threshold =0.9):
                                Click_BuaGo +=1
                                if self.Check(image_Tui.SuDung_Bua,khoang_y=300,Click=True):
                                    Click_BuaGo = 0
                                    CK_SuDung = True
                                    Start = time.time()
                                    continue

                                else :

                                    if Click_BuaLua >= 5:
                                        return

                                    if self.Time_Check(Start,2):
                                        return
  

                            else:
                                if self.Time_Check(Start,2):
                                    return


                # Check Ngoài Thành
                    elif self.Check(image_DangNhap.ThanhBenNgoai, Click=True):
                        continue

                # Vào Túi Khác
                    elif Click_Tui:
                        if self.Check(image_Tui.Tui_Khac,Click=True):
                            Click_Tui = False
                            Click_Tui_Khac = True
                            Start = time.time()
                            continue

                        elif self.Check(image_Tui.Tui,Click=True):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                self.out_MHchinh()
                                Click_Tui = True
                    

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return


    def AnRss_TrongThanh(self):
        """Ăn Tài Nguyên Trong Thành"""
        print("Ăn Tài Nguyên Trong Thành")

        da_swipe = False
        da_click = 0
        swipe = 0



        SWipeNL = self.Docfiletext("RssTrongThanh/SWipeNL")
        SwipeGocGame = self.Docfiletext("RssTrongThanh/SwipeGocGame")
        CK_NhaMay_NL = False
        Ra_GocGame = True
        An_4_Mo = False

        if self.out_MHchinh(NgayMayMan_XayDung= False):
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue



                # An 4 Mo
                    if An_4_Mo :

                        if self.Check(image_RssTrongThanh.XayDung, Click=True, ):
                            continue

                        if self.Check(image_RssTrongThanh.XayDung2, Click=True,):
                            An_4_Mo = False
                            Ra_GocGame = True
                            continue

                        # Check Mỏ 4
                        if self.Check(image_RssTrongThanh.Mo_4, khoang_x =5,khoang_y = 5, Click_Khac=True, khac_x=164, khac_y=383,sleep=0.1):
                            da_click = da_click + 1
                            if da_click >= 2:
                                return

                            Start = time.time()
                            continue


                        elif self.Check(image_RssTrongThanh.Mo_3, khoang_x =5,khoang_y = 5, Click_Khac=True, khac_x=72, khac_y=422,sleep=0.1):
                            Start = time.time()
                            continue

                        elif self.Check(image_RssTrongThanh.Mo_2, khoang_x =5,khoang_y = 5, Click_Khac=True, khac_x=21, khac_y=470,sleep=0.1):
                            Start = time.time()
                            continue

                        elif self.Check(image_RssTrongThanh.Mo_1, khoang_x =5,khoang_y = 5, Click_Khac=True, khac_x=16, khac_y=494, sleep = 0.1):
                            Start = time.time()
                            continue

                        elif self.Check(image_RssTrongThanh.Mo_0,  khoang_x =5,khoang_y = 5,Click_Khac=True, khac_x=46, khac_y=340,sleep = 0.1):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start):
                                Ra_GocGame = True
                                An_4_Mo = False
                                Start = time.time()




                # Check Nha May Nhien Lieu
                    elif CK_NhaMay_NL :
                        if self.Check(image_RssTrongThanh.CK_NhaMay_NL):
                            if da_swipe == False:
                                controller().Swipe(SWipeNL)
                                
                                da_swipe = True
                            self.out_MHchinh()
                            An_4_Mo = True
                            Start = time.time()
                            continue

                        elif self.Check(image_RssTrongThanh.NhaMay_Nl,Click=True,threshold =0.8,khoang_x = 20,khoang_y = 5):
                            Start = time.time()
                            continue

                        elif self.Check(image_RssTrongThanh.NhaMay_Nl2,Click=True,threshold =0.8,khoang_x = 20,khoang_y = 5):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,):
                                Ra_GocGame = True
                                CK_NhaMay_NL = False
                                Start = time.time()

                        

                # Ra Góc Góc Game
                    if Ra_GocGame:
                        if self.Check(image_RssTrongThanh.Goc_Game,Click=True):
                            Ra_GocGame = False
                            CK_NhaMay_NL = True
                            Start = time.time()

                        else:
                            if self.out_MHchinh(NgayMayMan_XayDung= False):
                                controller().Swipe(SwipeGocGame)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)
                                swipe +=1
                                if swipe >= 4:
                                    return
                                Start = time.time()

                            if self.Time_Check(Start):
                                return

                    else:
                        if self.Time_Check(Start):
                            return





                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            
            return


    def Di_AnMo(self,Email, loaimothu, capmo,set_sodao):
        print("Đi Thu Thập")
        Titan = False

        DaDi_6Mo_CK_xuatBinh = False
        KickHoatVip_XuatBinh = False

        def ChinhCapMo(self, capmo):
            """Chỉnh Cấp Mỏ"""
            print("Chỉnh Cấp Mỏ")
            cap_hientai = 0
            Ck_Di = False
            

            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if self.Check(image_DiAnMo.Find_Di):

                        if cap_hientai == capmo or Ck_Di == True:
                            if self.Check(image_DiAnMo.Find_Di, Click=True,sleep =1.5):
                                return True
                            else:
                                if self.Time_Check(Start,2):
                                    return


                        elif cap_hientai > 0:

                            if cap_hientai < capmo:
                                for l in range(int(cap_hientai), int(capmo)):
                                    if Exit_Event.is_set():
                                        return
                                    if self.Running :
                                        controller().Click(294,633)
                                Ck_Di = True
                                Start = time.time()
                                continue





                            elif cap_hientai > capmo:
                                for l in range(int(capmo), int(cap_hientai)):
                                    if Exit_Event.is_set():
                                        return
                                    if self.Running:
                                        controller().Click(73,633)
                                        Start = time.time()

                                Ck_Di = True
                                Start = time.time()
                                continue


                            else:
                                if self.Time_Check(Start,3):
                                    return False




                        elif cap_hientai == 0:

                            if self.Check(image_DiAnMo.Find_Cap6):
                                cap_hientai = 6
                                continue

                                
                            elif self.Check(image_DiAnMo.Find_Cap1):
                                cap_hientai = 1
                                continue

                            elif self.Check(image_DiAnMo.Find_Cap2):
                                cap_hientai = 2
                                continue

                            elif self.Check(image_DiAnMo.Find_Cap3):
                                cap_hientai = 3
                                continue

                            elif self.Check(image_DiAnMo.Find_Cap4):
                                cap_hientai = 4
                                continue
                            elif self.Check(image_DiAnMo.Find_Cap5):
                                cap_hientai = 5
                                continue


                            elif self.Check(image_DiAnMo.Find_Cap7):
                                cap_hientai = 7   
                                continue                         


                    else:
                        return False


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

            return False

        def Check_Mo(self):
            """Check Mỏ"""
            print("Check Mỏ")
            ClickTrungtam = False
            da_ClickTrungTam = 0
            nonlocal MucTieuTren200m
            nonlocal KickHoatVip_XuatBinh
            Start = time.time()

            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if self.Check(image_DiAnMo.MucTieuTren200m):
                        MucTieuTren200m = True
                        return False

                    if self.Check(image_KickHoat_Vip.KickHoatVip):
                            with open("DataText/log.txt","a+",encoding="utf-8") as f:
                                f.write(str(Email) +str(" -- Hết Đá Quý Hoặc Vip ")+'\n')
                            if self.Kick_Hoat_Vip():
                                self.out_MHchinh()
                                return

                            else:
                                KickHoatVip_XuatBinh = True
                                return

                    if da_ClickTrungTam >= 3:
                        return False



                    if ClickTrungtam == True:
                        controller().Click(197, 366)
                        Exit_Event.wait(timeout=0.6)
                        ClickTrungtam = False
                        da_ClickTrungTam = da_ClickTrungTam + 1
                        if self.Check_Mutil_zoom(image_DiAnMo.CK_Mo_CoRSS):
                            if self.Check(image_DiAnMo.chiem_Goc, Click=True):
                                return True
                            elif self.Check_Mutil_zoom(image_DiAnMo.chiem_x1, Click=True):
                                return True

                            else:
                                continue


                    if self.Check(image_DiAnMo.Find_Di):
                        Start = time.time()
                        ClickTrungtam = True

                    if ClickTrungtam == False:
                        self.Check(image_DiAnMo.Find_Rss, Click=True)
                        ClickTrungtam = True
                        Start = time.time()

                    else:
                        if self.Time_Check(Start):
                            return False

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()


            return False

        def XuatBinh(self):
            """Xuất Binh"""
            print("Xuất Binh")
            nonlocal DaDi_6Mo_CK_xuatBinh
            nonlocal KickHoatVip_XuatBinh
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    if self.Check(image_XuatBinh.CK_XuatBinh):
                        if self.Check(image_XuatBinh.XuatBinh, Click=True, khoang_x=5):
                            return True

                        else:
                            if self.Time_Check(Start,):
                                return False

                    else:                        
                        if self.Check(image_XuatBinh.XuatQua6Doi):
                            self.out_MHchinh()
                            DaDi_6Mo_CK_xuatBinh = True
                            return

                        if self.Time_Check(Start):
                            return False
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

            return False

        def ChonLoaimo(self,loaimothu):
            nonlocal Titan

            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:
                    if self.screenshot is None: continue
                    if self.Check(image_DiAnMo.Find_Di):

                        if int(loaimothu) == 1:
                            # Titan
                            if self.Check(image_DanhQuai.ChonQuai_Titan):
                                Titan = True
                                return False

                            if self.Check(image_DiAnMo.Find_Lua,khoang_x = 20, Click=True):
                                return True

                            else:
                                if self.Time_Check(Start,2):
                                    return False
                            
                        if int(loaimothu) == 2:
                            # Titan
                            if self.Check(image_DanhQuai.ChonQuai_Titan):
                                Titan = True
                                return False

                            if self.Check(image_DiAnMo.Find_Go,khoang_x = 20, Click=True):
                                return True
                            else:
                                if self.Time_Check(Start,2):
                                    return False

                        if int(loaimothu) == 3:
                            # Titan
                            if self.Check(image_DanhQuai.ChonQuai_Titan):
                                Titan = True
                                return False
                            if self.Check(image_DiAnMo.Find_KimLoai,khoang_x = 20, Click=True):
                                return True
                            else:
                                if self.Time_Check(Start,2):
                                    return False

                        if int(loaimothu) == 4:
                            # Titan
                            if self.Check(image_DanhQuai.ChonQuai_Titan):
                                Titan = True
                                return False

                            if self.Check(image_DiAnMo.Find_Bac,khoang_x = 20, Click=True):
                                return True

                            else:
                                if self.Time_Check(Start,2):
                                    return False
                    else:
                        return False
                        


        # Start
        MucTieuTren200m = False
        sodao_hientai = 0
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
                    # Set Số Đạo = 1
                    if Titan:
                        return
                    sodao_hientai = 1
                    if DaDi_6Mo_CK_xuatBinh:
                        self.Su_DungBuaFarm()
                        return

                    if KickHoatVip_XuatBinh:
                        return

                    # Check hết Lính
                    if self.Check(image_XuatBinh.HetLinh):
                        with open("DataText/log.txt","a+",encoding="utf-8") as f:
                            f.write(str(Email) +str(" -- Hết Lính ")+'\n')
                        self.out_MHchinh()
                        return



                    # if self.Check(image_XuatBinh.TroThanhVip10):
                    #     self.out_MHchinh()
                    #     self.Su_DungBuaFarm()


                        
                    # Mục Tiêu Trên 200m
                    if MucTieuTren200m == True:
                        self.out_MHchinh()
                        return

                    if self.Check(image_XuatBinh.GiaoTranh_Mo):
                        self.out_MHchinh()
                        Start = time.time()

                    if self.Check(image_DangNhap.ThanhBenTrong, Click=True,sleep = 0.2):
                        Start = time.time()
                        continue

                    if self.Check(image_DiAnMo.ChuyenThanh,sleep = 0.3):
                        Start = time.time()
                        continue

                    if self.Check(image_XuatBinh.ShowQuanDoi, Click=True):
                        Start = time.time()
                        continue

                    if self.Check(image_XuatBinh.Dao_3):
                        Start = time.time()
                        sodao_hientai = 3

                    if self.Check(image_XuatBinh.Dao_4):
                        Start = time.time()
                        sodao_hientai = 4

                    if self.Check(image_XuatBinh.Dao_5):
                        Start = time.time()
                        sodao_hientai = 5

                    if self.Check(image_XuatBinh.Dao_6):
                        Start = time.time()
                        sodao_hientai = 6



                    print("     ",sodao_hientai," set dao",set_sodao,"          SoDap Da Di :", sodao_hientai)
                    if sodao_hientai >= int(set_sodao):
                        self.Su_DungBuaFarm()
                        return

                    elif sodao_hientai >= 0:
                        if self.Check(image_DiAnMo.Find_Rss, Click=True,) or self.Check(image_DiAnMo.Find_Di):
                            if ChonLoaimo(self,loaimothu):
                                if ChinhCapMo(self, capmo):
                                    if Check_Mo(self):
                                        XuatBinh(self)
                                        Start = time.time()

                                    else:
                                        if self.Time_Check(Start,3):
                                            self.out_MHchinh()
                                            Start = time.time()
                                else:
                                    if self.Time_Check(Start,3):
                                        self.out_MHchinh()
                                        Start = time.time()

                            else:
                                if self.Time_Check(Start,3):
                                    self.out_MHchinh()
                                    Start = time.time()

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh()
                                Start = time.time()
                    else:

                        if self.Time_Check(Start,2):
                            self.out_MHchinh()
                            Start = time.time()

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return



    def SuaThanhDapLua(self):
        print("Sửa Thành Dập Lửa")
        Da_VaoDapLua = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if Da_VaoDapLua:
                        if self.Check(image_DapLua_suaThanh.ThemSu_PhongThu,Click=True):
                            Start = time.time()
                            continue
                        if self.Check(image_DapLua_suaThanh.DapLua,khoang_y = 100,threshold=0.8,Click=True):
                            Start = time.time()
                            return

                        #if self.Check(image_DapLua_suaThanh.DapLuaVaMua_50Da,Click=True):
                        else:
                            if self.Time_Check(Start,2):
                                return
                            


                    if self.Check(image_DapLua_suaThanh.VaoDapLua,Click=True,khoang_y = 100):
                        Da_VaoDapLua = True
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start,2):
                            return


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()


    def NhiemVu_XayDung(self,Email):
        print("Nhiem Vu Xay Dung")
        self.saikhac = 0
        saikhac2 = 0

        SwipeGocGame = self.Docfiletext("RssTrongThanh/SwipeGocGame")
        MoDa_TonTai = True
        Da_NangCap = False
        PhaHuy_MoTonTai = False
        XayDung = False
        Den_Mo6 = False
        Ra_GocGame = True

        if self.out_MHchinh(NgayMayMan_XayDung = False):
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if PhaHuy_MoTonTai:
                        if self.Check(image_XayDung.PhaHuy_GiamSucManh,Click_Khac=True,khac_x=190 ,khac_y= 426):
                            PhaHuy_MoTonTai = False 
                            Ra_GocGame = True
                            if Da_NangCap:
                                self.Update_Database_Running(email=Email, chucnang="XayDung", giatri=1)
                                return
                            Start = time.time()
                            continue

                        elif self.Check(image_XayDung.PhaHuy,Click=True):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,2):
                                PhaHuy_MoTonTai = False 
                                Ra_GocGame = True
                                Start = time.time()
                                continue


                    if XayDung:
                        # Mỏ Đã Tồn Tại
                        if MoDa_TonTai:
                            if self.Check(image_XayDung.ChiTiet,khoang_x =60,khoang_y =60   ,Click=True,sleep=0.3,threshold =0.925):
                                MoDa_TonTai = False
                                PhaHuy_MoTonTai = True
                                XayDung = False
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return

                        # # Chưa Có Mỏ
                        if self.Check(image_XayDung.NangCap_Mo,Click=True,sleep=0.3):
                            MoDa_TonTai = False
                            Start = time.time()
                            continue

                        if self.Check(image_XayDung.XayDung,Click=True):
                            MoDa_TonTai = False
                            Start = time.time()
                            continue

                            
                        if self.Check(image_XayDung.Xay_Dung_2,Click=True):
                            XayDung = False
                            
                            MoDa_TonTai = False
                            Ra_GocGame = True
                            Start = time.time()

                        if self.Check(image_XayDung.NangCap,Click=True):
                            Da_NangCap = True
                            MoDa_TonTai = True
                            XayDung = False
                            Ra_GocGame = True
                            Start = time.time()

                        else:
                            if self.Time_Check(Start,3):
                                XayDung = False
                                Ra_GocGame = True
                                Start = time.time()



                    if Den_Mo6:
                        if self.Check(image_XayDung.CK_Click_Mo_6,Click_Khac=True,khac_x=188 ,khac_y=121,sleep= 0.4):
                            Den_Mo6 =False
                            XayDung = True
                            Start = time.time()
                            continue
  
                        if self.Check(image_RssTrongThanh.Mo_0, Click_Khac=True,khac_x=46, khac_y=340):
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                Den_Mo6 = False
                                Ra_GocGame = True
                                return


                    if Ra_GocGame:
                        
                        if self.Check(image_RssTrongThanh.Goc_Game, Click=True):
                            Ra_GocGame = False
                            Den_Mo6 = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,2):
                                if self.out_MHchinh(NgayMayMan_XayDung = False):
                                    controller().Swipe(SwipeGocGame)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe)
                                    saikhac2 = saikhac2 + 1
                                    if saikhac2 >= 5:
                                        self.out_MHchinh(NgayMayMan_XayDung = False)
                                        saikhac2 = 0
                                        return
                                








                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return
    
    
    def MoDa_Quy(self,loai_tainguyen):
        """Mỏ Tài Nguyên Trong Túi"""
        Swipe_Tang_SoLuong =self.Docfiletext("Tui/Swipe_Tang_SoLuong")
        if loai_tainguyen == "Gems":
            mo_tainguyen = 1

        if loai_tainguyen == "Rice":
            mo_tainguyen = 3

        if loai_tainguyen == "Wood":
            mo_tainguyen = 2

        if loai_tainguyen == "Metal":
            mo_tainguyen = 4

        if loai_tainguyen == "Silver":
            mo_tainguyen = 5

        Click_DaQuy = 0
        da_swipe = False
        Click_Tui = True
        CK_Tui = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    if self.screenshot is None: continue
                    
                    if Click_DaQuy >= 4:
                        self.out_MHchinh()
                        return

                    if da_swipe == False:
                        if self.Check(image_Tui.Tang_SoLuong):
                            controller().Swipe(Swipe_Tang_SoLuong)
                            da_swipe = True
                            Start = time.time()
                            continue

                    if da_swipe == True:
                        if self.Check(image_Tui.SuDung_DaQuy_2,Click=True,sleep = 0.2):
                            Start = time.time()
                            da_swipe = False
                            
                    if self.Check(image_Tui.XacNhan_SuDung,Click_Khac=True,khac_x = 191 , khac_y = 423):
                        Start = time.time()
                        continue




                    if CK_Tui:
                        if self.Check(image_Tui.CK_CacMonDo,sleep = 0.1):
                            if mo_tainguyen == 1:
                                print("Timdaquy")
                                if self.Check(image_Tui.DaQuy_10,Click=True,khoang_y=100) or  self.Check(image_Tui.Da_Quy_1k,Click=True,khoang_x= 100):
                                    print("ThayDaQuy")
                                    if self.Check(image_Tui.SuDung_DaQuy_1,Click = True,khoang_y = 300):
                                        Click_DaQuy = 0
                                        Start = time.time()
                                        continue
                                    else:
                                        if self.Time_Check(Start,3):
                                            return
                                else:
                                    if self.Time_Check(Start,3):
                                        return
        
                            elif mo_tainguyen == 2:
                                if self.Check(image_Tui.Go_1000,Click=True,khoang_x = 300,khoang_y = 300,threshold =0.9):# or  self.Check(image_Tui.Da_Quy_1k,Click=True):
                                    if self.Check(image_Tui.SuDung_DaQuy_1,Click = True,khoang_y = 300):
                                        Click_DaQuy = 0
                                        Start = time.time()
                                        continue

                                    else:
                                        if self.Time_Check(Start,3):
                                            return
                                else:
                                    if self.Time_Check(Start,3):
                                        return

                            elif mo_tainguyen == 3:
                                if self.Check(image_Tui.Lua_1000,Click=True,khoang_x = 300,khoang_y = 300,threshold =0.9):# or  self.Check(image_Tui.Da_Quy_1k,Click=True):
                                    if self.Check(image_Tui.SuDung_DaQuy_1,Click = True,khoang_y = 300):
                                        Click_DaQuy = 0
                                        Start = time.time()
                                        continue

                                    else:
                                        if self.Time_Check(Start,3):
                                            return
                                else:
                                    if self.Time_Check(Start,3):
                                        return

                            elif mo_tainguyen == 4:
                                if self.Check(image_Tui.KimLoai_1000,Click=True,khoang_x = 300,khoang_y = 300,threshold =0.9):# or  self.Check(image_Tui.Da_Quy_1k,Click=True):
                                    if self.Check(image_Tui.SuDung_DaQuy_1,Click = True,khoang_y = 300):
                                        Click_DaQuy = 0
                                        Start = time.time()
                                        continue
                                    else:
                                        if self.Time_Check(Start,3):
                                            return
                                else:
                                    if self.Time_Check(Start,3):
                                        return
                            elif mo_tainguyen == 5:
                                if self.Check(image_Tui.Bac_1000,Click=True,khoang_x = 300,khoang_y = 300,threshold =0.9) :#or  self.Check(image_Tui.Da_Quy_1k,Click=True):
                                    if self.Check(image_Tui.SuDung_DaQuy_1,Click = True,khoang_y = 300):
                                        Click_DaQuy = 0 
                                        Start = time.time()
                                        continue
                                    else:
                                        if self.Time_Check(Start,3):
                                            return
                                else:
                                    if self.Time_Check(Start,3):
                                        return   

                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                CK_Tui = False
                                Click_Tui = True
                                Start = time.time()

                    if Click_Tui:
                        if self.Check(image_Tui.Tui,Click=True):
                            Click_Tui = False
                            CK_Tui = True
                            Start = time.time()
                            continue
                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                Start = time.time()

                    else:
                        if self.Time_Check(Start,2):
                            self.out_MHchinh()
                            Start = time.time()
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

        return   


    def Khien_Farm(self,Email,Ep_Khien = False,khien_50 = False,loaikhien = 1):
        """Khiên Farm"""
        print("Sử Dụng Khiên")

        Click_SuDung = False
        if self.out_MHchinh():
            Start = time.time()

            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    if self.screenshot is None: continue
                    if Click_SuDung == True:
                        if self.Check(image_ThuongThanhPho.CK_Cai_Khien):
                            return

                        else:
                            if self.Check(image_ThuongThanhPho.Cong_Don_Khien,Click_Khac= True,khac_x=194,khac_y= 420 ):
                                continue
                            if self.Check(image_ThuongThanhPho.Het_Da_Quy):

                                with open("DataText/log.txt","a+",encoding="utf-8") as f:
                                    f.write(str(Email) +str(" -- Hết Đá Quý Mua Khiên ")+'\n')
                                return
                            else:
                                if self.Time_Check(Start):
                                    return


                    elif self.Check(image_ThuongThanhPho.CK_Cai_Khien):
                        # Ép Khiên
                        if Ep_Khien == True:

                            if int(loaikhien) == 1:
                                if self.Check(image_ThuongThanhPho.SuDung8h,Click=True,):
                                    Click_SuDung = True
                                    Start = time.time()
                                    continue

                                elif self.Check(image_ThuongThanhPho.Mua_Da_Quy_8h,Click=True):
                                    Click_SuDung = True
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return

                            if int(loaikhien) == 2:
                                if self.Check(image_ThuongThanhPho.SuDung24h,Click=True,):
                                    Click_SuDung = True
                                    continue

                                elif self.Check(image_ThuongThanhPho.Mua_Da_Quy_24h,Click=True,):
                                    Click_SuDung = True
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return

                            if int(loaikhien) == 3:
                                if self.Check(image_ThuongThanhPho.SuDung3Day,Click=True):
                                    Click_SuDung = True
                                    Start = time.time()
                                    continue
                                elif self.Check(image_ThuongThanhPho.Mua_Da_Quy_3_Day,Click=True,):
                                    Click_SuDung = True
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start):
                                        return

                        #Sử Dụng khiên Ngẫu Nhiên
                        else:
                            if self.Check(image_ThuongThanhPho.SuDung3Day,Click=True,sleep = 0.2):
                                Click_SuDung = True
                                Start = time.time()
                                continue

                            elif self.Check(image_ThuongThanhPho.SuDung24h,Click=True,sleep = 0.2):
                                Click_SuDung = True
                                Start = time.time()
                                continue

                            elif self.Check(image_ThuongThanhPho.SuDung8h,Click = True,sleep = 0.2):
                                Click_SuDung = True
                                Start = time.time()
                                continue

                            else:
                                if self.Check(image_ThuongThanhPho.Mua_Da_Quy_8h,Click=True):
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return
                            

 

                    elif self.Check(image_ThuongThanhPho.CK_ThuongThanhPho,sleep=0.2):
                        if khien_50 == True:
                            # Còn Khiên
                            if self.Check(image_ThuongThanhPho.CK_ConKhien50):
                                return
                            
                            # Hết Khiên
                            else:
                                if self.Check(image_ThuongThanhPho.CaiKhien,khoang_y=50, Click=True):
                                    Start = time.time()
                                    continue

                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Check(image_ThuongThanhPho.CK_ConKhien25):
                                return
                            
                            # Hết Khiên
                            else:
                                if self.Check(image_ThuongThanhPho.CaiKhien,khoang_y = 50, Click=True):
                                    Start = time.time()

                                    continue

                                if self.Time_Check(Start):
                                    return


                    elif self.Check(image_SkillLanhChua.MoSach, Click=True, them_y=-50, sleep=0.3):
                        continue


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return


    def Uoc_Free(self, Email):
        print("Ước 20 Lần")

        saikhac2 = 0
        da_uoc = 0
        het_da = 0
        SwipeBenCang = self.Docfiletext("TongQuan/Swipebencang")
 
        Check_TongQuan = False
        CK_Uoc = False
        CK_DenNhaUoc = False

        Mo_TongQuan = True
        if self.out_MHchinh():
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):

                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
        
                # Check Đến Nhà ước
                    if CK_Uoc:
                        if saikhac2 == 3:
                            self.Update_Database_Running(email=Email, chucnang="Uoc", giatri=1)
                            return

                        if self.Check(image_TongQuan.DenNhaUoc, khoang_y=300, Click=True, them_x=200):
                            CK_DenNhaUoc = True
                            saikhac2 = saikhac2 + 1
                            Start = time.time()
                            continue


                    # Trong Nhà Ước
                        if CK_DenNhaUoc:

                            if het_da >= 3:
                                self.Update_Database_Running(email=Email, chucnang="Uoc", giatri=1)
                                return

                            if self.Check(image_UocFree.CK_TangBaoTri, ):
                                if da_uoc >= 20:
                                    self.Update_Database_Running(email=Email, chucnang="Uoc", giatri=1)
                                    return

                                elif self.Check(image_UocFree.UocThep, khoang_y=2, Click=True, sleep=0.05):
                                    da_uoc += 1
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start):
                                        return

                            if self.Check(image_UocFree.DungDaQuy, Click=True):
                                het_da += 1
                                Start = time.time()
                                continue
                                


                            elif self.Check(image_UocFree.VaoUoc, Click=True):
                                Start = time.time()
                                continue

                            elif self.Check(image_UocFree.CK_VaoNhaUoc,khoang_x=2,khoang_y=2, Click_Khac=True, khac_x =191 ,khac_y =385 ,sleep=0.1):
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start):
                                    return

                        else:
                            if self.Time_Check(Start):
                                return


                # Check Thành Bên Ngoài
                    if self.Check(image_DangNhap.ThanhBenNgoai, Click=True):
                        continue

                # Check Tổng Quan
                    if Check_TongQuan:
                        if self.Check(image_TongQuan.CK_TongQuan):
                            if self.Check(image_TongQuan.PhaiLamHangNgay, Click=True, sleep=0.3) or self.Check(image_TongQuan.PhaiLamHangNgay2, Click=True, sleep=0.3):
                                controller().Swipe(SwipeBenCang)
                                Exit_Event.wait(timeout= self.Sleep_Swipe)
                                CK_Uoc = True
                                Start = time.time()

                            else:
                                if self.Time_Check(Start):
                                    Mo_TongQuan = True
                                    Check_TongQuan = False
                                    Start = time.time()

                        else:
                            if self.Time_Check(Start,):
                                Mo_TongQuan = True
                                Check_TongQuan = False
                                Start = time.time()

                # Mở Tổng Quan
                    if Mo_TongQuan:
                        if self.Check(image_TongQuan.Mo_TongQuan,Click=True):
                            Mo_TongQuan = False
                            Check_TongQuan = True
                            Start = time.time()
                            continue
      
                        else:       
                                
                                
                            self.out_MHchinh()
                            Mo_TongQuan = True
                            Check_TongQuan = False
                            Start = time.time()


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return



    def Nhan_NhiemVu(self):
        """"Nhận Thưởng Nhiệm Vụ Hàng Ngày """
        print("Nhận Thưởng Nhiệm Vụ")

        dayeucau = 0
        NhanRuong =False
        Click_Nhiemvu = True
        CK_NhiemVu = False
        NhanXong = False

        Ruong1 = True
        Ruong2 = False
        Ruong3 = False
        Ruong4 = False
        Ruong5 = False
        Ruong6 = False

        Ruong7 = False
        Ruong8 = False
        Ruong9 = False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
                    

                    if NhanRuong:

                        if dayeucau >=1:
                            self.out_MHchinh()
                            dayeucau = 0
                            if NhanXong:
                                return

                        if self.Check(image_Nhan_NhiemVu.YeuCau,Click=True,sleep = 0.05) or self.Check(image_Nhan_NhiemVu.YeuCau2,Click=True,sleep = 0.05):
                            if NhanXong:
                                controller().Click(304, 139)
                                return
                            controller().Click(304, 139)
                            Start = time.time()

                            continue

                        if self.Check(image_Nhan_NhiemVu.YeuCau,Click=True) or self.Check(image_Nhan_NhiemVu.YeuCau2,Click=True):
                            dayeucau = dayeucau +1
                            Start = time.time()
                            continue

                        if self.Check(image_Nhan_NhiemVu.CK_NhiemVuHangNgay):

                            if Ruong1:
                                print("Ruong1")
                                dayeucau = 0
                                controller().Click(72 ,199)
                                Ruong1 = False
                                Ruong2 = True
                                Start = time.time()
                                continue

                            if Ruong2:
                                print("Ruong2")
                                dayeucau = 0
                                controller().Click(116, 202)
                                Ruong2 = False
                                Ruong3 = True
                                Start = time.time()
                                continue

                            if Ruong3:
                                print("Ruong3")
                                dayeucau = 0
                                controller().Click(164, 200)
                                Ruong3 = False
                                Ruong4 = True
                                Start = time.time()
                                continue

                            if Ruong4:
                                print("Ruong4")
                                dayeucau = 0
                                controller().Click(212, 201)
                                Ruong4 = False
                                Ruong5 = True
                                Start = time.time()
                                continue

                            if Ruong5:
                                print("Ruong5")
                                dayeucau = 0
                                controller().Click(266, 199)
                                Ruong5 = False
                                Ruong6 = True
                                Start = time.time()
                                continue

                            if Ruong6:
                                print("Ruong6")
                                dayeucau = 0
                                controller().Click(330 ,203)
                                Ruong6 = False
                                Ruong7 = True
                                Start = time.time()
                                continue

                            if Ruong7:
                                print("Ruong7")
                                dayeucau = 0
                                controller().Click(82, 286)
                                Ruong7 = False
                                Ruong8 = True
                                Start = time.time()
                                continue

                            if Ruong8:
                                print("Ruong8")
                                dayeucau = 0
                                controller().Click(192, 285)
                                Ruong8 = False
                                Ruong9 = True
                                Start = time.time()
                                continue

                            if Ruong9:
                                print("Ruong9")
                                dayeucau = 0
                                controller().Click(299, 286)
                                Ruong9 = False
                                NhanXong = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return

                        else:
                            if self.Time_Check(Start,3):
                                return

                    if CK_NhiemVu:
                        if self.Check(image_Nhan_NhiemVu.NhiemVuHangNgay1,Click=True):
                            NhanRuong = True
                            CK_NhiemVu = False
                            Start = time.time()
                            continue
                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh()
                                CK_NhiemVu = False
                                Click_Nhiemvu = True
                                continue


                    if Click_Nhiemvu:
                        if self.Check(image_Nhan_NhiemVu.NhiemVu,Click=True,):
                            CK_NhiemVu = True
                            Click_Nhiemvu = False
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh()
                                continue
                    else:
                        if self.Time_Check(Start,3):
                            self.out_MHchinh()
                            Click_Nhiemvu = True



                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()
            return



# MainAcc
    def NhanQua_ThanhDiaLienMinh_MainAcc(self):
        print("Nhận Quà Thánh Địa Liên Minh")

        VaoLienMinh = True
        CK_LienMinh = False
        NhanQua = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue
                    if NhanQua:
                        if self.Check(image_LienMinh.LinhToanBo,Click=True):
                            self.out_MHchinh()
                            return

                        else:
                            if self.Time_Check(Start,2):
                                return 

                    if CK_LienMinh:


                        if self.Check(image_LienMinh.CK_LienMinh):
                            if self.Check(image_LienMinh.ThanhDiaLienMinh,Click=True,khoang_y = 20):
                                NhanQua = True
                                Start = time.time()
                                continue

                        if self.Check(image_LienMinh.GiaNhapLienMinh):
                            return

                        else:
                            if self.Time_Check(Start,2):
                                CK_LienMinh = False
                                VaoLienMinh = True
                                Start = time.time()


                    if VaoLienMinh:
                        # Titan
                        if self.Check(image_LienMinh.LienQuan):
                            return

                        if self.Check(image_LienMinh.VaoLienMinh,Click=True):
                            VaoLienMinh = False
                            CK_LienMinh = True
                            Start = time.time()
                            continue

                        
                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                VaoLienMinh = True
                                Start = time.time()
                    

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def NhanQua_HoaDongLienMinh_MainAcc(self,Email):
        VaoLienMinh = True
        CK_LienMinh = False
        CK_HoatDongLienMinh = False
        NhanQua =False
        NhanDuocHoatDong = 0

        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:

                    if self.screenshot is None: continue

                    if NhanQua:
                        if NhanDuocHoatDong >=3:
                            self.Update_Database_Running(email = Email, chucnang= "HoatDongLienMinh", giatri=1)
                            return
                        if self.Check(image_LienMinh.NhanDuocHoatDong,Click_Khac= True, khac_x =55  ,khac_y= 222):
                            NhanDuocHoatDong +=1
                            Start = time.time()
                            continue
                        if self.Check(image_LienMinh.YeuCau_HoatDongLienMinh,Click=True):
                            self.Update_Database_Running(email = Email, chucnang= "HoatDongLienMinh", giatri=1)
                            return
                        else:
                            if self.Time_Check(Start,2):
                                self.Update_Database_Running(email = Email, chucnang= "HoatDongLienMinh", giatri=1)
                                return

                        

                    if CK_HoatDongLienMinh:
                        if self.Check(image_LienMinh.CK_HoatDongLienMinh,sleep = 0.05):
                            if self.Check(image_LienMinh.BangXepHangHomQua, Click=True,sleep = 0.1):
                                CK_HoatDongLienMinh = False
                                NhanQua =True
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,2):
                                    return
                        else:
                            if self.Time_Check(Start,2):
                                CK_HoatDongLienMinh = False
                                VaoLienMinh = True
                                Start = time.time()
 

                    if CK_LienMinh:


                        if self.Check(image_LienMinh.CK_LienMinh):
                            if self.Check(image_LienMinh.HoatDongLienMinh,Click=True):
                                CK_LienMinh = False
                                CK_HoatDongLienMinh = True
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,2):
                                    return

                        if self.Check(image_LienMinh.GiaNhapLienMinh):
                            return

                        else:
                            if self.Time_Check(Start,2):
                                CK_LienMinh = False
                                VaoLienMinh = True
                                Start = time.time()


                    if VaoLienMinh:
                        # Titan
                        if self.Check(image_LienMinh.LienQuan):
                            self.Update_Database_Running(email = Email, chucnang= "HoatDongLienMinh", giatri=1)

                            return
                        if self.Check(image_LienMinh.VaoLienMinh,Click=True):
                            VaoLienMinh = False
                            CK_LienMinh = True
                            Start = time.time()
                            continue

                        
                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                VaoLienMinh = True
                                Start = time.time()
                    

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def Pk_Titan(self):

        def XuatBinh(self,Set_Dao):
            '''Set Dao 2 Bo Binh, 3 Ky Binh, 4 Cung Thu'''
            print("Xuất Binh")
            Da_Click_Dao = False

            Start = time.time()
            for i in range (0,300):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.screenshot is None: continue
                if self.Check(image_XuatBinh.TapHop,sleep = 0):
                    if Da_Click_Dao:

                        if self.Check(image_XuatBinh.XuatBinh_TapHop,Click=True):
                            return
                        else:
                            if self.Time_Check(Start,3):
                                return
                        

                    # Click Số Đạo
                    if Da_Click_Dao == False:
                        if Set_Dao == 2:
                            if self.Check(image_DanhQuai.Dao2,Click=True,sleep =0.1):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return

                                
                        if Set_Dao == 3:
                            if self.Check(image_DanhQuai.Dao3,Click=True,sleep = 0.1):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return


                        if Set_Dao == 4:
                            if self.Check(image_DanhQuai.Dao4,Click=True,sleep =0.1):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return

                            
                else:
                    if self.Check(image_XuatBinh.BanChiCoThe):
                        return
                    if self.Time_Check(Start,3):
                        return


        VaoHopThu = True
        CK_HopThu = False
        Tim_PhatDong =False
        CK_Key = False
        Start = time.time()
        while True:
            if Exit_Event.wait(timeout=Setting_Bot.Delay):
                return

            if self.Running:
                if self.screenshot is None: continue

                if CK_Key:
                    if self.Check(image_Pk_Titan.Naia,khoang_x= 200, Click_Khac=True,khac_x =181,khac_y = 686) or self.Check(image_Pk_Titan.Rothai_jeb,khoang_x= 200,  Click_Khac=True,khac_x =181,khac_y = 686):
                        XuatBinh(self,Set_Dao = 2)
                        return

                    else:
                        if self.Time_Check(Start,2):
                            return



                if Tim_PhatDong:
                    if self.Check(image_Pk_Titan.ToiDaPhatDong, khoang_y =10, Click=True):
                        Tim_PhatDong = False
                        CK_Key = True
                        Start = time.time()
                        continue
                        

                    else:
                        if self.Time_Check(Start,2):
                            return


                if CK_HopThu:
                    if self.Check(image_Pk_Titan.CK_TroChuyen):
                        if self.Check(image_Pk_Titan.LienQuan,):#Click=True):
                            Tim_PhatDong = True
                            CK_HopThu = False
                            Start = time.time()

                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                VaoHopThu = True
                                CK_HopThu = False
                                Start = time.time()

                    else:
                        if self.Time_Check(Start,2):
                            self.out_MHchinh()
                            VaoHopThu = True
                            CK_HopThu = False
                            Start = time.time()

                if VaoHopThu:
                    if self.Check(image_Pk_Titan.HopThu,Click=True):
                        VaoHopThu = False
                        CK_HopThu = True
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start,2):
                            self.out_MHchinh()
                            Start = time.time()


                else:
                    if self.Time_Check(Start,2):
                        self.out_MHchinh()
                        Start = time.time()

                    


            
            



# Event
    
    def Event_RuongKVK(self):
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True

        Da_ClickNhanRuong =False
        ruong1 = True
        ruong2 = False
        ruong3 = False
        ruong4 = False
        ruong5 = False
        ruong6 = False
        nhanxong = False

        Vao_TrungTamSukien = True
        CK_TrungTamsuKien = False
        CK_VuongQuocManhNhat = False



        if self.out_MHchinh(TrungTamPhucLoi= False):
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:

                    if self.screenshot is None: continue


                    if CK_VuongQuocManhNhat:

                        if Da_ClickNhanRuong:
                            if self.Check(image_Event.DaYeuCau_RuongKVK,Click=True, khoang_x = 20,khoang_y =100,threshold = 0.7):
                                Da_ClickNhanRuong =False
                                Start = time.time()
                                if nhanxong:
                                     return
                                continue

                            if self.Check(image_Event.YeuCau_RuongKVK,Click=True, khoang_x = 20,khoang_y =100, sleep = 0.1,threshold = 0.7):
                                Da_ClickNhanRuong =False
                                Start = time.time()
                                if nhanxong:
                                    return
                                continue  

                            else:
                                if self.Time_Check(Start,3):

                                    return


                        if self.Check(image_Event.CK_VuongQuocManhNhat):

                            if self.Check(image_Event.ThuongDiemLienMinh):
                                if ruong1:
                                    ruong1 = False
                                    ruong2 =True
                                    controller().Click(66,567)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue

                
                                if ruong2:
                                    print("Ryuong2")
                                    ruong2 = False
                                    ruong3 = True
                                    controller().Click(193,567)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue                

                                if ruong3:
                                    ruong3 = False
                                    ruong4 = True
                                    controller().Click(312,567)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue

                                if ruong4:
                                    ruong4 = False
                                    ruong5 =True
                                    controller().Click(66, 404)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue

                
                                if ruong5:
                                    ruong5 = False
                                    ruong6 = True
                                    controller().Click(164,404)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue                

                                if ruong6:
                                    ruong6 = False
                                    nhanxong = True
                                    controller().Click(279,403)
                                    Da_ClickNhanRuong =True
                                    Start = time.time()
                                    continue

                            else:
                                if self.Time_Check(Start,3):
                                    return  

                        else:
                             if self.Time_Check(Start,3):
                                 return

                    if CK_TrungTamsuKien:
                        if self.Check(image_Event.CK_TrungTamSuKien):

                            if self.Check(image_Event.VuongQuocManhNhat,Click=True,khoang_y = 300):
                                CK_TrungTamsuKien = False
                                CK_VuongQuocManhNhat = True
                                Start = time.time()
                                continue
                            else:
                                if swipe_len == True:

                                    controller().Swipe(Swipe_Event_Len)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        da_swipe = 0
                                        swipe_len = False
                                    Start = time.time()
                                    continue

                                else:
                                    controller().Swipe(Swipe_Event_Xuong)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        return
                                    Start = time.time()
                                    continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Vao_TrungTamSukien = True
                                CK_TrungTamsuKien = False
                                Start = time.time()
                                

                    if Vao_TrungTamSukien:
                        if self.Check(image_Event.TrungTamSuKien,Click=True):
                            Vao_TrungTamSukien = False
                            CK_TrungTamsuKien = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Vao_TrungTamSukien = True
                                Start = time.time()



                    else:
                        if self.Time_Check(Start,3):
                            self.out_MHchinh(TrungTamPhucLoi= False)
                            Start = time.time()




                

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def Event_KhoBauBiAn(self):
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True

        Vao_TrungTamSukien = True
        CK_TrungTamSuKien = False
        CK_KhoBauBiAn = False

        if self.out_MHchinh(TrungTamPhucLoi= False):
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:

                    if self.screenshot is None: continue

                    if CK_KhoBauBiAn:

                        if self.Check(image_Event.CK_KhoBauBiAn):

                            if self.Check(image_Event.YeuCau_KhoBauBiAn,Click=True, sleep = 0.1, threshold = 0.7):
                                continue

                            else:
                                return

                        else:
                            if self.Time_Check(Start,3):
                                return



                    if CK_TrungTamSuKien:
                        if self.Check(image_Event.CK_TrungTamSuKien):

                            if self.Check(image_Event.KhoBauBiAn,Click=True,khoang_y = 300,threshold =0.9):
                                CK_TrungTamSuKien = False
                                CK_KhoBauBiAn = True
                                Start = time.time()
                                continue
                            else:
                                if swipe_len == True:
                                    controller().Swipe(Swipe_Event_Len)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        da_swipe = 0
                                        swipe_len = False
                                    Start = time.time()
                                    continue

                                else:
                                    controller().Swipe(Swipe_Event_Xuong)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        return
                                    Start = time.time()
                                    continue
                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Vao_TrungTamSukien = True
                                CK_TrungTamsuKien = False
                                Start = time.time()



                    if Vao_TrungTamSukien:
                        if self.Check(image_Event.TrungTamSuKien,Click=True,sleep=1):
                            Vao_TrungTamSukien = False
                            CK_TrungTamSuKien = True
                            Start = time.time()
                            continue
                        
                        else:
                            if self.Time_Check(Start,3):
                                Vao_TrungTamSukien = True
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Start = time.time()


                

                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def Event_MayBan_Da(self):
        print("Máy Bắn Đá")
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True
        Click_DangTienHanh = False
    
        if self.out_MHchinh(TrungTamPhucLoi = False):
            Start = time.time()
            for i in range (self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    
                    if self.screenshot is None: continue
                    if Click_DangTienHanh == True:
                        if self.Check(image_Event.DangTienHanh,Click=True):
                            Click_DangTienHanh = False
                            continue
                        
                        else:
                            if self.Time_Check(Start):
                                return

                    
                    if self.Check(image_Event.CK_MayBanDa,sleep=0.2):
                        if self.Check(image_Event.Luot_1,Click=True, sleep = 0.1,threshold = 0.7):
                            return

                        else:
                            return


                    elif self.Check(image_Event.CK_TrungTamSuKien):

                        if self.Check(image_Event.MayBanDa,Click=True,khoang_y = 300,threshold =0.9,sleep = 0.3):
                            continue
                        else:
                            if swipe_len == True:
                                controller().Swipe(Swipe_Event_Len)
                                Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                da_swipe +=1
                                if da_swipe == 5:
                                    da_swipe = 0
                                    swipe_len = False
                                continue

                            else:
                                controller().Swipe(Swipe_Event_Xuong)
                                Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                da_swipe +=1
                                if da_swipe == 5:
                                    return
                                continue




                    elif self.Check(image_Event.TrungTamSuKien,Click=True,sleep=1):
                        Click_DangTienHanh = True
                        continue
                    else:
                        if self.Time_Check(Start):
                            return



                
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def Event_ThuThapKietXuat(self):
        print("Thu Thap Kiet Xuat")
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True
        Vao_TrungTamSukien = True
        CK_TrungTamsuKien = False
        CK_ThuThapKietXuat = False

        if self.out_MHchinh(TrungTamPhucLoi = False):
            Start = time.time()
            for i in range (self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    if self.screenshot is None: continue

                    if CK_ThuThapKietXuat:

                        if self.Check(image_Event.CKThuThapKietXuat,sleep=0.1,):
                            if self.Check(image_Event.YeuCau,Click=True, sleep = 0.1,threshold = 0.7):
                                Start = time.time()
                                continue

                            else:
                                return

                    if CK_TrungTamsuKien:

                        if self.Check(image_Event.CK_TrungTamSuKien):

                            if self.Check(image_Event.ThuThapKietXuat,Click=True,khoang_y = 300,threshold =0.9,sleep = 0.3):
                                CK_ThuThapKietXuat = True
                                CK_TrungTamsuKien = False
                                continue

                            else:
                                if swipe_len == True:
                                    controller().Swipe(Swipe_Event_Len)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        da_swipe = 0
                                        swipe_len = False

                                    Start = time.time()
                                    continue

                                else:
                                    controller().Swipe(Swipe_Event_Xuong)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        return
                                    Start = time.time()
                                    continue

                        else:
                            if self.Time_Check(Start,3):
                                CK_TrungTamSuKien = False
                                Vao_TrungTamSukien = True
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Start = time.time()
                                    


                    if Vao_TrungTamSukien:

                        if self.Check(image_Event.TrungTamSuKien,Click=True,sleep=1):
                            Vao_TrungTamSukien = False
                            CK_TrungTamsuKien = True
                            continue
                        else:
                            if self.Time_Check(Start,3):
                                Vao_TrungTamSukien = True
                                CK_TrungTamsuKien = False
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Start = time.time()

                    else:
                        if self.Time_Check(Start):
                            return

                
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def Event_DoiCanhBauTroi(self):
        """Event Đôi Cánh Bầu Trời"""
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True


        CK_DoiCanhBauTroi = False
        Vao_TrungTamSukien = True
        CK_TrungTamsuKien = False
        
        if self.out_MHchinh(TrungTamPhucLoi= False):
            Start = time.time()
            for i in range (self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.Running:

                    if self.screenshot is None: continue



                    if CK_DoiCanhBauTroi:
                        if self.Check(image_Event.CK_DoiCanhBauTroi):
                            if self.Check(image_Event.YeuCau_DoiCanhBauTroi,Click=True, sleep = 0.1):
                                Start = time.time()
                                continue
                            if self.Check(image_Event.Di_DoiCanhBauTroi):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                return
                            else:
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                return
                        else:
                            if self.Time_Check(Start,2):
                                return


                    if CK_TrungTamsuKien:
                        if self.Check(image_Event.CK_TrungTamSuKien):

                            if self.Check(image_Event.DoiCanhBauTroi,Click=True,khoang_y = 300):
                                CK_TrungTamsuKien = False
                                CK_DoiCanhBauTroi = True
                                continue
                            else:
                                if swipe_len == True:
                                    controller().Swipe(Swipe_Event_Len)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        da_swipe = 0
                                        swipe_len = False
                                    continue

                                else:
                                    controller().Swipe(Swipe_Event_Xuong)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        return
                                    continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Vao_TrungTamSukien = True
                                CK_TrungTamsuKien = False
                                Start = time.time()
                                

                    if Vao_TrungTamSukien:
                        if self.Check(image_Event.TrungTamSuKien,Click=True):
                            Vao_TrungTamSukien = False
                            CK_TrungTamsuKien = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Vao_TrungTamSukien = True
                                Start = time.time()



                    else:
                        if self.Time_Check(Start,3):
                            self.out_MHchinh(TrungTamPhucLoi= False)
                            Start = time.time()





                
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()


    def DiQuan_XamLuoc(self):
        Swipe_Event_Len = self.Docfiletext("Event/Swipe_Event_Len")
        Swipe_Event_Xuong = self.Docfiletext("Event/Swipe_Event_Xuong")
        da_swipe = 0
        swipe_len = True
        Swipe_NguoiKhongLo = self.Docfiletext("Event/DiQuanXamLuoc/Swipe_NguoiKhongLo")
        

        Vao_TrungTamSukien = True
        CK_TrungTamsuKien = False
        CK_DiQuanXamLuoc = False
        CK_DiQuan = False
        Tap_Hop = False
        Click= 0
        if self.out_MHchinh(TrungTamPhucLoi = False):
            Start = time.time()
            for i in range (0,1000):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.Running:


                    
                    if self.screenshot is None: continue
                    if Click >=5:
                        return
                    if self.Check(image_DanhQuai.DaXuat_6Dao,sleep=1):
                        Start = time.time()
                        continue

                    if Tap_Hop:

                        if self.Check(image_Event.TapHop,Click=True):
                            return
                        elif self.Check(image_Event.OK_TapHop,Click=True,sleep = 0.1):
                            Start = time.time()
                            continue
                        
                        else:
                            if self.Time_Check(Start,3):
                                return

                    if CK_DiQuan:

                        
                        if self.Check(image_Event.TapHopTanCong,Click=True,khoang_x=0,khoang_y = 0):
                            CK_DiQuan = False
                            Tap_Hop = True
                            Start = time.time()
                            continue

                        if self.Check(image_DiAnMo.Find_Rss, Click_Khac=True, khac_x = 197, khac_y = 366):
                            Start = time.time()
                            Click +=1
                            continue


                        else:
                            if self.Time_Check(Start,3):
                                return







                    if CK_DiQuanXamLuoc:
                        if self.Check(image_Event.CK_DiQuanXamLuoc,sleep=0.2):
                            if self.Check(image_Event.NguoiKhongLo, khoang_y = 10):
                                if self.Check(image_Event.DiTieuDiet , Click=True,sleep = 1):
                                    CK_DiQuan = True
                                    CK_DiQuanXamLuoc = False
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start,3):
                                        return

                            elif self.Check(image_Event.ConDoi, khoang_y = 10):
                                controller().Swipe(Swipe_NguoiKhongLo)
                                Exit_Event.wait(timeout= 0.1)
                                Start = time.time()
                                continue
                                
                            else:
                                if self.Time_Check(Start,3):
                                    self.out_MHchinh(TrungTamPhucLoi= False)
                                    return
                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                return

                    if CK_TrungTamsuKien:
                        if self.Check(image_Event.CK_TrungTamSuKien):

                            if self.Check(image_Event.DiQuanXamLuoc,Click=True,khoang_y = 300,threshold =0.9,sleep = 0.3):
                                CK_DiQuanXamLuoc = True
                                CK_TrungTamsuKien = False
                                Start = time.time()
                                continue
                            else:
                                if swipe_len == True:
                                    controller().Swipe(Swipe_Event_Len)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        da_swipe = 0
                                        swipe_len = False
                                    Start = time.time()
                                    continue

                                else:
                                    controller().Swipe(Swipe_Event_Xuong)
                                    Exit_Event.wait(timeout= self.Sleep_Swipe_Event)
                                    da_swipe +=1
                                    if da_swipe == 5:
                                        return
                                    Start = time.time()
                                    continue


                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                CK_TrungTamsuKien= False
                                Vao_TrungTamSukien = True
                                Start = time.time()



                    if Vao_TrungTamSukien:
                        if self.Check(image_Event.TrungTamSuKien,Click=True,sleep=1):
                            Vao_TrungTamSukien = False
                            CK_TrungTamsuKien = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh(TrungTamPhucLoi= False)
                                Start = time.time()
                                continue



                
                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()





# Danh Vien Co

    def Danh_VienCo(self):

        def XuatBinh(self,Set_Dao):
            print("Xuất Binh")
            Da_Click_Dao = False
            Start = time.time()
            for i in range (0,100):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.screenshot is None: continue

                if self.Check(image_DanhQuai.CK_XuatBinh):
                    if Da_Click_Dao:
                    #    if self.Check(image_DanhQuai.CK_CoLinh,):
                        if self.Check(image_DanhQuai.XuatBinh,Click=True):
                            
                            return

                        else:
                            if self.Time_Check(Start,3):
                                return
                        
                        # else:
                        #     if self.Time_Check(Start,3):
                        #         return 
                        

                    if Da_Click_Dao == False:
                        if Set_Dao == 2:
                            if self.Check(image_DanhQuai.Dao2,Click=True):
                                Da_Click_Dao = True
                                Exit_Event.wait(0.05)
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,3):
                                    return 
                                
                        if Set_Dao == 3:
                            if self.Check(image_DanhQuai.Dao3,Click=True):
                                Da_Click_Dao = True
                                Exit_Event.wait(0.05)
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,3):
                                    return

                        if Set_Dao == 4:
                            if self.Check(image_DanhQuai.Dao4,Click=True):
                                Da_Click_Dao = True
                                Exit_Event.wait(0.05)
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,3):
                                    return
                                
                        if Set_Dao == 5:
                            if self.Check(image_DanhQuai.Dao5,Click=True):
                                Da_Click_Dao = True
                                Exit_Event.wait(0.05)
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,3):
                                    return
                else:
                    if self.Time_Check(Start,3):
                        return

        set_Dao = 2
        CK_XuatBinh =False
        if self.out_MHchinh():
            Start = time.time()

            for i in range(0,500):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                
 
                if self.screenshot is None: continue
                if self.Check(image_DangNhap.ThanhBenTrong, Click=True):
                    Exit_Event.wait(timeout= 0.5)

                    continue

                if self.Check(image_DanhQuai.DaXuat_6Dao):
                    continue
                if self.Check(image_XuatBinh.ShowQuanDoi, Click=True):
                    continue

                if set_Dao >= 6:
                    set_Dao = 2

                if CK_XuatBinh == False:
                    if self.Check(image_VienCo.Click_Monter_TanCong,khoang_x=30,khoang_y = 30):
                        controller().Click(159,560)
                        controller().Click(159,560)
                        CK_XuatBinh = True
                        Start = time.time()
                        continue

                if CK_XuatBinh == True:
                    if self.Check(image_DanhQuai.CK_XuatBinh):
                        XuatBinh(self,set_Dao)
                        CK_XuatBinh = False
                        set_Dao +=1
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start,3):
                            self.out_MHchinh()
                            CK_XuatBinh = False
                            Start = time.time()


                else:
                    if self.Time_Check(Start,3):
                        self.out_MHchinh()
                        CK_XuatBinh = False
                        Start = time.time()




# Quais KVK
    def Check_KhoangCach(self,screen_KhoangCach,anhnho):

        result = matchTemplate(screen_KhoangCach, anhnho.anh(),TM_CCOEFF_NORMED)# TM_CCORR_NORMED)
        (minVal, maxVal, minLoc, (x, y)) = minMaxLoc(result)
        if maxVal >= 0.8:
            if x + 1 >= int(anhnho.toado()[0]) >= x - 1 and y + 1 >= int(anhnho.toado()[1]) >= y - 1:
                return True
            else:
                return False
        else:
            return False

    def DoKhoangCach(self):
        Khoangcach = 0
        KC_x = True
        Start = time.time()


        for i in range(self.TimeLoad[0],self.TimeLoad[1]):
            if Exit_Event.wait(timeout=Setting_Bot.Delay): return Khoangcach

            if self.screenshot is None: continue

            if self.Check(image_DiAnMo.Find_Rss):
                screen_KhoangCach = self.screenshot
                if KC_x:

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_1x):
                        Khoangcach =10
                        return Khoangcach

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_2x):
                        Khoangcach =20
                        return Khoangcach


                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_3x):
                        Khoangcach =30
                        return Khoangcach


                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_4x):
                        Khoangcach =40
                        return Khoangcach
            
                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_5x):
                        Khoangcach =50
                        return Khoangcach

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_6x):
                        Khoangcach =60
                        return Khoangcach

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_7x):
                        Khoangcach =70
                        return Khoangcach

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_8x):
                        Khoangcach =80
                        return Khoangcach


                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_9x):
                        Khoangcach =90
                        return Khoangcach

                    if self.Check_KhoangCach(screen_KhoangCach,image_KhoangCach_Quai.KC_1xx):
                        Khoangcach =100
                        return Khoangcach


                    else:
                        return Khoangcach




            else:
                if self.Time_Check(Start,1):
                    return Khoangcach
        return Khoangcach
            


    def DanhQuai_KVK(self,CapQuai ,Set_Dao, DanhTitan = False):


        def Check_Quai(self):
            Da_Click = 0
            print("Check Quái")
            Start = time.time()
            TanCong  = False
            Click_TrungTam = True
            Click_Tim = False
            for i in range(0,1000):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.screenshot is None: continue

                if self.Check(image_DanhQuai.DaXuat_6Dao):
                    continue
                
                if Da_Click >= 5:
                    print(" 1             Loi                                    ")
                    return False

                if self.Check(image_DanhQuai.TanCong,Click=True,khoang_x= 0, khoang_y=0,sleep = 0.05):
                    return True

    


                else:
                    if Click_TrungTam:
                    #if self.Check(image_DiAnMo.Find_Di,sleep = 0.05):
                        controller().Click(197, 366)
                        Exit_Event.wait(timeout=0.2)
                        TanCong = True
                        Click_TrungTam = False
                        print("Click trungtam")
                        Da_Click +=1
                        Start = time.time()
                        continue



                    #elif Click_TrungTam == False:
                    else:
                        print("Click tim")
                    #if self.Check(image_DiAnMo.Find_Rss,Click=True,sleep = 0.05):
                        controller().Click(29, 491)
                        Exit_Event.wait(timeout= 0.2)
                        Start = time.time()
                        Click_TrungTam = True
                        continue
                    # else:
                    #     Click_TrungTam = True
                    #     TanCong = False
                    #     continue
                        

                    # if self.Time_Check(Start,1):
                    #     print("   222222                  Loi                                    ")
                    #     return False






        def Chinh_CapQuai(self,CapQuai,DanhTitan = False):
            print("Chỉnh Cấp Quái")
            CapQuai_HienTai = 0
            Start = time.time()
            for i in range(0,100):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.screenshot is None: continue
                if self.Check(image_DiAnMo.Find_Di,sleep = 0):
                    template = imread('New_Data/DanhQuai/CapQuaiKVK/Cap1.png', 0)
                    res = matchTemplate(self.screenshot,template, TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = minMaxLoc(res)
                    if max_val >= 0.9:
                    #

                        if DanhTitan == False:
                            if max_loc[1] == 626:
                                #Cấp 40
                                if max_loc[0] == Cap_QuaiKVK.Cap40:
                                    CapQuai_HienTai = 40
        
                                #Cấp 39
                                if max_loc[0] == Cap_QuaiKVK.Cap39:
                                    CapQuai_HienTai = 39

                                #Cấp 38
                                if max_loc[0] == Cap_QuaiKVK.Cap38:
                                    CapQuai_HienTai = 38

                                #Cấp 37
                                if max_loc[0] == Cap_QuaiKVK.Cap37:
                                    CapQuai_HienTai = 37

                                #Cấp 36
                                if max_loc[0] == Cap_QuaiKVK.Cap36:
                                    CapQuai_HienTai = 36

                                #Cấp 35
                                if max_loc[0] == Cap_QuaiKVK.Cap35:
                                    CapQuai_HienTai = 35

                                #Cấp 34
                                if max_loc[0] == Cap_QuaiKVK.Cap34:
                                    CapQuai_HienTai = 34

                                #Cấp 33
                                if max_loc[0] == Cap_QuaiKVK.Cap33:
                                    CapQuai_HienTai = 33

                                #Cấp 32
                                if max_loc[0] == Cap_QuaiKVK.Cap32:
                                    CapQuai_HienTai = 32

                                #Cấp 31
                                if max_loc[0] == Cap_QuaiKVK.Cap31:
                                    CapQuai_HienTai = 31

                                #Cấp 30
                                if max_loc[0] == Cap_QuaiKVK.Cap30:
                                    CapQuai_HienTai = 30

                                #Cấp 39
                                if max_loc[0] == Cap_QuaiKVK.Cap29:
                                    CapQuai_HienTai = 29

                                #Cấp 28
                                if max_loc[0] == Cap_QuaiKVK.Cap28:
                                    CapQuai_HienTai = 28

                                #Cấp 27
                                if max_loc[0] == Cap_QuaiKVK.Cap27:
                                    CapQuai_HienTai = 27


                                #Cấp 26
                                if max_loc[0] == Cap_QuaiKVK.Cap26:
                                    CapQuai_HienTai = 26

                                #Cấp 25
                                if max_loc[0] == Cap_QuaiKVK.Cap25:
                                    CapQuai_HienTai = 25


                                #Cấp 24
                                if max_loc[0] == Cap_QuaiKVK.Cap24:
                                    CapQuai_HienTai = 24

                                #Cấp 23
                                if max_loc[0] == Cap_QuaiKVK.Cap23:
                                    CapQuai_HienTai = 23

                                #Cấp 22
                                if max_loc[0] == Cap_QuaiKVK.Cap22:
                                    CapQuai_HienTai = 22


                                #Cấp 21
                                if max_loc[0] == Cap_QuaiKVK.Cap21:
                                    CapQuai_HienTai = 21



                                #Cấp 20
                                if max_loc[0] == Cap_QuaiKVK.Cap20:
                                    CapQuai_HienTai = 20

                                #Cấp 19
                                if max_loc[0] == Cap_QuaiKVK.Cap19:
                                    CapQuai_HienTai = 19

                                #Cấp 18
                                if max_loc[0] == Cap_QuaiKVK.Cap18:
                                    CapQuai_HienTai = 18

                                #Cấp 17
                                if max_loc[0] == Cap_QuaiKVK.Cap17:
                                    CapQuai_HienTai = 17

                                #Cấp 16
                                if max_loc[0] == Cap_QuaiKVK.Cap16:
                                    CapQuai_HienTai = 16

                                #Cấp 15
                                if max_loc[0] == Cap_QuaiKVK.Cap15:
                                    CapQuai_HienTai = 15

                                #Cấp 14
                                if max_loc[0] == Cap_QuaiKVK.Cap14:
                                    CapQuai_HienTai = 14

                                #Cấp 13
                                if max_loc[0] == Cap_QuaiKVK.Cap13:
                                    CapQuai_HienTai = 13

                                #Cấp 12
                                if max_loc[0] == Cap_QuaiKVK.Cap12:
                                    CapQuai_HienTai = 12

                                #Cấp 11
                                if max_loc[0] == Cap_QuaiKVK.Cap11:
                                    CapQuai_HienTai = 11

                                #Cấp 10
                                if max_loc[0] == Cap_QuaiKVK.Cap10:
                                    CapQuai_HienTai = 10

                                #Cấp 9
                                if max_loc[0] == Cap_QuaiKVK.Cap9:
                                    CapQuai_HienTai = 9

                                #Cấp 8
                                if max_loc[0] == Cap_QuaiKVK.Cap8:
                                    CapQuai_HienTai = 8

                                #Cấp 7
                                if max_loc[0] == Cap_QuaiKVK.Cap7:
                                    CapQuai_HienTai = 7

                                #Cấp 6
                                if max_loc[0] == Cap_QuaiKVK.Cap6:
                                    CapQuai_HienTai = 6

                                #Cấp 5
                                if max_loc[0] == Cap_QuaiKVK.Cap5:
                                    CapQuai_HienTai = 5


                                #Cấp 4
                                if max_loc[0] == Cap_QuaiKVK.Cap4:
                                    CapQuai_HienTai = 4

                                #Cấp 3
                                if max_loc[0] == Cap_QuaiKVK.Cap3:
                                    CapQuai_HienTai = 3


                                #Cấp 2
                                if max_loc[0] == Cap_QuaiKVK.Cap2:
                                    CapQuai_HienTai = 2

                                #Cấp 1
                                if max_loc[0] == Cap_QuaiKVK.Cap1:
                                    CapQuai_HienTai = 1

                        if DanhTitan == True:
                            if max_loc[1] == 626:
                                if max_loc[0] == Cap_QuaiTitan.Cap_26:
                                    CapQuai_HienTai = 26

                                if max_loc[0] == Cap_QuaiTitan.Cap_27:
                                    CapQuai_HienTai = 27

                                if max_loc[0] == Cap_QuaiTitan.Cap_28:
                                    CapQuai_HienTai = 28

                                if max_loc[0] == Cap_QuaiTitan.Cap_29:
                                    CapQuai_HienTai = 29

                                if max_loc[0] == Cap_QuaiTitan.Cap_30:
                                    CapQuai_HienTai = 30

                                if max_loc[0] == Cap_QuaiTitan.Cap_31:
                                    CapQuai_HienTai = 31

                                if max_loc[0] == Cap_QuaiTitan.Cap_32:
                                    CapQuai_HienTai = 32

                                if max_loc[0] == Cap_QuaiTitan.Cap_33:
                                    CapQuai_HienTai = 33
                                if max_loc[0] == Cap_QuaiTitan.Cap_34:
                                    CapQuai_HienTai = 34

                                if max_loc[0] == Cap_QuaiTitan.Cap_35:
                                    CapQuai_HienTai = 35

                                if max_loc[0] == Cap_QuaiTitan.Cap_36:
                                    CapQuai_HienTai = 36

                                if max_loc[0] == Cap_QuaiTitan.Cap_37:
                                    CapQuai_HienTai = 37
                                if max_loc[0] == Cap_QuaiTitan.Cap_38:
                                    CapQuai_HienTai = 38

                                if max_loc[0] == Cap_QuaiTitan.Cap_39:
                                    CapQuai_HienTai = 39

                                if max_loc[0] == Cap_QuaiTitan.Cap_40:
                                    CapQuai_HienTai = 40







                        if CapQuai_HienTai > 0:
                            # Bằng Cấp Set
                            if CapQuai_HienTai == int(CapQuai):
                                if self.Check(image_DiAnMo.Find_Di,Click=True, sleep = 0.05):
                                    Start = time.time()
                                    return True

                                else:
                                    if self.Time_Check(Start,2):
                                        return False

                            # Lớn Hơn Cấp Set
                            elif CapQuai_HienTai > int(CapQuai):
                                for i in range(int(CapQuai),CapQuai_HienTai):
                                    if self.Check(image_DiAnMo.Find_Di, sleep = 0):
                                        controller().Click(73,633)


                                if self.Check(image_DiAnMo.Find_Di,Click=True, sleep = 0.05):
                                    return True

                                # else:
                                #     return False

                            # Nhỏ Hơn Cấp int(CapQuai)
                            elif CapQuai_HienTai < int(CapQuai):
                                for i in range(CapQuai_HienTai,int(CapQuai)):
                                    if self.Check(image_DiAnMo.Find_Di, sleep = 0):
                                        controller().Click(294,633)
                                    #self.Check(image_DiAnMo.Find_Tang_LV,Click=True, sleep = 0.01)

                                if self.Check(image_DiAnMo.Find_Di,Click=True, sleep = 0.05):
                                    return True
                        
                        else:
                            if self.Time_Check(Start,2):
                                return False

                    else:
                        return False
                                           
                else:
                    if self.Time_Check(Start,2):
                        return False

        def XuatBinh(self,Set_Dao):
            print("Xuất Binh")
            Da_Click_Dao = False

            Start = time.time()
            for i in range (0,300):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.screenshot is None: continue
                if self.Check(image_DanhQuai.CK_XuatBinh,sleep = 0):
                    if Da_Click_Dao:
                        print("VaoDAy11111111111111111111111",i)
                    # Check Có Lính, Xuất Binh
                        if self.Check(image_DanhQuai.CK_CoLinh,sleep = 0):
                            if self.Check(image_DanhQuai.XuatBinh,Click=True):
                                return
                            else:
                                if self.Time_Check(Start,3):
                                    return
                        
                        else:
                            if self.Time_Check(Start,3):
                                return


                    # Click Số Đạo
                    if Da_Click_Dao == False:
                        if Set_Dao == 2:
                            if self.Check(image_DanhQuai.Dao2,Click=True,sleep =0):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return

                                
                        if Set_Dao == 3:
                            if self.Check(image_DanhQuai.Dao3,Click=True,sleep = 0):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return


                        if Set_Dao == 4:
                            if self.Check(image_DanhQuai.Dao4,Click=True,sleep =0):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue
                            else:
                                if self.Time_Check(Start,3):
                                    return

                               
                        if Set_Dao == 5:
                            if self.Check(image_DanhQuai.Dao5,Click=True,sleep = 0):
                                Da_Click_Dao = True
                                Start = time.time()
                                continue

                            else:
                                if self.Time_Check(Start,3):
                                    return
                else:
                    if self.Time_Check(Start,3):
                        return


        # if Check_Quai(self):
        #     return
        # return 
        # Start
        MucTieuTren200m = False
        Click_Find= True
        CK_Quai = False

        if self.out_MHchinh():
            Start = time.time()
            while 1:
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return


                #Đang ở Thành Bên Trong
                if self.Check(image_DangNhap.ThanhBenTrong, Click=True):
                    Start = time.time()
                    continue 

                #Show Quân Đội 
                if self.Check(image_XuatBinh.ShowQuanDoi, Click=True):
                    Start = time.time()
                    continue

                if CK_Quai:
                    if DanhTitan == False:
                        if self.Check(image_DanhQuai.ChonQuai,Click=True):
                            if Chinh_CapQuai(self,CapQuai):
                                if Check_Quai(self):
                                    XuatBinh(self,Set_Dao)
                                    Start = time.time()
                                    return

                                else:
                                    if self.Time_Check(Start,2):
                                        print("                               Check Quai = False")
                                        self.out_MHchinh()
                                        CK_Quai = False
                                        Click_Find = True
                                        Start = time.time()

                            else:
                                if self.Time_Check(Start,2):
                                    print("                               Chinh Cap Quai= False")
                                    self.out_MHchinh()
                                    CK_Quai = False
                                    Click_Find = True
                                    Start = time.time()

                        else:
                            if self.Time_Check(Start,2):
                                print("                               Click Quai = False")
                                self.out_MHchinh()
                                CK_Quai = False
                                Click_Find = True
                                Start = time.time()

                    if DanhTitan == True:
                        if self.Check(image_DanhQuai.ChonQuai_Titan,Click=True):
                            if Chinh_CapQuai(self,CapQuai, DanhTitan = DanhTitan):
                                if Check_Quai(self):
                                    XuatBinh(self,Set_Dao)
                                    return

                                else:
                                    if self.Time_Check(Start,2):
                                        print("                               Check Quai = False")
                                        self.out_MHchinh()
                                        CK_Quai = False
                                        Click_Find = True
                                        Start = time.time()

                            else:
                                if self.Time_Check(Start,2):
                                    print("                               Chinh Cap Quai= False")
                                    self.out_MHchinh()
                                    CK_Quai = False
                                    Click_Find = True
                                    Start = time.time()

                        else:
                            if self.Time_Check(Start,2):
                                print("                               Click Quai = False")
                                self.out_MHchinh()
                                CK_Quai = False
                                Click_Find = True
                                Start = time.time()


                        

                if Click_Find:
                    if self.Check(image_DiAnMo.Find_Rss, Click=True, sleep=0.01) or self.Check(image_DiAnMo.Find_Di,sleep=0.01):
                        Click_Find = False
                        CK_Quai = True
                        Start = time.time()
                        continue

                    else:
                        if self.Time_Check(Start,2):
                            self.out_MHchinh()
                            Click_Find = True
                            Start = time.time()
                else:

                    if self.Time_Check(Start,2):
                        self.out_MHchinh()
                        Click_Find = True
                        Start = time.time()


                








    def DungBuaNgauNhien(self):
        Click_Tui = True
        Click_ChienTranh = False
        Check_BuaNgauNhien = False
        Check_SuDung = False
        if self.out_MHchinh:
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                
                if self.Running:

                    if self.screenshot is None: continue

                    if Check_SuDung:
                        if self.Check(image_Tui.Ok_SuDung_BuaNgauNhien) or self.Check(image_Tui.Titan_DiChuyen_OK):
                            controller().Click(187 ,427)
                            self.out_MHchinh()
                            return

                        elif self.Check(image_Tui.SuDung_BuaNgauNhien,Click=True):
                            Start = time.time()
                            continue

                        
                           
                        else:
                            if self.Time_Check(Start,2):
                                self.out_MHchinh()
                                return

                    if Check_BuaNgauNhien:
                        if self.Check(image_Tui.CK_CacMonDo):
                            if self.Check(image_Tui.Bua_NgauNhien,Click=True):
                                Check_BuaNgauNhien = False
                                Check_SuDung = True
                                Start = time.time()
                            
                            else:
                                if self.Time_Check(Start,2):
                                    print("Het Bua Ngau Nhien")
                                    self.out_MHchinh()
                                    return

                        else:
                            if self.Time_Check(Start,3):
                                Check_BuaNgauNhien = False
                                Click_Tui = True
                                Start = time.time()

                        


                    if Click_ChienTranh:
                        if self.Check(image_Tui.Tui_ChienTranh,Click=True):
                            Click_ChienTranh = False
                            Check_BuaNgauNhien = True
                            Start = time.time()
                            continue
                        else:
                            if self.Time_Check(Start,3):
                                Click_ChienTranh = False
                                Click_Tui = True
                                Start = time.time()


                    if Click_Tui:
                        if self.Check(image_Tui.Tui,Click=True):
                            Click_Tui = False
                            Click_ChienTranh = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh()
                                Start = time.time()
                    else:
                        if self.Time_Check(Start,3):
                            Click_Tui = True
                            self.out_MHchinh()
                            Start = time.time()



    def SuDung_BuaNgauNhien(self):
        if self.out_MHchinh():
            Start = time.time()
            while True:
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.screenshot is None: continue

                if self.Check(image_DanhQuai.Linh_DangVe,khoang_x =2) or self.Check(image_DanhQuai.Linh_TangToc):
                    Start = time.time()
                    continue

                else:
                    if self.Time_Check(Start,3):
                        return

                    self.DungBuaNgauNhien()
                    return

#


    def DocThu(self):
        Vao_Thu = True
        CK_Thu = False
        Tin_Nhan_LienMinh = True
        Tin_Nhan_DaiHoi = False
        Tin_Nhan_Thong_Bao = False
        Tin_Nhan_HeThong = False
        NhanXong = False
        Da_Nhan_DongLoat = False
        if self.out_MHchinh():
            Start = time.time()
            for i in range(self.TimeLoad[0],self.TimeLoad[1]):

                if Exit_Event.wait(timeout=Setting_Bot.Delay):
                    return

                if self.Running:
                    if self.screenshot is None: continue




                    if CK_Thu:

                        if self.Check(image_HopThu.DA_DocDongLoat,Click=True):
                            if NhanXong:
                                return
                            self.out_MHchinh()
                            Start = time.time()
                            continue

                        if self.Check(image_HopThu.CK_Thu):
                            
                            if Tin_Nhan_LienMinh:
                                if self.Check(image_HopThu.Tn_LienMinh,Click=True):
                                    Tin_Nhan_LienMinh = False
                                    Tin_Nhan_DaiHoi = True
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return

                            if Tin_Nhan_DaiHoi:

                                print("Tin_Nhan_DaiHoi")
                                if self.Check(image_HopThu.Tn_DaiHoi,Click=True):
                                    Tin_Nhan_DaiHoi = False
                                    Tin_Nhan_Thong_Bao = True
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start):
                                        return

                            if Tin_Nhan_Thong_Bao:
                                print("Tin_Nhan_Thong_Bao")
                                if self.Check(image_HopThu.Tn_ThongBao,Click=True):
                                    Tin_Nhan_Thong_Bao = False
                                    Tin_Nhan_HeThong = True
                                    Start = time.time()
                                    continue
                                else:
                                    if self.Time_Check(Start):
                                        return

                            if Tin_Nhan_HeThong:
                                print("Tin_Nhan_HeThong")
                                if self.Check(image_HopThu.Tn_HeThong,Click=True):
                                    Tin_Nhan_HeThong = False
                                    NhanXong = True
                                    Start = time.time()
                                    continue

                                else:
                                    if self.Time_Check(Start):
                                        return

                            else:
                                if self.Time_Check(Start):
                                    return




                        else:
                            if self.Time_Check(Start):
                                return  


                    if Vao_Thu:
                        if self.Check(image_HopThu.Thu,Click=True):
                            Vao_Thu = False
                            CK_Thu = True
                            Start = time.time()
                            continue

                        else:
                            if self.Time_Check(Start,3):
                                self.out_MHchinh()
                                Vao_Thu = True
                                CK_Thu = False
                                Start = time.time()
                                continue

                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            Vao_Thu =True
                            CK_Thu = False
                            Start = time.time()


                else:
                    while not self.Running: 
                        if Exit_Event.wait(timeout= Setting_Bot.Delay):
                            return 
                    Start = time.time()

    def GomRss(self,Vi_Tri_Acc = 1,Set_Dao = 2):
        print("GomRss")
        VaoDanhDau = True
        CK_DanhDau = False
        Acc_1 = True
        CK_TanCong = False



        def XuatBinh(self,Set_Dao):
            print("Xuất Binh")
            Da_Click_Dao = False

            Start = time.time()
            for i in range (0,300):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return

                if self.screenshot is None: continue
                if self.Check(image_DanhQuai.CK_XuatBinh,):

                    if self.Check(image_DanhQuai.XuatBinh,Click=True):
                        time.sleep(0.1)
                        return True
                    else:
                        if self.Time_Check(Start,3):
                            return False
                        


                else:
                    if self.Time_Check(Start,3):
                        return False

        if self.out_MHchinh():
            Start = time.time()
            for i in range(1,500):
                if Exit_Event.wait(timeout=Setting_Bot.Delay): return
                if self.screenshot is None: continue


                if self.Check(image_XuatBinh.ShowQuanDoi, Click=True):
                    Start = time.time()
                    continue

                if self.Check(image_DanhQuai.DaXuat_6Dao):
                    Start = time.time()
                    continue

                if self.Check(image_DangNhap.ThanhBenTrong,Click=True):
                    Exit_Event.wait(timeout=0.3)
                    Start = time.time()
                    continue

                if CK_TanCong:
                    if self.Check(image_Gomrss.TanCong,Click=True):
                        if XuatBinh(self,Set_Dao):
                            return True

                        else:
                            return False

                    else:
                        if self.Time_Check(Start):
                            return False






                if CK_DanhDau:
                    if self.Check(image_Gomrss.CK_DanhDau):
                        if Vi_Tri_Acc == 1:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(174,181)
                            Start = time.time()
                            continue

                        if Vi_Tri_Acc == 2:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(226,275)
                            Start = time.time()
                            continue

                        if Vi_Tri_Acc == 3:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(243 ,368)
                            Start = time.time()
                            continue

                        if Vi_Tri_Acc == 4:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(245,462)
                            Start = time.time()
                            continue

                        if Vi_Tri_Acc == 5:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(218,553)
                            Start = time.time()
                            continue

                        if Vi_Tri_Acc == 6:
                            CK_DanhDau = False
                            CK_TanCong = True
                            controller().Click(218,553)
                            Start = time.time()
                            continue





                    
                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            CK_DanhDau = False
                            VaoDanhDau = True
                            continue


                if VaoDanhDau:
                    if self.Check(image_Gomrss.DanhDau,Click=True):
                        VaoDanhDau = False
                        CK_DanhDau = True
                        Start = time.time()
                        continue
                    
                    else:
                        if self.Time_Check(Start):
                            self.out_MHchinh()
                            VaoDanhDau = True
                            CK_DanhDau = False
                            Start = time.time()
                            continue
                else:
                    if self.Time_Check(Start):
                        self.out_MHchinh()
                        VaoDanhDau = True
                        CK_DanhDau = False
                        Start = time.time()
                        continue










# Controller
    def Update_Screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def Start(self):
        print("[...Start_Bot_ChucNang...]")
        Exit_Event.clear()
        self.Running = True



    def Pause(self):
        print("[...Pause_Bot_ChucNang...]")
        self.Running = False

        

    def Continue(self):
        print("[...Continue_Bot_ChucNang...]")
        self.Running = True



    def Stop(self):
        print("[...Stop_Bot_ChucNang...]")

        self.Running = False
        Exit_Event.set()
        


