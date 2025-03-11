% rebase('layout.tpl', title='Home Page', year=year)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Online Phone Store</title>
    <style>
      body {
        font-family: Gill Sans MT;
        margin: 0;
        padding: 0;
        background-color: #f8f8f8;
        letter-spacing: 1px;
      }

      .container {
        max-width: 1300px;
        margin: 0;
        padding: 2px;
      }

      main {
        display: flex;
        margin-top: 10px;
      }

      .sidebar {
        width: 260px;
        background-color: #e0ffff;
        padding: 15px;
        border-radius: 10px;
        margin-right: 40px;
        position: sticky;
        top: 20px;
      }

      .sidebar h3 {
        margin-top: 0;
      }

      .sidebar ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
      }

     .sidebar li {
        margin-bottom: 20px;
        padding: 0;
        border-radius: 10px;
        background-color: #d0ffff;
        cursor: pointer;
      }


      .checkbox-container {
        display: flex;
        align-items: center;
        padding-left: 8px; 
      }

      .checkbox-container input[type="checkbox"] {
        margin: 0;
        margin-right: 5px;
      }

       .product-list {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        padding: 10px; 
        gap: 40px;
      }

      .product-card {
        width: auto;
        margin: 10px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        text-align: center;
        background-color: #f0ffff;
      }

      .product-card img {
        max-width: 100%;
        height: 240px;
        width: auto;
        margin-top: 10px;
        margin-bottom: 10px;
        object-fit: contain;
      }

      .product-name {
        font-weight: bold;
        margin-bottom: 5px;
      }

      .product-price {
        font-size: 1.2em;
        color: #007bff;
        margin-bottom: 10px;
      }

      .favorite-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        font-size: 1.5em;
        color: #ccc;
      }

      .favorite-button.active {
        color: #e91e63;
      }

    </style>


</head>
<body>

    <div class="container">


        <main>
            <aside class="sidebar">
                <h3>Select Phone Models</h3>
                <ul>
                    <li class="checkbox-container"><input type="checkbox"> Samsung</li>
                    <li class="checkbox-container"><input type="checkbox"> Apple</li>
                    <li class="checkbox-container"><input type="checkbox"> Honor</li>
                    <li class="checkbox-container"><input type="checkbox"> Xiaomi</li>
                    <li class="checkbox-container"><input type="checkbox"> Pixel</li>
                </ul>
            </aside>
            <section class="product-list">
                <div class="product-card">
                    <img src="/static/images/samsungA35.png" alt="Samsung">
                    <a href="/viewingProduct">
                        <div class="product-name" >Samsung A35</div>
                    </a>
                    <div class="product-price">$999.99</div>
                    <button class="favorite-button">&#10084;</button>
                </div>

                <div class="product-card">
                    <img src="/static/images/honor.jpg" alt="Honor">
                    <div class="product-name">Honor 5</div>
                    <div class="product-price">$899.99</div>
                    <button class="favorite-button">&#10084;</button>
                </div>
                <div class="product-card">
                    <img src="/static/images/iPhone15.png" alt="iPhone">
                    <div class="product-name">iPhone 15</div>
                    <div class="product-price">$999.99</div>
                    <button class="favorite-button">&#10084;</button>
                </div>
            </section>
        </main>

    </div>

    <script>
        const favoriteButtons = document.querySelectorAll('.favorite-button');

        favoriteButtons.forEach(button => {
            button.addEventListener('click', () => {
                button.classList.toggle('active');
            });
        });
    </script>

</body>
</html>