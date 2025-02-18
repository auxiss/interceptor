from scapy.all import wrpcap


def run_plugin(pkt):
    wrpcap('captured_packets.pcap',pkt)
    print("packet saved")

