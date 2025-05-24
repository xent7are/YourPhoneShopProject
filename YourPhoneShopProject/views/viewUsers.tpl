% rebase('layout.tpl', title=title, year=year)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" type="text/css" href="/static/content/viewUsersStyle.css">
</head>
<body>

<div class="container">
    <h2>{{title}}</h2>

    <form method="POST" action="/users">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{{form_data['name']}}">
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="text" id="email" name="email" value="{{form_data['email']}}">
        </div>
        <div>
            <label for="phone">Phone (e.g., +71234567890):</label>
            <input type="text" id="phone" name="phone" value="{{form_data['phone']}}">
        </div>
        <div>
            <label for="birth_date">Birth Date (YYYY-MM-DD):</label>
            <input type="text" id="birth_date" name="birth_date" value="{{form_data['birth_date']}}">
        </div>
        <button type="submit">Add User</button>
    </form>

    % if errors:
        <div class="errors">
            <ul>
                % for error in errors:
                    <li>{{error}}</li>
                % end
            </ul>
        </div>
    % end

    <div id="empty-users-message" style="display: {{'block' if not users else 'none'}};">
        <p>No active users found.</p>
    </div>

    <section class="user-list">
        % for i, user in enumerate(users):
            <div class="user-card" data-user-id="{{i}}">
                <div class="user-info">
                    <div class="user-name">{{user['name']}}</div>
                    <div class="user-email">Email: {{user['email']}}</div>
                    <div class="user-phone">Phone: {{user['phone']}}</div>
                    <div class="user-birth-date">Birth Date: {{user['birth_date']}}</div>
                    <div class="user-registration-date">Registration Date: {{user['registration_date']}}</div>
                </div>
                <button class="remove-user">
                    <img src="/static/images/rubbish.png" alt="Delete">
                </button>
            </div>
        % end
    </section>
</div>

<script>
    // Add event listeners to delete buttons
    document.querySelectorAll('.remove-user').forEach(button => {
        button.addEventListener('click', function() {
            const userCard = this.parentElement;
            const userId = userCard.getAttribute('data-user-id');
            
            // Send AJAX request to delete user
            fetch('/delete_user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    userCard.remove();
                    checkIfEmpty();
                } else {
                    alert('Error deleting user: ' + (data.message || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Error deleting user: ' + error);
            });
        });
    });

    // Check if the user list is empty
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