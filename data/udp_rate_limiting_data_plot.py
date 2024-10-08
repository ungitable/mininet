import matplotlib.pyplot as plt
import numpy as np
import csv


def plot_throughput_loss(x, ya1, ya2, yb1, yb2, title, type1, type2):
    fig = plt.figure()
    ax1 = fig.add_subplot()


    ax1.plot(x, ya1, label=type1)
    ax1.plot(x, ya2, label=type2)
    ax1.set_xlabel("time(s)", fontweight='bold', fontsize=14)
    ax1.set_ylabel("throughput(Mbits/sec)", fontweight='bold', fontsize=14)
    ax1.set_ylim(0, 10)
    ax1.tick_params('y')
    ax1.legend(loc='upper left', title='throughput', frameon=False)

    ax2 = ax1.twinx()
    ax2.plot(x, yb1, linestyle='dotted', label=type1)
    ax2.plot(x, yb2, linestyle='dotted', label=type2)
    ax2.set_ylabel("lost(%)", fontweight='bold', fontsize=14)
    ax2.set_ylim(0, 105)
    ax2.tick_params('y')
    ax2.legend(loc='upper right', title='lost', frameon=False)

    plt.title(title, fontweight='bold', fontsize=14)

    # plt.show()
    
    save_path = '/home/mininet/Desktop/' + title + '.jpg'
    plt.savefig(save_path, format='jpg', dpi=300)


def plot_case_0x00_id_0():
    #15&35
    x = np.arange(1,31,1)
    ya1 = [5.19,1.82,1.93,1.86,1.98,1.78,1.91,1.91,1.89,1.99,
           1.83,1.99,1.89,1.79,1.78,1.86,1.82,1.91,1.85,1.81,
           1.91,1.87,1.86,1.87,1.85,1.81,1.98,1.72,1.91,1.87]
    ya2 = [5.06,3.09,3.06,3.13,3.01,3.18,3.09,3.08,3.07,3.00,
           3.10,3.07,3.07,3.19,3.16,3.19,3.09,3.13,3.12,3.13,
           3.09,3.09,3.18,3.02,3.18,3.14,3.06,3.21,3.10,3.09]
    yb1 = [1.8,65,63,65,63,65,64,64,64,62,
           65,62,64,66,66,65,64,65,64,66,
           63,65,64,65,64,66,63,66,64,64]
    yb2 = [3.8,41,42,40,43,39,41,41,41,43,
           41,42,41,39,40,39,41,41,40,40,
           41,41,40,42,40,40,42,39,41,41]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x00_0',
                         type1='mice flow(5M)', type2='mice flow(5M)')


def plot_case_0x00_id_1():
    # 17&37
    x = np.arange(1,31,1)
    ya1 = [5.17,2.03,1.96,1.94,1.95,1.96,1.99,1.91,2.07,1.86,
           1.89,1.95,1.93,2.11,1.87,1.88,1.94,1.87,1.96,1.91,
           1.96,2.02,1.89,2.09,2.06,1.88,2.05,1.73,1.94,1.91]
    ya2 = [5.00,2.98,3.05,2.98,3.01,3.02,3.01,3.03,2.95,3.13,
           3.08,3.03,3.00,2.92,3.10,3.10,3.05,3.07,3.08,3.02,
           3.02,2.95,3.05,2.92,2.96,3.03,2.96,3.20,3.06,3.06]
    
    yb1 = [1.8,61,64,62,63,63,62,64,62,64,
           64,62,63,60,65,64,63,64,63,64,
           63,62,64,61,60,64,61,67,63,64]
    yb2 = [5.3,43,42,43,43,42,43,42,44,40,
           41,42,43,45,41,41,41,42,41,43,
           42,44,42,44,44,42,44,39,42,42]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x00_1',
                         type1='mice flow(5M)', type2='mice flow(5M)')


