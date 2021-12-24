from cv2 import imread
from functools import lru_cache


@lru_cache
class anhnho:
    '''Thông Tin Ảnh Temple'''
    def __init__(self,Thumuc_TenAnh):
        self.template = imread("New_Data/%s.png"%(Thumuc_TenAnh), 0)
        self.needle_w = self.template.shape[1]
        self.needle_h = self.template.shape[0]
        with open("New_Data/%s.txt"%(Thumuc_TenAnh), encoding = 'utf-8') as f:
            self.toado1 = f.read().split(',')
        self.name1 =str(Thumuc_TenAnh).split('/')
        self.a = self.name1[-1:]

    def toado(self):
        return self.toado1

    def anh(self):
        return self.template

    def x(self):
        return  self.needle_w // 2

    def y(self):
        return  self.needle_h // 2

    def name(self):
        return self.a


class image_VienTro:
    Thuongmai = anhnho("VienTroTaiNguyen/Thuongmai")
    CK_TiepTeNguonLuc = anhnho("VienTroTaiNguyen/CK_TiepTeNguonLuc")
    TiepTeNguonLuc = anhnho("VienTroTaiNguyen/TiepTeNguonLuc")
    Sao1 = anhnho("VienTroTaiNguyen/Sao1")
    VaoToaDo = anhnho("VienTroTaiNguyen/VaoToaDo")
class image_VienCo:
    Click_Monter_TanCong = anhnho("DanhVienCo/Click_Monter_TanCong")
    

class image_DapLua_suaThanh:
    VaoDapLua = anhnho("DapLuaSuaThanh/VaoDapLua")
    DapLua = anhnho("DapLuaSuaThanh/DapLua")
    ThemSu_PhongThu = anhnho("DapLuaSuaThanh/ThemSu_PhongThu")
#    DapLuaVaMua_50Da = anhnho("DapLuaSuaThanh/DapLuaVaMua_50Da")

class image_XayDung:
    CK_Xay_1 = anhnho("XayDung/CK_Xay_1")
    XayDung_MienPhi = anhnho("XayDung/XayDung_MienPhi")
    XayDung = anhnho("XayDung/XayDung")
    Xay_Dung_2 = anhnho("XayDung/Xay_Dung_2")
    CK_Mo_6 = anhnho("XayDung/CK_Mo_6")
    NangCap = anhnho("XayDung/NangCap")
    NangCap_Mo = anhnho("XayDung/NangCap_Mo")

    CK_Click_Mo_6 = anhnho("XayDung/CK_Click_Mo_6")
    ChiTiet = anhnho("XayDung/ChiTiet")
    PhaHuy = anhnho("XayDung/PhaHuy")
    PhaHuy_GiamSucManh = anhnho("XayDung/PhaHuy_GiamSucManh")
    HuyBo_NangCap = anhnho("XayDung/HuyBo_NangCap")
    NeuBan_HuyBo = anhnho("XayDung/NeuBan_HuyBo")



class image_Nhan_NhiemVu:
    NhiemVu = anhnho("NhanNhiemVu/NhiemVu")
    CK_NhiemVu = anhnho("NhanNhiemVu/CK_NhiemVu")
    NhiemVuHangNgay1 = anhnho("NhanNhiemVu/NhiemVuHangNgay1")
    CK_NhiemVuHangNgay = anhnho("NhanNhiemVu/CK_NhiemVuHangNgay")
    YeuCau = anhnho("NhanNhiemVu/YeuCau")
    YeuCau2 = anhnho("NhanNhiemVu/YeuCau2")
    Ruongtren_6 = anhnho("NhanNhiemVu/Ruongtren_6")
    Ruongtren_5 = anhnho("NhanNhiemVu/Ruongtren_5")
    Ruongtren_4 = anhnho("NhanNhiemVu/Ruongtren_4")
    Ruongtren_3 = anhnho("NhanNhiemVu/Ruongtren_3")
    Ruongtren_2 = anhnho("NhanNhiemVu/Ruongtren_2")
    Ruongtren_1 = anhnho("NhanNhiemVu/Ruongtren_1")

    Ruongduoi_1 = anhnho("NhanNhiemVu/Ruongduoi_1")
    Ruongduoi_2 = anhnho("NhanNhiemVu/Ruongduoi_2")
    Ruongduoi_3 = anhnho("NhanNhiemVu/Ruongduoi_3")

class image_HopThu:
    CK_Thu = anhnho("HopThu/CK_Thu")


