from scapy.all import conf



def getIfaces():
    interfaces = conf.ifaces
    ifaces = []
    for iface in interfaces: #convert to array type from dict ; )
        ifaces.append(iface)
    print(ifaces)
    return ifaces



def packet_to_dict(pkt):

    if pkt:
        pkt_info = {}
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

    return pkt_info 