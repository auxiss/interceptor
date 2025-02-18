const BrigeIfaceSelector = document.getElementById('BrigeIfaceSelector');
const SnifIfaceSelector = document.getElementById('SnifIfaceSelector');
const setButton = document.getElementById('setButton');
const stopButton = document.getElementById('stopButton');
const messageBox = document.getElementById('message');




function loadIfaces(ifaces){
    ifaces.forEach(iface => {
        const newOption = document.createElement('option'); 
        newOption.value = iface.toLowerCase().replace(" ", "-");
        newOption.text = iface;
        BrigeIfaceSelector.add(newOption);

        const newOption2 = document.createElement('option'); 
        newOption2.value = iface.toLowerCase().replace(" ", "-");
        newOption2.text = iface;
        SnifIfaceSelector.add(newOption2);
        
    });
}


setButton.addEventListener('click', () => { 
    console.log('click');
    const BrigeIface = BrigeIfaceSelector.value;
    const SnifIface = SnifIfaceSelector.value;
    if(BrigeIface != SnifIface){
        console.log('ok');
        messageBox.textContent = 'ifaces set & running!';

        fetch('http://127.0.0.1:5000/ifaceConfigApi',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                action: 'set_ifaces',
                BrigeIface: BrigeIface,
                SnifIface: SnifIface,

            })
        })
        .then(res => {
            if (!res.ok) {
                messageBox.textContent = 'Network response was not ok';
                throw new Error('Network response was not ok');
                
            }
            else{
                refresh()
                return res.json();

            }
               
        })

    }
    else{
        let err = 'ifaces must be defrent'
        
        console.log(err)
        messageBox.textContent = err;
    
    }

})




stopButton.addEventListener('click', () => {
    fetch('http://127.0.0.1:5000/ifaceConfigApi',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'stop_ifaces',
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
        refresh()
    })

})




function refresh(){
    fetch('http://127.0.0.1:5000/ifaceConfigApi',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'get_status',
        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json()
    })
    .then(data => {
        console.log(data)
        running = data[0]
        if (running) {
            BrigeIfaceSelector.value = data[1]; 
            SnifIfaceSelector.value = data[2];
            messageBox.textContent = 'sniffer is running';
            BrigeIfaceSelector.disabled = true;
            SnifIfaceSelector.disabled = true;

            setButton.hidden = true;
            stopButton.hidden = false;
        }
        else{
            BrigeIfaceSelector.value = data[1]; 
            SnifIfaceSelector.value = data[2];
            messageBox.textContent = ' ';
            BrigeIfaceSelector.disabled = false;
            SnifIfaceSelector.disabled = false;

            setButton.hidden = false;
            stopButton.hidden = true;
        }
    })
}



fetch('http://127.0.0.1:5000/ifaceConfigApi',{
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        action: 'get_ifaces',
    })
})
.then(res => {
    if (!res.ok) {
        throw new Error('Network response was not ok');
    }
    return res.json()
})
.then(data => {
    console.log(data)
    loadIfaces(data)

})





refresh()