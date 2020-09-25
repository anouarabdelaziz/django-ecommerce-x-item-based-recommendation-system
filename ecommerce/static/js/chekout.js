
var viewbtns = document.getElementsByClassName('btn-danger')

for(var i=0; i < viewbtns.length ; i++ ){

    var btn = viewbtns[i]
    btn.addEventListener('click', function(event){
          
          var itemid = this.dataset.product
          var action = this.dataset.action
          btn.parentElement.parentElement.remove()
        
          update_item(itemid, action)


        })
}


var updatebtns = document.getElementsByClassName('btn-outline-secondary')


for(var i=0; i < updatebtns.length ; i++ ){

    var btn = updatebtns[i]
    btn.addEventListener('click', function(event){
          
          var itemid = this.dataset.product
          var action = this.dataset.action
        
          update_item(itemid, action)


        })
}

function update_item(itemid, action){
        console.log(itemid)
        var url = '/updated_item/'

        fetch(url,  {
          method : 'POST',
          headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken,

          },
          body:JSON.stringify({'itemid' : itemid , 'action' : action}),

        })

        .then((response) =>{
          return response.json()
        })
        .then((data) =>{
           location.reload(data)
        })

}


