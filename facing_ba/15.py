import cv2  # OpenCV：影像處理
import mediapipe as mp  # MediaPipe：臉部特徵點偵測
import numpy as np  # NumPy：陣列與遮罩處理

# 圖片路徑
# 請確保此路徑是正確的！
image_path = r"C:\Users\isach\Downloads\IMG_4093.png"

# 讀取圖片
image = cv2.imread(image_path)
if image is None:
    print("圖片載入失敗，請檢查路徑是否正確")
    exit()
h, w = image.shape[:2]  # 取得圖片尺寸

# 初始化 MediaPipe 臉部網格偵測器
mp_face_mesh = mp.solutions.face_mesh
# 啟用 refine_landmarks=True 可以提高眼睛和嘴唇周圍特徵點的準確性
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)

# 將圖片轉成 RGB 並進行臉部偵測
results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
if not results.multi_face_landmarks:
    print("未偵測到臉部")
    exit()
landmarks = results.multi_face_landmarks[0].landmark  # 取得第一張臉的 landmark 資料

# --- 臉部遮罩 (與原程式碼相同，用於限制痘痘偵測範圍) ---
face_mask = np.zeros((h, w), dtype=np.uint8)  # 建立空白遮罩
face_outline = []

# 使用下巴輪廓 landmark index（0–16）
for idx in range(0, 17):
    lm = landmarks[idx]
    px, py = int(lm.x * w), int(lm.y * h)
    face_outline.append([px, py])

# 額頭補點（簡單向上延伸）
# 為了避免遮罩邊緣被當作瑕疵，我們可以讓額頭線條更平滑或使用更多點
# 這裡維持您原來的簡單延伸方式
forehead = [
    [face_outline[0][0], face_outline[0][1] - 60],
    [face_outline[-1][0], face_outline[-1][1] - 60]
]
# 組合臉部輪廓點位 (從下巴一側到另一側)
# 修正輪廓點位組合的邏輯，確保它是一個封閉且順時針/逆時針的環
face_outline_complete = [face_outline[0]] + forehead + [face_outline[-1]]
# 逆序加入下巴其他點 (避免重覆 0 和 16 號點)
for i in range(len(face_outline) - 2, 0, -1):
    face_outline_complete.append(face_outline[i])

face_outline_np = np.array([face_outline_complete], dtype=np.int32)
cv2.fillPoly(face_mask, face_outline_np, 255)  # 將輪廓填入遮罩
# --- 臉部遮罩結束 ---

# 將圖片轉成 HSV 色彩空間
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 套用遮罩，只分析臉部區域
masked_hsv = cv2.bitwise_and(hsv, hsv, mask=face_mask)

# -------------------------------------------
# --- 黑眼圈偵測 (改良：使用眼下區域遮罩) ---
# -------------------------------------------

# 定義眼睛周圍的特徵點索引 (以 MediaPipe Face Mesh 的 FACEMESH_LEFT_EYE 舉例)
# 由於 FACEMESH_LEFT_EYE/RIGHT_EYE 是連接點的集合，我們需要從中提取出構成眼下區域的點。
# 這裡我們使用一個包含眼下輪廓點的近似集合（需要參考 MediaPipe Face Mesh 的點位圖）
# 參考 MediaPipe 官方 Face Mesh 點位圖，眼睛下方大致輪廓點：
LEFT_EYE_LOWER_CONTOUR = [374, 380, 381, 382, 385, 386, 387, 388, 390, 398, 461, 462, 463, 464, 465, 466, 467, 468]  # 左眼下方
RIGHT_EYE_LOWER_CONTOUR = [145, 153, 154, 155, 157, 158, 159, 160, 161, 163, 243, 244, 245, 246, 247, 249, 252, 253] # 右眼下方

# --- 建立左眼黑眼圈區域遮罩 ---
left_eye_mask = np.zeros((h, w), dtype=np.uint8)
left_eye_points = []
for idx in LEFT_EYE_LOWER_CONTOUR:
    if idx < len(landmarks):
        lm = landmarks[idx]
        px, py = int(lm.x * w), int(lm.y * h)
        left_eye_points.append([px, py])

