import math
import cv2 as cv
import numpy as np
def HEPT(PT1, PT2, space):
    a1 = PT1[0]
    b1 = PT1[1]
    c1 = PT1[2]
    a2 = PT2[0]
    b2 = PT2[1]
    c2 = PT2[2]
    D  = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1
    if D == 0:
        if Dx + Dy == 0:
            return -1 #trung nhau
        else:
            return 0 #song song
    x = Dx/D
    y = Dy/D
    if x < space[0, 0] or x > space[0, 1] or y < space[1, 0] or y > space[1, 1]:
        return 0
    else:
        return 1 # cat nhau
def KTVUONGGOC(a, b, space):
    X0 = a[2] - a[0]
    Y0 = a[3] - a[1]
    X1 = b[2] - b[0]
    Y1 = b[3] - b[1]
    NX0 = -Y0
    NY0 = X0
    NX1 = -Y1
    NY1 = X1
    C0 = NX0 * (-a[0]) + NY0 * (-a[1])
    C1 = NX1 * (-b[0]) + NY1 * (-b[1])
    PTTQ1 = np.array([NX0, NY0, C0], ndmin=1)
    PTTQ2 = np.array([NX1, NY1, C1], ndmin=1)
    result = HEPT(PTTQ1, PTTQ2, space)
    if result != 1:
        return 0
    else:
        if X1 * X0 + Y1 * Y0 != 0:
            return 0
        else:
            return 1
def KTSONGSONG(a, b, space):
    X0 = a[2] - a[0]
    Y0 = a[3] - a[1]
    X1 = b[2] - b[0]
    Y1 = b[3] - b[1]
    NX0 = -Y0
    NY0 = X0
    NX1 = -Y1
    NY1 = X1
    C0 = NX0 * (-a[0]) + NY0 * (-a[1])
    C1 = NX1 * (-b[0]) + NY1 * (-b[1])
    PTTQ1 = np.array([NX0, NY0, C0], ndmin=1)
    PTTQ2 = np.array([NX1, NY1, C1], ndmin=1)
    result = HEPT(PTTQ1, PTTQ2, space)
    if result == 0:
        return 1
    else:
        return 0
def SOSANH(x, y):
    a = math.sqrt((x[2] - x[0])**2 + (x[3] - x[1])**2)
    b = math.sqrt((y[2] - y[0])**2 + (y[3] - y[1])**2)
    e = abs(((a + b) / 2) * 0.05)
    if (a - b) > e:
        return 1# a > b
    elif (a - b) < -e:
        return -1#a < b
    else:
        return 0# a = b
