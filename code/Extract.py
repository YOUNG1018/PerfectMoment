import numpy as np
import cv2
import dlib


def extract(img, dialation=0.25):
    '''
    Read an image and extract key points from it
    :param img: image to extract, type is ndarray
           dialation: bounding box dialtion rate
    :return: 68 key points list extracted form the image

    '''
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # img = cv2.imread(img)
    pts = []  # the key points

    # 取灰度
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 人脸数rects
    rects = detector(img_gray, 0)
    # print(rects)
    for i in range(len(rects)):
        landmarks = np.matrix([[p.x, p.y]
                               for p in predictor(img, rects[i]).parts()])
        for idx, point in enumerate(landmarks):
            # 68点的坐标
            pos = [point[0, 0], point[0, 1]]
            pts.append(pos)

    # head bounding boxes
    head_bounding_boxes = []
    for subject in rects:
        h = subject.height()
        w = subject.width()
        top = subject.top()
        bottom = subject.bottom()
        left = subject.left()
        right = subject.right()
        head_bounding_boxes.append(
            [int(left-dialation*w), int(top-dialation*h), int(w+2*dialation*w), int(h+2*dialation*h)])
    print(head_bounding_boxes)

    haar_upper_body_cascade = cv2.CascadeClassifier(
        "./haarcascade_upperbody.xml")
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    upper_body_bounding_boxes = haar_upper_body_cascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(25, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    width, height = img_gray.shape
    if len(upper_body_bounding_boxes)<len(head_bounding_boxes):
        upper_body_bounding_boxes=[]
        for subject in head_bounding_boxes:
            left = subject[0]-0.25*subject[2]
            top = subject[1]+subject[3]
            w = subject[2]*2
            h = height - top-1
            upper_body_bounding_boxes.append([int(left),int(top),int(w),int(h)])
    print(upper_body_bounding_boxes)

    data = [head_bounding_boxes, upper_body_bounding_boxes]
    data = np.array(data)
    data = data.T

    # return head_bounding_boxes, upper_body_bounding_boxes
    return data


if __name__ == '__main__':
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # cv2读取图像
    img = cv2.imread("imgs/homo_test_2/photo2.jpg")
    extract(img)
    # 取灰度
    # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 人脸数rects
    # rects = detector(img_gray, 0)
    # for i in range(len(rects)):
    #     landmarks = np.matrix([[p.x, p.y] for p in predictor(img, rects[i]).parts()])
    #     for idx, point in enumerate(landmarks):
    # 68点的坐标
    # pos = (point[0, 0], point[0, 1])
    # print(idx, pos)

    # 利用cv2.circle给每个特征点画一个圈，共68个
    # cv2.circle(img, pos, 3, color=(0, 255, 0))
    # 利用cv2.putText输出1-68
    # font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(img, str(idx + 1), pos, font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    # cv2.namedWindow("img", 2)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
