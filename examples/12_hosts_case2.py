#!/usr/bin/env python

import os
from time import sleep
import numpy as np
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from threading import Thread
import matplotlib.pyplot as plt
from get_lost import Lost


def cmd_client(host, dst_host, port, flow_type, rate):
    flow = ''
    
    if flow_type == 'udp':
        flow = '-u'

    filename = str(host) + 'client' + str(port) + '.out'
    host.cmd( 'iperf3  ' + flow + ' -c ' + str(dst_host.IP()) + ' -p ' + str(port) + 
             ' -b ' + str(rate) + 'M -i 1 -t 5 ' \
             ' >> /home/mininet/Desktop/c3p/' + filename + ' & ')
    
def cmd_server(host, port):
    filename = str(host) + 'server' + str(port) + '.out'
    output_file = '/home/mininet/Desktop/c3p/' + filename
    cmd = 'iperf3  -s -i 1 -p ' + str(port) + ' >> /home/mininet/Desktop/c3p/' + filename + \
    ' & '
    host.cmd(cmd)

def turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12):
    h1.cmd('ethtool -K h1-eth0 tx off')
    h2.cmd('ethtool -K h2-eth0 tx off')
    h3.cmd('ethtool -K h3-eth0 tx off')
    h4.cmd('ethtool -K h4-eth0 tx off')
    h5.cmd('ethtool -K h5-eth0 tx off')
    h6.cmd('ethtool -K h6-eth0 tx off')
    h7.cmd('ethtool -K h7-eth0 tx off')
    h8.cmd('ethtool -K h8-eth0 tx off')
    h9.cmd('ethtool -K h9-eth0 tx off')
    h10.cmd('ethtool -K h10-eth0 tx off')
    h11.cmd('ethtool -K h11-eth0 tx off')
    h12.cmd('ethtool -K h12-eth0 tx off')

def clear_directory(directory):
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            os.remove(path)
    # print('fininshed')


