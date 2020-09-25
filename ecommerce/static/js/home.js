
var viewbtns = document.getElementsByClassName('btn-outline-secondary')


for(var i=0; i < viewbtns.length ; i++ ){

    var btn = viewbtns[i]

    btn.addEventListener('click', function(event){
    
        var itemid = this.dataset.product
        var action = this.dataset.action
        console.log('the item id is :', itemid)
        console.log('the action is :', action)
        update_item(itemid, action)
    })


}


var searchbtns = document.getElementsByClassName('btn-outline-info')


for(var i=0; i < searchbtns.length ; i++ ){

    var btn = searchbtns[i]
    console.log(btn)
    btn.addEventListener('click', function(event){
    
        var itemid = this.dataset.product
        var action = this.dataset.action
        console.log('the item id is :', itemid)
        console.log('the action is :', action)
        // update_item(itemid, action)
    })


}
function update_item(itemid, action){
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

