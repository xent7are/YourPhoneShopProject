% rebase('layout.tpl', title='Favorites', year=year)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - YourPhoneShop</title>
    <link rel="stylesheet" type="text/css" href="/static/content/viewFavStyle.css">
</head>
<body>

<div class="container">
    <h2>Your favorites</h2>

    <div id="empty-favorites-message" style="display: none;">
        <p>Your favorites will be displayed on this page.</p>
    </div>

    <section class="favorite-list">
        <div class="favorite-card">
            <img src="/static/images/samsungA35.png" alt="Samsung A35">
            <div class="favorite-info">
                <div class="favorite-name">Samsung Galaxy A35 256GB Purple Smartphone</div>
                <div class="favorite-specs">Main features: Cores - 8x (2.4 GHz), 8 GB, 2 SIM, Super AMOLED, 2340 x 1080, Camera 50+8+5 MP, NFC, 5G, GPS, 5000 mAh</div>
                <div class="favorite-availability">You can pick it up tomorrow from 7 stores</div>
                <div class="favorite-rating">
                    <img src="/static/images/star.png" alt="Star" class="rating-star">
                    <span class="rating-value">4.8</span>
                </div>
                <div class="favorite-price">32 999 rub</div>
            </div>
            <button class="book-smartphone">To book</button>
            <button class="remove-favorite">
                <img src="/static/images/rubbish.png" alt="Remove">
            </button>
        </div>

        <div class="favorite-card">
            <img src="/static/images/honor.jpg" alt="Honor">
            <div class="favorite-info">
                <div class="favorite-name">Honor 5</div>
                <div class="favorite-specs">Main features: Cores - 8x (2.2 GHz), 6 GB, 2 SIM, IPS LCD, 2400 x 1080, Camera 48+8+2 MP, NFC, 4G, GPS, 4000 mAh</div>
                <div class="favorite-availability">You can pick it up tomorrow from 5 stores</div>
                <div class="favorite-rating">
                    <img src="/static/images/star.png" alt="Star" class="rating-star">
                    <span class="rating-value">4.6</span>
                </div>
                <div class="favorite-price">24 999 rub</div>
            </div>
            <button class="book-smartphone">To book</button>
            <button class="remove-favorite">
                <img src="/static/images/rubbish.png" alt="Remove">
            </button>
        </div>

        <div class="favorite-card">
            <img src="/static/images/iPhone15.png" alt="iPhone 15">
            <div class="favorite-info">
                <div class="favorite-name">iPhone 15</div>
                <div class="favorite-specs">Main features: Cores - 6x (3.46 GHz), 6 GB, 1 SIM, Super Retina XDR, 2556 x 1179, Camera 48+12 MP, NFC, 5G, GPS, 3349 mAh</div>
                <div class="favorite-availability">You can pick it up tomorrow from 3 stores</div>
                <div class="favorite-rating">
                    <img src="/static/images/star.png" alt="Star" class="rating-star">
                    <span class="rating-value">4.8</span>
                </div>
                <div class="favorite-price">75 999 rub</div>
            </div>
            <button class="book-smartphone">To book</button>
            <button class="remove-favorite">
                <img src="/static/images/rubbish.png" alt="Remove">
            </button>
        </div>

        <div class="favorite-card">
            <img src="/static/images/pixel.jpg" alt="Google Pixel">
            <div class="favorite-info">
                <div class="favorite-name">Google Pixel</div>
                <div class="favorite-specs">Main features: Cores - 8x (2.84 GHz), 8 GB, 1 SIM, OLED, 2400 x 1080, Camera 50+12 MP, NFC, 5G, GPS, 4080 mAh</div>
                <div class="favorite-availability">You can pick it up tomorrow from 4 stores</div>
                <div class="favorite-rating">
                    <img src="/static/images/star.png" alt="Star" class="rating-star">
                    <span class="rating-value">4.7</span>
                </div>
                <div class="favorite-price">49 999 rub</div>
            </div>
            <button class="book-smartphone">To book</button>
            <button class="remove-favorite">
                <img src="/static/images/rubbish.png" alt="Remove">
            </button>
        </div>

        <div class="favorite-card">
            <img src="/static/images/xiaomi.png" alt="Xiaomi">
            <div class="favorite-info">
                <div class="favorite-name">Xiaomi</div>
                <div class="favorite-specs">Main features: Cores - 8x (2.2 GHz), 6 GB, 2 SIM, AMOLED, 2400 x 1080, Camera 64+8+5 MP, NFC, 5G, GPS, 4500 mAh</div>
                <div class="favorite-availability">You can pick it up tomorrow from 6 stores</div>
                <div class="favorite-rating">
                    <img src="/static/images/star.png" alt="Star" class="rating-star">
                    <span class="rating-value">4.5</span>
                </div>
                <div class="favorite-price">29 999 rub</div>
            </div>
            <button class="book-smartphone">To book</button>
            <button class="remove-favorite">
                <img src="/static/images/rubbish.png" alt="Remove">
            </button>
        </div>
    </section>
</div>

<script>
    
    document.querySelectorAll('.remove-favorite').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.remove();
            checkIfEmpty();
        });
    });


    document.querySelectorAll('.book-smartphone').forEach(button => {
        button.addEventListener('click', function() {
            alert("To book a smartphone, you can call this phone: +7 (XXX) XXX-XX-XX");
        });
    });


    function checkIfEmpty() {
        const favoriteList = document.querySelector('.favorite-list');
        const emptyMessage = document.getElementById('empty-favorites-message');

        if (favoriteList.children.length === 0) {
            emptyMessage.style.display = 'block';
        } else {
            emptyMessage.style.display = 'none';
        }
    }

    checkIfEmpty();
</script>

</body>
</html>