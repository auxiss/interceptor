from scapy.all import wrpcap


def run_plugin(pkt):
    #print("actiVe")
    pass

def load_plugin(lisener,BrigeIface): # set plugin informasiion and add fire wall ruls etc...
    print(BrigeIface)
    print(len(lisener.pktBuffer))
    pass

def unload_plugin():
    print(str(__name__),": deactiveting")