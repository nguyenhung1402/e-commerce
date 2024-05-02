function addToCart(id,name,price){

    event.preventDefault()

    fetch('/api/add-cart',{
        method: 'post',
        body :JSON.stringify({
            'id' : id,
            'name' : name,
            'price' : price

        }),
        headers:{
            'Content-Type' : 'application/json'
        }
    }).then(function (res){
        console.info(res)
        return res.json()
    }).then(function (data){
        console.info(data)

        let counter = document.getElementsByClassName('cart-counter')
        for (let i=0 ; i<counter.length ; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function (err){
        console.info(err)
    })

}

function pay(){
    if(confirm('Ban chac chan muon thanh toan khong?')==true){
        fetch('api/pay',{
            method : 'post'
        }).then(res => res.json()).then(data=>{
           if (data.code == 200)
               location.reload()
        }).catch(err => console.error(err))

    }
}

function  updateCart(id, obj){
    fetch('/api/update-cart',{
        method: 'PUT',
        body:JSON.stringify({
            'id' : id,
            'quantity': parseInt(obj.value)
        }),
        headers:{
            'Content-Type' : 'application/json'
        }
    }).then(res => res.json()).then(data =>{
        let counter = document.getElementsByClassName('cart-counter')
        for (let i=0 ; i<counter.length ; i++)
            counter[i].innerText = data.total_quantity

        let amount  = document.getElementById('total-amount')
        amount.innerText = new Intl.NumberFormat().format(data.total_amount)
    })
}

function deleteCart(id){
    if (confirm("Ban chac chan xoa san pham nay khong?") == true){
        fetch('/api/delete-cart/' + id,{
            method: 'DELETE',

            headers:{
                'Content-Type' : 'application/json'
            }
        }).then(res => res.json()).then(data =>{
            let counter = document.getElementsByClassName('cart-counter')
            for (let i=0 ; i<counter.length ; i++)
                counter[i].innerText = data.total_quantity

            let amount  = document.getElementById('total-amount')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let e = document.getElementById("product"+id)
            e.style.display= "none"
        }).catch(err => console.error(err))
    }


}

function addComment(productId){
    let content = document.getElementById('commentId')
    if (content !== null){
        fetch('/api/comments',{
            method: 'post',
            body: JSON.stringify({
                'product_id' : productId,
                'content': content.value
            }),
            headers:{
                'Content-Type' : 'application/json'
            }
        }).then(res => res.json()).then(data=>{
            if (data.status = 201){
                let  c = data.comment
                console.log(data)
                let area = document.getElementById('commentArea')

                area.innerHTML = `
                <div class="row comment">
                    <div class="col-md-1 col-xs-4">
                        <img  src="data:image/jpeg;base64,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" class="img-fluid rounded-circle"/>
                    </div>
            
                    <div class="col-md-11 col-xs-8">
                        <p>${c.content}</p>
                        <p><em>${moment(c.create_date).locale('vi').fromNow()}</em></p>
                    </div>
                </div>
                ` + area.innerHTML
            } else if (data.status = 404)
                alert(data.err_msg)
        })
    }
}