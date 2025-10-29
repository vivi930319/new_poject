import cv2
import mediapipe as mp
import json

# 圖片路徑
image_path = r"C:\Users\isach\Downloads\IMG_4093.png"
# 輸出 JSON 路徑（可選）
output_path = r"C:\Users\isach\PycharmProjects\makeup_facing\mediapipe_landmarks.json"

# 讀取圖片
image = cv2.imread(image_path)
if image is None:
    print("圖片載入失敗")
    exit()

# 初始化 MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# 偵測臉部
results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
if not results.multi_face_landmarks:
    print("未偵測到臉部")
    exit()

# 取得 landmark 座標
landmarks = results.multi_face_landmarks[0].landmark
h, w = image.shape[:2]

# 儲存座標用
landmark_points = {}

# 標記每個點
for i, lm in enumerate(landmarks):
    px = int(lm.x * w)
    py = int(lm.y * h)
    landmark_points[i] = [round(px, 2), round(py, 2)]
    cv2.circle(image, (px, py), 1, (0, 255, 0), -1)
    cv2.putText(image, str(i), (px + 2, py - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

# 顯示圖片
resized = cv2.resize(image, (800, 800))
cv2.imshow("MediaPipe Landmarks", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 可選：輸出 JSON
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(landmark_points, f, indent=2)