import time
import cv2
import numpy as np
import _controller
import win32gui,win32api,win32ui,win32con



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

# Picture path
def get():
  img =  chupanh()
  height, width = img.shape[:2]

  a = []
  b = []
  

  def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
      if event == cv2.EVENT_LBUTTONDOWN:
          xy = "%d,%d" % (x, y)
          a.append(x)
          b.append(y)
          color_ = img[y,x]
          
        #  cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        #  cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
      #               1.0, (0, 0, 0), thickness=1)
      #   cv2.imshow("image", img)

          print(x,y)
          print("color_",color_)
  
  
  cv2.namedWindow("image")
  cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
  cv2.imshow("image", img)
  cv2.waitKey(0)


get()


