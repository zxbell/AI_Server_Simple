from showwelcome import welcome
import tkinter
import tkinter as tk
from tkinter import *
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import threading
class main_ui:
    '''
    主窗口界面设计
    菜单：
    文件          视图          配置          工具          帮助
    |——保存       |——精简       |——网络       |——打包       |——帮助
    |——载入       |——详细       |——搜索       |——备份       |——关于
    |——退出                    |——参数       |——上传
    工具：
    |——保存 载入 视图 配置 上传
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("分布式智能监控系统")
        self.root.protocol('WM_DELETE_WINDOW', self.closeWindow)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        self.loading_finished = False
        alignstr = '%dx%d+%d+%d' % (screenwidth, screenheight, 0, 0)
        self.root.geometry(alignstr)
        self.factory_frame = tk.Frame(self.root, relief='ridge')
        self.canvas = tkinter.Canvas(self.factory_frame, bg='green', height=800, width=900)
        self.camera_label = tk.Label(self.root)
        self.text_log = StringVar(self.root)
        self.text_log.set("系统初始化完成\n")
        self.text_label = tk.Label(self.root, textvariable=self.text_log, relief='ridge', anchor='nw', bg='#F7F7F7')
        self.VScroll3 = tkinter.Scrollbar(self.text_label, orient='vertical', command='')
        self.VScroll4 = tkinter.Scrollbar(self.text_label, orient='horizontal', command='')

        self.lock = [threading.RLock(), threading.RLock(), threading.RLock()]
        self.video_ready = [False, False, False]
        self.video_enable = [False, False, False]
        self.img = [None, None, None]
        self.img_bak = [None, None, None]
        self.counter = 0
        self.cam_loop = False
        self.process_loop_camera = None
        self.img_video_offline = cv2.imread("offline.jpg", cv2.IMREAD_UNCHANGED)  # 不支持中文
        self.img_video_offline_streched=None

        self.loading_finished = True



    def ui_menu(self):
        # 创建一个顶级菜单
        menubar = tk.Menu(self.root)

        # 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="打开配置", command=None)
        filemenu.add_command(label="保存配置", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="开始监控", command=self.callback_start_monitor)
        filemenu.add_command(label="停止监控", command=self.callback_stop_monitor)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=None)
        menubar.add_cascade(label="文件", menu=filemenu)

        # 创建一个下拉菜单“视图”，然后将它添加到顶级菜单中
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="精简", command=None)
        filemenu.add_command(label="详细", command=None)
        menubar.add_cascade(label="视图", menu=filemenu)

        # 创建一个下拉菜单“配置”，然后将它添加到顶级菜单中
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="网络", command=None)
        filemenu.add_command(label="架构", command=None)
        filemenu.add_command(label="搜索", command=None)
        menubar.add_cascade(label="配置", menu=filemenu)

        # 创建一个下拉菜单“工具”，然后将它添加到顶级菜单中
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="打包", command=None)
        filemenu.add_command(label="备份", command=None)
        filemenu.add_command(label="上传", command=None)
        menubar.add_cascade(label="工具", menu=filemenu)

        # 创建一个下拉菜单“帮助”，然后将它添加到顶级菜单中
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="帮助", command=None)
        filemenu.add_command(label="关于", command=None)
        menubar.add_cascade(label="帮助", menu=filemenu)
        # 显示菜单
        self.root.config(menu=menubar)

        '''
        左侧有部分区域未充满
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        root.geometry("%dx%d" %(w,h))
        '''

        self.root.state("zoomed")
        self.root.iconbitmap('./logo.ico')
        # self.layout_display()

        self.root.bind("<Configure>", self.layout_display_bind)

        # root.attributes('-fullscreen', True)   #无状态条、窗口
        # root.attributes("-topmost",True)       #置顶，消除WIN状态栏干扰
        self.root.mainloop()

    def closeWindow(self):
        self.root.destroy()
        root.destroy()

    def callback_start_monitor(self):
        self.display_enable=True
        display_process = threading.Thread(target=self.display,
                                        args=(self.camera_label, self.camera_label))
        display_process.daemon = True
        display_process.start()
        print("display process started:", display_process)
        current_url="rtsp://admin:admin@10.193.232.4:554/cam/realmonitor?channel=1&subtype=1"
        self.video_enable[0]=True
        video0_process=threading.Thread(target=self.video_loop,
                         args=(0, self.camera_label,
                             current_url, "0"))
        video0_process.daemon = True
        video0_process.start()
        print("video_0 process started:", video0_process)
        current_url="rtsp://admin:admin@10.193.232.4:554/cam/realmonitor?channel=1&subtype=0"
        self.video_enable[1]=True
        video1_process=threading.Thread(target=self.video_loop,
                         args=(1, self.camera_label,
                             current_url, "1"))
        video1_process.daemon = True
        video1_process.start()
        print("video_1 process started:", video1_process)
        return

    def callback_stop_monitor(self):
        return

    def layout_display_bind(self, Event=None):
        #print(self.root.winfo_width(), self.root.winfo_height())
        # win=Event
        # print(Event)
        # self.Event_prev=Event
        if (Event == None or self.loading_finished != True):
            return
        # print(Event)
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        label_height=int(width / 2 / 4 * 3)
        self.camera_label.place(x=1, y=1,
                                width=width - 2, height=label_height)  # 4:3
        self.text_label.place(x=0, y=label_height+1, width=width,height=height - label_height-1)
        self.VScroll3.place(x= width- 16-3, y=1, width=16, height=height - label_height-16-3)
        self.VScroll4.place(x=1, y=height - label_height-16-4, width=width-16-1, height=16)

        if (self.camera_label.winfo_width() * self.camera_label.winfo_height() > 1000):
            self.img_video_offline_streched = cv2.resize(self.img_video_offline, (
                int(self.camera_label.winfo_width()/2), int(self.camera_label.winfo_height())))
            cv2image = cv2.cvtColor(self.img_video_offline_streched, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            self.img_video_offline_streched = Image.fromarray(cv2image)  # 将图像转换成Image对象
            self.current_image = Image.new('RGB', (
                (int(self.camera_label.winfo_width())), int(self.camera_label.winfo_height())))
    def display(self, master, panel):
        # print("self.display_enable",self.display_enable)
         if self.display_enable:
            # time.sleep(0.01)
            img = []
            for i in range(2):
                if self.lock[i].acquire():
                    if self.video_ready[i]:
                        img.append(self.img[i].copy())
                        self.img_bak[i]=self.img[i]
                    else:
                        if self.img_bak[i] == None:
                            img.append(self.img_video_offline_streched)
                        else:
                            draw = ImageDraw.Draw(self.img_bak[i])  # 生成绘制对象draw
                            typeface = ImageFont.truetype('simhei.ttf', 18)  # 参数： 字体  字体大小
                            draw.text((10, 10), "连接中。。。。\n", fill=(255, 0, 0), font=typeface)
                            img.append(self.img_bak[i])
                    self.lock[i].release()
                #else:
                #    img.append(self.img_video_offline_streched)
            #print("len of Img:",len(img),img)
            # img = (img1, img2, img3)
            # print(img1.shape,img2.shape,img3.shape)
            # imgs = np.concatenate(img, axis=0)
            # cv2.imshow("test",imgs)
            # cv2image = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
            # current_image = Image.fromarray(cv2image).copy()  # 将图像转换成Image对象
            if len(img)==2:
                box = (0, 0, img[0].width, img[0].height)
                # print(box,img1.width,img1.height)
                self.current_image.paste(img[0], box)
                box = (img[0].width, 0, img[0].width+img[1].width, img[1].height)
                #box = (0, img[0].height, img[1].width , img[0].height+img[1].height)
                # print(box, img2.width, img2.height)
                self.current_image.paste(img[1], box)
                #box = (0, img[0].height + img[1].height, img[2].width, img[0].height + img[1].height + img[2].height)
                # print(box, img3.width, img3.height)
                #self.current_image.paste(img[2], box)
                self.imgtk1 = ImageTk.PhotoImage(image=self.current_image, master=master)

                panel.imgtk = self.imgtk1
                # self.lock1.acquire()
                panel.config(image=self.imgtk1)
                # self.lock1.release()
                # panel.update_idletasks()
                self.counter = self.counter + 1
                if self.counter >= 50:
                    self.counter = 0
                    print("video displaying.....................................：","len(img):",len(img))
            master.after(50, self.display, master, panel)
            # self.display(master, panel)
        # print("quit display")

    def video_loop(self, video_th, panel, url, cam_id):
        print("process for video", video_th, "  ", url)
        cap = cv2.VideoCapture(url)
        print("process for video", video_th, "  ", cap)
        counter = 0
        previous_time = time.time()
        fps = 30

        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
        net_false_counter=0
        while self.video_enable[video_th]:
            width = int(panel.winfo_width()/2)
            height = int(width *3 / 4)
            success, img = cap.read()
            # cv2.waitKey(5)
            success, img = cap.read()  # 从摄像头读取照片
            if success and img.size > 10000:
                # self.lock1.acquire()
                net_false_counter=0
                img = cv2.resize(img, (width, height))
                cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同

                img_ = Image.fromarray(cv2img)  # 转成PIL
                draw = ImageDraw.Draw(img_)  # 图片上打印
                draw.text((width - 80, height - 20), 'FPS: ' + str(fps), (0, 255, 0),
                          font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                draw.text(( 50, height - 20), '位置: CAM' + str(cam_id)+'  '+url, (255, 255, 0), font=font)
                # img = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                # cv2.putText(img, org=(width-80, height-20), text='FPS: ' + str(fps), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, thickness=2,
                #            color= (0, 255, 0))
                # cv2.putText(img, org=(int(width/2)-50, height-20), text=str(cam_id), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, thickness=2,
                #            color= (255, 255, 0))
                if self.lock[video_th].acquire():
                    self.img[video_th] = img_
                    self.video_ready[video_th] = True
                    self.lock[video_th].release()
            else:
                if net_false_counter > 30:
                    self.video_ready[video_th] = False
                net_false_counter=net_false_counter+1
            counter = counter + 1
            if counter == 30:
                current_time = time.time()
                fps = int(counter / (current_time - previous_time))
                previous_time = current_time
                counter = 0
                print("video", video_th, "capturing......", fps, "net_false_counter:",net_false_counter)
                net_state=True
                if fps == 0:
                    cap.release()
                    time.sleep(2)
                    cap = cv2.VideoCapture(url)

            time.sleep(0.05)
        cap.release()


if __name__ == '__main__':
    # t1=threading.Thread(target=welcome)
    # t1.setDaemon(True)
    # t1.start()
    # welcome()

    w = welcome()
    w.show_img()

    root = tkinter.Tk()

    root.wm_attributes('-topmost', 1)
    root.overrideredirect(True)
    # 设置窗口居中
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width = screenwidth / 2
    height = screenheight / 2
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2 + 200, (screenheight - height) / 2)
    root.geometry(alignstr)
    # time.sleep(2)
    # root.overrideredirect(True)#置顶
    # root.attributes("-alpha", 0.3)窗口透明度70 %
    # root.attributes("-alpha", 0.4)  # 窗口透明度60 %
    # root.geometry("300x200+100+100")#大小和位置
    # root.iconbitmap('./logo.ico')
    # root.withdraw()#隐藏tk主窗
    if True:  # (get_local_info()):
        error = 0
        # root.update()

        # canvas = tkinter.Canvas(root)
        # canvas.configure(width=width)
        # canvas.configure(height=height)
        # canvas.configure(bg="blue")
        # canvas.configure(highlightthickness=0)
        # canvas.pack()

        root.withdraw()
        # root.destroy()

        main_process = main_ui()
        main_process.ui_menu()
    else:
        print("网络未连接！")
        result = tk.messagebox.showerror(title='错误', message='网络未连接！')
    exit(0)