class image_Tui:
    Tui =anhnho("Tui/Tui")
    Tui_Khac = anhnho("Tui/Tui_Khac")
    Bua_Lua = anhnho("Tui/Bua_Lua")
    Bua_Go = anhnho("Tui/Bua_Go")
    Bua_KimLoai = anhnho("Tui/Bua_KimLoai")
    Bua_Bac = anhnho("Tui/Bua_Bac")
    SuDung_Bua = anhnho("Tui/SuDung_Bua")
    OK_SuDung = anhnho("Tui/OK_SuDung")
    Dung_Xong_Bua = anhnho("Tui/Dung_Xong_Bua")
    CK_Tui_Khac = anhnho("Tui/CK_Tui_Khac")

    #Mỏ Đá Quý
    Tang_SoLuong = anhnho("Tui/Tang_SoLuong")
    SuDung_DaQuy_2 = anhnho("Tui/SuDung_DaQuy_2")
    CK_CacMonDo = anhnho("Tui/CK_CacMonDo")
    SuDung_DaQuy_1 = anhnho("Tui/SuDung_DaQuy_1")
    DaQuy_10 = anhnho("Tui/DaQuy_10")
    XacNhan_SuDung = anhnho("Tui/XacNhan_SuDung")
    Da_Quy_1k = anhnho("Tui/Da_Quy_1k")
    #Mó Tài Nguyên
    Go_1000 = anhnho("Tui/Go_1000")
    Lua_1000 = anhnho("Tui/Lua_1000")
    KimLoai_1000 = anhnho("Tui/KimLoai_1000")
    Bac_1000 = anhnho("Tui/Bac_1000")

    # Bau Ngau Nhien
    Tui_ChienTranh = anhnho("Tui/Tui_ChienTranh")
    Bua_NgauNhien = anhnho("Tui/Bua_NgauNhien")
    SuDung_BuaNgauNhien = anhnho("Tui/SuDung_BuaNgauNhien")
    Ok_SuDung_BuaNgauNhien = anhnho("Tui/Ok_SuDung_BuaNgauNhien")
    Titan_DiChuyen_OK = anhnho("DanhQuai/Titan/Titan_DiChuyen_OK")




class image_Event:
    TrungTamSuKien = anhnho("Event/TrungTamSuKien")
    CK_TrungTamSuKien = anhnho("Event/CK_TrungTamSuKien")
    DangTienHanh = anhnho("Event/DangTienHanh")

    # Máy Bắn Đá
    Luot_1 = anhnho("Event/MayBanDa/Luot_1")
    MayBanDa = anhnho("Event/MayBanDa/MayBanDa")
    CK_MayBanDa = anhnho("Event/MayBanDa/CK_MayBanDa")

    #Đôi Cánh Bầu Trời
    DoiCanhBauTroi = anhnho("Event/DoiCanhBauTroi/DoiCanhBauTroi")
    YeuCau_DoiCanhBauTroi = anhnho("Event/DoiCanhBauTroi/YeuCau_DoiCanhBauTroi")
    Di_DoiCanhBauTroi = anhnho("Event/DoiCanhBauTroi/Di_DoiCanhBauTroi")
    CK_DoiCanhBauTroi = anhnho("Event/DoiCanhBauTroi/CK_DoiCanhBauTroi")

    #Gác Lầu Kho Báu
    GacLauKhoBau = anhnho("Event/GacLauKhoBau/GacLauKhoBau")
    CK_GacLauKhoBau = anhnho("Event/GacLauKhoBau/CK_GacLauKhoBau")
    ThongThuong = anhnho("Event/GacLauKhoBau/ThongThuong")
    HiemCo = anhnho("Event/GacLauKhoBau/HiemCo")
    HuyenThoai = anhnho("Event/GacLauKhoBau/HuyenThoai")
    TrangVienHo = anhnho("Event/GacLauKhoBau/TrangVienHo")
    CK_ThuongHiemCo = anhnho("Event/GacLauKhoBau/CK_ThuongHiemCo")
    Ok = anhnho("Event/GacLauKhoBau/Ok")
    Go = anhnho("Event/GacLauKhoBau/Go")
    Lua = anhnho("Event/GacLauKhoBau/Lua")

    #ThuongThuogng
    XayDung = anhnho("Event/GacLauKhoBau/XayDung")
    HuanLuyen = anhnho("Event/GacLauKhoBau/HuanLuyen")
    Lua_150 = anhnho("Event/GacLauKhoBau/Lua_150")
    Go_150 = anhnho("Event/GacLauKhoBau/Go_150")
    KL_150 = anhnho("Event/GacLauKhoBau/KL_150")
    Bac_150 = anhnho("Event/GacLauKhoBau/Bac_150")
    MienPhi = anhnho("Event/GacLauKhoBau/MienPhi")

    ThuThapKietXuat = anhnho("Event/ThuThapKietXuat/ThuThapKietXuat")
    CKThuThapKietXuat = anhnho("Event/ThuThapKietXuat/CKThuThapKietXuat")
    YeuCau = anhnho("Event/ThuThapKietXuat/YeuCau")


    # RuongKVK
    VuongQuocManhNhat = anhnho("Event/RuongKVK/VuongQuocManhNhat")
    CK_VuongQuocManhNhat = anhnho("Event/RuongKVK/CK_VuongQuocManhNhat")
    YeuCau_RuongKVK = anhnho("Event/RuongKVK/YeuCau_RuongKVK")
    DaYeuCau_RuongKVK = anhnho("Event/RuongKVK/DaYeuCau_RuongKVK")
    YeuCau_RuongKVK_2 = anhnho("Event/RuongKVK/YeuCau_RuongKVK_2")
    ThuongDiemLienMinh = anhnho("Event/RuongKVK/ThuongDiemLienMinh")

    # KHoBau Bi an
    YeuCau_KhoBauBiAn = anhnho("Event/KhoBauBiAn/YeuCau_KhoBauBiAn")
    CK_KhoBauBiAn = anhnho("Event/KhoBauBiAn/CK_KhoBauBiAn")
    KhoBauBiAn =anhnho("Event/KhoBauBiAn/KhoBauBiAn")

    # DiQuanXamLuoc
    DiQuanXamLuoc = anhnho("Event/DiQuanXamLuoc/DiQuanXamLuoc")
    CK_DiQuanXamLuoc = anhnho("Event/DiQuanXamLuoc/CK_DiQuanXamLuoc")
    ConDoi = anhnho("Event/DiQuanXamLuoc/ConDoi")
    NguoiKhongLo = anhnho("Event/DiQuanXamLuoc/NguoiKhongLo")
    DiTieuDiet = anhnho("Event/DiQuanXamLuoc/DiTieuDiet")
    TapHopTanCong = anhnho("Event/DiQuanXamLuoc/TapHopTanCong")
    OK_TapHop = anhnho("Event/DiQuanXamLuoc/OK_TapHop")
    TapHop = anhnho("Event/DiQuanXamLuoc/TapHop")


