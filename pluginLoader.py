#!./venv/bin/python3
from scapy.all import *
import os
import importlib.util
import sys
from flask import jsonify


def load_module_from_path(plugin_path):


    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Error: {plugin_path} not found")

    # Extract module name from the filename
    module_name = os.path.splitext(os.path.basename(plugin_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
    module = importlib.util.module_from_spec(spec)

    # Add the module to sys.modules
    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    return module





def get_plugin_paths(plugin_folder = "plugins"):
    plugins = []

    for filename in os.listdir(plugin_folder):
        if filename.endswith(".plug"):
            module_folder = filename
            module_name = filename[:-5]  # Strip ".plug"
            module_path = f"{plugin_folder}/{module_folder}/{module_name}.py"

            plugins.append(module_path)

    return plugins



class FLowParcer:
    def __init__(self,rx):
        self.active_aplugins = []
        self.running = True
        
        print("variable type: "+str(type(rx)))
        def loop(self):
            while self.running:

                pkt = rx.BufferRead()
                if pkt:
                    #print(pkt.summary())

                    for active_module in self.active_aplugins:
                        if hasattr(active_module, "run_plugin"):
                            active_module.run_plugin(pkt)
                    
                else:
                    #print("buffer ampty (cooling down)")
                    time.sleep(1)
        tloop = Thread(target=loop, args=(self,))
        tloop.start()

    def load_plugin(self,plugin_name,lisener,BrigeIface):
        print(f'plugin name: {plugin_name}')
        plugin_paths = get_plugin_paths()
        for plugin_path in plugin_paths:
            print(f'avelable plugin: {plugin_path}')
            if plugin_name.lower() in plugin_path.lower():
                print(f'plugin path: {plugin_path}')
                break


        module = load_module_from_path(plugin_path)
        #module = importlib.import_module(plugin_path)
        
        if hasattr(module, "load_plugin"):
            module.load_plugin(lisener,BrigeIface)
        self.active_aplugins.append(module)


    def unload_plugin(self,plugin_name):
        for active_aplugin in self.active_aplugins:

            print("active:,input: "+str(active_aplugin.__name__)+","+str(plugin_name))

            if plugin_name in active_aplugin.__name__:
                
                if hasattr(active_aplugin, "unload_plugin"):
                    active_aplugin.unload_plugin()

                self.active_aplugins.remove(active_aplugin)
                print(len(self.active_aplugins))


              
    def get_plugin_html(self,plugin_name):
        print(f'plugin name: {plugin_name}')

        for active_aplugin in self.active_aplugins:

            print("active:,input: "+str(active_aplugin.__name__)+","+str(plugin_name))

            if plugin_name.lower() in active_aplugin.__name__.lower():
                
                if hasattr(active_aplugin, "get_html"):
                    html_cont =  active_aplugin.get_html()

                    return html_cont
                
                else:
                    print(f'pluginLoader: plugin {plugin_name} has no attribute "get_html"')
                    return jsonify(f'plugin {plugin_name} has no attribute "get_html"')

            else:
                print(f'pluginLoader: plugin {plugin_name} is not active')
                return jsonify(f'plugin {plugin_name} is not active')
                



    def post_api(self,plugin_name,post_request):
        print(f'plugin name: {plugin_name}')

        for active_aplugin in self.active_aplugins:

            print("active:,input: "+str(active_aplugin.__name__)+","+str(plugin_name))

            if plugin_name.lower() in active_aplugin.__name__.lower():
                
                if hasattr(active_aplugin, "request_handler"):
                    json =  active_aplugin.request_handler()

                    return json
                
                else:
                    print(f'pluginLoader: plugin {plugin_name} has no attribute "request_handler"')
                    return jsonify(f'plugin {plugin_name} has no attribute "request_handler"')

            else:
                print(f'pluginLoader: plugin {plugin_name} is not active')
                return jsonify(f'plugin {plugin_name} is not active')