#!venv/bin/python3
from scapy.all import *
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS



from lisener import snifer
import helperFunc
import pluginLoader as pl
interfaces =  helperFunc.getIfaces()
pkts = []


app = Flask(__name__)
CORS(app)

BrigeIface = 'None'
SnifIface = 'None'


rx = snifer()




FLowParcer = pl.FLowParcer(rx)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ifaceConfigApi', methods=['POST'])
def ifaceConfigApi():
    global BrigeIface
    global SnifIface
    req = request.get_json()
    print(req)

    if req['action'] == 'stop_ifaces':           #stop
        rx.stop()
        return jsonify('sniffer stoped'), 201
        

    if req['action'] == 'get_status':           #get running status and current ifaces 
        print("sniffer status: " ,rx.running)

        status = [rx.running,  BrigeIface, SnifIface]
        return jsonify(status), 201
        

    if req['action'] == 'get_ifaces':       #get all the device's ifaces
        return jsonify(interfaces), 201
    

    if req['action'] == 'set_ifaces':         #start
        BrigeIface = req['BrigeIface']
        SnifIface = req['SnifIface']
        rx.start(SnifIface)

        return jsonify({"message": "ok"}), 201
    else:
        return jsonify({"error": "incorect format!"}), 400



@app.route('/overView')
def overView():
    #print("well come over view")
    return render_template('overview.html')

@app.route('/overViewApi', methods=['POST'])
def overViewApi():
    req = request.get_json()
    print(req)

    if req['action'] == 'get_packets':
        pkts = rx.getPkts()
        #print(type(pkts))

        #print(len(pkts))
            
        pkts_name = []
        filters =req['filters']
        print(filters)

        if len(filters) != 0:
            print("data needs filtering")
            id=0
            for packet in pkts:
                #print(type(packet))
                if filters in str(packet.show):
                    packet_name = str(packet.summary())
                    pkts_name.insert(0,packet_name+" ID:"+str(pkts.index(packet)))
                    id = id+1

                    #print(pkts_name)

            return jsonify(pkts_name)

        else:
            for packet in pkts:
                packet_name = str(packet.summary())
                pkts_name.insert(0,packet_name+" ID:"+str(pkts.index(packet)))
            #print(pkts_name)#'''

            return jsonify(pkts_name)
        
    if req['action'] == 'get_pkt_by_id':
            pkts = rx.getPkts()
            pktIndex = int(req['pktIndex'])
            print(pktIndex)

            ditales = str(pkts[pktIndex].show).split('Packet.show of ')[1].replace('|','\n').replace('  ','\n').replace(' ','\n   ')
            
            pkt_dict = helperFunc.packet_to_dict(pkts[pktIndex])
            

            print(pkt_dict)
            return jsonify(pkt_dict)



@app.route('/plugins')
def plugins():
    return render_template('plugins.html')

@app.route('/pluginsApi', methods=['POST'])
def pluginsApi():
    global BrigeIface
    req = request.get_json()
    print(req)

    if req['action'] == 'get_plugins':
        plugins = []
        plugin_paths = pl.get_plugin_paths()
        for plugin_path in plugin_paths:
            plugin_path = plugin_path.split('/')[1]
            plugin_path = plugin_path.split('.')[0]
            plugins.append(plugin_path)

        print( jsonify(plugins))

        return jsonify(plugins), 201
    
    
    if req['action'] == 'activate_plugin':
        plugin_name =req['plugin_name']
        print(plugin_name)
        FLowParcer.load_plugin(plugin_name=plugin_name, lisener=rx , BrigeIface=BrigeIface)
        return jsonify('plugin activated!'), 201
    
    if req['action'] == 'get_active_plugins':
        active_plugins = FLowParcer.active_aplugins
        active_plugins_Names = []
        for plugin in active_plugins:

            plugin_name = plugin.__name__
            active_plugins_Names.append(plugin_name)
            print(active_plugins_Names)
            
        return jsonify(active_plugins_Names), 201
    
    if req['action'] == 'stop_plugin':
        plugin_name =req['plugin_name']
        FLowParcer.unload_plugin(plugin_name)
        return jsonify("server: plugin unloaded"), 201
    


@app.route('/plugin/<pluginName>')
def plugin(pluginName):
    html = FLowParcer.get_plugin_html(pluginName)

    if not html: return jsonify("server: plugin not found"), 404

    return html



@app.route('/pluginApi/<pluginName>', methods=['POST'])
def plugindata(pluginName):
    req = request.get_json()
    print(req)
    json = FLowParcer.post_api(pluginName, req)

    if not json: return jsonify("json object is Nona type"), 404

    return json
    



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)