def plot_case_0x01_id_0():
    # 15&35
    x = np.arange(1,31,1)
    ya1 = [8.13,4.08,4.12,4.10,4.23,4.15,4.27,4.12,4.21,4.23,
           4.16,4.19,4.19,4.27,4.26,4.30,4.17,4.21,4.22,4.22,
           4.21,4.26,4.19,4.29,4.28,4.25,4.21,4.26,4.10,4.22]
    ya2 = [1.93,870,847,858,753,823,729,847,741,788,
           811,811,741,741,694,670,835,764,741,741,
           811,694,776,741,635,764,776,706,870,776]
    
    for i, item in enumerate(ya2):
        if item > 10:
            ya2[i] /= 1024
    
    yb1 = [3.4,51,51,51,50,50,49,51,50,50,
           50,50,50,49,49,49,50,50,50,50,
           50,49,50,49,49,49,50,50,51,50]
    yb2 = [8.4,59,60,60,63,61,65,60,65,63,
           60,61,65,65,67,68,61,64,64,64,
           62,68,62,65,70,64,63,66,59,62]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x01_0', 
                         type1='mice flow(8M)', type2='elephant flow(2M)')


def plot_case_0x01_id_1():
    # 17&37
    x = np.arange(1,31,1)
    ya1 = [8.11,4.16,4.12,4.08,3.96,4.12,4.08,4.07,4.12,4.12,
           4.08,4.08,4.15,4.07,4.02,4.22,4.17,4.09,4.19,4.09,
           4.08,4.09,4.16,4.17,4.13,4.09,4.17,4.15,4.13,4.10]
    ya2 = [1.87,870,870,882,988,882,870,906,894,847,
           906,894,800,953,941,764,776,870,823,894,
           882,906,800,788,894,870,776,882,823,847]
    for i, item in enumerate(ya2):
        if item > 10:
            ya2[i] /= 1024
    
    yb1 = [3.2,50,51,51,53,51,52,51,51,51,
           51,51,51,52,52,50,50,51,50,51,
           51,51,50,50,51,51,50,51,51,51]
    yb2 = [13,58,58,58,53,58,59,57,57,60,
           56,58,60,54,55,64,63,59,61,57,
           58,57,62,62,58,59,63,58,60,60]

    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x01_1',
                         type1='mice flow(8M)', type2='elephant flow(2M)')

def plot_case_0x02_id_0():
    # 15&35
    x = np.arange(1,31,1)
    ya1 = [2.07,412,482,470,553,482,482,353,435,564,
           482,435,506,494,529,388,482,435,482,506,
           553,517,482,588,435,541,447,494,494,435]
    for i, item in enumerate(ya1):
        if item > 10:
            ya1[i] /= 1024

    ya2 = [8.03,4.55,4.48,4.54,4.41,4.50,4.49,4.63,4.50,4.43,
           4.49,4.53,4.48,4.49,4.48,4.56,4.52,4.52,4.48,4.46,
           4.45,4.48,4.46,4.41,4.54,4.47,4.54,4.47,4.45,4.57]
    
    yb1 = [4.9,80,77,78,72,77,77,84,78,73,
           77,80,75,77,76,80,78,78,77,76,
           73,75,77,72,80,74,79,77,76,79]
    yb2 = [4.5,46,47,46,47,46,46,45,46,47,
           46,46,46,46,47,46,46,46,47,47,
           47,47,47,47,46,47,46,47,47,46]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x02_0',
                         type1='mice flow(2M)', type2='elephant flow(8M)')

