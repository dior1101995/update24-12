
import wmi
from datetime import datetime , timedelta
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


# dd/mm/YY H:M:S
    #    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")




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










