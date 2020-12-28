# coding=gbk
#from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import time
import tkinter.font as tkFont
import threading

class welcome():
    def __init__(self,masteroot=None):
        if(masteroot==None):
            self.hideroot= tk.Tk()
            self.hideroot.withdraw()
        else:
            self.hideroot=masteroot
        self.root = tk.Toplevel(master=masteroot)#Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.closeWelcome)


    def show_img(self):
        if (self.root != None):
            if os.path.exists('./云监控.png'):
                #print("Lib/img exist")
                bm = tk.PhotoImage(file='./云监控.png')
                width = bm.width()
                height = bm.height()
                #bm=bm.subsample(2,2)
                screenwidth = self.root.winfo_screenwidth()
                screenheight = self.root.winfo_screenheight()
                alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                self.root.overrideredirect(True)
                self.root.attributes("-alpha", 1)  # 窗口透明度（1为不透明，0为全透明）
                self.root.geometry(alignstr)
                lb_welcomelogo = tk.Label(self.root, image=bm, bg='black')
                #lb_welcomelogo.bm = bm
                lb_welcomelogo.place(x=0, y=0, )
                # bm_load = PhotoImage(file='./loading.gif')
                # lb_loading = Label(root, image=bm_load, bg='black')
                # lb_loading.bm = bm_load
                # lb_loading.place(x=0, y=0, )
        t1 = threading.Thread(target=self.closeWelcome)
        t1.setDaemon(True)
        t1.start()
        self.root.mainloop()



    def closeWelcome(self):
        # 设置欢迎页停留时间
        time.sleep(2)
        for i in range(50):
            self.root.attributes("-alpha", 1 - 0.02 * i)  # 窗口透明度
            time.sleep(0.02)
        # global rootMSCT
        self.root.destroy()
        self.hideroot.destroy()
        # rootMSCT.destroy()
        #print("roots destroyed")

if __name__ == '__main__':

    w=welcome()
    w.show_img()
    print("welcome finished")
    #ideroot = tk.Tk()
    #ideroot.withdraw()
    #ideroot.mainloop()

    #hideroot.mainloop()
#    hideroot.destroy()

    #mains.root.mainloop()
    #print('tk quit')
#global root,rootMSCT
#rootMSCT= Tk()  #创建应用程序主窗口
#rootMSCT.title("welcome v1.0")
#rootMSCT.attributes("-alpha", 0) #透明状态下加载主程序
#rootMSCT.withdraw()

#创建欢迎界面窗口
#root = Tk()#Toplevel(rootMSCT)
'''

#tMain=threading.Thread(target=showWelcome)
#tMain.start()
#showWelcome(root)
#closeWelcome(root)
#tMain.join()

def showWelcome(root):
    # 设置窗口大小不可改变
    #root.resizable(width=False, height=False)
    #root['bg']='black'
    #插入欢迎图片，可以是logo
    if os.path.exists('./云监控.png'):
        print("Lib/img exist")
        bm = PhotoImage(file = './云监控.png')
        width = bm.width()
        height = bm.height()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        print(screenwidth,screenheight)
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        #root.overrideredirect(True)
        root.attributes("-alpha", 1)  # 窗口透明度（1为不透明，0为全透明）
        root.geometry(alignstr)
        #lb_welcomelogo = Label(root, image = bm,bg='black')
        #lb_welcomelogo.bm = bm
        #lb_welcomelogo.place(x=0, y=0,)
        #bm_load = PhotoImage(file='./loading.gif')
        #lb_loading = Label(root, image=bm_load, bg='black')
        #lb_loading.bm = bm_load
        #lb_loading.place(x=0, y=0, )

    #插入文字，可以显示开发者或出处
        #lb_welcometext = Label(root, text = '欢迎使用分布式智能云监控系统',
        #     fg='lightgray',bg='black',font=('华文隶书', 25))
        #lb_welcometext.place(x=int((width-475)/2), y=height-150,width=475,height=100)

t1=threading.Thread(target=closeWelcome)
t1.start()
'''
#主窗口程序代码
'''
#root.mainloop()
#rootMSCT.mainloop()
'''


