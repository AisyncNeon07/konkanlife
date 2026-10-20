# Explore Ratnagiri - Beginner's Code Guide

Welcome! This guide explains how your Django project works, step-by-step. Think of Django as a restaurant:
*   **URLs (`urls.py`)**: The Menu (What can you order?)
*   **Views (`views.py`)**: The Waiter/Chef (Takes your order, gets the food/data, prepares it).
*   **Models (`models.py`)**: The Pantry (Where the raw food/data is stored).
*   **Templates (`.html`)**: The Plate (How the food/page is presented to you).

---

## 1. Project Structure (The Kitchen Layout)

*   **`config/`**: This is the control center.
    *   `settings.py`: The rulebook. It tells Django where the database is, what apps are installed, and where to find images.
    *   `urls.py`: The main entrance. It directs incoming web traffic to the right "App".
*   **`core/`**: Handles general pages like the Homepage.
*   **`destinations/`**: Handles everything about places (Forts, Beaches).
*   **`reviews/`**: Handles user comments and ratings.
*   **`accounts/`**: Handles Login and Registration.
*   **`templates/`**: Contains the HTML files (the visual part).
*   **`static/`**: Contains CSS (styling), JavaScript, and static images (logos).
*   **`media/`**: Contains images uploaded by users (like destination photos).

---

## 2. The Flow: What happens when you visit the Homepage?

1.  **You type** `http://127.0.0.1:8000/` in your browser.
2.  **Django checks `config/urls.py`**:
    ```python
    path('', include('core.urls')), # It sees empty path '' matches core.urls
    ```
3.  **It goes to `core/urls.py`**:
    ```python
    path('', views.home, name='home'), # It calls the 'home' view function
    ```
4.  **It executes `core/views.py` (The Logic)**:
    ```python
    def home(request):
        # 1. Get data from the database (The Pantry)
        featured = Destination.objects.all()[:3] 
        
        # 2. Pack it into a 'context' dictionary
        context = { 'featured_destinations': featured }
        
        # 3. Send it to the template (The Plate)
        return render(request, 'core/index.html', context)
    ```
5.  **It renders `templates/core/index.html`**:
    The HTML file takes the data (`featured_destinations`) and displays it using `{}` tags.

---

## 3. Key Files Explained

### A. The Data: `destinations/models.py`
This defines what a "Destination" looks like in the database.
```python
class Destination(models.Model):
    title = models.CharField(max_length=200) # Text field for name
    slug = models.SlugField(...) # URL-friendly name (e.g., "ratnadurg-fort")
    category = models.CharField(...) # Dropdown for Fort, Beach, etc.
    main_image = models.ImageField(...) # Stores the photo
    
    def __str__(self):
        return self.title # Shows the name in Admin panel instead of "Object 1"
```

### B. The Logic: `destinations/views.py`
This handles the "Search" and "Filter" logic.
```python
def destination_list(request):
    # Get the search text from the URL (e.g., ?q=beach)
    query = request.GET.get('q') 
    
    destinations = Destination.objects.all() # Start with ALL destinations

    if query:
        # Filter: Title CONTAINS query OR Location CONTAINS query
        destinations = destinations.filter(
            Q(title__icontains=query) | Q(location_name__icontains=query)
        )
    
    # Send the filtered list to the HTML
    return render(request, 'destinations/destination_list.html', {'destinations': destinations})
```

### C. The Look: `templates/base.html`
This is the "Master Template". Every other page extends this. It contains the Navbar and Footer so you don't have to copy-paste them on every page.
```html
<!-- The Navbar is here -->
<nav>...</nav>

<!-- This is a placeholder where other pages fill in their content -->
{% block content %}{% endblock %}

<!-- The Footer is here -->
<footer>...</footer>
```

---

## 4. How to add a new Destination?
You don't need to write code for this! We used Django's **Admin Panel**.
1.  Go to `/admin`.
2.  Login with the superuser you created.
3.  Click "Destinations".
4.  Click "Add Destination".
5.  Fill the form and Save. Django saves it to the database automatically.

## 5. Next Steps for You
*   **Try changing the colors**: Go to `templates/base.html` and change the CSS classes (e.g., `bg-primary` to `bg-danger`).
*   **Add a new field**: Try adding a `contact_number` to the `Destination` model in `models.py`. (Remember to run `makemigrations` and `migrate` after changing models!).
