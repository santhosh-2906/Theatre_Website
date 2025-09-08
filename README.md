**🎬 Movie Theatre Booking System**

**Overview**

		A full-stack movie theatre booking app built with Flask + MySQL. Users can browse movies, select seats, book tickets with snacks, and view booking history. Admins have a secure panel to manage movies, shows, 		users, and theatre screens.

 **Features**

 		User authentication (Flask-Login)

 		Interactive seat selection (prevents double booking)

	 	Ticket booking with snack add-ons

 		Booking history for users

 		Admin panel: manage movies, shows, snacks, users, and bookings

 **Tech Stack**

		Backend: Python (Flask), Gunicorn

		Frontend: HTML, CSS, JS, Jinja2

		Database: MySQL

		Deployment: Render (Clever Cloud for DB)
```
## 📁 Folder Structure

THEATRE_PROJECT/
├── .venv/ # Virtual environment
├── config/ # Configuration files
├── routes/ # API endpoints and views
│ ├── admin_routes.py # Routes for the admin panel
│ └── user_routes.py # Routes for user-facing features
├── static/ # Static assets (CSS, JS, images)
│ ├── css/
│ │ └── style.css
│ ├── img/
│ └── js/
├── templates/ # Jinja2 HTML templates
│ ├── add_movie.html
│ ├── add_show.html
│ └── ... (all other HTML files)
├── .env # Environment variables
└── app.py # Main application entry point
```

 **Quick Start**
 ```
git clone <repo-url>
cd theatre_project
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py

```
