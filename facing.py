import cv2
import numpy as np
import trimesh
import os

# 圖片路徑
image_path = r"C:\Users\isach\Downloads\2016110547400701.jpg"
# 模型路徑
# 我原先用mediapipe 跑向速點去標示很正常，但是要畫圖行標記一直亂掉
# 我就上網去查詢ig特效使用的模組，試試看
mesh_path = r"C:\Users\isach\OneDrive\桌面\Spark-AR-Face-Assets-main\Mesh\faceMesh.obj"
# 輸出 JSON 路徑
output_path = r"C:\Users\isach\PycharmProjects\PythonProject7\face_output.json"

# 讀圖片
image = cv2.imread(image_path)
if image is None:
    print(f"圖片載入失敗：{image_path}")
    exit()
# 灰階處理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 臉部偵測器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# 沒偵測到臉就跳出
if len(faces) == 0:
    print("圖片中未偵測到臉部")
    exit()

# 檢查模型檔案
if not os.path.exists(mesh_path):
    print(f"Face Mesh 模型不存在：{mesh_path}")
    exit()

# 讀模型
try:
    mesh = trimesh.load(mesh_path, force='mesh')
    vertices = mesh.vertices
except Exception as e:
    print(f"Face Mesh 載入失敗：{e}")
    exit()

# 五官點位 index
# 先用blender載入faceMesh.obj模型
# 這裡有個問題是blender載入faceMesh.obj模型是3D的可能這樣導致 點位沒標好
'''
我先標左眼，但是結果很奇怪 一點都不對
其他的數據先讓gpt給我(但都是錯的)
要去找不用手動輸入的方法
'''
FACIAL_GROUPS = {
    "left_eye": [67, 72, 75, 96, 97, 98, 149, 156, 158, 160, 298, 377, 379, 398, 423, 434, 451, 469, 1152, 1154, 1187, 1188, 1232, 1233],
    "right_eye": [78, 79, 80, 81, 82, 83, 84],
    "nose": [2, 6, 9, 12, 15, 18],
    "mouth": [308, 309, 310, 311, 312, 313, 314, 315, 316, 317],
    "mouth_inner": [318, 319, 320, 321, 322, 323, 324]
}

# 用不同顏色去標示五官
GROUP_COLORS = {
    "left_eye": (0, 255, 255),       # 黃色
    "right_eye": (255, 0, 255),      # 紫色
    "nose": (0, 255, 0),             # 綠色
    "mouth": (0, 0, 255),            # 紅色
    "mouth_inner": (255, 255, 0)     # 淺藍
}

output = {}
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for group, indices in FACIAL_GROUPS.items():
        output[group] = []
        for idx in indices:
            if idx >= len(vertices):
                continue
            vx, vy, vz = vertices[idx]
            px = int(x + vx * w)
            py = int(y + vy * h)
            output[group].append([round(px, 2), round(py, 2), round(vz, 4)])
            if 0 <= px < image.shape[1] and 0 <= py < image.shape[0]:
                color = GROUP_COLORS.get(group, (255, 255, 255))
                cv2.circle(image, (px, py), 3, color, -1)
                cv2.putText(image, group[0].upper(), (px + 2, py - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color, 1)

# 這個json是錯誤的格式，我先造一個我這裡跑看得舒服的格式
formatted = "{\n"
for group, points in output.items():
    formatted += f'  "{group}": [\n'
    for pt in points:
        formatted += f"    {pt},\n"
    formatted = formatted.rstrip(",\n") + "\n  ],\n\n"
formatted = formatted.rstrip(",\n\n") + "\n}"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(formatted)

cv2.imshow("Face Landmarks", image)
print("五官座標 JSON：\n")
print(formatted)
cv2.waitKey(0)
cv2.destroyAllWindows()
