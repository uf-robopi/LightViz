import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 定义起始颜色和终止颜色
start_color = [50, 0, 0]
end_color = [255, 0, 0]

# 定义色条的分段
segments = 256  # 256个颜色段

# 生成颜色列表
colors = np.zeros((segments, 3))
for i in range(3):
    colors[:, i] = np.linspace(start_color[i], end_color[i], segments) / 255

# 创建颜色映射
cmap = LinearSegmentedColormap.from_list('custom_red', colors)

# 绘制色条，使其垂直显示并反转方向
gradient = np.linspace(1, 0, segments)
gradient = np.vstack((gradient, gradient))
gradient = np.rot90(gradient)
plt.figure(figsize=(1.8, 3)) 
plt.imshow(gradient, aspect=0.1, cmap=cmap)
plt.xticks([])  # 去除 x 轴刻度
plt.yticks(np.linspace(0, 255, 7), np.linspace(22, 16, 7, dtype=int))  # 去除 y 轴刻度
plt.title('SQM (mag/arcsec2)')
# plt.gca().invert_yaxis()  # 反转y轴，使色条从下到上渐变

# plt.show()
plt.savefig('custom_colorbar.png')  # 保存为PNG格式，设置dpi和边界框

