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
    cv2.rectangle(img, (xs, ys), (xs+ + ws, ys + hs), (255, 255, 255), 1)
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
