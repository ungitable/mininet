import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from turtle import color
from matplotlib import rcParams

config = {
    "font.family":'serif',
    "font.size": 20,
    "mathtext.fontset":'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)

prop_cycle = plt.rcParams["axes.prop_cycle"]
colors = prop_cycle.by_key()["color"]

# 读取CSV文件
csv_file = '/home/mininet/mininet/data/case6 jfi.csv'  # 请替换为你的CSV文件路径
df = pd.read_csv(csv_file)

line_maker = ['o','v','^','*','>','x','D','s','p']
colors = prop_cycle.by_key()["color"]


# 提取数据
x = df.iloc[:51, 0]  # 第一列作为 x 轴数据
y1 = df.iloc[:51, 1]  # 第二列作为第一个折线的 y 轴数据
y2 = df.iloc[:51, 2]  # 第三列作为第二个折线的 y 轴数据
# y3 = df.iloc[:, 3]  # 第四列作为第三个折线的 y 轴数据
# y4 = df.iloc[:, 4]  # 第四列作为第三个折线的 y 轴数据
# y5 = df.iloc[:, 5]  # 第四列作为第三个折线的 y 轴数据
# y6 = df.iloc[:, 6]  # 第四列作为第三个折线的 y 轴数据


# 创建折线图
plt.figure(figsize=(8, 6))
plt.ylim(0.25, 1.05)

mark_size = 12
line_width = 3
marker_facecolor = 'none'

l1 = plt.plot(x, y1, color=colors[2], label='Group 1', marker='o', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)
l2 = plt.plot(x, y2, color=colors[0], label='Group 2', marker='^', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)
# l3 = plt.plot(x, y3, color=colors[1], label='C3PDAG-20node-di4', marker="s", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)
# l4 = plt.plot(x, y4, color=colors[3], label='C3P-20node-di4', marker="p", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)
# l5 = plt.plot(x, y5, color=colors[4], label='C3PDAG-30node-di4', marker="x", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)
# l6 = plt.plot(x, y6, color=colors[5], label='C3P-30node-di4', marker="*", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor)

#plt.plot(x, y1, label='Line 1')
#plt.plot(x, y2, label='Line 2')
#plt.plot(x, y3, label='Line 3')
#plt.plot(x, y4, label='Line 4')

# 添加标签和标题

plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)
plt.xlabel('Times ($\Delta$t)', fontname="Times New Roman", fontsize=25, fontweight="bold")
plt.ylabel('JFI(P(t))', fontname="Times New Roman", fontsize=25, fontweight="bold")

#plt.xlabel('X-axis Label')
#plt.ylabel('Y-axis Label')
#plt.title('Line Chart')

# 辅助线
plt.axhline(y=0.90, color='r', linestyle='--')
plt.text(plt.xlim()[1], 0.90, 'P90', color='r', verticalalignment='center', backgroundcolor='white', fontsize=12)
plt.axhline(y=0.95, color='r', linestyle='--')
plt.text(plt.xlim()[1], 0.95, 'P95', color='r', verticalalignment='center', backgroundcolor='white', fontsize=12)
plt.axhline(y=0.99, color='r', linestyle='--')
plt.text(plt.xlim()[1], 0.99, 'P99', color='r', verticalalignment='center', backgroundcolor='white', fontsize=12)

# 添加图例
#plt.legend(fontsize = 20)
plt.legend(fontsize=20, frameon=False, prop={"family" : "Times New Roman", 'weight':'bold'})

# add grid
plt.grid(color = 'gainsboro', linestyle = 'dotted', linewidth=line_width)

# plt.savefig("./sigcomm-plot/5.2.2-2030node-46tb.png", format="png", dpi=1200, bbox_inches="tight")
plt.savefig("/home/mininet/mininet/plot/case6 jfi.pdf", format="pdf", dpi=1200, bbox_inches="tight")

# 保存图表为PDF文件
#pdf_file = './sigcomm-plot/tmp.pdf'  # 请替换为你想要保存的PDF文件路径
#with PdfPages(pdf_file) as pdf:
#    pdf.savefig()
#    plt.close()

#print(f'PDF文件已生成：{pdf_file}')
