

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
    src_ip = None

    if pkt.haslayer(IP):
        #print('from ip')
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst

        if pkt.haslayer(TCP):
            #print('TCP flags:')
            #print(pkt[TCP].flags)
            if pkt[TCP].flags == 'S':
                print(f"client: {src_ip}")
                print(f"server ip: {dst_ip}")
                print(f"port: {pkt[TCP].dport}")


    elif pkt.haslayer(IPv6):
        src_ip = pkt[IPv6].src
        dst_ip = pkt[IPv6].dst

        if pkt.haslayer(TCP):
            #print('TCP flags:')
            #print(pkt[TCP].flags)
            if pkt[TCP].flags == 'S':
                print(f"client: {src_ip}")
                print(f"server ip: {dst_ip}")
                print(f"port: {pkt[TCP].dport}")



    elif pkt.haslayer(ARP):
        #print('from ARP')
        src_ip = pkt[ARP].psrc
        dst_ip = pkt[ARP].pdst



    if src_ip != None:
        #print(src_ip)
        #print('passed')
        if src_ip not in Network.nodes() or dst_ip not in Network.nodes():

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
        print("(unresolved packet type!) :")
        print(pkt.summary())
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


def get_html():
    
    html_cont = "<h1>it works!!</h1>"

    return html_cont
