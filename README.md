This is a full-stack event scheduling application built with:

* **Backend:** Django + Django REST Framework (DRF)
* **Frontend:** React 18 + TypeScript + TailwindCSS (Vite-powered SPA)
* **Database:** MySQL
* **Containerization:** Docker

Users can create, view, and manage both one-time and complex recurring events. The frontend includes a dynamic calendar grid that displays booked dates with visual markers.

---
### Setup
**Follow these simple steps & run the commands**
- step - 1 : docker-compose up --build
- step -2 : docker-compose exec backend python manage.py migrate

### 1. **Monorepo Structure**


### 2. **Separation of Concerns**

* Backend handles all business logic (e.g., recurrence rules, validation, user auth)
* Frontend consumes backend APIs and handles UI interactivity, form state, and calendar rendering

### 3. **Recurrence Logic**

* Implemented fully in the backend using a modular approach:

  * one_time, daily, weekly, monthly, interval, weekday, relative
* Using calendar_grid table to pre-generate and store all days between 2025–2030 allows for optimized lookups and simplifies recurrence logic.

### 4. **Signals for Initialization**

* A signals.py file populates the calendar_grid table

### 5. **Token-based Authentication**

* Used Django REST Framework's TokenAuthentication for simplicity
* Tokens are stored in localStorage on the frontend for authenticated API calls

---

Intentional Shortcuts

* Used DRF TokenAuth instead of OAuth or JWT for speed and simplicity
* Reloaded entire page after create/edit/delete instead of patching local state

Trade-offs

* Used minimal libraries for the sake of demonstrating competence & problem solving skill

---


## Testing

* DRF API endpoints tested via Postman
* Frontend event handling and state transitions tested manually


---

## Future Improvements

* Modularize React into reusable components
* Add test coverage for critical recurrence paths
* Replace token auth with JWT for better security
* Add drag/drop or interactive calendar features
* Optimize calendar API with caching or pagination

