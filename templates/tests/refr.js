const internetIfaceSelector = document.getElementById('ConIfaceSelector');
const ApIfaceSelector = document.getElementById('ApIfaceSelector');
const ssidInput = document.getElementById('ssid');
const passwordInput = document.getElementById('password');
const macInput = document.getElementById('macAddress');
const startButton = document.getElementById('startButton');
const divContainer = document.getElementById('blackPlate')
const infoLabel = document.getElementById('infoLabel')



function loadIfaces(ifaces){
    ifaces.forEach(iface => {
        const newOption = document.createElement('option'); 
        newOption.value = iface.toLowerCase().replace(" ", "-");
        newOption.text = iface;
        internetIfaceSelector.add(newOption);

        const newOption2 = document.createElement('option'); 
        newOption2.value = iface.toLowerCase().replace(" ", "-");
        newOption2.text = iface;
        ApIfaceSelector.add(newOption2);
        
    });
}




fetch('http://127.0.0.1:5000/ifaces')
    .then(res => {
        if(res.ok){
            console.log("infaces data ok!");
            return res.json();
        }
    })
    .then(data => {
        console.log(data);
        loadIfaces(data)
        
    })
    .catch(error => console.log('error with feching ifaces'))





startButton.addEventListener('click', () => { 

    console.log('button clicked!')
    const internetIface = internetIfaceSelector.value;
    const APIface = ApIfaceSelector.value;
    const ssid = ssidInput.value;
    const password = passwordInput.value;
    const macAddress = macInput.value;
    let mode = 'wifi' //not inplomented yet (to be added to api's json )

    if (internetIface && APIface && ssid && password && macAddress){
        if (internetIface != APIface){
            console.log('ok')

            
            fetch('http://127.0.0.1:5000/ApSetup',{
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    internetIface: internetIface,
                    ApIface: APIface,
                    ssid: ssid,
                    password: password,
                    macAddress: macAddress
                })
            })
            .then(res => {
                if (!res.ok) {
                    infoLabel.textContent = 'uneble to config server ap';
                    throw new Error('Network response was not ok');
                }
                return res.json()
            })
            .then(data => {
                console.log(data)
                divContainer.classList.toggle('disabled');
                infoLabel.textContent = 'AP started!';
            })
            


        }else{
            console.log('ifaces must be defrent');
            infoLabel.textContent = 'Ifaces musy be defrent!';
        }
        
    }else{
        console.log('all inputs must be filed');
        infoLabel.textContent = 'All inputs must be filed!';
    }

});

