#!./venv/bin/python3
from scapy.all import *
import importlib
import os



# all plugins must be in lowers case

def get_plugin_paths(plugin_folder = "plugins"):
    plugins = []

    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Strip ".py"
            module_path = f"{plugin_folder}.{module_name}"

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
        plugin_paths = get_plugin_paths()
        for plugin_path in plugin_paths:
            if plugin_name in plugin_path:
                break

        module = importlib.import_module(plugin_path)
        
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

              

