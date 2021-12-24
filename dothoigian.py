import cv2
import _controller
from _controller import *
import numpy as np
import win32gui,win32ui

import numpy as np



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

def laytoado(anhto,duongdan,tenanh):
    f1 = open(f'New_Data/{duongdan}/{tenanh}.txt ', "r" )
    toado1 = f1.readline()
    f1.close()
 
    
    template = cv2.imread(f'New_Data/{duongdan}/{tenanh}.png', 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(anhto,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9

    loc = np.where(res >= threshold)
    (minVal, maxVal, minLoc, (x , y) ) = cv2.minMaxLoc(res)
 
    toadoanh = ("%s, %s") % (x, y)
 
  
    if toadoanh ==   toado1 :
        print( f"Khop Anh,{x},{y}==[{toado1}]")
        for pt in zip(*loc[::-1]):
            cv2.rectangle(anhto, pt, (pt[0] + w, pt[1] + h), (1,255,255), 4)
        

        cv2.imshow('Detected',anhto)
        cv2.waitKey(0)


       
    if toadoanh !=   toado1 :
        print(f"Sai Khac [{x},{y}]---[{toado1}]")
        for pt in zip(*loc[::-1]):
            cv2.rectangle(anhto, pt, (pt[0] + w, pt[1] + h), (1,255,255), 6)


 

        cv2.imshow('Detected',anhto)
        cv2.waitKey(0)




 


laytoado(anhto,"CloseQuangCao","Keyblack2")

    

