import cv2
from numpy.core.fromnumeric import ptp
import _controller
from _controller import *
import numpy as np
import cv2

import numpy as np

DEBUG = True

#_controller.nox_name= "MainAcc"
#Window_Name = Window_Name()
#Window_Name.start()

import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2
from ctypes import windll


import cv2 as cv
import os
import subprocess
import time
id_device='127.0.0.1:62027'

def adb_click(coord_x,coord_y):
    adb_command='adb -s %s shell input tap %s %s'%(id_device,coord_x,coord_y)
    subprocess.call(adb_command)
def adb_send_text(text):
    adb_command='adb -s %s shell input text %s'%(id_device,text)
    subprocess.call(adb_command)

def click(x, y):
    hwnd = win32gui.FindWindow(None, '')
    lParam = win32api.MAKELONG(x, y + 35)

    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

def chupanh():
    # get the window image data
    try:
        hwnd = win32gui.FindWindow(None, 'MainAcc')
        (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bottom - top
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        if cDC == 0:
            print('saveDC = ', cDC)
            return None
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)


        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (h, w,4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = img[:, :, ::3].copy()



        img = np.ascontiguousarray(img)

        return img
    except:
        print('Exception')
        return None



anhto = chupanh()


a= "CK_CoLinh"
b = "KEy_KyBinh"
c ="Key_CungThu"
global tenanh,duongdan
tenanh = "TiepTeNguonLuc"
duongdan = "VienTroTaiNguyen"

cropping = False
x_start, y_start, x_end, y_end = 0, 0, 0, 0
image = anhto
#oriImage = image.copy()
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
        refPoint = [(x_start, y_start), (x_end, y_end)]
        if len(refPoint) == 2: #when two points were found
            roi = anhto[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            cv2.imwrite(f'New_Data/{duongdan}/{tenanh}.png', roi)
            print("tim")
            template = cv2.imread(f'New_Data/{duongdan}/{tenanh}.png', 0)
            w, h = template.shape[::-1]
            while 1:
                print(".....")

                res = cv2.matchTemplate(anhto, template, cv2.TM_CCOEFF_NORMED)
                (minVal, maxVal, minLoc, (x, y)) = cv2.minMaxLoc(res)
                if maxVal >= 0.925:


                    print(x,y)
                    f = open(f"New_Data/{duongdan}/{tenanh}.txt",'w')
                    f.write(f"{x}, {y}")
                    f.close()
                    break
                time.sleep(0.1)

                

cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
while True:

    i  = image.copy()

    if not cropping:
        cv2.imshow("image", i)
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
    cv2.waitKey(1)


# close all open windows
cv2.destroyAllWindows()

