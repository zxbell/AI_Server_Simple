from showwelcome import welcome
import tkinter
import tkinter as tk
from tkinter import *
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import threading
import multiprocessing
import socket
import requests
import datetime

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
        self.que = []
        self.que_time=[]
        self.cam1_que = []
        self.cam2_que = []
        self.img = [None, None, None]
        self.img_bak = [None, None, None]
        self.counter = 0
        self.cam_loop = False
        self.process_loop_camera = None
        self.img_video_offline = cv2.imread("offline.jpg", cv2.IMREAD_UNCHANGED)  # 不支持中文
        self.img_video_offline_streched=None

        self.loading_finished = True
        self.start_time=[0,0,0,0]
        self.current_time=[0,0,0,0]
        self.ai_ip=['192.168.3.102:7788','192.168.3.100:7788']
        self.ai_status=[False,False]
        self.cam_ip=['10.193.232.5','10.193.232.4']
        self.cam_res=[]
        self.ai_rec=[]
        for i in range(len(self.ai_ip)):
            self.ai_rec.append([])
        self.tcp_server_process = None


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
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            HOST = s.getsockname()[0]
        finally:
            s.close()
        return HOST

    def IsOpen(self, i, ip, port):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((ip, int(port)))
                self.ai_status[i] = True
                s.shutdown(2)
                #return True
            except:
                #return False
                print(ip,":",port," lost!......")
                self.ai_status[i]=False

            time.sleep(2)


    def ai_process_start(self,i):
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        [ip, port] = self.ai_ip[i].split(":")
        print(ip, port)
        is_connected = False
        HOST = self.get_local_ip()
        HOST="hostip_192.168.3.153_7788"
        try:
            tcp_client.connect((ip, 10086))  # 10086是所有AI模块接收控制的服务端口
            is_connected = True
            data = HOST
            tcp_client.sendall(data.encode())  # 发送本机的报警处理服务端口
            received = tcp_client.recv(4096)
            print("Bytes Sent:     {}".format(data))
            print("Bytes Received: {}".format(received))  # .decode()))
            tcp_client.sendall(('camip_' + self.cam_ip[i]).encode())  # 发送AI配对的cam的ip
            received = tcp_client.recv(4096)  # 接收cam的分辨率
            print("Bytes Sent:     {}".format(data))
            print("Bytes Received: {}".format(received))  # .decode()))
            x = received.decode('gbk').split("_")
            if len(x) == 3:
                if x[0] == 'resolution':
                    self.cam_res.append([int(x[1]), int(x[2])])
                    time.sleep(0.5)
                    data = 'start'
                    tcp_client.sendall(data.encode())
                    received = tcp_client.recv(4096)
                    print("Bytes Sent:     {}".format(data))
                    print("Bytes Received: {}".format(received))  # .decode()))
                    time.sleep(0.5)
                    print(self.ai_ip[i], " connect succeed")
        except Exception as e:  # 连接失败
            print(e, self.ai_ip[i], " connect failed")
            self.ai_status[i]= False
            if is_connected:
                tcp_client.shutdown(2)
                tcp_client.close()
            time.sleep(2)
        finally:
            tcp_client.close()
            self.ai_status[i] = True
            aidetect_process = threading.Thread(target=self.IsOpen,
                                               args=(i, ip, 10086))
            aidetect_process.daemon = True
            aidetect_process.start()
            print("aidetect process started:", aidetect_process)
            time.sleep(2)

    def callback_start_monitor(self):
        self.display_enable=True
        display_process = threading.Thread(target=self.display,
                                        args=(self.camera_label, self.camera_label))
        display_process.daemon = True
        display_process.start()
        print("display process started:", display_process)
        current_url="rtsp://admin:admin@10.193.232.4:554/cam/realmonitor?channel=1&subtype=1"
        '''
        try:
            print(current_url, "checking")
            r = requests.get(current_url)
            if '200' in str(r):
                print(current_url," --------------------------------------------active")
            else:
                print(current_url, " ********************************************inactive")
                pass
        except requests.exceptions.ConnectionError:
            pass
        '''
        #current_url="rtmp://58.200.131.2:1935/livetv/dfhd"
        self.video_enable[0]=True
        video0_process=threading.Thread(target=self.video_loop,
                         args=(0, self.camera_label,
                             current_url, "0"))
        video0_process.daemon = True
        video0_process.start()
        print("video_0 process started:", video0_process)
        current_url="rtsp://admin:admin@10.193.232.4:554/cam/realmonitor?channel=1&subtype=1"
        #current_url = "rtmp://58.200.131.2:1935/livetv/cctv1hd"
        self.video_enable[1]=True
        video1_process=threading.Thread(target=self.video_loop,
                         args=(1, self.camera_label,
                             current_url, "1"))
        video1_process.daemon = True
        video1_process.start()
        print("video_1 process started:", video1_process)
        self.ai_start=True
        if self.tcp_server_process == None :

            self.tcp_server_process=threading.Thread(target=self.tcp_server,
                             args=())
            self.tcp_server_process.daemon = True
            self.tcp_server_process.start()
            print("tcp_server_process started:", self.tcp_server_process)
        else:
            if self.tcp_server_process.is_alive() == False:
                self.tcp_server_process = threading.Thread(target=self.tcp_server,
                                                           args=())
                self.tcp_server_process.daemon = True
                self.tcp_server_process.start()
                print("tcp_server_process restarted:", self.tcp_server_process)



        for i in range(len(self.ai_ip)):
            p=threading.Thread(target=self.ai_process_start,args=(i,))
            p.daemon = True
            p.start()
        return


    def callback_stop_monitor(self):
        self.display_enable=False
        self.ai_start = False
        self.video_enable[0] = False
        self.video_enable[1] = False
        self.que.clear()
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect(('192.168.3.100', 10086))
            data='stop'
            tcp_client.sendall(data.encode())
            received = tcp_client.recv(4096)
            # print("Bytes Sent:     {}".format(data2))
            print("Bytes Received: {}".format(received))  # .decode()))
            time.sleep(0.5)
        except Exception as e:
            print(e)
            tcp_client.close()



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
        width=panel.winfo_width()
        height=panel.winfo_height()

        y_ratio=height/144
        x_ratio = y_ratio


        if self.display_enable:
            # time.sleep(0.01)
            img = []
            for i in range(2):
                if self.lock[i].acquire():
                    if self.video_ready[i]:
                        if i==1 :
                            if len(self.que)>=2: #延时显示
                                img_pop=self.que.pop(0)
                                time_pop=self.que_time.pop(0)
                                draw = ImageDraw.Draw(img_pop)  # 图片上打印  此处可以绘制识别结果
                                time_string = time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime(int(time_pop / 1000)))
                                font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
                                #draw.text((int(width/2), int(height/2)), time_string, (255, 255, 0),
                                #draw.text((int(width/4), int(height/4)), time_string, (255, 255, 0),
                                #          font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                                if self.ai_status[i] == True:
                                    draw.text((int(width/4)-200, 30), 'AI: 在线', (255, 255, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

                                else:
                                    draw.text((int(width/4)-200, 30), 'AI: 掉线', (255, 0, 0),
                                              font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                                if len(self.ai_rec[i]) > 0:
                                    draw.text((int(width/4), int(height/2)), 'Warning', (255, 255, 0),
                                              font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                                    xy=[0,0,0,0]
                                    for j in range(len(self.ai_rec[i])):
                                        for k in range(2):
                                            xy[k*2]=int(self.ai_rec[i][j][k*2]*x_ratio)
                                            xy[k * 2+1] = int(self.ai_rec[i][j][k*2+1] * y_ratio)
                                        #xy[2]=xy[2]-xy[0]
                                        #xy[3]=xy[3]-xy[1]
                                        print(xy)
                                        if(len(self.ai_rec[i][j])>0):
                                            xys=tuple(xy)
                                            #print(xys)
                                            if(len(xys)==4):
                                                draw.rectangle(xy=xys, fill=None, outline=(255, 0, 0), width=6)
                                    self.ai_rec[i]=[]
                                img.append(img_pop)

                                self.img_bak[i] = img_pop
                            #else:
                            #    img.append(self.img_video_offline_streched)
                            #    self.img_bak[i] = self.img[i]
                        else:
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
        now_time = int(round(time.time()*1000))
        self.start_time[video_th]=int(now_time)
        print("process for video", video_th, "  ", cap, self.start_time[video_th])
        counter = 0
        previous_time = time.time()
        fps = 30
        for i in range(1,30):
            success, img = cap.read()
            #if video_th ==1:
            #    self.que.append(img)
            time.sleep(0.02)
        milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
        raw_time = int(milliseconds)
        now_time = int(round(time.time() * 1000))
        self.current_time[video_th] = self.start_time[video_th] + raw_time
        dtime=self.current_time[video_th]-now_time
        self.start_time[video_th]=self.start_time[video_th]-3*dtime   #每台相机延时不同，需要修正

        font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
        net_false_counter=0
        while self.video_enable[video_th]:
            width = int(panel.winfo_width()/2)
            height = int(width *3 / 4)
            success, img = cap.read()
            #cv2.waitKey(5)
            success, img = cap.read()  # 从摄像头读取照片
            if success and img.size > 10000:
                milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)
                fps_ = cap.get(cv2.CAP_PROP_FPS)
                raw_time=int(milliseconds)
                now_time = int(round(time.time() * 1000))
                self.current_time[video_th]=self.start_time[video_th]+raw_time
                milliseconds=self.current_time[video_th]
                seconds = milliseconds // 1000
                milliseconds = milliseconds % 1000
                minutes = 0
                hours = 0
                if seconds >= 60:
                    minutes = seconds // 60
                    seconds = seconds % 60

                if minutes >= 60:
                    hours = minutes // 60
                    minutes = minutes % 60

                #print("video", video_th,raw_time, int(hours), int(minutes), int(seconds), int(milliseconds),now_time,self.current_time[video_th],self.current_time[video_th]-now_time)
                # self.lock1.acquire()
                net_false_counter=0
                img = cv2.resize(img, (width, height))
                cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同

                img_ = Image.fromarray(cv2img)  # 转成PIL
                draw = ImageDraw.Draw(img_)  # 图片上打印
                time_string=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(self.current_time[video_th]/1000)))

                draw.text((width - 300, 80), time_string, (0, 255, 0),
                          font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

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
                    if video_th == 1:
                        if len(self.que) > 3:
                            self.que.clear()
                        self.que.append(img_)
                        self.que_time.append(self.current_time[video_th])
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

            #time.sleep(0.01)
        cap.release()

    def tcp_server(self):
        # 创建socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 本地信息
        local_ip=self.get_local_ip()
        address = (local_ip, 7788)
        print(address)
        # 绑定
        tcp_server_socket.bind(address)
        # 监听多个端口
        tcp_server_socket.listen(128)
        # 同步锁
        # R = threading.Lock()
        while self.ai_start:
            # 阻塞等待新的客户端连接
            print("Waiting for AI.....")
            client_socket, clientAddr = tcp_server_socket.accept()

            # 客户端连接成功后，调用打开视频流
            print(str(clientAddr[0]) + "出现疑似火警！")
            print("IP:" + str(clientAddr[0]) + " Port:" + str(clientAddr[1]))

            # 开一个线程从FPGA端不断接收数据
            # _thread.start_new_thread(recv, (client_socket,))

            # 多进程
            p = threading.Thread(target=self.get_warning_info, args=(client_socket, clientAddr))
            p.daemon = True
            p.start()
            time.sleep(0.1)
            # print(p.pid)

        tcp_server_socket.shutdown(how='SHUT_RDWR')
        tcp_server_socket.close()
        print("tcp_server_socket closed")

        time.sleep(1)

    def get_warning_info(self,client_socket, clientAddr):
        is_matched = False
        for id in range(len(self.ai_ip)):  #寻找当前通讯ip在ai_ip中的位置
            [ip, port] = self.ai_ip[id].split(":")
            if clientAddr[0] == ip:
                is_matched=True
                index=id
        print(is_matched,index)
        if is_matched:
            self.ai_rec[index] = []
            try:
                while True:
                    recv_data = client_socket.recv(1024)  # 接收1024个字节
                    #print(recv_data)
                    if True:#self.lock[index].acquire():
                        if(len(self.ai_rec[index])>5):
                            self.ai_rec[index].pop(0)
                        x = recv_data.decode('gbk').split("_")
                        if len(x)>0 and len(x) %4 ==0:
                            self.warning = True
                            for i in range(int(len(x) / 4)):
                                self.ai_rec[index].append([])
                                for j in range(4):
                                    #print(i, j, i * 4 + j)
                                    self.ai_rec[index][i].append(float(x[i * 4 + j]))
                            print(self.ai_rec[index])
                            #self.lock[index].release()
                    if recv_data==b'':
                        break
            except Exception as e:
                print(e)





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