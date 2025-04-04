

from scapy.all import *
import matplotlib.pyplot as plt
import networkx as nx
from flask import render_template
from flask import jsonify


Network = nx.Graph()
lisener = None
BrigeIface = None

tracingMode = False


import json

def net_to_json(net_map):
  
    pos = nx.spring_layout(net_map)  

    graph_data = {
        "nodes": [{"id": node, "x": float(pos[node][0]), "y": float(pos[node][1])} for node in net_map.nodes],
        "edges": [{"source": u, "target": v} for u, v in net_map.edges]
    }

    return graph_data




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

    #plt.figure(figsize=(6, 6))
    #nx.draw(Network, with_labels=True, node_color="skyblue", node_size=100, font_size=10)
    #plt.show()


from flask import current_app

def get_html():
    try:
        print("Attempting to render webmaper_html.html...")

        absolute_template_path = os.path.join(os.path.dirname(__file__), "templates")
        print(f"Using template path: {absolute_template_path}")

        with current_app.app_context():
            current_app.jinja_loader.searchpath.insert(0, absolute_template_path)
            html_cont = render_template("webmaper_html.html")
            current_app.jinja_loader.searchpath.pop(0)

        print("webmaper_html.html rendered successfully.")
        return html_cont
    except Exception as e:
        print(f"Error rendering webmaper_html.html: {e}")
        return f"Error: {e}"
    

def request_handler():
    return jsonify(net_to_json(Network))