class image_Pk_Titan:
    HopThu = anhnho("Pk_Titan/HopThu")
    LienQuan = anhnho("Pk_Titan/LienQuan")
    CK_TroChuyen = anhnho("Pk_Titan/CK_TroChuyen")
    Naia = anhnho("Pk_Titan/Naia")
    Rothai = anhnho("Pk_Titan/Rothai")
    ToiDaPhatDong = anhnho("Pk_Titan/ToiDaPhatDong")
    Rothai_jeb = anhnho("Pk_Titan/Rothai_jeb")




class image_DangNhap: 
    ThanhBenTrong = anhnho("DangNhap/ThanhBenTrong")
    CaiDat = anhnho("DangNhap/CaiDat")
    TaiKhoan = anhnho("DangNhap/TaiKhoan")
    ChuyenDoiTaiKhoan = anhnho("DangNhap/ChuyenDoiTaiKhoan")
    VuiLongNhapDiaChiEmail = anhnho("DangNhap/VuiLongNhapDiaChiEmail")
    DangNhap2 = anhnho("DangNhap/DangNhap2")
    DaDangNhapHopThu = anhnho("DangNhap/DaDangNhapHopThu")
    ThanhBenNgoai = anhnho("DangNhap/ThanhBenNgoai")
    TroLaiDangNhap = anhnho("DangNhap/TroLaiDangNhap")
    


class image_TongQuan:
    Mo_TongQuan = anhnho("TongQuan/Mo_TongQuan")
    NapPhao = anhnho("TongQuan/NapPhao")
    
    Dong_TongQuan = anhnho("TongQuan/Dong_TongQuan")
    CK_TongQuan = anhnho("TongQuan/CK_TongQuan")
    PhaiLamHangNgay = anhnho("TongQuan/PhaiLamHangNgay")
    PhaiLamHangNgay2 = anhnho("TongQuan/PhaiLamHangNgay2")
    DoHang = anhnho("TongQuan/DoHang")
    DenNhaUoc = anhnho("TongQuan/DenNhaUoc")
    DieuTri = anhnho("TongQuan/DieuTri")
    QuanSu = anhnho("TongQuan/QuanSu")
    QuanSu_2 = anhnho("TongQuan/QuanSu_2")
    CongXuong = anhnho("TongQuan/CongXuong")
    CK_CongXuong = anhnho("TongQuan/CK_CongXuong")

    TroGiupLienMinh = anhnho("TongQuan/TroGiupLienMinh")


class image_ThayPhap:
    CK_ThayPhap = anhnho("ThayPhap/CK_ThayPhap")
    OK_LamMoi = anhnho("ThayPhap/OK_LamMoi")

    VaoThayPhap = anhnho("ThayPhap/VaoThayPhap")
    Mua_Lua_1 = anhnho("ThayPhap/Mua_Lua_1")
    Mua_Go_1 = anhnho("ThayPhap/Mua_Go_1")
    Mua_KL_1 = anhnho("ThayPhap/Mua_KL_1")
    Mua_Bac_1 = anhnho("ThayPhap/Mua_Bac_1")
    Mua_Mon_HangQuy = anhnho("ThayPhap/Mua_Mon_HangQuy")
    TiepTucMua = anhnho("ThayPhap/TiepTucMua")
    LamMoi_10Da = anhnho("ThayPhap/LamMoi_10Da")
    LamMoi_20Da = anhnho("ThayPhap/LamMoi_20Da")
    LamMoi_5Da = anhnho("ThayPhap/LamMoi_5Da")
    LamMoi_MienPhi = anhnho("ThayPhap/LamMoi_MienPhi")
    Mua_1Da = anhnho("ThayPhap/Mua_1Da")
    DayLaMonHangQuy_TiepTucLamMoi = anhnho("ThayPhap/DayLaMonHangQuy_TiepTucLamMoi")
    BanKhongDuNguonLuc = anhnho("ThayPhap/BanKhongDuNguonLuc")






