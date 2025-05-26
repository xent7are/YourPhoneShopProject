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

    <form method="POST" action="/users" enctype="multipart/form-data">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" value="{{form_data['name']}}">
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="text" id="email" name="email" value="{{form_data['email']}}">
        </div>
        <div>
            <label for="phone">Phone (e.g., +71234567894):</label>
            <input type="text" id="phone" name="phone" value="{{form_data['phone']}}">
        </div>
        <div>
            <label for="birth_date">Birth Date (YYYY-MM-DD):</label>
            <input type="date" id="birth_date" name="birth_date" value="{{form_data['birth_date']}}">
        </div>
        <div class="file-input-wrapper">
            <label for="profile_picture">Profile Picture (PNG, JPG, max 5MB):</label>
            <input type="file" id="profile_picture" name="profile_picture" accept="image/png,image/jpeg" class="file-input">
            <input type="hidden" name="profile_picture_name" value="{{form_data['profile_picture_name']}}">
            <button type="button" class="file-input-button">Choose File</button>
            <span class="file-name">{{form_data['profile_picture_name'] or 'No file chosen'}}</span>
        </div>

        % if errors:
            <div class="errors">
                <ul>
                    % for error in errors:
                        <li>{{error}}</li>
                    % end
                </ul>
            </div>
        % end

        <button type="submit">Add User</button>
    </form>
    
    <div id="empty-users-message" style="display: {{'block' if not users else 'none'}};">
        <h3>No active users found.</h3>
    </div>

    <section class="user-list">
        % for i, user in enumerate(users):
            <div class="user-card" data-user-id="{{i}}">
                <div class="user-profile-picture">
                    % if user['profile_picture']:
                        <img src="{{user['profile_picture']}}" alt="{{user['name']}}'s profile picture">
                    % else:
                        <img src="/static/images/user_icons/default_profile.png" alt="Default profile picture">
                    % end
                </div>
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
            const userName = userCard.querySelector('.user-name').textContent;
            
            // Show confirmation dialog
            if (!confirm(`Are you sure you want to delete the user "${userName}"?`)) {
                return;
            }
            
            // Send request to delete user
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

    // Handle file input display
    const fileInput = document.querySelector('.file-input');
    const fileNameDisplay = document.querySelector('.file-name');
    const fileButton = document.querySelector('.file-input-button');

    fileButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = '{{form_data["profile_picture_name"] or "No file chosen"}}';
        }
    });

    checkIfEmpty();
</script>

</body>
</html>