document.addEventListener('DOMContentLoaded', function() {
    const purchaseButton = document.querySelector('.view-product-btn');
    const popupOverlay = document.getElementById('popup-overlay');
    const closePopupButton = document.getElementById('close-popup');
    const payNowButton = document.getElementById('pay-now-btn');
    const paymentPopup = document.querySelector('.popup');
    const waitingPopup = document.getElementById('waiting-popup');

    purchaseButton.addEventListener('click', function() {
        popupOverlay.style.visibility = 'visible';
    });

    closePopupButton.addEventListener('click', function() {
        popupOverlay.style.visibility = 'hidden';
    });

    popupOverlay.addEventListener('click', function(event) {
        if (event.target === popupOverlay) {
            popupOverlay.style.visibility = 'hidden';
        }
    });

    payNowButton.addEventListener('click', function() {
        paymentPopup.style.display = 'none';
        waitingPopup.style.display = 'block';
    });
});