class image_DieuTri:
    DieuTri_BenhVien = anhnho("DieuTri/DieuTri_BenhVien")


class image_KickHoat_Vip:
    KickHoatVip = anhnho("BatVip/KickHoatVip")
    TrungTam_KickHoatVip = anhnho("BatVip/TrungTam_KickHoatVip")
    CK_KickHoatVip = anhnho("BatVip/CK_KickHoatVip")
    Vip_30Day = anhnho("BatVip/Vip_30Day")
    Vip_Thuong = anhnho("BatVip/Vip_Thuong")
    SuDung_Vip = anhnho("BatVip/SuDung_Vip")

class image_BenCang:
    BenCang= anhnho("BenCang/BenCang")
    YeuCau_BenCang = anhnho("BenCang/YeuCau_BenCang")
    CK_BenCang = anhnho("BenCang/CK_BenCang")

class image_Qua_DangNhap:
    KhinhKhiCau = anhnho("Qua_DangNhap/KhinhKhiCau")
    DangNhap = anhnho("Qua_DangNhap/DangNhap")
    DangNhap_1 = anhnho("Qua_DangNhap/DangNhap_1")
    YeuCau_DangNhap = anhnho("Qua_DangNhap/YeuCau_DangNhap")
    DaNhan_DangNhap = anhnho("Qua_DangNhap/DaNhan_DangNhap")
    ThangDiemDanh = anhnho("Qua_DangNhap/ThangDiemDanh")
    ThangDiemDanh_DangNhap = anhnho("Qua_DangNhap/ThangDiemDanh_DangNhap")
    CK_TrungTamPhucLoi = anhnho("Qua_DangNhap/CK_TrungTamPhucLoi")
    DaNhan_ThangDiemDanh = anhnho("Qua_DangNhap/DaNhan_ThangDiemDanh")

 
class image_RssTrongThanh:
    Goc_Game = anhnho("RssTrongThanh/Goc_Game")
    NhaMay_Nl = anhnho("RssTrongThanh/NhaMay_Nl")
    NhaMay_Nl2 = anhnho("RssTrongThanh/NhaMay_Nl2")
    CK_NhaMay_NL = anhnho("RssTrongThanh/CK_NhaMay_NL")
    Mo_0 = anhnho("RssTrongThanh/Mo_0")
    Mo_1 = anhnho("RssTrongThanh/Mo_1")
    Mo_2 = anhnho("RssTrongThanh/Mo_2")
    Mo_3 = anhnho("RssTrongThanh/Mo_3")
    Mo_4 = anhnho("RssTrongThanh/Mo_4")
    XayDung = anhnho("RssTrongThanh/XayDung")
    XayDung2 = anhnho("RssTrongThanh/XayDung2")
    CK_Xong4Mo = anhnho("RssTrongThanh/CK_Xong4Mo")

class image_SkillLanhChua:
    MoSach = anhnho("SkillLanhChua/MoSach")
    CK_KyNangLanhChua = anhnho("SkillLanhChua/CK_KyNangLanhChua")
    KyNangLanhChua = anhnho("SkillLanhChua/KyNangLanhChua")
    Skill_MuaGat = anhnho("SkillLanhChua/Skill_MuaGat")
    Skill_ThuThap = anhnho("SkillLanhChua/Skill_ThuThap")
    SuDung_Skill = anhnho("SkillLanhChua/SuDung_Skill")

    ThuThap_DangNguoi = anhnho("SkillLanhChua/ThuThap_DangNguoi")
    ThuThap_DangduyTri = anhnho("SkillLanhChua/ThuThap_DangduyTri")
    Tang_SanLuong_DangNguoi = anhnho("SkillLanhChua/Tang_SanLuong_DangNguoi")

class image_UocFree:
    CK_VaoNhaUoc = anhnho("UocFree/CK_VaoNhaUoc")
    VaoUoc = anhnho("UocFree/VaoUoc")
    CK_TangBaoTri = anhnho("UocFree/CK_TangBaoTri")
    UocThep = anhnho("UocFree/UocThep")
    DungDaQuy = anhnho("UocFree/DungDaQuy")



class image_DiAnMo:
    ChuyenThanh = anhnho("CloseQuangCao/ChuyenThanh")
    Find_Rss = anhnho("DiAnMo/Find_Rss")
    Find_Lua = anhnho("DiAnMo/Find_Lua")
    Find_Go = anhnho("DiAnMo/Find_Go")
    Find_Bac = anhnho("DiAnMo/Find_Bac")
    Find_KimLoai = anhnho("DiAnMo/Find_KimLoai")
    Find_Di = anhnho("DiAnMo/Find_Di")
    Find_Tang_LV = anhnho("DiAnMo/Find_Tang_LV")
    Find_Giam_LV = anhnho("DiAnMo/Find_Giam_LV")
    Find_Cap1 = anhnho("DiAnMo/Find_Cap1")
    Find_Cap2 = anhnho("DiAnMo/Find_Cap2")
    Find_Cap3 = anhnho("DiAnMo/Find_Cap3")
    Find_Cap4 = anhnho("DiAnMo/Find_Cap4")
    Find_Cap5 = anhnho("DiAnMo/Find_Cap5")
    Find_Cap6 = anhnho("DiAnMo/Find_Cap6")
    Find_Cap7 = anhnho("DiAnMo/Find_Cap7")
    chiem_x1 = anhnho("DianMo/chiem_x1")
    chiem_Goc = anhnho("DianMo/chiem_Goc")
    MucTieuTren200m = anhnho("DianMo/MucTieuTren200m")
    CK_Mo_CoRSS = anhnho("DianMo/CK_Mo_CoRSS")




