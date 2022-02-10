# partly-zoom-out
## How to use
1. specify image path at 
2. 
  `path = './imgs'`

2. change default setup:
3. 
  `LINE_COLOR = (255, 255, 255)  # 获取在原图上画的线的颜色
  LINE_WIDTH = 2  # 在原图上线的宽度
  SCALE = 2  # 对选取区域的放大倍数
  ADD_BBOX = True  # 是否对要保存的图像增加边框
  BBOX_WIDTH = 3   # 增加的边框的宽度
  BBOX_COLOR = (255, 255, 255)  # 默认为白色
  INTER_METHOD = cv2.INTER_LINEAR  # 默认使用最近邻, 双三次INTER_CUBIC, INTER_LANCZOS4, INTER_LINEAR`

3. click and drag mouse to select ROI
4. 'Enter' to save ROI.
5. 'Space' to save all images with the same ROI.
6. 'ESC' to quit.
