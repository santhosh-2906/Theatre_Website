from flask import Blueprint, render_template, request, redirect, session
from config.db import get_db_connection
from datetime import datetime

user_bp = Blueprint('user', __name__)

# Homepage
@user_bp.route('/')
def home():
    return render_template('home.html')

# User Registration
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (name,email,password) VALUES (%s,%s,%s)", 
            (name, email, password)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/login')

    return render_template('register.html')

# User Login
@user_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Users WHERE email=%s AND password=%s", 
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# Movies Listing
@user_bp.route('/movies')
def movies():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()

    movies_list = [
        {
            'id': m[0],
            'title': m[1],
            'description': m[2],
            'duration': m[3],
            'poster_url': m[4],
            'release_date': m[5]
        }
        for m in movies
    ]
    return render_template('movies.html', movies=movies_list)

# Shows for a specific movie
@user_bp.route('/shows/<int:movie_id>')
def shows(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Shows.id, Movies.title, Screens.name, Shows.show_time, Shows.price
        FROM Shows
        JOIN Movies ON Shows.movie_id = Movies.id
        JOIN Screens ON Shows.screen_id = Screens.id
        WHERE Movies.id = %s
        ORDER BY Shows.show_time ASC
    """, (movie_id,))
    shows = cursor.fetchall()
    cursor.close()
    conn.close()

    shows_list = [
        {
            'id': s[0],
            'movie_title': s[1],
            'screen_name': s[2],
            'show_time': s[3],
            'price': s[4]
        }
        for s in shows
    ]
    return render_template('shows.html', shows=shows_list)

# Snacks Ordering
@user_bp.route('/snacks', methods=['GET', 'POST'])
def snacks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Snacks")
    snacks = cursor.fetchall()
    cursor.close()
    conn.close()

    snacks_list = [{'id': s[0], 'name': s[1], 'price': s[2]} for s in snacks]

    if request.method == 'POST':
        selected_snack_id = request.form.get('snack_id')
        selected_snack = next(
            (s for s in snacks_list if str(s['id']) == selected_snack_id), None
        )
        if selected_snack:
            session['ordered_snack'] = selected_snack
        return redirect('/my_bookings')

    return render_template('snacks.html', snacks=snacks_list)

# Upcoming Movies
@user_bp.route('/upcoming')
def upcoming():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Movies WHERE release_date > %s", 
        (datetime.today(),)
    )
    upcoming = cursor.fetchall()
    cursor.close()
    conn.close()

    upcoming_list = [
        {
            'id': u[0],
            'title': u[1],
            'description': u[2],
            'duration': u[3],
            'poster_url': u[4],
            'release_date': u[5]
        }
        for u in upcoming
    ]
    return render_template('upcoming.html', upcoming=upcoming_list)

# Seat Selection and Booking
from flask import session, redirect, url_for, flash

# Seat Selection and Booking
@user_bp.route('/seat_selection/<int:show_id>', methods=['GET', 'POST'])
def seat_selection(show_id):
    # Redirect if user is not logged in
    if not session.get('user_id'):
        flash("Please log in to book seats.")
        return redirect(url_for('user.login')) 

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch show details
    cursor.execute("""
        SELECT Shows.id, Shows.movie_id, Shows.screen_id, Shows.show_time, Shows.price, Screens.capacity
        FROM Shows
        JOIN Screens ON Shows.screen_id = Screens.id
        WHERE Shows.id = %s
    """, (show_id,))
    show = cursor.fetchone()

    # Fetch movie title
    cursor.execute("SELECT title FROM Movies WHERE id=%s", (show[1],))
    movie = cursor.fetchone()

    # Fetch already booked seats
    cursor.execute("SELECT seat_number FROM Bookings WHERE show_id=%s", (show_id,))
    booked_seats = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    if request.method == 'POST':
        selected_seats = request.form.getlist('seats')
        total_price = len(selected_seats) * show[4]

        conn = get_db_connection()
        cursor = conn.cursor()
        for seat in selected_seats:
            cursor.execute(
                "INSERT INTO Bookings (user_id, show_id, seat_number, booking_time) VALUES (%s,%s,%s,%s)",
                (session['user_id'], show_id, seat, datetime.now())
            )
        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            'booking_confirmation.html',
            movie=movie[0],
            show=show,
            seats=selected_seats,
            total_price=total_price
        )

    return render_template('seat_selection.html', show=show, movie=movie[0], booked_seats=booked_seats)


# My Bookings
@user_bp.route('/my_bookings')
def my_bookings():
    if not session.get('user_id'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT B.id, M.title, S.show_time, B.seat_number, S.price
        FROM Bookings B
        JOIN Shows S ON B.show_id = S.id
        JOIN Movies M ON S.movie_id = M.id
        WHERE B.user_id = %s
        ORDER BY S.show_time DESC
    """, (session['user_id'],))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()

    ordered_snack = session.pop('ordered_snack', None)
    return render_template('booking.html', bookings=bookings, ordered_snack=ordered_snack)

# Logout
@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')
