<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - YourPhoneShop</title>

    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />

    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <header>
        <link rel="stylesheet" href="static/content/header.css">

        <div class="logo">
            <a href="/home">
                <img src="/static/images/logo.png" alt="Logo">
            </a>
        </div>

        <div class="search-container">

            <input type="text" placeholder="Search products on the site">

            <button class="search-button">
                <img src="/static/images/magnifier.png" alt="Search">
            </button>
        </div>

        <div class="favorites">
            <a href="/about">
                <img src="/static/images/blueHeart.png" alt="Favorites">
                <span>Favorites</span>
            </a>
        </div>
    </header>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - YourPhoneShop</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>