% rebase('layout.tpl', title='Product', year=year)

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Samsung Galaxy A35 - YourPhoneShop</title>
    <link rel="stylesheet" type="text/css" href="/static/content/viewingProductStyle.css">
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>
<body>
    <link rel="stylesheet" href="style.css">
    <div class="product-container">
        <div class="product-image">
            <img src="static/images/samsungA35.png" alt="Samsung Galaxy A35">
        </div>
        <div class="product-details">
            <h1>Samsung Galaxy A35</h1>
            <p class="main-features"><strong>Main Features</strong></p>
            <div class="features">
                8-core processor (2.4 GHz), 8 GB RAM, 256 GB internal storage, 6.6" Super AMOLED display (2340x1080), Triple camera: 50 MP + 8 MP + 5 MP, 5000 mAh battery, 5G support, NFC, GPS
            </div>
            <div class="price-and-reviews">
                <div class="price">
                    <span class="price-label">Price:</span>
                    <span class="price-value">32 999 rubles</span>
                </div>
                <div class="reviews">
                    <span class="rating-product">4.7</span>
                    <img src="static/images/star.png" alt="Star" class="star-icon">
                    <span class="reviews-count">Reviews</span>
                </div>
            </div>
            <div class="actions">
                <div class="availability-box">
                    <span>In stock</span>
                    <span>Available in 5 stores</span>
                </div>
                <button class="btn-reserve">Reserve</button>
                <button class="btn-favorite">
                    <span class="heart">&#10084;</span>
                    <span class="favorite-text">Add to Favorites</span>
                </button>
            </div>
            <div class="options">
                <div class="color-options">
                    <span>Color</span>
                    <div class="color-buttons">
                        <button class="color-option black"></button>
                        <button class="color-option pink selected"></button>
                        <button class="color-option yellow"></button>
                    </div>
                </div>
                <div class="storage-options">
                    <span>Memory (GB)</span>
                    <div class="storage-buttons">
                        <button class="storage-option">128</button>
                        <button class="storage-option selected">256</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="specifications">
        <h2>Phone Specifications</h2>
        <div class="specifications-grid">
            <ul>
                <li><strong>Factory Data</strong></li>
                <li>Seller's Warranty: 12 months</li>
                <li>Country of Manufacture: Vietnam</li>
                <li><strong>General Parameters</strong></li>
                <li>Type: Smartphone</li>
                <li>Model: Samsung Galaxy A35</li>
                <li>Release Year: 2024</li>
                <li><strong>Appearance</strong></li>
                <li>Color: Dark Blue</li>
                <li><strong>Display</strong></li>
                <li>Size: 6.6"</li>
                <li>Resolution: 2340x1080</li>
                <li>Matrix Type: Super AMOLED</li>
                <li>Refresh Rate: 120 Hz</li>
                <li><strong>Camera</strong></li>
                <li>Main Camera: 50 MP + 8 MP + 5 MP</li>
                <li>Front Camera: 13 MP</li>
                <li><strong>Memory</strong></li>
                <li>RAM: 8 GB</li>
                <li>Internal Storage: 256 GB</li>
                <li><strong>Battery</strong></li>
                <li>Capacity: 5000 mAh</li>
                <li>Fast Charging: Yes</li>
                <li><strong>Additional Features</strong></li>
                <li>NFC, 5G, GPS</li>
                <li>Protection: IP67</li>
            </ul>
        </div>
    </div>
    
    <div class="reviews-section">
        <h2>Reviews</h2>
        <div class="review">
            <div class="review-header">
                <span class="review-rating">4.5</span>
                <img src="static/images/star.png" alt="Star" class="star-icon">
                <span class="review-user">Ivan Ivanov</span>
                <span class="review-date">05.03.2025</span>
            </div>
            <p>Great phone for the price! The camera is impressive, and the battery lasts long. Highly recommend!</p>
        </div>
        <div class="review">
            <div class="review-header">
                <span class="review-rating">5.0</span>
                <img src="static/images/star.png" alt="Star" class="star-icon">
                <span class="review-user">Maria Petrova</span>
                <span class="review-date">10.02.2025</span>
            </div>
            <p>Very happy with my purchase. The screen is bright, the sound is high quality. Works fast with no lag.</p>
        </div>
        <div class="review">
            <div class="review-header">
                <span class="review-rating">4.0</span>
                <img src="static/images/star.png" alt="Star" class="star-icon">
                <span class="review-user">Alexey Smirnov</span>
                <span class="review-date">01.12.2024</span>
            </div>
            <p>A good choice for those looking for a balance of price and quality. The camera is excellent!</p>
        </div>
        <div class="review">
            <div class="review-header">
                <span class="review-rating">4.7</span>
                <img src="static/images/star.png" alt="Star" class="star-icon">
                <span class="review-user">Elena Kuznetsova</span>
                <span class="review-date">27.11.2024</span>
            </div>
            <p>The phone met all my expectations. The battery lasts more than a day, and the display is simply gorgeous.</p>
        </div>
    </div>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
    <script>
        const favoriteButton = document.querySelector('.btn-favorite');
        const colorButtons = document.querySelectorAll('.color-option');
        const storageButtons = document.querySelectorAll('.storage-option');

        favoriteButton.addEventListener('click', () => {
            favoriteButton.classList.toggle('active');
        });

        colorButtons.forEach(button => {
            button.addEventListener('click', () => {
                colorButtons.forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
            });
        });

        storageButtons.forEach(button => {
            button.addEventListener('click', () => {
                storageButtons.forEach(btn => btn.classList.remove('selected'));
                button.classList.add('selected');
            });
        });
    </script>
</body>
</html>