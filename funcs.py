import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
def distance(pt1,pt2):
    p1 = np.array(pt1)
    p2 = np.array(pt2)
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4

def rec_extend_auto(xs,ys,ws,hs,img_x,img_y):
    x_coe = img_x / ws / 10  # 矩形越小外扩越大，最大扩8倍
    if x_coe > 8:
        x_coe = 8
    wsn = int(ws * (1 + x_coe - 0.1))  # 新窗口尺寸
    y_coe = img_y / hs / 10
    if y_coe > 8:
        y_coe = 8
    hsn = int(hs * (1 + y_coe - 0.1))
    rec_x = xs - int((wsn - ws) / 2)  # 中心平移对准
    if rec_x < 0:
        rec_x = 0
    if rec_x + wsn > img_x:
        rec_x = img_x - wsn
    rec_y = ys - int((hsn - hs) / 2)
    if rec_y < 0:
        rec_y = 0
    if rec_y + hsn > img_y:
        rec_y = img_y - hsn
    return [rec_x,rec_y,wsn,hsn]

def island_remove(rec,c_contour):
    #contour=c_contour.tolist()
    points_4=[[],[],[],[]]  #对应4个象限中存在的点序号
    center_x=rec[0]+rec[2]/2
    center_y=rec[1]+rec[3]/2
    contour_n=[]
    index=0
    for r in c_contour:
        if r[0][0]-center_x>=0:
            x_sign=True
        else:
            x_sign=False
        if r[0][1]-center_y>=0:
            y_sign=True
        else:
            y_sign=False
        if x_sign:
            if y_sign:
                points_4[0].append(index)
            else:
                points_4[1].append(index)
        else:
            if y_sign:
                points_4[2].append(index)
            else:
                points_4[3].append(index)
        index=index+1
    c_contour_list = c_contour.tolist() #nparray转成list方便处理
    c_contour_list_new=[]
    remove_point_th=[]
    for p in points_4: #4个象限依次处理
        if len(p)>2 : #象限里不是一个孤立点，为有效点，否则删除
            for index in p:
                c_contour_list_new.append(c_contour_list[index]) #将该点添加到新list中
    c_contour=[]
    c_contour.append(np.array(c_contour_list_new)) #格式转化
    if len(c_contour[0])>3:
        xs, ys, ws, hs = cv2.boundingRect(c_contour[0])
        rec = [xs,ys,ws,hs]
    return rec







if __name__ == '__main__':
    rimg = cv2.imread('d:\\test.jpg')
    img = cv2.cvtColor(rimg, cv2.COLOR_RGB2GRAY)
    print(img.shape)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img[1:30,40:100]=254
    cv2.threshold(img, 200, 255, cv2.THRESH_BINARY, dst=img)
    img = cv2.medianBlur(img, 5)
    NonZero = cv2.countNonZero(img)
    img = cv2.dilate(img, kernel)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, color=(80, 80, 80), thickness=3, maxLevel=5)
    center_list = []
    for c in contours:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # print(cX,cY)
        center_list.append([[cX, cY]])

    c_contour=[]
    c_contour.append(np.array(center_list))
    cv2.drawContours(img, c_contour, -1, color=(127, 127, 127), thickness=3, maxLevel=5)
    xs, ys, ws, hs = cv2.boundingRect(c_contour[0])
    cv2.rectangle(img, (xs, ys), (xs + + ws, ys + hs), (255, 255, 255), 2)
    [xs, ys, ws, hs] = island_remove([xs, ys, ws, hs], c_contour[0])
    cv2.rectangle(img, (xs, ys), (xs+ + ws, ys + hs), (100, 100, 100), 5)
    cv2.imshow('1',img)
    '''
    hist = cv2.calcHist([img], [0], None, [256], [0, 255])
    hist_v=hist.tolist()
    maxhist = np.argmax(hist_v)
    # hist是一个shape为(256,1)的数组，表示0-255每个像素值对应的像素个数，下标即为相应的像素值
    # plot一般需要输入x,y,若只输入一个参数，那么默认x为range(n)，n为y的长度
    print(hist,max(max(hist)),maxhist)
    
    plt.plot(hist)
    plt.show()
    '''
    cv2.waitKey()
