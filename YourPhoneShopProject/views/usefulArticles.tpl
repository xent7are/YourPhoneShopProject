% rebase('layout.tpl', title='Useful Articles', year=year)

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" type="text/css" href="/static/content/usefulArticlesStyle.css">
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const addButton = document.querySelector('.add-article');
            const formSection = document.querySelector('.add-article-form');
            addButton.addEventListener('click', function() {
                formSection.style.display = 'block';
                formSection.scrollIntoView({ behavior: 'smooth' });
            });

            % if errors:
                formSection.style.display = 'block';
                formSection.scrollIntoView({ behavior: 'smooth' });
            % end

            // Character counter for author
            const authorInput = document.getElementById('author');
            const authorCounter = document.getElementById('author-counter');
            authorInput.addEventListener('input', function() {
                const count = this.value.length;
                authorCounter.textContent = `${count}/50`;
                if (count > 50) {
                    authorCounter.style.color = 'red';
                } else {
                    authorCounter.style.color = '#124176';
                }
            });
            authorInput.dispatchEvent(new Event('input'));

            // Character counter for title
            const titleInput = document.getElementById('title');
            const titleCounter = document.getElementById('title-counter');
            titleInput.addEventListener('input', function() {
                const count = this.value.length;
                titleCounter.textContent = `${count}/100`;
                if (count > 100) {
                    titleCounter.style.color = 'red';
                } else {
                    titleCounter.style.color = '#124176';
                }
            });
            titleInput.dispatchEvent(new Event('input'));

            // Character counter for description
            const descInput = document.getElementById('description');
            const descCounter = document.getElementById('desc-counter');
            descInput.addEventListener('input', function() {
                const count = this.value.length;
                descCounter.textContent = `${count}/300`;
                if (count > 300) {
                    descCounter.style.color = 'red';
                } else {
                    descCounter.style.color = '#124176';
                }
            });
            descInput.dispatchEvent(new Event('input'));

            // File input name display and image preview
            const fileInput = document.getElementById('image');
            const fileNameDisplay = document.getElementById('file-name');
            const imagePreview = document.getElementById('image-preview');
            fileInput.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    fileNameDisplay.textContent = file.name;
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        imagePreview.src = e.target.result;
                        imagePreview.style.display = 'block';
                    };
                    reader.readAsDataURL(file);
                } else {
                    fileNameDisplay.textContent = 'No file chosen';
                    imagePreview.src = '';
                    imagePreview.style.display = 'none';
                }
            });

            // Delete article
            document.querySelectorAll('.delete-article').forEach(button => {
                button.addEventListener('click', function() {
                    const author = this.dataset.author;
                    const date = this.dataset.date;
                    const index = this.dataset.index;
                    if (confirm('Are you sure you want to delete this article?')) {
                        fetch('/deleteArticle', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ author, date, index })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                location.reload();
                            } else {
                                alert('Error deleting article: ' + data.message);
                            }
                        })
                        .catch(error => alert('Error: ' + error));
                    }
                });
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header-section">
            <div class="title">List of Useful Articles</div>
            <button class="add-article">
                <img src="/static/images/addArticle.png" alt="Add article icon">
                Add an Article
            </button>
        </div>
        <div class="cards">
            % for i, article in enumerate(articles):
                <div class="card">
                    <h2>{{article['title']}}</h2>
                    <div class="card-img-container">
                        <img src="{{article['image']}}" alt="{{article['title']}}">
                    </div>
                    <p>{{article['description']}}</p>
                    <div class="card-footer">
                        <div class="article-meta-container">
                            <span class="article-author">Author: {{article['author']}}</span>
                            <span class="article-date">Date added: {{article['date_added']}}</span>
                        </div>
                        <div class="button-group">
                            <a href="{{article['link']}}" class="read-more" target="_blank">Read more</a>
                            <button class="delete-article" data-author="{{article['author']}}" data-date="{{article['date_added'].split(' ')[0].split('.')[2] + '-' + article['date_added'].split(' ')[0].split('.')[1] + '-' + article['date_added'].split(' ')[0].split('.')[0]}}" data-index="{{article['index_in_date']}}"></button>
                        </div>
                    </div>
                </div>
            % end
        </div>
        % if show_form:
            <div class="add-article-form" style="display: block;">
        % else:
            <div class="add-article-form" style="display: none;">
        % end
            <form action="/usefulArticles" method="POST" enctype="multipart/form-data">
                <h2>Add New Article</h2>
                <label for="author">Author:</label>
                <input type="text" id="author" name="author" maxlength="50" value="{{form_data['author']}}" required>
                <span id="author-counter" class="char-count">0/50</span>
                <label for="phone">Phone Number:</label>
                <input type="tel" id="phone" name="phone" value="{{form_data['phone']}}" required>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" value="{{form_data['email']}}" required>
                <label for="title">Title:</label>
                <input type="text" id="title" name="title" maxlength="100" value="{{form_data['title']}}" required>
                <span id="title-counter" class="char-count">0/100</span>
                <label for="image" class="reduced-margin">Image:</label>
                <div class="file-input-wrapper">
                    <input type="file" id="image" name="image" accept="image/*" required>
                    <span class="file-input-button">Choose File</span>
                    <span id="file-name" class="file-name-display">No file chosen</span>
                </div>
                <div class="image-preview">
                    <img id="image-preview" src="" alt="Image preview">
                </div>
                <label for="description">Description:</label>
                <textarea id="description" name="description" maxlength="300" required>{{form_data['description']}}</textarea>
                <span id="desc-counter" class="char-count">0/300</span>
                <label for="link" class="reduced-margin">Link:</label>
                <input type="url" id="link" name="link" value="{{form_data['link']}}" required>
                % if errors:
                    <div class="errors">
                        <ul>
                            % for error in errors:
                                <li>{{error}}</li>
                            % end
                        </ul>
                    </div>
                % end
                <button type="submit">Submit</button>
            </form>
        </div>
    </div>
</body>
</html>