class image_XuatBinh:
    TapHop = anhnho("XuatBinh/TapHop") # Titan
    XuatBinh_TapHop = anhnho("XuatBinh/XuatBinh_TapHop") #Titan
    BanChiCoThe = anhnho("XuatBinh/BanChiCoThe")
    CK_XuatBinh = anhnho("XuatBinh/CK_XuatBinh")
    CK_CoLinh = anhnho("XuatBinh/CK_CoLinh")
    CK_CoLinh2 = anhnho("XuatBinh/CK_CoLinh2")
    GiaoTranh_Mo = anhnho("XuatBinh/GiaoTranh_Mo")
    XuatBinh = anhnho("XuatBinh/XuatBinh")
    HetLinh = anhnho("XuatBinh/HetLinh")
    ShowQuanDoi = anhnho("XuatBinh/ShowQuanDoi")
    Dao_3 = anhnho("XuatBinh/Dao_3")
    Dao_4 = anhnho("XuatBinh/Dao_4")
    Dao_5 = anhnho("XuatBinh/Dao_5")
    Dao_6 = anhnho("XuatBinh/Dao_6")
    XuatQua6Doi = anhnho("XuatBinh/XuatQua6Doi")
    TroThanhVip10 = anhnho("XuatBinh/TroThanhVip10")




class image_ThuongThanhPho:
    SuDung_BuaNguonLuc = anhnho("ThuongThanhPho/SuDung_BuaNguonLuc")
    TongHop = anhnho("ThuongThanhPho/TongHop")
    BuaChuNguonLuc = anhnho("ThuongThanhPho/BuaChuNguonLuc")
    CK_ThuongThanhPho = anhnho("ThuongThanhPho/CK_ThuongThanhPho")
    CK_BuaChuNguonLuc = anhnho("ThuongThanhPho/CK_BuaChuNguonLuc")
    SuDung_BuaNguonLuc = anhnho("ThuongThanhPho/SuDung_BuaNguonLuc")
    CheckBua = anhnho("ThuongThanhPho/CheckBua")

    # Sử Dụng Khiên

    CaiKhien = anhnho("ThuongThanhPho/CaiKhien")
    CK_Cai_Khien = anhnho("ThuongThanhPho/CK_Cai_Khien")
    SuDung3Day = anhnho("ThuongThanhPho/SuDung3Day")
    SuDung24h = anhnho("ThuongThanhPho/SuDung24h")
    SuDung8h = anhnho("ThuongThanhPho/SuDung8h")
    Cong_Don_Khien = anhnho("ThuongThanhPho/Cong_Don_Khien")
    Mua_Da_Quy_3_Day = anhnho("ThuongThanhPho/Mua_Da_Quy_3_Day")
    Mua_Da_Quy_24h = anhnho("ThuongThanhPho/Mua_Da_Quy_24h")
    Mua_Da_Quy_8h = anhnho("ThuongThanhPho/Mua_Da_Quy_8h")
    Het_Da_Quy = anhnho("ThuongThanhPho/Het_Da_Quy")
    CK_ConKhien25 = anhnho("ThuongThanhPho/CK_ConKhien25")
    CK_ConKhien50 = anhnho("ThuongThanhPho/CK_ConKhien50")



class image_CongHienDao:
    LienMinh = anhnho("CongHienDao/LienMinh")
    QuanLy = anhnho("CongHienDao/QuanLy")
    ThoatLienMinh = anhnho("CongHienDao/ThoatLienMinh")
    O_Nhap_Ten = anhnho("CongHienDao/O_Nhap_Ten")
    ThamGia = anhnho("CongHienDao/ThamGia")
    ChiaSe_GiaNhapLM = anhnho("CongHienDao/ChiaSe_GiaNhapLM")
    XinGiaNhap = anhnho("CongHienDao/XinGiaNhap")
    ThoatLienMinh2 = anhnho("CongHienDao/ThoatLienMinh2")
    Ok_Thoat = anhnho("CongHienDao/Ok_Thoat")
    Ck_NapBom = anhnho("CongHienDao/Ck_NapBom")
    Nap_DaQuy = anhnho("CongHienDao/Nap_DaQuy")
    NapXong = anhnho("CongHienDao/NapXong")
    NapHet20= anhnho("CongHienDao/NapHet20")

