import cv2  # OpenCV：影像處理
import mediapipe as mp  # MediaPipe：臉部特徵點偵測
import numpy as np  # NumPy：陣列與遮罩處理

# 圖片路徑
image_path = r"C:\Users\isach\Downloads\IMG_4093.png"

# 讀取圖片
image = cv2.imread(image_path)
if image is None:
    print("圖片載入失敗")
    exit()
h, w = image.shape[:2]  # 取得圖片尺寸

# 初始化 MediaPipe 臉部網格偵測器
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# 將圖片轉成 RGB 並進行臉部偵測
results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
if not results.multi_face_landmarks:
    print("未偵測到臉部")
    exit()
landmarks = results.multi_face_landmarks[0].landmark  # 取得第一張臉的 landmark 資料

# 建立臉部遮罩（使用 jaw + 額頭 landmark）
face_mask = np.zeros((h, w), dtype=np.uint8)
face_outline = []

# 下巴輪廓 landmark index（0–16）
jaw_indices = list(range(0, 17))
# 額頭 landmark index（10, 338）可視為左右額頭
forehead_indices = [10, 338]

# 收集 jaw 點位
for idx in jaw_indices:
    lm = landmarks[idx]
    px, py = int(lm.x * w), int(lm.y * h)
    face_outline.append([px, py])

# 收集額頭點位（向上偏移）
for idx in forehead_indices:
    lm = landmarks[idx]
    px, py = int(lm.x * w), int(lm.y * h) - 30
    face_outline.insert(0, [px, py])  # 插入到最前面

# 建立臉部遮罩
face_outline_np = np.array([face_outline], dtype=np.int32)
cv2.fillPoly(face_mask, face_outline_np, 255)

# 將圖片轉成 HSV 色彩空間
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 黑眼圈偵測：擴大眼下區域遮罩
eye_mask = np.zeros((h, w), dtype=np.uint8)

# 左眼下方 landmark（向下延伸）
left_eye_indices = [33, 133, 160, 159, 158, 144, 153, 154, 155]
left_eye_region = []
for idx in left_eye_indices:
    lm = landmarks[idx]
    px, py = int(lm.x * w), int(lm.y * h) + 10  # 向下偏移 10px
    left_eye_region.append([px, py])
left_eye_np = np.array([left_eye_region], dtype=np.int32)
cv2.fillPoly(eye_mask, left_eye_np, 255)

# 右眼下方 landmark（向下延伸）
right_eye_indices = [263, 362, 387, 386, 385, 373, 380, 381, 382]
right_eye_region = []
for idx in right_eye_indices:
    lm = landmarks[idx]
    px, py = int(lm.x * w), int(lm.y * h) + 10
    right_eye_region.append([px, py])
right_eye_np = np.array([right_eye_region], dtype=np.int32)
cv2.fillPoly(eye_mask, right_eye_np, 255)

# 套用遮罩並分析暗色區域（放寬 HSV 範圍）
masked_dark = cv2.bitwise_and(hsv, hsv, mask=eye_mask)
dark_mask = cv2.inRange(masked_dark, np.array([0, 0, 0]), np.array([180, 80, 130]))
dark_contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 標記黑眼圈（黑色框）
for cnt in dark_contours:
    if cv2.contourArea(cnt) > 15:
        x, y, ww, hh = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + ww, y + hh), (0, 0, 0), 2)
        cv2.putText(image, "Dark", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

# 痘痘偵測：紅色遮罩 + 臉部遮罩限制
masked_hsv = cv2.bitwise_and(hsv, hsv, mask=face_mask)
red1 = cv2.inRange(masked_hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
red2 = cv2.inRange(masked_hsv, np.array([160, 100, 100]), np.array([180, 255, 255]))
red_mask = cv2.bitwise_or(red1, red2)
red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 標記痘痘（紅色框）
for cnt in red_contours:
    if cv2.contourArea(cnt) > 30:
        x, y, ww, hh = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + ww, y + hh), (0, 0, 255), 2)
        cv2.putText(image, "Acne", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

# 將圖片縮放為 800x800 並顯示結果
resized = cv2.resize(image, (800, 800))
cv2.imshow("Facial Blemish Detection", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()