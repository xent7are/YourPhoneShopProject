% rebase('layout.tpl', title=title, year=year)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YourPhoneShop</title>
    <link rel="stylesheet" type="text/css" href="/static/content/viewUsersStyle.css">
</head>
<body>

<div class="container">
    <h2>Active users</h2>

    <div id="empty-users-message" style="display: none;">
        <p>No active users found for this date.</p>
    </div>

    <section class="user-list">
        % for user in users:
            <div class="user-card">
                <div class="user-info">
                    <div class="user-name">{{user['name']}}</div>
                    <div class="user-email">Email: {{user['email']}}</div>
                </div>
                <button class="remove-user">
                    <img src="/static/images/rubbish.png" alt="Remove">
                </button>
            </div>
        % end
    </section>
</div>

<script>
    document.querySelectorAll('.remove-user').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.remove();
            checkIfEmpty();
        });
    });

    function checkIfEmpty() {
        const userList = document.querySelector('.user-list');
        const emptyMessage = document.getElementById('empty-users-message');

        if (userList.children.length === 0) {
            emptyMessage.style.display = 'block';
        } else {
            emptyMessage.style.display = 'none';
        }
    }

    checkIfEmpty();
</script>

</body>
</html>