class image_TaiThiet:
    TrangBi1 = anhnho("TaiThiet/TrangBi1")
    ThamLoRen = anhnho("TaiThiet/ThamLoRen")
    CK_TrangBi = anhnho("TaiThiet/CK_TrangBi")
    TaiThiet = anhnho("TaiThiet/TaiThiet")
    CK_TaiThiet = anhnho("TaiThiet/CK_TaiThiet")
    CK_TrangSuc = anhnho("TaiThiet/CK_TrangSuc")
    Cai_DatLai = anhnho("TaiThiet/Cai_DatLai")
    HetDa_TaiThiet = anhnho("TaiThiet/HetDa_TaiThiet")
    CaiDatMienPhi = anhnho("TaiThiet/CaiDatMienPhi")

class image_HienTangLienMinh:
    HienTangLienMinh = anhnho("HienTangLienMinh/HienTangLienMinh")
    CK_KyThuatLienMinh = anhnho("HienTangLienMinh/CK_KyThuatLienMinh")
    Cap = anhnho("HienTangLienMinh/Cap")
    DeNghi = anhnho("HienTangLienMinh/DeNghi")
    CK_Close_Tang = anhnho("HienTangLienMinh/CK_Close_Tang")
    CongHien_Go1 = anhnho("HienTangLienMinh/CongHien_Go1")
    CongHien_Go2 = anhnho("HienTangLienMinh/CongHien_Go2")
    CongHien_Go3 = anhnho("HienTangLienMinh/CongHien_Go3")
    CongHien_Lua1 = anhnho("HienTangLienMinh/CongHien_Lua1")
    CongHien_Lua2 = anhnho("HienTangLienMinh/CongHien_Lua2")
    CongHien_Lua3 = anhnho("HienTangLienMinh/CongHien_Lua3")
    CongHienXong = anhnho("HienTangLienMinh/CongHienXong")
    GiaNhapLienMinh = anhnho("HienTangLienMinh/GiaNhapLienMinh")
    TangFull = anhnho("HienTangLienMinh/TangFull")

class image_KhoTang_TTrong:
    NhaEvent = anhnho("KhoTang/NhaEvent")
    KhoTang = anhnho("KhoTang/KhoTang")
    KhoTang2 = anhnho("KhoTang/KhoTang2")
    CK_KhoTang = anhnho("KhoTang/CK_KhoTang")
    MienPhi = anhnho("KhoTang/MienPhi")
    CK_Quay_KhoTang = anhnho("KhoTang/CK_Quay_KhoTang")
    KhanCap_MienPhi = anhnho("KhoTang/KhanCap_MienPhi")
    KetThuc = anhnho("KhoTang/KetThuc")
    KhanCap10 = anhnho("KhoTang/KhanCap10")
    Da_Choi_KhoTang = anhnho("KhoTang/Da_Choi_KhoTang")
    DuoiVip6 = anhnho("KhoTang/DuoiVip6")

    # Thử Thách Tồng
    NhaEvent_2 = anhnho("KhoTang/NhaEvent_2")
    CK_Vao_ThuThachRong= anhnho("KhoTang/CK_Vao_ThuThachRong")
    OK_CheDoNhanh = anhnho("KhoTang/OK_CheDoNhanh")
    ThuThachRong = anhnho("KhoTang/ThuThachRong")
    Close_CheDoNhanh = anhnho("KhoTang/Close_CheDoNhanh")
    CK_ThuThachRong = anhnho("KhoTang/CK_ThuThachRong")
    CheDoNhanh = anhnho("KhoTang/CheDoNhanh")




@lru_cache
class image_close_QuangCao:
    print("Load Data QC")
    TroGiupLienMinh = anhnho("CloseQuangCao/TroGiupLienMinh")
    TranhDoatTp=anhnho("CloseQuangCao/TranhDoatTp")
    TranhDoat_Tp2 = anhnho("CloseQuangCao/TranhDoat_Tp2")
    TranhDoat_Tp3 = anhnho("CloseQuangCao/TranhDoat_Tp3")
    TranhDoat_Tp4 = anhnho("CloseQuangCao/TranhDoat_Tp4")
    TranhDoat_Tp5 = anhnho("CloseQuangCao/TranhDoat_Tp5")

    Keyblack=anhnho("CloseQuangCao/Keyblack")
    Keyblack2=anhnho("CloseQuangCao/Keyblack2")

    NgayMayMan = anhnho("CloseQuangCao/NgayMayMan")
    Loi_Mang = anhnho("CloseQuangCao/Loi_Mang")
    Oops_ThuLai = anhnho("CloseQuangCao/Oops_ThuLai")
    Oops_ThuLai2 = anhnho("CloseQuangCao/Oops_ThuLai2")
    ThoatGame = anhnho("CloseQuangCao/ThoatGame")
    Open_game= anhnho("CloseQuangCao/Open_game")
    Close_1 = anhnho("CloseQuangCao/Close_1")
    Opps_Het_Time_DangNhap = anhnho("CloseQuangCao/Opps_Het_Time_DangNhap")
    TrungTamPhucLoi = anhnho("CloseQuangCao/TrungTamPhucLoi")
    NapTien = anhnho("CloseQuangCao/NapTien")
    Wellcome_game = anhnho("CloseQuangCao/Wellcome_game")
    Onemt = anhnho("CloseQuangCao/Onemt")
    HetDaQuy = anhnho("CloseQuangCao/HetDaQuy")
    DangNhapNoiKhac = anhnho("CloseQuangCao/DangNhapNoiKhac")
    Qc_VuongQuoc = anhnho("CloseQuangCao/Qc_VuongQuoc")


    #CK_NgayMayMan
    CK_NgayMayMan_HocVien = anhnho("CloseQuangCao/CK_NgayMayMan_HocVien")
    CK_NgayMayMan_NangCap = anhnho("CloseQuangCao/CK_NgayMayMan_NangCap")
    CK_NgayMayMan_HuanLuyen = anhnho("CloseQuangCao/CK_NgayMayMan_HuanLuyen")

    ChieuMoChiaSeLienMinh = anhnho("CloseQuangCao/ChieuMoChiaSeLienMinh")


