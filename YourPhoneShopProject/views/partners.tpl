% rebase('layout.tpl', title='Partners', year=year)
<link rel="stylesheet" href="/static/content/partners.css">
<div class="container">
    <main>
        <section class="partners-content">
            <h2>Our Partners</h2>
            <section class="partners-form" id="add-partner">
                <h3>Add a New Partner</h3>
                % if errors:
                    <div class="errors">
                        <ul>
                            % for error in errors:
                                <li>{{ error }}</li>
                            % end
                        </ul>
                    </div>
                % end
                <form method="POST" action="/partners" enctype="multipart/form-data">
                    <div>
                        <label for="name">Name or Company</label>
                        <input type="text" id="name" name="name" value="{{ form_data.get('name', '') }}" required>
                    </div>
                    <div>
                        <label for="email">Email</label>
                        <input type="text" id="email" name="email" value="{{ form_data.get('email', '') }}" required>
                    </div>
                    <div>
                        <label for="address">Address</label>
                        <input type="text" id="address" name="address" value="{{ form_data.get('address', '') }}" required>
                    </div>
                    <div class="phone-input-wrapper">
                        <label for="phone">Phone</label>
                        <select id="region_code" name="region_code">
                            <option value="+1" {{ 'selected' if form_data.get('region_code', '') == '+1' else '' }}>+1 (USA/Canada)</option>
                            <option value="+7" {{ 'selected' if form_data.get('region_code', '') == '+7' else '' }}>+7 (Russia)</option>
                            <option value="+44" {{ 'selected' if form_data.get('region_code', '') == '+44' else '' }}>+44 (UK)</option>
                            <option value="+33" {{ 'selected' if form_data.get('region_code', '') == '+33' else '' }}>+33 (France)</option>
                            <option value="+49" {{ 'selected' if form_data.get('region_code', '') == '+49' else '' }}>+49 (Germany)</option>
                        </select>
                        <input type="text" id="phone" name="phone" value="{{ form_data.get('phone', '') }}" placeholder="(XXX) XXX-XXXX">
                    </div>
                    <div>
                        <label for="description">Description</label>
                        <textarea id="description" name="description" required>{{ form_data.get('description', '') }}</textarea>
                    </div>
                    <div class="file-input-wrapper">
                        <label for="partner_logo">Partner Logo (PNG, JPG, max 5MB)</label>
                        <input type="file" id="partner_logo" name="partner_logo" accept="image/png,image/jpeg" class="file-input">
                        <button type="button" class="file-input-button">Choose File</button>
                        <span class="file-name">{{ form_data.get('logo_filename', 'No file chosen') }}</span>
                        % if form_data.get('temp_logo_path'):
                            <input type="hidden" name="temp_logo_path" value="{{ form_data.get('temp_logo_path') }}">
                            <input type="hidden" name="logo_filename" value="{{ form_data.get('logo_filename') }}">
                            <img src="{{ form_data.get('temp_logo_path') }}" alt="Uploaded logo" style="max-width: 200px; margin-top: 10px;">
                        % end
                    </div>
                    <button type="submit">Add Partner</button>
                </form>
            </section>
            <section class="partners-list">
                <h3>Partner List</h3>
                <div id="empty-partners-message" style="display: {{'block' if not partners else 'none'}};">
                    <p>No partners yet.</p>
                </div>
                % if partners:
                    <div class="partner-list">
                        % for i, partner in enumerate(partners):
                            <div class="partner-card" data-partner-id="{{i}}">
                                <div class="partner-profile-picture">
                                    % if partner['logo']:
                                        <img src="{{partner['logo']}}" alt="{{partner['name']}}'s logo">
                                    % else:
                                        <img src="/static/images/partner_icons/default_logo.png" alt="Default partner logo">
                                    % end
                                </div>
                                <div class="partner-info">
                                    <div class="partner-name">{{ partner['name'] }}</div>
                                    <p>{{ partner['description'] }}</p>
                                    <p><strong>Email:</strong> {{ partner['email'] }}</p>
                                    <p><strong>Address:</strong> {{ partner['address'] }}</p>
                                    <p><strong>Date:</strong> {{ partner['date'] }}</p>
                                    % if partner['phone']:
                                        <p><strong>Phone:</strong> {{ partner['region_code'] }} {{ partner['phone'] }}</p>
                                    % end
                                </div>
                                <button class="remove-partner">
                                    <img src="/static/images/rubbish.png" alt="Delete">
                                </button>
                            </div>
                        % end
                    </div>
                % end
            </section>
        </section>
    </main>
</div>
<script>
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
        }
    });

    // Auto-format phone number
    const phoneInput = document.querySelector('#phone');
    phoneInput.addEventListener('input', () => {
        let value = phoneInput.value.replace(/\D/g, ''); // Remove non-digits
        if (value.length > 10) value = value.slice(0, 10); // Limit to 10 digits
        let formatted = '';
        if (value.length > 0) {
            formatted = '(' + value.slice(0, 3);
            if (value.length > 3) {
                formatted += ') ' + value.slice(3, 6);
                if (value.length > 6) {
                    formatted += '-' + value.slice(6, 10);
                }
            }
        }
        phoneInput.value = formatted;
    });

    // Add event listeners to delete buttons
    document.querySelectorAll('.remove-partner').forEach(button => {
        button.addEventListener('click', function() {
            const partnerCard = this.parentElement;
            const partnerId = partnerCard.getAttribute('data-partner-id');
            
            fetch('/delete_partner', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ partner_id: partnerId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    partnerCard.remove();
                    checkIfEmpty();
                } else {
                    alert('Error deleting partner: ' + (data.message || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Error deleting partner: ' + error);
            });
        });
    });

    // Check if the partner list is empty
    function checkIfEmpty() {
        const partnerList = document.querySelector('.partner-list');
        const emptyMessage = document.getElementById('empty-partners-message');

        if (!partnerList || partnerList.children.length === 0) {
            emptyMessage.style.display = 'block';
        } else {
            emptyMessage.style.display = 'none';
        }
    }

    checkIfEmpty();
</script>