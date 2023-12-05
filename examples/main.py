import os
from time import sleep
import time


def run_case(case, times):
    for i in range(times):
        sleep(10.0)
        print('\nNow we are running {0}, {1}/{2}'.format(case, i+1, times))
        os.chdir('/home/mininet/mininet/examples')
        os.system('sudo python3 12_hosts_case{0}.py'.format(case))

def run_case_no_intervention(case, times):
    for i in range(times):
        sleep(10.0)
        print('\nNow we are running {0}, {1}/{2}'.format(case, i+1, times))
        os.chdir('/home/mininet/mininet/examples')
        os.system('sudo python3 12_hosts_case{0}_no_intervention.py'.format(case))
        
    
if __name__ == '__main__':
    start_time = time.time()
    
    for i in range(1, 1+1):
        run_case(i, 1)
        
    # for j in range(5, 6+1):
    #     run_case(j, 1)
    #     run_case_no_intervention(j, 1)
        
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"程序运行时间：{execution_time}秒")
