'''#!home/oddy/projects/interseptor/venv/bin/python3'''
import importlib
import os

def execute_plugins(data):
    plugin_folder = "plugins"

    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py"):
            module_name = filename[:-3]  # Strip ".py"
            module_path = f"{plugin_folder}.{module_name}"
            
            print(module_name,module_path)
            
            # Import the module dynamically
            module = importlib.import_module(module_path)

            # Execute the plugin's run_plugin function, if it exists
            if hasattr(module, "run_plugin"):
                module.run_plugin(data)

# Example complex variable
complex_data = {
    "key1": [1, 2, 3],
    "key2": {"nested_key": "value"},
    "key3": (4, 5)
}

execute_plugins(complex_data)

