const pluginSelector = document.getElementById('pluginSelector');
const addPluginButton = document.getElementById('addPluginButton');
const HTMLmain = document.getElementsByTagName('main')[0];

function loadplugins(){
    function show_options(plugins){
        plugins.forEach(plugin => {
            const newOption = document.createElement('option'); 
            newOption.value = plugin.toLowerCase().replace(" ", "-");
            newOption.text = plugin;
            pluginSelector.add(newOption);
            
        });
    }
        fetch('http://127.0.0.1:5000/pluginsApi',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                action: 'get_plugins',
            })
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json()
        })
        .then(data => {
            console.log(data);
            show_options(data);
        })

}

function showActivePLugins(){
    function sumonPlugins(plugins){
        document.querySelectorAll("div#plugin_panel").forEach(div => div.remove());
        plugins.forEach(plugin => {
            const div = document.createElement('div');
            const span = document.createElement('span');
            const p = document.createElement('p');
            const stopButton = document.createElement('button');


            stopButton.textContent = 'unplug'
            stopButton.id = 'stopButton'
            p.textContent = plugin
            p.style='margin-right: 30px'
            span.style='display: inline-flex'
            div.id = 'plugin_panel'
            div.classList.add('container');
            
            

            
            div.appendChild(span);
            span.appendChild(p);
            span.appendChild(stopButton);

            HTMLmain.appendChild(div); 
            
            div.addEventListener('click', () => {
                window.open(`http://127.0.0.1:5000/plugin/${plugin}`, '_blank');
            });


            stopButton.addEventListener('click',() =>{
                console.log("delete")
                
                fetch('http://127.0.0.1:5000/pluginsApi',{
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'stop_plugin',
                        plugin_name: plugin,
                    })
                })
                .then(res => {
                    if (!res.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return res.json()
                })
                .then(data => {
                    console.log(data);
                    //add some html with a button to stop/unload the plugin
                })
            

            })



        })
    }

    fetch('http://127.0.0.1:5000/pluginsApi',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'get_active_plugins',
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json()
    })
    .then(data => {
        console.log(data);
        sumonPlugins(data);
    })
    
}






addPluginButton.addEventListener('click',() =>{
    let plugin_name = pluginSelector.value
    console.log(plugin_name)

    fetch('http://127.0.0.1:5000/pluginsApi',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'activate_plugin',
            plugin_name: plugin_name,
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json()
    })
    .then(data => {
        console.log(data);
        //add some html with a button to stop/unload the plugin
    })

})

loadplugins()

function ref(){

    
    
    showActivePLugins()

}

setInterval(ref, 500);