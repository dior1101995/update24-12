import subprocess

import win32api
import win32con
import win32gui

DETACHED_PROCESS = 0x00000008

class controller:
    '''Các Chức Năng Điều Khiển Chính'''
    c_name = None
    c_id_device = None

    def __init__(self):
        self.hwnd = win32gui.FindWindow(None, self.c_name)
        # if not self.hwnd:
        #     raise Exception('Window not found: {}'.format(self.c_name))

    def Swipe(self, toado):
        adb_command = f'adb -s {self.c_id_device} shell input swipe {toado} 300'
        subprocess.call(adb_command, creationflags=DETACHED_PROCESS)


    def KeyEvent(self, key):
        '''Send Key event'''
        adb_command = f'adb -s {self.c_id_device} shell input keyevent {key}'
        subprocess.call(adb_command, creationflags=DETACHED_PROCESS)




    def SendText(self, Text):
        adb_command = f'adb -s {self.c_id_device} shell input text {Text}'
        subprocess.call(adb_command, creationflags=DETACHED_PROCESS)




    def Click(self, x, y):
        lParam = win32api.MAKELONG(x, y)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)


    def ResetGame(self):
        # lay tengame  adb Shell dumpsys window windows | find "mCurrentFocus"
        print("reset game")
        adb_command = 'adb -s %s shell am force-stop com.and.riseofthekings' % (self.c_id_device)
        subprocess.call(adb_command, creationflags=DETACHED_PROCESS)

    # adb_command = 'adb -s %s shell am start -n com.and.riseofthekings/org.cocos2dx.lua.AppActivity' % (self.c_id_device)

    # subprocess.call(adb_command, creationflags=DETACHED_PROCESS)


