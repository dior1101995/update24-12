from time import gmtime, strftime
import time

from datetime import datetime

# đối tượng datetime chứa ngày và giờ hiện tại
# viết bởi Quantrimang.com
now = datetime.now()


# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")


# while 1:


# Mở Auto
# so sánh ngày hiện tại với lần đóng cuối cùng
#nếu ngày hiện tại > ngày đóngcuối cùng => true Tiếp Tục
# nếu ngày hiện tại <ngày cuối cùng => False


# đóng lúc 12.32.10.22.2021
#mỏ lên lúc 12.33.10.22.2021


def dong():

    with open('Time_Dong.txt', 'w+') as FileLic:
        FileLic.write(dt_string)

# Mở:
with open('Time_Dong.txt', 'r') as FileLic:
    Doc_Licence = FileLic.read()



print("sadasd")

Thoigiandong = datetime.strptime(Doc_Licence,'%d/%m/%Y %H:%M:%S')

print("Đóng Lúc :", Thoigiandong,"Mở Lúc :",now)


if Thoigiandong < now:
    print("True", "Đóng Lúc :", Thoigiandong, "Mở Lúc",now)



else:
    print("Lỗi Kiêm Tra Ngày Giờ")
