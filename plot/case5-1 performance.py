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
csv_file = '/home/mininet/mininet/data/case5 performance.csv'  # 请替换为你的CSV文件路径
df = pd.read_csv(csv_file)

line_maker = ['o','v','^','*','>','x','D','s','p']
colors = prop_cycle.by_key()["color"]


# 提取数据
x = df.iloc[:51, 0]  # 第一列作为 x 轴数据
y1 = df.iloc[:51, 1] * 10  # 第二列作为第一个折线的 y 轴数据
y2 = df.iloc[:51, 2] * 10 # 第三列作为第二个折线的 y 轴数据
y3 = df.iloc[:51, 3] * 10 # 第四列作为第三个折线的 y 轴数据
y4 = df.iloc[:51, 4] * 10 # 第四列作为第三个折线的 y 轴数据
y5 = df.iloc[:51, 5] * 10
y6 = df.iloc[:51, 6] * 10
y7 = df.iloc[:51, 7] * 10
y8 = df.iloc[:51, 8] * 10

# 创建折线图
plt.figure(figsize=(16, 6))
plt.ylim(40, 235)

mark_size = 12
line_width = 3
marker_facecolor = 'none'

l1 = plt.plot(x, y1, color=colors[2], label='Host 5', marker='o', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l2 = plt.plot(x, y2, color=colors[0], label='Host 6', marker='^', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l3 = plt.plot(x, y3, color=colors[1], label='Host 7', marker="s", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l4 = plt.plot(x, y4, color=colors[3], label='Host 8', marker="p", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l5 = plt.plot(x, y5, color=colors[4], label='Host 9', marker='>', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l6 = plt.plot(x, y6, color=colors[5], label='Host 10', marker='x', markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l7 = plt.plot(x, y7, color=colors[6], label='Host 11', marker="D", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')
l8 = plt.plot(x, y8, color=colors[7], label='Host 12', marker="s", markersize=mark_size,linewidth=line_width, markerfacecolor=marker_facecolor, linestyle='--')

#plt.plot(x, y1, label='Line 1')
#plt.plot(x, y2, label='Line 2')
#plt.plot(x, y3, label='Line 3')
#plt.plot(x, y4, label='Line 4')

# 添加标签和标题

plt.xticks(fontname="Times New Roman", fontsize=20)
plt.yticks(fontname="Times New Roman", fontsize=20)
plt.xlabel('Times ($\Delta$t)', fontname="Times New Roman", fontsize=25, fontweight="bold")
plt.ylabel('Global Limit Value (Mbps)', fontname="Times New Roman", fontsize=25, fontweight="bold")

#plt.xlabel('X-axis Label')
#plt.ylabel('Y-axis Label')
#plt.title('Line Chart')

# 添加图例
#plt.legend(fontsize = 20)
plt.legend(fontsize=20, frameon=False, prop={"family" : "Times New Roman", 'weight':'bold'})

# add grid
plt.grid(color = 'gainsboro', linestyle = 'dotted', linewidth=line_width)

# plt.savefig("5.2.1-8node-tb.png", format="png", dpi=1200, bbox_inches="tight")
plt.savefig("/home/mininet/mininet/plot/case5-1 performance.pdf", format="pdf", dpi=1200, bbox_inches="tight")

# 保存图表为PDF文件
#pdf_file = './sigcomm-plot/tmp.pdf'  # 请替换为你想要保存的PDF文件路径
#with PdfPages(pdf_file) as pdf:
#    pdf.savefig()
#    plt.close()

#print(f'PDF文件已生成：{pdf_file}')
