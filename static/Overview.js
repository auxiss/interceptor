packetList = document.getElementById('packetList');
filterInput = document.getElementById('filterInput');
setFilterButton = document.getElementById('setFilterButton');
pktInfoBox = document.getElementById('text-message');



let filters = '';


function displayLayers(layersData) {
    
    pktInfoBox.innerHTML = ''; 
    Object.entries(layersData).forEach(([layer, fields]) => {
        // Create an h3 for the layer
        const layerTitle = document.createElement("h3");
        layerTitle.textContent = layer;

        // Create a div to hold the fields (initially hidden)
        const fieldsContainer = document.createElement("div");
        fieldsContainer.style.display = "none";

        // Loop through the fields
        Object.entries(fields).forEach(([key, value]) => {
            const fieldParagraph = document.createElement("p");
            fieldParagraph.textContent = `${key}: ${value}`;
            fieldsContainer.appendChild(fieldParagraph); // Append to the container
        });

        // Toggle visibility when clicking the h3 element
        layerTitle.addEventListener("click", () => {
            fieldsContainer.style.display = 
                fieldsContainer.style.display === "none" ? "block" : "none";
        });

        
        // Append the elements to the container
        pktInfoBox.appendChild(layerTitle);
        pktInfoBox.appendChild(fieldsContainer);
    });
}



function updateList(filters = '') {
    console.log('updateing')

    fetch('http://127.0.0.1:5000/overViewApi',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'get_packets',
            filters: filters,

        })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.json()
    })
    .then(data => {
        console.log('data:')
        console.log(data);    
    
        packetList.innerHTML = '';

        data.forEach(pkt => {
            const li = document.createElement('li');

            
            
            li.textContent = pkt; 
            packetList.appendChild(li);  

            //const p = document.createElement('p');
            //li.appendChild(p);
            //p.hidden = true;



            li.addEventListener('click',() =>{
                pktInfoBox.classList.add("show");


               
                
                const id = li.textContent.split('ID:')[1]
                console.log(id);

                fetch('http://127.0.0.1:5000/overViewApi',{
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        action: 'get_pkt_by_id',
                        pktIndex: id,
            
                    })
                })
                .then(res => {
                    if (!res.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return res.json()
                })
                .then(data => {
                    console.log('data:')
                    console.log(data);
                    displayLayers(data)

                    const okButton = document.createElement("button");
                    okButton.id = 'ok-buuton'
                    okButton.textContent = 'close'
                    pktInfoBox.appendChild(okButton);
                    okButton.addEventListener('click',() =>{
                        pktInfoBox.classList.remove("show");
                    })


                    

                    


                })


                
            
            })

 
        });
    })

}


setFilterButton.addEventListener('click', () => { 
    filters = filterInput.value;
    console.log(filters);
    //updateList(filters);
})

//setInterval(updateList(), 1000);

setInterval( function() { updateList(filters); }, 1000 );