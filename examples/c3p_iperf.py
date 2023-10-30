#!/usr/bin/env python

import os
from time import sleep
from mininet.examples.popen import monitorhosts
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from subprocess import call
from threading import Thread
from get_lost import Lost
import subprocess


def cmd_client(host, dst_host, port, flow_type, rate):
    flow = ''
    
    if flow_type == 'udp':
        flow = '-u'

    filename = str(host) + 'client' + str(port) + '.out'
    host.cmd( 'iperf3  ' + flow + ' -c ' + str(dst_host.IP()) + ' -p ' + str(port) + 
             ' -b ' + str(rate) + 'M -i 1 -t 15 ' \
             ' > /home/mininet/Desktop/c3p/' + filename + ' & ')
    
def cmd_server(host, port):
    filename = str(host) + 'server' + str(port) + '.out'
    output_file = '/home/mininet/Desktop/c3p/' + filename
    cmd = 'nohup iperf3  -s -i 1 -p ' + str(port) + ' > /home/mininet/Desktop/c3p/' + filename + \
    ' 2>&1 & '
    host.cmd(cmd)

    # process = host.popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # while True:
    #     output_line = process.stdout.readline().decode().strip()
    #     if output_line:
    #         print(output_line)
    #     else:
    #         print('error')

    #     # 检查主机进程是否已结束
    #     if process.poll() is not None:
    #         break

    #     # 延迟1秒
    #     time.sleep(1)


def set_normal_policing(controller, rate):
    port = 's2-eth5'
    cmd_policing_rate = "ovs-vsctl set interface {0} ingress_policing_rate={1}".format(
        port, rate)
    controller.cmd(cmd_policing_rate)

def turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8):
    h1.cmd('ethtool -K h1-eth0 tx off')
    h2.cmd('ethtool -K h2-eth0 tx off')
    h3.cmd('ethtool -K h3-eth0 tx off')
    h4.cmd('ethtool -K h4-eth0 tx off')
    
    h5.cmd('ethtool -K h5-eth0 tx off')
    h6.cmd('ethtool -K h6-eth0 tx off')
    h7.cmd('ethtool -K h7-eth0 tx off')
    h8.cmd('ethtool -K h8-eth0 tx off')


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

    # get instances of controller, switches and hosts
    c0 = net.get('c0')
    s1, s2 = net.get('s1', 's2')
    h1, h2, h3, h4, h5, h6, h7, h8 = net.get('h1', 'h2', 'h3', 'h4', 
                                             'h5', 'h6', 'h7', 'h8')

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


    sleep(0)

    servers = []
    servers.append(Thread(target=cmd_server, args=(h5, 5015,)))

    # servers.append(Thread(target=cmd_server, args=(h6, 5026,)))
    # servers.append(Thread(target=cmd_server, args=(h7, 5017,)))
    # servers.append(Thread(target=cmd_server, args=(h8, 5048,)))
    # servers.append(Thread(target=cmd_server, args=(h5, 5035,)))
    # servers.append(Thread(target=cmd_server, args=(h6, 5046,)))
    # servers.append(Thread(target=cmd_server, args=(h7, 5037,)))
    # servers.append(Thread(target=cmd_server, args=(h8, 5028,)))
    
    for server in servers:
        server.start()
        sleep(0.1)

    

    speed_host12 = 5
    speed_host34 = 5
    flow_host12 = 'udp'
    flow_host34 = 'udp'
    clients = []
    cmd_client(h1, h5, 5015, flow_host12, speed_host12)
    # clients.append(Thread(target=cmd_client, args=(h1, h5, 5015, flow_host12, speed_host12)))
    # clients.append(Thread(target=cmd_client, args=(h1, h7, 5017, flow_host12, speed_host12)))
    # clients.append(Thread(target=cmd_client, args=(h2, h6, 5026, flow_host12, speed_host12)))
    # clients.append(Thread(target=cmd_client, args=(h2, h8, 5028, flow_host12, speed_host12)))
    # clients.append(Thread(target=cmd_client, args=(h3, h5, 5035, flow_host34, speed_host34)))
    # clients.append(Thread(target=cmd_client, args=(h3, h7, 5037, flow_host34, speed_host34)))
    # clients.append(Thread(target=cmd_client, args=(h4, h6, 5046, flow_host34, speed_host34)))
    # clients.append(Thread(target=cmd_client, args=(h4, h8, 5048, flow_host34, speed_host34)))

    for client in clients:
        client.start()
        sleep(0.1)

    sleep(15.1) # 15.3 is accpetable
    lost_obj = Lost()

    temp_lost = lost_obj.get_rate()

    CLI(net)

    net.stop()

    # clear the network topology, switches and hosts 
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
