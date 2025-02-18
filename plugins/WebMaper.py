

from scapy.all import *
import matplotlib.pyplot as plt
import networkx as nx

import plugins.icmpTracer as tacer

Network = nx.Graph()
lisener = None
BrigeIface = None

tracingMode = False



def run_plugin(pkt):
    global lisener
    global BrigeIface

    if pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst


        if src_ip not in Network.nodes() or dst_ip not in Network.nodes():

            if tracingMode:
                if dst_ip != '192.168.1.4':
                    print('tracing is active!')
                    print(f'om iface: {lisener.iface}')
                    path = tacer.TraceRoute(dst_ip,lisener.iface)

                    src = path[0]
                    for ip in path:
                        Network.add_node(ip)
                        Network.add_edge(src, ip)
                        src = ip
            else:



                try:
                    print("------->>new packet")
                    print("src ip: "+src_ip)
                    print("dst ip: "+dst_ip)
                    
                    Network.add_node(src_ip)
                    Network.add_node(dst_ip)
                    Network.add_edge(src_ip, dst_ip)

                except:
                    print("ERROR: in webmaper network addsion")

    else:
        #print(pkt.summary())
        pass



def load_plugin(lisener_passed,BrigeIface_passed):
    global lisener
    global BrigeIface
    
    lisener = lisener_passed
    BrigeIface = BrigeIface_passed

    


def unload_plugin():
    print(str(__name__),": deactiveting")

    print("Nodes:", Network.nodes())
    print("Edges:", Network.edges())

    plt.figure(figsize=(6, 6))
    nx.draw(Network, with_labels=True, node_color="skyblue", node_size=100, font_size=10)
    plt.show()