def DUONGTHANG(src):
    if src is None:
        print('Error opening image!')
        return -1
    dst = cv.Canny(src, 50, 200, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
            cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
    return linesP
def LAYMAU(path):
    img = cv.imread(cv.samples.findFile(path), cv.IMREAD_GRAYSCALE)
    space = np.array([[img.shape[0] * (-5), img.shape[0] * 5],
                      [img.shape[1] * (-5), img.shape[1] * 5]], ndmin=2)
    TOADODINH = DUONGTHANG(img)
    if len(TOADODINH) != 4:
        return
    DK1  = KTSONGSONG(TOADODINH[0, 0], TOADODINH[1, 0], space)
    DK2  = KTSONGSONG(TOADODINH[0, 0], TOADODINH[2, 0], space)
    DK3  = KTSONGSONG(TOADODINH[0, 0], TOADODINH[3, 0], space)
    DK4  = KTSONGSONG(TOADODINH[1, 0], TOADODINH[2, 0], space)
    DK5  = KTSONGSONG(TOADODINH[1, 0], TOADODINH[3, 0], space)
    DK6  = KTSONGSONG(TOADODINH[2, 0], TOADODINH[3, 0], space)

    DK7  = KTVUONGGOC(TOADODINH[0, 0], TOADODINH[1, 0], space)
    DK8  = KTVUONGGOC(TOADODINH[0, 0], TOADODINH[2, 0], space)
    DK9  = KTVUONGGOC(TOADODINH[0, 0], TOADODINH[3, 0], space)
    DK10 = KTVUONGGOC(TOADODINH[1, 0], TOADODINH[2, 0], space)
    DK11 = KTVUONGGOC(TOADODINH[1, 0], TOADODINH[3, 0], space)
    DK12 = KTVUONGGOC(TOADODINH[2, 0], TOADODINH[3, 0], space)
    
    DK13 = SOSANH(TOADODINH[0, 0], TOADODINH[1, 0])
    DK14 = SOSANH(TOADODINH[0, 0], TOADODINH[2, 0])
    DK15 = SOSANH(TOADODINH[0, 0], TOADODINH[3, 0])
    DK16 = SOSANH(TOADODINH[1, 0], TOADODINH[2, 0])
    DK17 = SOSANH(TOADODINH[1, 0], TOADODINH[3, 0])
    DK18 = SOSANH(TOADODINH[2, 0], TOADODINH[3, 0])
    result = np.array([ DK1, DK2, DK3, DK4, DK5, DK6, 
                        DK7, DK8, DK9, DK10, DK11, DK12, 
                        DK13, DK14, DK15, DK16, DK17, DK18], ndmin=1)
    return result 
def hardlim(x):
    I = x < 0
    x[I] = 0
    x[~I] = 1
    return x
def SOSANHKHACMANG(x, y):
    if x[0, 0] == y[0, 0] and \
    x[0, 1] == y[0, 1] and \
    x[0, 2] == y[0, 2] and \
    x[0, 3] == y[0, 3] and \
    x[0, 4] == y[0, 4] and \
    x[0, 5] == y[0, 5] and \
    x[0, 6] == y[0, 6] and \
    x[0, 7] == y[0, 7] and \
    x[0, 8] == y[0, 8] and \
    x[0, 9] == y[0, 9] and \
    x[0, 10] == y[0, 10] and \
    x[0, 11] == y[0, 11] and \
    x[0, 11] == y[0, 11] and \
    x[0, 11] == y[0, 11] and \
    x[0, 12] == y[0, 12] and \
    x[0, 13] == y[0, 13] and \
    x[0, 14] == y[0, 14] and \
    x[0, 15] == y[0, 15] and \
    x[0, 16] == y[0, 16] and \
    x[0, 17] == y[0, 17]:
        return False
    else:
        return True
def TEST(path):
    try:
        ex = LAYMAU(path)
        result = hardlim(w @ ex + bias)
    except:
        result = -1
    if result == 0:
        print(path, '==> HINH CHU NHAT')
    elif result == 1:
        print(path, '==> HINH BINH HANH')
    else:
        print(path, "==> CHUA BIET HINH NAY LA HINH GI")
if __name__ == "__main__":
    p1 = LAYMAU('picture/HINHCHUNHAT.png')
    p2 = LAYMAU('picture/HINHBINHHANH.png')
    t1 = np.array([0], ndmin=2) #HINH CHU NHAT
    t2 = np.array([1], ndmin=2) #HINH BINH HANH
    w  = np.random.randint(-1, 2, (1, 18))
    print(w)
    bias = 0.5
    w_old = np.full((1, 18), 0)
    bias_old = 0
    lanlap = 0
    while SOSANHKHACMANG(w, w_old) or bias != bias_old:
        w_old = w
        bias_old = bias
        a = hardlim(w @ p1 + bias)
        e = t1 - a
        w = w + e * p1.T
        bias = bias + e

        a = hardlim(w @ p2 + bias)
        e = t2 - a
        w = w + e * p2.T
        bias = bias + e

        lanlap += 2
    print('Da hoc xong voi so lan lap la {0}'.format(lanlap))
    print('Ma tran trong so w = ', w)
    print('Bias = ', bias)
    TEST('picture/HINHCHUNHATTEST.png')
    TEST('picture/HINHBINHHANHTEST.png')
    TEST('picture/HINHKHACLA.png')
    TEST('picture/HINHTRON.png')