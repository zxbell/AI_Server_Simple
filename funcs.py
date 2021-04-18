import numpy as np
import math
import cv2
import matplotlib.pyplot as plt


def distance(pt1, pt2):
    p1 = np.array(pt1)
    p2 = np.array(pt2)
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4


def rec_extend_auto(xs, ys, ws, hs, img_x, img_y):
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
    return [rec_x, rec_y, wsn, hsn]


def island_remove(rec, c_contour):
    # contour=c_contour.tolist()
    points_4 = [[], [], [], []]  # 对应4个象限中存在的点序号
    center_x = rec[0] + rec[2] / 2
    center_y = rec[1] + rec[3] / 2
    contour_n = []
    index = 0
    contour_num = len(c_contour)
    thrd = contour_num / 5
    if thrd < 1:
        thrd = 1
    for r in c_contour:
        if r[0][0] - center_x >= 0:
            x_sign = True
        else:
            x_sign = False
        if r[0][1] - center_y >= 0:
            y_sign = True
        else:
            y_sign = False
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
        index = index + 1
    c_contour_list = c_contour.tolist()  # nparray转成list方便处理
    c_contour_list_new = []

    for p in points_4:  # 4个象限依次处理
        if len(p) > thrd:  # 象限里不是一个孤立点，为有效点，否则删除
            for index in p:
                c_contour_list_new.append(c_contour_list[index])  # 将该点添加到新list中
    c_contour = []
    c_contour.append(np.array(c_contour_list_new))  # 格式转化
    if len(c_contour[0]) > 3:
        xs, ys, ws, hs = cv2.boundingRect(c_contour[0])
        rec = [xs, ys, ws, hs]
    return rec

def contour_pts(c,thrd=50):
    result=[]
    if len(c) > 0:
        #result.append(c[0])
        for i in range(0,len(c)):
            if i == len(c)-1:
                i_next=0
            else:
                i_next=i+1
            insertnum = int(dist(c[i_next], c[i]) /thrd) + 1
            x_step = (c[i_next][0] - c[i][0]) / (insertnum )
            y_step = (c[i_next][1] - c[i][1]) / (insertnum )
            for j in range(0, insertnum):
                result.append([int(c[i][0]+j*x_step), int(c[i][1]+j*y_step)])
            #result.append(c[i])
    return result

def dist(pt1, pt2):  # 计算两点间xy两个方向的大值，比算距离快一些
    dx = abs(pt1[0] - pt2[0])
    dy = abs(pt1[1] - pt2[1])
    if dx > dy:
        return dx
    else:
        return dy


def dist_list(pts):  # 计算点序列所有点之间的距离
    lenth = len(pts)
    dists = [0]*(lenth * lenth)
    index = 0
    max_dist = -100
    for pt1 in pts:
        for i in range(index, lenth):
            dst = dist(pt1, pts[i])
            if dst > max_dist:
                max_dist = dst
            dists[index * lenth + i] = dst
        index = index + 1
    return max_dist, dists

def list_clean(list0):
    list4 = []
    for i in list0:
        if not i in list4:
            list4.append(i)
    return list4
# 聚类
# pts: 点列表
# cluster_thrd_coe：相对阈值系数*最大点间距为聚类阈值
# thrd: 最小聚类阈值
def cluster(pts, cluster_thrd_coe=0.5, thrd=50):
    cluster_list=[[],[],[],[],[],[],[],[]] #最多分四类
    max_dist, dists = dist_list(pts) #计算所有点间距
    cluster_thrd = cluster_thrd_coe * max_dist
    #if cluster_thrd > thrd:
    #    cluster_thrd = thrd
    if cluster_thrd < 50:
        cluster_thrd = 50
    cluster_thrd=100
    lenth = len(pts)
    list_indexed=0
    clustered_pts_index=[]
    for pt_index in range(lenth):
        list_index_now = 0
        lens = len(cluster_list[list_indexed]) #当前类的长度
        if lens > 0:
            list_indexed = list_indexed + 1 #默认当前点不在之前的分类中，新建一个类
        for cluster_t in cluster_list:  # 在已聚好的类中检索是否已记录过
            if pt_index in cluster_t:
                list_indexed = list_index_now #若已分过类，则向已分过的类中添加满足条件的点
                break
            list_index_now = list_index_now + 1
        if list_indexed > 4:
            break
        for i in range(pt_index, lenth):
            if not i in clustered_pts_index:  # 如果该点未被聚过类
                dst = dists[pt_index * lenth + i]
                if dst < cluster_thrd: #如果是可聚类的
                    cluster_list[list_indexed].append(i)  # 在聚类表中添加当前点
                    clustered_pts_index.append(i)  #在已聚过类的表中添加当前点
    result=[]
    for clst in cluster_list:  #清理类中的重复点
        if len(clst)>0:
            clst=list_clean(clst)
            result.append(clst)
    return result



if __name__ == '__main__':
    pts = [[1, 0], [2, 0], [5, 0], [400, 0], [30, 0], [180, 0], [195, 0]]
    new_pts=contour_pts(pts, thrd=50)
    cls_result=cluster(new_pts, thrd=150)
    rimg = cv2.imread('d:\\test.jpg')
    img = cv2.cvtColor(rimg, cv2.COLOR_RGB2GRAY)
    print(img.shape)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img[1:30, 40:100] = 254
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

    c_contour = []
    c_contour.append(np.array(center_list))
    cv2.drawContours(img, c_contour, -1, color=(127, 127, 127), thickness=3, maxLevel=5)
    xs, ys, ws, hs = cv2.boundingRect(c_contour[0])
    cv2.rectangle(img, (xs, ys), (xs + + ws, ys + hs), (255, 255, 255), 2)
    [xs, ys, ws, hs] = island_remove([xs, ys, ws, hs], c_contour[0])
    cv2.rectangle(img, (xs, ys), (xs + + ws, ys + hs), (100, 100, 100), 5)
    cv2.imshow('1', img)
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