# 為了包含眼睛下方的黑眼圈區域，我們將輪廓點向下延伸並閉合
if len(left_eye_points) > 2:
    left_eye_points_np = np.array([left_eye_points], dtype=np.int32)
    # 填充眼下輪廓 (注意：這裡的點位需要閉合形成一個區域，可能需要手動增加點位來閉合)
    # 簡單起見，我們使用凸包 (Convex Hull) 來近似眼下區域
    hull_left = cv2.convexHull(left_eye_points_np)
    # 稍微向下平移填充區域 (近似黑眼圈位置)
    hull_left_shifted = hull_left.copy()
    hull_left_shifted[:, 0, 1] += 10 # 向下平移 10 像素
    cv2.fillConvexPoly(left_eye_mask, hull_left_shifted, 255)

# --- 建立右眼黑眼圈區域遮罩 ---
right_eye_mask = np.zeros((h, w), dtype=np.uint8)
right_eye_points = []
for idx in RIGHT_EYE_LOWER_CONTOUR:
    if idx < len(landmarks):
        lm = landmarks[idx]
        px, py = int(lm.x * w), int(lm.y * h)
        right_eye_points.append([px, py])

if len(right_eye_points) > 2:
    right_eye_points_np = np.array([right_eye_points], dtype=np.int32)
    hull_right = cv2.convexHull(right_eye_points_np)
    # 稍微向下平移填充區域 (近似黑眼圈位置)
    hull_right_shifted = hull_right.copy()
    hull_right_shifted[:, 0, 1] += 10 # 向下平移 10 像素
    cv2.fillConvexPoly(right_eye_mask, hull_right_shifted, 255)

# 合併兩眼下的遮罩
eye_region_mask = cv2.bitwise_or(left_eye_mask, right_eye_mask)

# 黑眼圈偵測：建立低亮度遮罩（暗沉區域）
# 針對暗沉膚色的 HSV 範圍：低飽和度 (S < 80) 和低亮度 (V < 120)
# 這裡嘗試調整範圍：H 任意 (0-180), S 較低 (0-70), V 較低 (0-110)
dark_mask = cv2.inRange(masked_hsv, np.array([0, 0, 0]), np.array([180, 70, 110]))

# 只保留在眼下區域的低亮度區域
masked_dark_circles = cv2.bitwise_and(dark_mask, dark_mask, mask=eye_region_mask)

# 找出輪廓
dark_contours, _ = cv2.findContours(masked_dark_circles, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 在圖片上標記黑眼圈區域（黑色框框）
for cnt in dark_contours:
    # 過濾太小的區域 (閾值根據實際測試調整，例如 50)
    if cv2.contourArea(cnt) > 50:
        x, y, ww, hh = cv2.boundingRect(cnt)
        # 標記為深藍色 (或深色)
        cv2.rectangle(image, (x, y), (x + ww, y + hh), (139, 0, 0), 2)  # 深藍色
        cv2.putText(image, "Dark_Circle", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (139, 0, 0), 1)

# -------------------------------------------
# --- 痘痘偵測 (維持原程式碼邏輯，但使用臉部遮罩) ---
# -------------------------------------------

# 痘痘偵測：建立紅色遮罩（紅色分兩段）
red1 = cv2.inRange(masked_hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))  # 紅色區段1 (H: 0-10)
red2 = cv2.inRange(masked_hsv, np.array([160, 100, 100]), np.array([180, 255, 255]))  # 紅色區段2 (H: 160-180)
red_mask = cv2.bitwise_or(red1, red2)  # 合併紅色遮罩

# 僅在臉部遮罩範圍內尋找紅色區域
masked_red = cv2.bitwise_and(red_mask, red_mask, mask=face_mask)

# 找出紅色輪廓
red_contours, _ = cv2.findContours(masked_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 在圖片上標記痘痘區域（紅色框框）
for cnt in red_contours:
    # 過濾太小的紅點 (閾值根據實際測試調整，例如 30)
    if cv2.contourArea(cnt) > 30:
        x, y, ww, hh = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + ww, y + hh), (0, 0, 255), 2)  # 紅色
        cv2.putText(image, "Acne", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

# 將圖片縮放為 800x800 並顯示結果
resized = cv2.resize(image, (800, 800))  # 統一尺寸
cv2.imshow("Facial Blemish Detection", resized)  # 顯示結果
cv2.waitKey(0)
cv2.destroyAllWindows()