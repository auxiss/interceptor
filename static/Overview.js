packetList = document.getElementById('packetList');
filterInput = document.getElementById('filterInput');
setFilterButton = document.getElementById('setFilterButton');
pktInfoBox = document.getElementById('text-message');



let filters = '';

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

                let packetName = pktInfoBox.getElementsByTagName('h2')[0]; // Gets all <p> tags inside
                let ditaials = pktInfoBox.getElementsByTagName('p')[0]; // Gets all <p> tags inside

                packetName.textContent = li.textContent

               
                
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

                    ditaials.textContent = data


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