class image_Gomrss:
    DanhDau = anhnho("GomRss/DanhDau")
    CK_DanhDau = anhnho("GomRss/CK_DanhDau")
    TanCong = anhnho("GomRss/TanCong")



class image_HopThu:
    Thu = anhnho("HopThu/Thu")
    CK_Thu = anhnho("HopThu/CK_Thu")
    DA_DocDongLoat = anhnho("HopThu/DA_DocDongLoat")
    Tn_HeThong = anhnho("HopThu/Tn_HeThong")
    Tn_LienMinh = anhnho("HopThu/Tn_LienMinh")
    Tn_DaiHoi = anhnho("HopThu/Tn_DaiHoi")
    Tn_ThongBao = anhnho("HopThu/Tn_ThongBao")


class image_GuiDaQuy:
    GuiDaQuy = anhnho("GuiDaQuy/GuiDaQuy")
    Gui3Ngay = anhnho("GuiDaQuy/Gui3Ngay")
    Gui_DaQuy2 = anhnho("GuiDaQuy/Gui_DaQuy2")
    RutKhongLoiTuc = anhnho("GuiDaQuy/RutKhongLoiTuc")
    XacNhanRut = anhnho("GuiDaQuy/XacNhanRut")
    CK_NganHang = anhnho("GuiDaQuy/CK_NganHang")
    Rut_Da_Quy = anhnho("GuiDaQuy/Rut_Da_Quy")
    TrongCung1ThoiGian = anhnho("GuiDaQuy/TrongCung1ThoiGian")


class image_NangCapAnhHung:
    AnhHung = anhnho("NangCapAnhHung/AnhHung")
    TongQuan_AnhHung = anhnho("NangCapAnhHung/TongQuan_AnhHung")
    NangCap = anhnho("NangCapAnhHung/NangCap")


    NangCap = anhnho("NangCApAnhHung/NangCap")
    KinhNghiem300 = anhnho("NangCapAnhHung/KinhNghiem300")
    ChiTietAnhHung = anhnho("NangCapAnhHung/ChiTietAnhHung")
    CK_KyNangAnhHung = anhnho("NangCapAnhHung/CK_KyNangAnhHung")


class image_ChieuMoAnhHung:
    VaoChieuMoAnhHung = anhnho("ChieuMoAnhHung/VaoChieuMoAnhHung")
    CK_ChieuMoAnhHung = anhnho("ChieuMoAnhHung/CK_ChieuMoAnhHung")
    MienPhi_Thuong = anhnho("ChieuMoAnhHung/MienPhi_Thuong")
    MienPhi_Vang = anhnho("ChieuMoAnhHung/MienPhi_Vang")
    Ok_ChieuMoXong = anhnho("ChieuMoAnhHung/Ok_ChieuMoXong")
    OK_RaAnhHung = anhnho("ChieuMoAnhHung/OK_RaAnhHung")


class Cap_QuaiKVK:

    Cap1 = 94
    Cap2 = 97
    Cap3 = 102
    Cap4 = 105
    Cap5 = 110
    Cap6 = 113
    Cap7 = 118
    Cap8 = 121
    Cap9 = 125
    Cap10 = 130

    Cap11 = 133
    Cap12 = 138
    Cap13 = 141
    Cap14 = 146
    Cap15 = 149
    Cap16 = 154
    Cap17 = 158
    Cap18 = 162
    Cap19 = 166
    Cap20 = 169

    Cap21 = 174
    Cap22 = 177
    Cap23 = 182
    Cap24 = 185
    Cap25 = 190
    Cap26 = 195
    Cap27 = 198
    Cap28 = 202
    Cap29 = 206
    Cap30 = 210

    Cap31 = 213
    Cap32 = 218
    Cap33 = 223
    Cap34 = 226
    Cap35 = 231
    Cap36 = 234
    Cap37 = 239
    Cap38 = 242
    Cap39 = 246
    Cap40 = 251


