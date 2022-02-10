import cv2
import os
from glob import glob
import numpy as np

LINE_COLOR = (255, 255, 255)  # 获取在原图上画的线的颜色
LINE_WIDTH = 2  # 在原图上线的宽度
SCALE = 2  # 对选取区域的放大倍数
ADD_BBOX = True  # 是否对要保存的图像增加边框
BBOX_WIDTH = 3   # 增加的边框的宽度
BBOX_COLOR = (255, 255, 255)  # 默认为白色
INTER_METHOD = cv2.INTER_LINEAR  # 默认使用最近邻, 双三次INTER_CUBIC, INTER_LANCZOS4, INTER_LINEAR

class ZoomOut():
    def __init__(self, path, out_path = './output') -> None:
        self.image_path_list = glob(os.path.join(path, '*.png'))
        self.image_name_list = [os.path.basename(l).rstrip('.png') for l in self.image_path_list]
        self.out_path = out_path

    def _read_images(self):
        images = []
        for image_path in self.image_path_list:
                image = cv2.imread(image_path)
                images.append(image)
        return images
    
    def _draw_circle(self,event, x, y, flags, params):
        image_copy = params['image'].copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # 获取左上角的坐标
            params['coordinate'] = (x, y)
            print("point1: ",params['coordinate'])
            cv2.circle(image_copy, params['coordinate'], 10, LINE_COLOR, LINE_WIDTH)
            cv2.imshow("ori_image", image_copy)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(image_copy, params['coordinate'], (x, y), LINE_COLOR, LINE_WIDTH)
            cv2.imshow("ori_image", image_copy)
        elif event == cv2.EVENT_LBUTTONUP:  # 鼠标左键按钮松开的时候画图
            point2 = (x, y)
            print("point2:", point2)
            if params['coordinate'] != point2:
                min_x = min(params['coordinate'][0], point2[0])
                min_y = min(params['coordinate'][1], point2[1])
                width = abs(params['coordinate'][0] - point2[0])
                height = abs(params['coordinate'][1] - point2[1])
                params['grect'] = [min_x, min_y, width, height]
                print("g_rect: ", params['grect'])
                cv2.rectangle(image_copy, params['coordinate'], point2, LINE_COLOR, LINE_WIDTH)
            scaled_image = self._get_scaled_image(image = params['image'], G_RECT = params['grect'])
            splice_image = np.zeros_like(image_copy)
            splice_image[:scaled_image.shape[0], :scaled_image.shape[1],:] = scaled_image
            splice_image = np.hstack([image_copy, splice_image])
            cv2.imshow('ori_image', splice_image)
        
    def _get_roi(self, images):
        for n, image in enumerate(images):
            params = {
                'image': image,
                'coordinate': (0,0),
                'grect': [],
            }
            while True:
                cv2.namedWindow('ori_image')
                cv2.setMouseCallback('ori_image', self._draw_circle, params)
                cv2.imshow('ori_image', image)
                k = cv2.waitKey(0)
                if k == 32:  # 空格键保存对比图
                    self._plot_compair_image(images, params['grect'])
                if k == 13:  # 回车键退出
                    if params['grect']:
                        scaled_image = self._get_scaled_image(image, params['grect'])
                        self._save_clip(scaled_image, self.image_name_list[n])
                    break
                if k == 27:
                    return   
    
    def _save_clip(self, image, name):
        save_path = os.path.join(self.out_path, 'clips')
        if not os.path.exists(save_path):          
            os.makedirs(save_path)
        cv2.imwrite(os.path.join(save_path, '{}_clip.png'.format(name)), image)
        

    def _get_scaled_image(self,image, G_RECT):
        roi_image = image[G_RECT[1]:G_RECT[1] + G_RECT[3], G_RECT[0]:G_RECT[0] + G_RECT[2]]  # 提取选择的区域
        if roi_image.shape[1]*SCALE < image.shape[1] and roi_image.shape[0]*SCALE < image.shape[0]: #判断放大后的ROI尺寸是否超过当前图尺寸
            scaled_shape = (roi_image.shape[1]*SCALE, roi_image.shape[0]*SCALE)
            scaled_image = cv2.resize(roi_image, scaled_shape,
                                            interpolation=INTER_METHOD)# 对选择的区域放大
            borderType = cv2.BORDER_CONSTANT
            add_borders_image = cv2.copyMakeBorder(scaled_image, BBOX_WIDTH, BBOX_WIDTH,
                                                BBOX_WIDTH, BBOX_WIDTH, borderType, value=BBOX_COLOR) # 增加边框
        else:
            ratio = min(image.shape[1]/roi_image.shape[1], image.shape[0]/roi_image.shape[0]) #最长边不超过原图最长边
            scaled_shape = (int(ratio*roi_image.shape[1]), int(ratio*roi_image.shape[0]))
            add_borders_image = cv2.resize(roi_image, scaled_shape,
                                            interpolation=INTER_METHOD)# 对选择的区域放大
        return add_borders_image
    
    def _plot_compair_image(self, images, G_RECT):
        if G_RECT:
            scaled_images = []
            for image in images:
                add_borders_image = self._get_scaled_image(image, G_RECT)
                scaled_images.append(add_borders_image)
            compare_images = np.hstack(scaled_images)
            cv2.imwrite(os.path.join(self.out_path, 'partlly_zom_out.png'), compare_images)

    def __call__(self):
        images = self._read_images()
        self._get_roi(images)

if __name__ == '__main__':
    path = './imgs'
    zoom_out = ZoomOut(path)
    zoom_out()
