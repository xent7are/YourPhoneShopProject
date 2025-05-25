% rebase('layout.tpl', title='Home Page', year=year)
    <div class="container">
        <main>
        <link rel="stylesheet" href="/static/content/main_site.css" />
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