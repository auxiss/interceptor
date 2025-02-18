#!venv/bin/python3
from scapy.all import *
import time

class snifer:
    def __init__(self):
        self.running= False
        self.iface = 'not set'
        self.pkts_clean = []    # add a limit to size! (not inpemented)
        self.pktBuffer = []
        self.storage_size = 128

    def start(self,iface):
        self.running= True
        self.iface = iface
        def lisener(self):
            def packetHandler(pkt):
                if pkt:
                    self.pkts_clean.append(pkt)
                    self.pktBuffer.append(pkt)

                    if len(self.pkts_clean) > self.storage_size -1:
                        #print("stored pkts are too many droping one")
                        #print(len(self.pkts_clean))
                        self.pkts_clean.pop(0)
                        #print(len(self.pkts_clean))

            while self.running:
                #print("i am alive")
                sniff(iface=self.iface, prn=packetHandler, count=3)
            


        tlisener = Thread(target=lisener, args=(self,))
        tlisener.start()
        
    
    def getPkts(self, ):
        
        return self.pkts_clean
    
    def clearPktList(self):
        self.pkts_clean = []

    def stop(self):
        self.running = False

    def BufferRead(self):
        if self.pktBuffer != []:
            return self.pktBuffer.pop()
        else:
            return None
        
        




if __name__ == '__main__':
    iface = 'wlp0s20f3'
    rx = snifer()
    rx.start(iface)


    try:

        pkt_info = {}

        while True:
            pkt = rx.BufferRead()
            print(pkt)
            if pkt:
                for layer in pkt.layers():
                    print("layer: ",layer)
                    for field in pkt[layer].fields:
                        field_val = str(pkt[layer].getfieldval(field))
                        field = str(field)
                        str_layer = str(layer).split("'")[1].split("'")[0]
                        print(type(str_layer))
                        print('\t',field, field_val)

                        if str_layer not in pkt_info:
                            pkt_info[str_layer] = {}
                        pkt_info[str_layer][field] = field_val
                        print(pkt_info)
                        
                        
            input()

    except KeyboardInterrupt:
        rx.stop()