# #基本妝容
# style="韓系妝"
# color="珊瑚粉"
# print("我想分析的妝容是:",style)
# print("這個妝容主打的色系是:",color)

# #妝容風格判斷
# style=input("請輸入想分析的妝容風格(日系妝,韓系妝,歐美妝,泰系妝):")
# if style=="日系妝":
#     print("底妝打造自然清透感，眼妝推薦使用暖色系")
# elif style=="韓系妝":
#     print("底妝打造清透水光肌，眼妝減少色彩，重點在眼尾和臥蠶")
# elif style=="歐美妝":
#     print("底妝保留一些瑕疵突出原生感，眼妝加深眼窩打造深邃立體感")
# elif style=="泰系妝":
#     print("底妝貼合膚色注重立體感，眼妝突出下睫毛，睫毛濃密有毛茸感")
# else:
#     print("目前暫無此妝容，敬啟期待!")

#推薦色塊
# makeup_styles={
#     "日系妝": "蜜桃粉、珊瑚橘",
#     "韓系妝": "珊瑚粉、乾玫瑰色",
#     "歐美妝": "暖棕色、酒紅色",
#     "泰系妝": "焦糖橘、古銅棕"
# }
# print("歡迎使用妝容分析系統!")
# style=input("輸入想分析的妝容色系:")
# if style in makeup_styles:
#     print("推薦的色系是:"+makeup_styles[style])
# else:
#     print("目前尚未有此妝容，敬啟期待!")

# 10/10
#建立資料(list/dict)
# makeup_styles={
#     "日系妝": ["蜜桃粉", "珊瑚橘"],
#     "韓系妝": ["珊瑚粉", "乾玫瑰色"],
#     "歐美妝": ["暖棕色",  "酒紅色"],
#     "泰系妝": ["焦糖橘", "古銅棕"]
# }
# print(makeup_styles["日系妝"][0]) #取出日系妝色塊

# #巢狀條件判斷邏輯
# tone=input("妝容濃淡(自然/濃郁):") 
# color=input("偏好色調(粉色系/橘色系/棕色系):")

# def new_func():
#     style="泰系妝"

# if tone=="自然":
#     if color=="粉色系":
#         style="韓系妝"

#     elif color=="橘色系":
#         style="日系妝"
#     else:
#         style="日系妝" #日系妝偏自然

# else:
#     if color=="粉色系":
#         style="歐美妝"
#     elif color=="橘色系":
#         style="泰系妝"
#     else:
#         style="歐美妝"

# print(f"妝容推薦風格:{style}")

# #函式(function)
# def recommend_style(color,tone):
#     "根據色調和濃淡推薦妝容風格"
#     if tone=="自然":
#         if color=="粉色系":
#             style="韓系妝"
#         elif color=="橘色系":
#             style="日系妝"
#         else:
#             style="日系妝"

#     else:
#         if tone=="粉色系":
#             style="歐美妝"
#         elif tone=="橘色系":
#             style="泰系妝"
#         else:
#             style="歐美妝"
#     return style

#整合輸入，查找，輸出
#妝容資料庫
# makeup_styles={
#     "日系妝": ["蜜桃粉", "珊瑚橘"],
#     "韓系妝": ["珊瑚粉", "乾玫瑰色"],
#     "歐美妝": ["暖棕色",  "酒紅色"],
#     "泰系妝": ["焦糖橘", "古銅棕"]
# }
# def recommend_style(color,tone):
#     if tone=="自然":
#         if color=="粉色系":
#             return "韓系妝"
#         elif color=="橘色系":
#             return "日系妝"
#         else:
#             return "日系妝"
#     else:
#         if tone=="粉色系":
#             return "歐美妝"
#         elif tone=="橘色系":
#             return "泰系妝"
#         else:
#             return "歐美妝"
    
# #主程式
# print("妝容風格推薦系統")
# color=input("選擇偏好色調(粉色系/橘色系/棕色系):")
# tone=input("妝容濃淡(自然/濃郁):")
# style=recommend_style(color,tone)
# print(f"推薦妝容風格:{style}")
# print(f"推薦色系:{','.join(makeup_styles[style])}")

# 10/21
{
    # 主分類
  "makeup_styles": {
    "日系妝": {
    # 主要色塊
      "main_colors": ["蜜桃粉", "珊瑚橘", "奶茶色"],
    #  色調族群
      "tone_family": "暖粉調",
    #  底妝特性
      "base_style": "輕透自然",
    #  風格標籤 
      "keywords": ["清新", "柔和", "自然光感"],
    #   建議用法
      "suggested_use": {
        "eye": "柔霧橘粉眼影，少量暈染",
        "cheek": "蜜桃粉腮紅",
        "lip": "珊瑚粉潤澤唇"
      }
    },
    "韓系妝": {
      "main_colors": ["豆沙粉", "珊瑚粉", "乾玫瑰色"],
      "tone_family": "粉棕調",
      "base_style": "水光亮澤",
      "keywords": ["甜美", "透亮", "乾淨"],
      "suggested_use": {
        "eye": "粉棕眼影漸層，搭配淺眼線",
        "cheek": "乾玫瑰色腮紅",
        "lip": "豆沙粉漸層唇"
      }
    },
    "歐美妝": {
      "main_colors": ["暖棕色", "金銅色", "酒紅色"],
      "tone_family": "暖棕調",
      "base_style": "霧面立體",
      "keywords": ["性感", "強烈", "修容明顯"],
      "suggested_use": {
        "eye": "深色暈染眼影搭配金屬光澤",
        "cheek": "陰影修容與高光",
        "lip": "酒紅或霧面裸棕色唇"
      }
    },
    "泰系妝": {
      "main_colors": ["焦糖橘", "玫瑰金", "古銅棕"],
      "tone_family": "金橘調",
      "base_style": "光澤立體",
      "keywords": ["異國感", "艷麗", "陽光"],
      "suggested_use": {
        "eye": "金橘眼影＋亮片層次",
        "cheek": "古銅色修容腮紅",
        "lip": "玫瑰金或橘棕潤澤唇"
      }
    }
  },
#   資料說明
  "metadata": {
    "version": "0.1-draft",
    "created_by": "Hsieh Chia Hsuan (Iris)",
    "description": "妝容風格與色塊對應規則 Placeholder，提供給核心AI模組測試使用"
  }
}

# 測試python帶入
import json

# 讀取 JSON 規則（假設儲存為 makeup_rules.json）
with open("makeup_rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

# 測試存取
style = "韓系妝"
print("風格名稱：", style)
print("主打色：", ", ".join(rules["makeup_styles"][style]["main_colors"]))
print("風格關鍵字：", ", ".join(rules["makeup_styles"][style]["keywords"]))
print("建議唇色：", rules["makeup_styles"][style]["suggested_use"]["lip"])
