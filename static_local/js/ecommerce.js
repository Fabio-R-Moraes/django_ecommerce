$(document).ready(function(){
    //Contact Form Handler
    const contactForm = $(".contact-form")
    const contactFormMethod = contactForm.attr("method")
    const contactFormEndPoint = contactForm.attr("action")

    function displaySubmiting(submitBtn, defaultText, doSubmit){
        if(doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i>Enviando...")
        }else{
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()

        const contactFormSubmitBtn = contactForm.find("[type='submit']")
        const contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
        const contactFormData = contactForm.serialize()
        const thisForm = $(this)

        displaySubmiting(contactFormSubmitBtn,"",true)

        $.ajax({
            method: contactFormMethod,
            url: contactFormEndPoint,
            data: contactFormData,
            success: function(data){
                contactForm[0].reset()

                $.alert({
                    title: "Sucesso",
                    content: data.message,
                    theme: "modern",
                })

                setTimeout(function(){
                    displaySubmiting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
                }, 500)
            },
            error: function(error){
                console.log(error.responseJSON)

                const jsonData = error.responseJSON
                let msg = ""

                $.each(jsonData, function(key,value){
                    msg += key + ":" + value[0].message + "<br />"
                })
                $.alert({
                    title: "Ooopsss...",
                    content: msg,
                    theme: "modern",
                })

                setTimeout(function(){
                    displaySubmiting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
                }, 500)
            }
        })
    })

    //Auto Search
    const searchForm = $(".search-form")
    const searchInput = searchForm.find("[name='q']")
    const typingTimer = 0
    const typingInterval = 500  //0.5 second
    const searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        //key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(peformSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        //key pressed
        clearTimeout(typingTimer)
    })

    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spinner'></i>Buscando...")
    }

    function peformSearch(){
        displaySearching()
        const query = searchInput.val()
        
        setTimeout(function(){
            window.location.href = '/search/?q=' + query
        }, 1000)
    }

    //Cart + Add Product
    const productForm = $(".form-product-ajax")

    productForm.submit(function(event){
        event.preventDefault();
        //console.log("O formulário não foi enviado!!!");

        //O this pega os dados reacionados a esse formulário
        const thisForm = $(this);
        //const actionEndPoint = thisForm.attr("action");
        const actionEndPoint = thisForm.attr("data-endpoint");
        const httpMethod = thisForm.attr("method");
        const formData = thisForm.serialize();

        $.ajax({
            url:actionEndPoint,
            method:httpMethod,
            data:formData,
            success:function(data){
                console.log("Sucesso!!!")
                console.log(data)
                console.log("Adicionado",data.added)
                console.log("Removido",data.removed)

                const submitSpan = thisForm.find(".submit-span")

                if(data.added){
                    submitSpan.html("No carrinho <button type='submit' class='btn btn-link'>Excluir</button>")
                }else{
                    submitSpan.html("<button type='submit' class='btn btn-success'>Adicionar</button>")
                }

                const navbarCount = $(".navbar-cart-count")
                const currentPath = window.location.href

                navbarCount.text(data.cartItemCount)

                if(currentPath.indexOf("cart")!=-1){
                    refreshCart()
                }
            },
            error:function(errorData){
                $.alert({
                    title: "Ooopsss...",
                    content: "Ocorreu um erro, tente mais tarde novamente!!!",
                    theme: "modern",
                })
                console.log("Erro...")
                console.log(errorData)
            }
        })
    })
    
    function refreshCart(){
        //console.log("Excluindo do carrinho atual...")
        const cartTable = $(".cart-table")
        const cartBody = cartTable.find(".cart-body")
        const productsRow = cartBody.find(".cart-product")
        const currentUrl = window.location.href
        const refreshCartUrl = '/api/cart/';
        const refreshCartMethod = 'GET';
        const data = {};

        //cartBody.html("<h1>Mudou!!!</h1>")
        $.ajax({
            url:refreshCartUrl,
            method:refreshCartMethod,
            data:data,
            success:function(data){
                console.log(data)
                const hiddenCartItemRemoveForm = $(".cart-item-remove-form")

                if(data.products.lenght>0){
                    productsRow.html(" ")
                    let i = data.products.lenght

                    $.each(data.products,function(index,value){
                        const newCartItemRemove = hiddenCartItemRemoveForm.clone()

                        newCartItemRemove.css("display","block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">"+ i + "</th><td><a href=" + value.url + ">" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                        i--
                    })

                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                }else{
                    window.location.href = currentUrl
                }
            },
            error:function(errorData){
                $.alert({
                    title: "Ooopsss...",
                    content: "Ocorreu um erro, tente mais tarde novamente!!!",
                    theme: "modern",
                })
                console.log("Erro...")
                console.log(errorData)
            }
        })

    }
})