class Cap_QuaiTitan:
    Cap_26 = 94
    Cap_27 = 105
    Cap_28 = 116
    Cap_29 = 127
    Cap_30 = 138

    Cap_31 = 149
    Cap_32 = 160
    Cap_33 = 173
    Cap_34 = 184
    Cap_35 = 195
    Cap_36 = 206
    Cap_37 = 217
    Cap_38 = 228
    Cap_39 = 239
    Cap_40 = 251

class image_KhoangCach_Quai:

    KC_1x = anhnho("DAnhQuai/KhoangCach/KC_1x")
    KC_2x = anhnho("DAnhQuai/KhoangCach/KC_2x")
    KC_3x = anhnho("DAnhQuai/KhoangCach/KC_3x")
    KC_4x = anhnho("DAnhQuai/KhoangCach/KC_4x")
    KC_5x = anhnho("DAnhQuai/KhoangCach/KC_5x")
    KC_6x = anhnho("DAnhQuai/KhoangCach/KC_6x")
    KC_7x = anhnho("DAnhQuai/KhoangCach/KC_7x")
    KC_8x = anhnho("DAnhQuai/KhoangCach/KC_8x")
    KC_9x = anhnho("DAnhQuai/KhoangCach/KC_9x")
    KC_1xx = anhnho("DAnhQuai/KhoangCach/KC_1xx")


    KC_x0 = anhnho("DAnhQuai/KhoangCach/KC_x0")
    KC_x1 = anhnho("DAnhQuai/KhoangCach/KC_x1")
    KC_x2 = anhnho("DAnhQuai/KhoangCach/KC_x2")
    KC_x3 = anhnho("DAnhQuai/KhoangCach/KC_x3")
    KC_x4 = anhnho("DAnhQuai/KhoangCach/KC_x4")
    KC_x5 = anhnho("DAnhQuai/KhoangCach/KC_x5")
    KC_x6 = anhnho("DAnhQuai/KhoangCach/KC_x6")
    KC_x7 = anhnho("DAnhQuai/KhoangCach/KC_x7")
    KC_x8 = anhnho("DAnhQuai/KhoangCach/KC_x8")
    KC_x9 = anhnho("DAnhQuai/KhoangCach/KC_x9")

    KC_0 = anhnho("DAnhQuai/KhoangCach/KC_0")
    KC_1 = anhnho("DAnhQuai/KhoangCach/KC_1")
    KC_2 = anhnho("DAnhQuai/KhoangCach/KC_2")
    KC_3 = anhnho("DAnhQuai/KhoangCach/KC_3")
    KC_4 = anhnho("DAnhQuai/KhoangCach/KC_4")
    KC_5 = anhnho("DAnhQuai/KhoangCach/KC_5")
    KC_6 = anhnho("DAnhQuai/KhoangCach/KC_6")
    KC_7 = anhnho("DAnhQuai/KhoangCach/KC_7")
    KC_8 = anhnho("DAnhQuai/KhoangCach/KC_8")
    KC_9 = anhnho("DAnhQuai/KhoangCach/KC_9")


class image_LienMinh:
    # Vao Lien Minh
    VaoLienMinh = anhnho("LienMinh/VaoLienMinh")
    CK_LienMinh = anhnho("LienMinh/CK_LienMinh")
    GiaNhapLienMinh = anhnho("LienMinh/GiaNhapLienMinh")

    # Qua Thanh Dia Lien Minh
    ThanhDiaLienMinh = anhnho("LienMinh/ThanhDiaLienMinh")
    LinhToanBo = anhnho("LienMinh/LinhToanBo")
    
    # Qua Hoat Dong Lien Lien Minh
    HoatDongLienMinh = anhnho("LienMinh/HoatDongLienMinh")
    CK_HoatDongLienMinh = anhnho("LienMinh/CK_HoatDongLienMinh")
    BangXepHangHomQua = anhnho("LienMinh/BangXepHangHomQua")
    NhanDuocHoatDong = anhnho("LienMinh/NhanDuocHoatDong")
    YeuCau_HoatDongLienMinh = anhnho("LienMinh/YeuCau_HoatDongLienMinh")

    # Titan
    LienQuan = anhnho("LienMinh/Titan/LienQuan")


    

    




class image_DanhQuai:
    TanCong = anhnho("DanhQuai/TanCong")
    Dao2 = anhnho("DanhQuai/Dao2")
    Dao3 = anhnho("DanhQuai/Dao3")
    Dao4 = anhnho("DanhQuai/Dao4")
    Dao5 = anhnho("DanhQuai/Dao5")
    CK_XuatBinh = anhnho("DanhQuai/CK_XuatBinh")
    XuatBinh = anhnho("DanhQuai/XuatBinh")
    CK_CoLinh = anhnho("DanhQuai/CK_CoLinh")
    ChonQuai = anhnho("DanhQuai/ChonQuai")
    DaXuat_6Dao = anhnho("DanhQuai/DaXuat_6Dao")
    # Linh Dang DiHoac Ve
    Linh_DangVe = anhnho("DanhQuai/Linh_DangVe")
    Linh_TangToc = anhnho("DanhQuai/Linh_TangToc")

    #Titan
    ChonQuai_Titan = anhnho("DanhQuai/Titan/ChonQuai_Titan")