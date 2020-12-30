# encoding: utf-8
import multiprocessing
import os
import signal
import socket
import threading
import time
import cv2
import queue
recv_data = bytes()

def recv(client_socket):
    global recv_data
    # 接收对方发送过来的数据
    try:
        while True:
            recv_data = client_socket.recv(1024)  # 接收1024个字节
    except:
        pass

def demode_img(recv_data, img):
    x = recv_data.decode('gbk').split("_")
    # print(recv_data.decode('gbk'))
    for i in range(int((len(x) - 1) / 5)):
        # print(x)
        WarningType = int(x[i * 5])
        xmin = int(float(x[i * 5 + 1]))
        # print(xmin)
        ymin = int(float(x[i * 5 + 2]))
        # print(ymin)
        xmax = int(float(x[i * 5 + 3]))
        # print(xmax)
        ymax = int(float(x[i * 5 + 4]))

        if WarningType == 0:
            cv2.putText(img, 'fire', (xmin, ymin - 1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
        else:
            cv2.putText(img, 'smoke', (xmin, ymin - 1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
# 子进程执行的方法
def load_and_show(client_socket, clientAddr):
    global recv_data
    # 线程1——处理数据并保存时间戳
    t1 = threading.Thread(target=recv, args=(client_socket,), daemon=True)
    t1.start()
    cap = cv2.VideoCapture("rtsp://admin:wuhuaxun960727@192.168.0.3:554/cam/realmonitor?channel=1&subtype=0")
    start_time = time.time()
    counter = 0
    img_buffer = []
    i = 0
    # 先缓存帧
    start = time.time()
    for i in range(20):
        img_buffer.append(cap.read()[1])
        cv2.waitKey(30)  # 设置延迟时间
    cv2.namedWindow(str(clientAddr[0]))
    while True:
        # 逐帧捕获
        ret, img = cap.read()
        if len(img_buffer) == 0:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        img_show = img_buffer[i]
        #cv2.flip(img_show, 0, img_show)
        # 如果读到新的帧，覆盖已取出的位置
        if ret:
            img_buffer[i] = img

        # 处理下标
        if i != len(img_buffer) - 1:
            i = i + 1

        else:
            i = 0
        
        if (len(recv_data.decode('gbk')) != 0):
            demode_img(recv_data, img_show)
            # 清空buffer
            recv_data = bytes()
        counter += 1

        if (time.time() - start_time) != 0:
            cv2.putText(img_show, "FPS {0}".format(float('%.1f' % (counter / (time.time() - start_time)))), (50, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        3)
            cv2.imshow(str(clientAddr[0]), img_show)
            #cv2.waitKey(10)
            counter = 0
            start_time = time.time()

        k = cv2.waitKey(30)
        if k == ord('a') or k == ord('A'):
            break

    cv2.destroyAllWindows()  # 删除建立的全部窗口
    client_socket.close()
    # 销毁子进程
    os.kill(os.getpid(), signal.SIGTERM)


def main():
    # 创建socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 本地信息
    address = ('192.168.0.155', 7788)

    # 绑定
    tcp_server_socket.bind(address)

    # 监听多个端口
    tcp_server_socket.listen(128)

    # 同步锁
    # R = threading.Lock()

    while True:
        # 阻塞等待新的客户端连接
        client_socket, clientAddr = tcp_server_socket.accept()

        # 客户端连接成功后，调用打开视频流
        print(str(clientAddr[0]) + "出现疑似火警！")
        print("IP:" + str(clientAddr[0]) + " Port:" + str(clientAddr[1]))

        # 开一个线程从FPGA端不断接收数据
        # _thread.start_new_thread(recv, (client_socket,))

        # 多进程
        p = multiprocessing.Process(target=load_and_show, args=(client_socket, clientAddr))
        p.daemon = True
        p.start()
        # print(p.pid)
    tcp_server_socket.close()


if __name__ == '__main__':
    main()
