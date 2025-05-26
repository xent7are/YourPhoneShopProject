<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - YourPhoneShop</title>

    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" href="/static/content/header.css">

    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <!--Our header-->
    <header>
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
            <a href="/favorites">
                <img src="/static/images/blueHeart.png" alt="Favorites">
                <span>Favorites</span>
            </a>
        </div>
        <div class="partners">
            <a href="/partners">
                <img src="/static/images/partners.png" alt="Partners">
                <span>Partners</span>
            </a>
        </div>
        <div class="articles">
            <a href="/usefulArticles">
                <img src="/static/images/usefulArticles.png" alt="Articles">
                <span>Articles</span>
            </a>
        </div>
        <div class="users">
            <a href="/users">
                <img src="/static/images/account.png" alt="Users">
                <span>Users</span>
            </a>
        </div>
    </header>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <div class="footer-container">
                <div class="footer-top">
                    <div class="footer-slogan">
                        <h2>"Your Connection, Our Priority."</h2>
                        <p>Find the perfect phone at the perfect price with YourPhoneShop!</p>
                    </div>

                    <div class="footer-contact">
                        <h3>Contact Us</h3>
                        <p>Email: support@yourphoneshop.com</p>
                        <p>Phone: +7 (812) 555-1234</p>
                    </div>
                </div>

                <div class="footer-stores">
                    <h3>Our Stores in St. Petersburg</h3>
                    <ul>
                        <li>
                            <strong>Nevsky Prospekt Store</strong>
                            <p>Nevsky Prospekt, 28</p>
                            <div class="rating">
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9734;</span> (4.0 Stars)
                            </div>
                        </li>
                        <li>
                            <strong>Ligovsky Prospekt Store</strong>
                            <p>Ligovsky Prospekt, 74</p>
                            <div class="rating">
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span> (5.0 Stars)
                            </div>
                        </li>
                        <li>
                            <strong>Sadovaya Street Store</strong>
                            <p>Sadovaya Street, 42</p>
                            <div class="rating">
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9732;</span>
                        <span class="star">&#9732;</span> (3.0 Stars)
                            </div>
                        </li>
                        <li>
                            <strong>Vasilyevsky Island Store</strong>
                            <p>Bolshoy Prospekt, 18</p>
                            <div class="rating">
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span> (5.0 Stars)
                            </div>
                        </li>
                        <li>
                            <strong>Pulkovo Airport Store</strong>
                            <p>Pulkovskoye shosse, 41</p>
                            <div class="rating">
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9733;</span>
                        <span class="star">&#9734;</span> (4.0 Stars)
                            </div>
                        </li>
                    </ul>
                </div>

                <div class="footer-bottom">
            <p>&copy; {{ year }} YourPhoneShop. All rights reserved.</p>
                    <p><a href="/terms">Terms of Service</a> | 
                    <a href="/privacy">Privacy Policy</a></p>
                </div>
            </div>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</body>
</html>