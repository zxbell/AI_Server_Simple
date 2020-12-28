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
            if os.path.exists('./�Ƽ��.png'):
                #print("Lib/img exist")
                bm = tk.PhotoImage(file='./�Ƽ��.png')
                width = bm.width()
                height = bm.height()
                #bm=bm.subsample(2,2)
                screenwidth = self.root.winfo_screenwidth()
                screenheight = self.root.winfo_screenheight()
                alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
                self.root.overrideredirect(True)
                self.root.attributes("-alpha", 1)  # ����͸���ȣ�1Ϊ��͸����0Ϊȫ͸����
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
        # ���û�ӭҳͣ��ʱ��
        time.sleep(2)
        for i in range(50):
            self.root.attributes("-alpha", 1 - 0.02 * i)  # ����͸����
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
#rootMSCT= Tk()  #����Ӧ�ó���������
#rootMSCT.title("welcome v1.0")
#rootMSCT.attributes("-alpha", 0) #͸��״̬�¼���������
#rootMSCT.withdraw()

#������ӭ���洰��
#root = Tk()#Toplevel(rootMSCT)
'''

#tMain=threading.Thread(target=showWelcome)
#tMain.start()
#showWelcome(root)
#closeWelcome(root)
#tMain.join()

def showWelcome(root):
    # ���ô��ڴ�С���ɸı�
    #root.resizable(width=False, height=False)
    #root['bg']='black'
    #���뻶ӭͼƬ��������logo
    if os.path.exists('./�Ƽ��.png'):
        print("Lib/img exist")
        bm = PhotoImage(file = './�Ƽ��.png')
        width = bm.width()
        height = bm.height()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        print(screenwidth,screenheight)
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        #root.overrideredirect(True)
        root.attributes("-alpha", 1)  # ����͸���ȣ�1Ϊ��͸����0Ϊȫ͸����
        root.geometry(alignstr)
        #lb_welcomelogo = Label(root, image = bm,bg='black')
        #lb_welcomelogo.bm = bm
        #lb_welcomelogo.place(x=0, y=0,)
        #bm_load = PhotoImage(file='./loading.gif')
        #lb_loading = Label(root, image=bm_load, bg='black')
        #lb_loading.bm = bm_load
        #lb_loading.place(x=0, y=0, )

    #�������֣�������ʾ�����߻����
        #lb_welcometext = Label(root, text = '��ӭʹ�÷ֲ�ʽ�����Ƽ��ϵͳ',
        #     fg='lightgray',bg='black',font=('��������', 25))
        #lb_welcometext.place(x=int((width-475)/2), y=height-150,width=475,height=100)

t1=threading.Thread(target=closeWelcome)
t1.start()
'''
#�����ڳ������
'''
#root.mainloop()
#rootMSCT.mainloop()
'''


