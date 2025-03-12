# from PIL import Image, ImageDraw

# # 規劃多個顏色 （參考qis 的分色階層數量 目前大概分10層 從 16~22）

# # 圖片大小和顏色設置
# width, height = 5, 5
# color = (255, 0, 0, 128)  # RGBA 色彩碼：紅色，透明度為 50%

# # 創建透明的紅色圓形圖片
# image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 透明背景
# draw = ImageDraw.Draw(image)
# draw.ellipse((0, 0, width, height), fill=color)

# # 保存圖片為 PNG
# image.save('transparent_red_circle.png')

from PIL import Image, ImageDraw

# 定義分色階層數量和顏色
num_layers = 10
start_red = 50
end_red = 255
color = (255, 0, 0)  # 紅色

# 圖片大小
width, height = 50, 50   #10, 10

# 紅色值步長
red_step = (end_red - start_red) // num_layers

for i in range(num_layers):
    # 計算當前層次的紅色值
    red = start_red + red_step * i
    
    # 創建紅色圓形圖片
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # 透明背景
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, width, height), fill=(red, color[1], color[2], 90))
    
    # 保存圖片為 PNG
    image.save(f'red_circle_{red}.png')