def plot_case_0x02_id_1():
    # 17&37
    x = np.arange(1,31,1)
    ya1 = [2.08,376,447,553,847,1.29,1.39,1.38,1.51,1.41,
           1.46,1.40,1.38,1.45,1.36,1.48,1.41,1.49,1.48,1.46,
           1.46,1.33,1.46,1.45,1.46,1.35,1.40,1.32,1.43,1.46]
    for i, item in enumerate(ya1):
        if item > 10:
            ya1[i] /= 1024

    ya2 = [8.02,4.61,4.48,4.47,4.02,3.69,3.58,3.63,3.47,3.54,
           3.56,3.56,3.58,3.53,3.59,3.55,3.53,3.48,3.52,3.54,
           3.49,3.66,3.50,3.55,3.55,3.61,3.54,3.69,3.54,3.48]
    
    yb1 = [2.2,82,78,75,57,39,34,35,28,33,
           30,34,34,31,35,30,33,28,30,30,
           30,37,31,31,31,36,32,37,31,30]
    yb2 = [4.6,45,47,47,52,56,57,57,59,58,
           58,58,57,58,57,58,58,59,58,58,
           58,57,58,58,58,57,58,56,58,58]

    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x02_1',
                         type1='mice flow(2M)', type2='elephant flow(8M)')
    
    
def plot_case_0x03_id_0():
    # 15&35
    x = np.arange(1,31,1)
    ya1 = [5.17,2.66,2.62,2.70,2.58,2.76,2.65,2.78,2.63,2.65,
           2.73,2.62,2.66,2.79,2.75,2.74,2.75,1.86,2.65,2.76,
           2.63,2.85,2.78,2.72,2.83,2.66,2.74,2.80,2.66,2.90]
    ya2 = [4.95,2.35,2.30,2.34,2.35,2.22,2.33,2.22,2.35,2.33,
           2.28,2.27,2.32,2.25,2.22,2.21,2.23,3.15,2.27,2.25,
           2.30,2.16,2.15,2.32,2.15,2.32,2.25,2.16,2.32,2.08]
    
    yb1 = [2,49,50,49,51,48,49,48,49,50,
           48,50,49,47,48,48,47,65,50,47,
           50,46,47,48,46,49,48,47,49,45]
    yb2 = [5.6,56,56,55,55,58,56,58,56,55,
           57,56,56,57,58,58,58,39,57,57,
           56,59,59,56,59,56,57,59,56,60]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x03_0',
                         type1='elephant flow(5M)', type2='elephant flow(5M)')
    
    
def plot_case_0x03_id_1():
    # 17&37
    x = np.arange(1,31,1)
    ya1 = [5.17,2.59,2.46,2.43,2.39,2.72,2.47,2.54,2.47,2.52,
           2.59,2.61,2.40,2.42,2.49,2.55,2.52,2.08,2.56,2.61,
           2.43,2.50,2.47,2.40,2.48,2.54,2.28,2.66,2.35,2.41]
    ya2 = [4.97,2.40,2.54,2.50,2.60,2.23,2.52,2.42,2.54,2.49,
           2.40,2.30,2.66,2.56,2.47,2.39,2.45,2.88,2.41,2.39,
           2.54,2.50,2.48,2.61,2.45,2.55,2.56,2.39,2.63,2.49]

    yb1 = [1.6,51,53,54,54,48,53,52,53,52,
           50,50,54,54,53,51,52,60,51,50,
           54,52,53,54,53,53,55,50,54,54]
    yb2 = [5.2,54,52,52,50,57,52,54,51,53,
           54,56,50,50,53,54,53,45,54,55,
           51,53,52,51,53,51,51,55,50,52]
    
    plot_throughput_loss(x, ya1, ya2, yb1, yb2, title='0x03_1',
                         type1='elephant flow(5M)', type2='elephant flow(5M)')

    

if __name__ == '__main__':
    plt.rc('font', family='Times New Roman') 
    plt.rc('font', weight='bold')
    plt.rc('font', size=14)
    plot_case_0x00_id_0()
    plot_case_0x00_id_1()
    plot_case_0x01_id_0()
    plot_case_0x01_id_1()
    plot_case_0x02_id_0()
    plot_case_0x02_id_1()
    plot_case_0x03_id_0()
    plot_case_0x03_id_1()

    pass