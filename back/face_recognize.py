from cv2 import cv2
import os
import numpy as np
import pandas as pd
from net.mtcnn import mtcnn
import utils.utils as utils
from net.inception import InceptionResNetV1

import tensorflow as tf
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class face_rec():
    def __init__(self):
        # 创建mtcnn对象
        # 检测图片中的人脸
        self.mtcnn_model = mtcnn()
        # 门限函数
        self.threshold = [0.5, 0.8, 0.9]

        # 载入facenet
        # 将检测到的人脸转化为128维的向量
        self.facenet_model = InceptionResNetV1()
        # model.summary()
        model_path = './model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)

        # -----------------------------------------------#
        #   对数据库中的人脸进行编码
        #   known_face_encodings中存储的是编码后的人脸
        #   known_face_names为人脸的名字
        # -----------------------------------------------#

        self.known_face_encodings = []

        self.useless_faces = []

        self.current_faces = []

        self.known_face_numbers = []

    def detect_and_align_face(self, img):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        if type(img) == 'str':
            img = cv2.imread(img)
        else:
            img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        height, width, _ = np.shape(img)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 检测人脸
        rectangles = self.mtcnn_model.detectFace(img_rgb, self.threshold)

        if len(rectangles) == 0:
            return
            

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, 0] = np.clip(rectangles[:, 0], 0, width)
        rectangles[:, 1] = np.clip(rectangles[:, 1], 0, height)
        rectangles[:, 2] = np.clip(rectangles[:, 2], 0, width)
        rectangles[:, 3] = np.clip(rectangles[:, 3], 0, height)
        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array(
                [int(rectangle[0]), int(rectangle[1])])) / (rectangle[3] -
                                                            rectangle[1]) * 160

            crop_img = img_rgb[int(rectangle[1]):int(rectangle[3]),
                               int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))

            new_img, _ = utils.Alignment_1(crop_img, landmark)
            new_img = np.expand_dims(new_img, 0)

            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            face_encodings.append(face_encoding)
        return face_encodings

    def verify_faces(self, face_encodings=None, img=None):
        if img is not None:
            face_encodings = np.array(self.detect_and_align_face(img))
        
        self.current_faces = face_encodings
            
        result = False
        # ratios = []
        # face_names = []
        try:
            for face_encoding in face_encodings:
                ratio = self.match_face_embedding(np.array(self.known_face_encodings),
                                                face_encoding)
                if ratio > 0.5:
                    result = True
                    break
        except Exception as e:
            return False

        return result
        # ratios.append(ratio)
        # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
        # matches = utils.compare_faces(self.known_face_encodings,
        #                               face_encoding,
        #                               tolerance=0.75)
        # # name = "Unknown"
        # print(f'matches {matches}')
        # # 找出距离最近的人脸
        # face_distances = utils.face_distance(self.known_face_encodings,
        #                                      face_encoding)
        # # print(face_distances)
        # # print(len(face_distances))
        # # print(face_distances)
        # # # 取出这个最近人脸的评分
        # print(face_distances)
        # best_match_index = np.argmin(face_distances)
        # if matches[best_match_index]:
        #     # name = self.known_face_[best_match_index]
        #     print(f'best {best_match_index}')
        # ratio = np.sum(matches) / len(matches)
        # ratios.append(ratio)
        # # face_names.append(name)

        # result = 'no'
        # print(f'ratios {ratios}')
        # if max(ratios) > 0.5:
        #     result = 'yes'
        # return result

    def match_face_embedding(self, known_face_encodings, face_encoding):
        matches = utils.compare_faces(known_face_encodings,
                                      face_encoding,
                                      tolerance=0.75)
        # name = "Unknown"
        print(f'matches {matches}')
        # 找出距离最近的人脸
        face_distances = utils.face_distance(known_face_encodings,
                                             face_encoding)
        print(face_distances)
        # print(len(face_distances))
        # print(face_distances)
        # # 取出这个最近人脸的评分
        # print(face_distances)
        # best_match_index = np.argmin(face_distances)
        # if matches[best_match_index]:
        #     # name = self.known_face_[best_match_index]
        #     print(f'best {best_match_index}')
        ratio = np.sum(matches) / len(matches)
        return ratio

    def facelist_to_Code(self, name):
        face_list = os.listdir(f'./face_dataset/{name}')
        for face in face_list:
            number = face.split(".")[0]

            img = cv2.imread(f"./face_dataset/{name}/{face}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 检测人脸
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)

            # 转化成正方形
            if len(rectangles) == 0:
                self.useless_face.append(face)
                continue

            rectangles = utils.rect2square(np.array(rectangles))
            # facenet要传入一个160x160的图片
            rectangle = rectangles[0]
            # print(rectangle)
            # 记下他们的landmark
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array(
                [int(rectangle[0]), int(rectangle[1])])) / (rectangle[3] -
                                                            rectangle[1]) * 160

            crop_img = img[int(rectangle[1]):int(rectangle[3]),
                           int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))

            new_img, _ = utils.Alignment_1(crop_img, landmark)

            new_img = np.expand_dims(new_img, 0)
            # 将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)

            self.known_face_encodings.append(face_encoding)
            self.known_face_numbers.append(number)

    def save_embeddings(self, face_encodings, name):
        embeddings = pd.DataFrame(face_encodings)
        embeddings.to_csv(f'./face_dataset/{name}.csv', header=False, index=False)

    def load_embeddings(self, name):
        
        data = pd.read_csv(f'./face_dataset/{name}.csv', header=None)
        embeddings = data.to_numpy(dtype='float64')
        return embeddings


# if __name__ == "__main__":
#     np.set_printoptions(suppress=True)
#     name = 'E000004'
#     face = face_rec()
#     face.facelist_to_Code(name)
#     face.save_embeddings(face.known_face_encodings, name)
#     encodings = face.load_embeddings(name)
#     print(np.array(face.known_face_encodings))
#     print(encodings)
#     result = face.verify_faces(img='test2.jpg')
#     # print(np.shape(encodings))
#     # print(np.shape(face.known_face_encodings))
#     # print(type(face.known_face_encodings))
#     # print(type(encodings))
#     result2 = face.verify_faces(face_encodings=face.current_faces)
#     print(result, result2)