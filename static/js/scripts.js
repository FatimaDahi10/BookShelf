// Gestione del carrello
$(document).on('click', '.add-cart', function(e) {
    e.preventDefault();

    var productid = $(this).val();
    var productqty = $('#qty-cart').val() || 1;

    if (productid && productqty) {
        $.ajax({
            type: 'POST',
            url: cartAddUrl,
            data: {
                product_id: productid,
                product_qty: productqty,
                csrfmiddlewaretoken: csrf_token,
                action: 'post'
            },
            success: function(json) {
                document.getElementById("cart_quantity").textContent = json.qty;
                location.reload();
            },
            error: function(xhr, errmsg, err) {
                console.log("Errore:", errmsg);
            }
        });
    } else {
        console.log('ID prodotto o quantità non validi');
    }
});

// Gestione dei preferiti
$(document).on('click', '.add-favourite', function(e) {
    e.preventDefault();

    var productid = $(this).val();

    if (productid) {
        $.ajax({
            type: 'POST',
            url: favouriteAddUrl,
            data: {
                product_id: productid,
                csrfmiddlewaretoken: csrf_token,
                action: 'post'
            },
            success: function(json) {
                location.reload();
            },
            error: function(xhr, errmsg, err) {
                console.log("Errore:", errmsg);
            }
        });
    } else {
        console.log('ID prodotto o quantità non validi');
    }
});


    function updateNotificationCount() {
        fetch('/unread-notifications-count/')
            .then(response => response.json())
            .then(data => {
                const notifyElement = document.querySelector('.notify');
                if (data.count > 0) {
                    notifyElement.textContent = data.count;
                    notifyElement.style.display = 'inline-block';
                } else {
                    notifyElement.style.display = 'none';
                }
            });
    }

    // Aggiorna il conteggio ogni 30 secondi
    setInterval(updateNotificationCount, 30000);

    // Aggiorna subito il conteggio al caricamento della pagina
    updateNotificationCount();