def myNetwork():

    # ryu location
    # /usr/lib/python3/dist-packages/ryu/app
    
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    # info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    # info( '*** Add switches\n')
    # UserSwitch, OVSKernelSwitch
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002')

    # info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None,)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None,)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None,)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None,)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None,)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None,)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None,)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None,)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None,)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None,)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None,)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None,)

    
    # info( '*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)
    net.addLink(s2, h5) # net.addLink(s2, h5, cls=TCLink, bw = 10)
    net.addLink(s2, h6)
    net.addLink(s2, h7)
    net.addLink(s2, h8)
    net.addLink(s1, s2)
    net.addLink(s2, h9)
    net.addLink(s2, h10)
    net.addLink(s2, h11)
    net.addLink(s2, h12)


    info( '*** Starting network\n')
    net.build()

    # starting controllers
    for controller in net.controllers:
        controller.start()

    # starting switches
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    info( '*** Testing connectivity of all hosts\n')
    net.pingAll()

    # clear files in targeted directory
    directory = '/home/mininet/Desktop/c3p'
    clear_directory(directory)

    output = c0.cmd('ovs-vsctl set bridge s1 datapath_type=netdev; \
                    ovs-vsctl set bridge s1 protocols=OpenFlow13; \
                    ovs-vsctl set bridge s2 datapath_type=netdev; \
                    ovs-vsctl set bridge s2 protocols=OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=2,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.5,action=meter:2,output:1" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=3,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.6,action=meter:3,output:2" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=4,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.7,action=meter:4,output:3" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=5,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.8,action=meter:5,output:4" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=6,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.9,action=meter:6,output:6" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=7,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.10,action=meter:7,output:7" -O OpenFlow13; \
                   \
                    ovs-ofctl add-meter s2 "meter=8,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.11,action=meter:8,output:8" -O OpenFlow13; \
                   \
                    ovs-ofctl add-meter s2 "meter=9,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.12,action=meter:9,output:9" -O OpenFlow13; \
                    \
                    '.format(10*1024))
    # print(output)


    turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12) # this commmend is incredibly important

    sleep(3.0)

    servers = []
    servers.append(Thread(target=cmd_server, args=(h5, 5105)))
    servers.append(Thread(target=cmd_server, args=(h6, 5206)))
    servers.append(Thread(target=cmd_server, args=(h7, 5307)))
    servers.append(Thread(target=cmd_server, args=(h8, 5408)))

    servers.append(Thread(target=cmd_server, args=(h9, 5109)))
    servers.append(Thread(target=cmd_server, args=(h10, 5210)))
    servers.append(Thread(target=cmd_server, args=(h11, 5311)))
    servers.append(Thread(target=cmd_server, args=(h12, 5412)))
    

    for server in servers:
        server.start()
        sleep(0.1)

    
    # h1 and h2 send elephant flows
    speed_host12 = 10
    flow_host12 = 'udp'
    # h3 and h4 send mice flows
    speed_host34 = 10
    flow_host34 = 'udp'

    clients = []
    clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h3, h7, 5307, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h2, h6, 5206, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h4, h8, 5408, flow_host34, speed_host34)))

    clients.append(Thread(target=cmd_client, args=(h1, h9, 5109, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h3, h11, 5311, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h2, h10, 5210, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h4, h12, 5412, flow_host34, speed_host34)))

    for client in clients:
        client.start()
        sleep(0.03) 

    
    lost_obj = Lost()
    losts = []

    limit = []
    for i in range(8):
        limit.append(10.0)

    limits = []
    res_limit = []
    for l in limit:
        res_limit.append(l)
    limits.append(res_limit)

    coefficient = 1


    for i in range(1, 41):
        
        sleep(6.0) # x.1 is accpetable

        # get lost
        # format: lost / total

        lost5105, total5105 = lost_obj.get_rate(h5, 5105)
        lost5109, total5109 = lost_obj.get_rate(h9, 5109)
        lost5206, total5206 = lost_obj.get_rate(h6, 5206)
        lost5210, total5210 = lost_obj.get_rate(h10, 5210)
        lost5307, total5307 = lost_obj.get_rate(h7, 5307)
        lost5311, total5311 = lost_obj.get_rate(h11, 5311)
        lost5408, total5408 = lost_obj.get_rate(h8, 5408)
        lost5412, total5412 = lost_obj.get_rate(h12, 5412)

        if i > 8:
            one_piece = total5109 / 4
            total5109 = total5109 - one_piece
            lost5109 = lost5109 - one_piece

        lost_rate_h5 = lost5105 / total5105
        lost_rate_h6 = lost5206 / total5206
        lost_rate_h7 = lost5307 / total5307
        lost_rate_h8 = lost5408 / total5408
        lost_rate_h9 = lost5109 / total5109
        lost_rate_h10 = lost5210 / total5210
        lost_rate_h11 = lost5311 / total5311
        lost_rate_h12 = lost5412 / total5412


        temp_list = [i, lost_rate_h5, lost_rate_h6, lost_rate_h7, lost_rate_h8,
                     lost_rate_h9, lost_rate_h10, lost_rate_h11, lost_rate_h12,]
        print(temp_list)
        losts.append(temp_list)
        

        # update limiting rate
        lost_list = [lost_rate_h5, lost_rate_h6, lost_rate_h7, lost_rate_h8,
                     lost_rate_h9, lost_rate_h10, lost_rate_h11, lost_rate_h12,]
        

        # use c3p strategy independently
        # for hosts ranging from h5 to h8
        for h in range(0, 4):
            left = (h+4-1) % 4
            right = (h+1) % 4
            lost_sum = lost_list[h] * 2 - lost_list[left] - lost_list[right]
            limit[h] = limit[h] + coefficient * lost_sum

        # for hosts ranging from h9 to h12
        for h in range(4, 8):
            t = h - 4
            left = (t+4-1) % 4 + 4
            right = (t+1) % 4 + 4
            lost_sum = lost_list[h] * 2 - lost_list[left] - lost_list[right]
            limit[h] = limit[h] + coefficient * lost_sum
     
        print(limit)
        print()
        res_limit = []
        for l in limit:
            res_limit.append(l)
        limits.append(res_limit)
        
        
        # update limitation of flow speed in hosts ranging from h5 to h8

        for j in range(8):
            command = 'ovs-ofctl mod-meter s2 "meter={},kbps,burst,band=type=drop,rate={},burst_size={}" -O OpenFlow13; \
                        '.format(j+2, int(limit[j]*1024), 100)
            
            output = c0.cmd(command)
            # print(output)


        # limit the speed of elephant flows
        if i == 8:
            print('elephant flow limiting begins')
            '''
            h1 -> h9
            h1 -> h10
            h2 -> h11
            h2 -> h12
            '''
            output = c0.cmd('ovs-ofctl add-meter s1 "meter=20,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.1,nw_dst=10.0.0.5,action=meter:20,output:5" -O OpenFlow13; \
                            \
                            ovs-ofctl add-meter s1 "meter=21,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.2,nw_dst=10.0.0.6,action=meter:21,output:6" -O OpenFlow13; \
                        '.format(30*1024))
            print(output)


        clients = []
        if i < 5:
            clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, speed_host12)))
            clients.append(Thread(target=cmd_client, args=(h1, h9, 5109, flow_host12, speed_host12)))
            clients.append(Thread(target=cmd_client, args=(h2, h6, 5206, flow_host12, speed_host12)))
            clients.append(Thread(target=cmd_client, args=(h2, h10, 5210, flow_host12, speed_host12)))
        else:
            clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, 40)))
            clients.append(Thread(target=cmd_client, args=(h1, h9, 5109, flow_host12, 40)))
            clients.append(Thread(target=cmd_client, args=(h2, h6, 5206, flow_host12, 20)))
            clients.append(Thread(target=cmd_client, args=(h2, h10, 5210, flow_host12, 20)))

        clients.append(Thread(target=cmd_client, args=(h3, h7, 5307, flow_host34, speed_host34)))
        clients.append(Thread(target=cmd_client, args=(h4, h8, 5408, flow_host34, speed_host34)))

        clients.append(Thread(target=cmd_client, args=(h3, h11, 5311, flow_host34, speed_host34)))
        clients.append(Thread(target=cmd_client, args=(h4, h12, 5412, flow_host34, speed_host34)))


        for client in clients:
            client.start()
            sleep(0.03) # cannot set sleeptime = 0, idealy 0.1s

    print('experiment ended.')


    # expand limits 10 times
    for i in range(len(limits)):
        for j in range(len(limits[i])):
            limits[i][j] = limits[i][j] * 10


    # calculate avg & std
    avg1 = []
    std1 = []
    avg2 = []
    std2 = []

    for k in range(len(limits)):
        arr1 = limits[k][0:4]
        arr2 = limits[k][4:]

        arr1_mean = np.mean(arr1)
        arr1_std = np.std(arr1)
        arr2_mean = np.mean(arr2)
        arr2_std = np.std(arr2)
        # print(arr, arr_mean, arr_std)

        avg1.append(arr1_mean)
        std1.append(arr1_std)
        avg2.append(arr2_mean)
        std2.append(arr2_std)

    print('avg1:', avg1)
    print('std1:', std1)
    print('avg2:', avg2)
    print('std2:', std2)


    # plot 8 hosts limits
    num_nodes = len(limits[0])
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

    plt.figure(figsize=(10, 6))

    for i in range(num_nodes):
        node_values = [sublist[i] for sublist in limits]
        plt.plot(range(1, len(limits) + 1), node_values, color=colors[i], label='Node {}'.format(i+5))

    plt.xlabel('Rounds')
    plt.ylabel('Values')
    plt.title('Node Values')
    plt.legend()

    plt.tight_layout()
    plt.savefig('/home/mininet/Desktop/pic/case2_plot1.png')
    plt.show()
        

    # plot JFI
    jfi1 = []
    jfi2 = []

    for k in range(len(losts)):
        arr1 = losts[k][1:5]
        arr2 = losts[k][5:]

        # for group1
        numerator = np.sum(arr1) ** 2
        denominator = len(arr1) * sum([x**2 for x in arr1])
        jfi1.append(numerator/denominator)

        # for group2
        numerator = np.sum(arr2) ** 2
        denominator = len(arr2) * sum([x**2 for x in arr2])
        jfi2.append(numerator/denominator)

    print('jfi1:', jfi1)
    print('jfi2:', jfi2)

    plt.figure(figsize=(10, 6))

    plt.plot(range(1, len(jfi1) + 1), jfi1, color='blue', label='Group 1')
    plt.plot(range(1, len(jfi2) + 1), jfi2, color='red', label='Group 2')

    plt.xlabel('Rounds')
    plt.ylabel('Values')
    plt.title('Group 1 and Group 2 Values')
    plt.legend()

    plt.savefig('/home/mininet/Desktop/pic/case2_plot2.png')
    plt.show()

    
    CLI(net)

    net.stop()

    # clear the network topology, switches and hosts 
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
