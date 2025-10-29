import cv2

img = cv2.imread(r"C:\Users\isach\Downloads\IMG_4093.png", cv2.COLOR_BGR2HSV)

if img is None:
    print("❌ 圖片載入失敗")
else:
    print("原始尺寸：", img.shape)
    resized = cv2.resize(img, (800, 800))
   
    cv2.imshow("gray", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()