import os
from time import sleep


def run_case(case, times):
    for i in range(times):
        sleep(30.0)
        print('Now we are running {0}, {1}/{2}'.format(case, i+1, times))
        os.chdir('/home/mininet/mininet/examples')
        os.system('sudo python3 12_hosts_case{0}.py'.format(case))
        # give the machine a break
        
    
if __name__ == '__main__':
    run_case(1, 2)