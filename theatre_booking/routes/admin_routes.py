from flask import Blueprint, render_template, request, redirect, session
from config.db import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# -------------------- Admin Login --------------------
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin')  # Admin dashboard
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')


# -------------------- Admin Logout --------------------
@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')


# -------------------- Admin Dashboard --------------------
@admin_bp.route('/')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Movies
    cursor.execute("SELECT * FROM Movies")
    movies = cursor.fetchall()
    movies_list = []
    for m in movies:
        movies_list.append({
            'id': m[0],
            'title': m[1],
            'description': m[2],
            'duration': m[3],
            'poster_url': m[4],
            'release_date': m[5]
        })

    # Shows with movie and screen names
    cursor.execute("""
        SELECT Shows.id, Movies.title, Screens.name, Shows.show_time, Shows.price
        FROM Shows
        LEFT JOIN Movies ON Shows.movie_id = Movies.id
        LEFT JOIN Screens ON Shows.screen_id = Screens.id
    """)
    shows = cursor.fetchall()
    shows_list = []
    for s in shows:
        shows_list.append({
            'id': s[0],
            'movie_title': s[1],
            'screen_name': s[2],
            'show_time': s[3],
            'price': s[4]
        })

    # Snacks
    cursor.execute("SELECT * FROM Snacks")
    snacks = cursor.fetchall()
    snacks_list = []
    for s in snacks:
        snacks_list.append({
            'id': s[0],
            'name': s[1],
            'price': s[2]
        })

    cursor.close()
    conn.close()
    return render_template('admin.html', movies=movies_list, shows=shows_list, snacks=snacks_list)


# -------------------- Movies CRUD --------------------
@admin_bp.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form['duration']
        poster_url = request.form['poster_url']
        release_date = request.form['release_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Movies (title, description, duration, poster_url, release_date) VALUES (%s,%s,%s,%s,%s)",
            (title, description, duration, poster_url, release_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    return render_template('add_movie.html')


@admin_bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute(
            "UPDATE Movies SET title=%s, description=%s, duration=%s, poster_url=%s, release_date=%s WHERE id=%s",
            (request.form['title'], request.form['description'], request.form['duration'],
             request.form['poster_url'], request.form['release_date'], movie_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    cursor.execute("SELECT * FROM Movies WHERE id=%s", (movie_id,))
    movie = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_movie.html', movie=movie)


@admin_bp.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Movies WHERE id=%s", (movie_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin')


# -------------------- Shows CRUD --------------------
@admin_bp.route('/add_show', methods=['GET', 'POST'])
def add_show():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM Movies")
    movies = cursor.fetchall()
    cursor.execute("SELECT id, name FROM Screens")
    screens = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Shows (movie_id, screen_id, show_time, price) VALUES (%s,%s,%s,%s)",
            (request.form['movie_id'], request.form['screen_id'], request.form['show_time'], request.form['price'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    return render_template('add_show.html', movies=movies, screens=screens)


@admin_bp.route('/edit_show/<int:show_id>', methods=['GET', 'POST'])
def edit_show(show_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM Movies")
    movies = cursor.fetchall()
    cursor.execute("SELECT id, name FROM Screens")
    screens = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute(
            "UPDATE Shows SET movie_id=%s, screen_id=%s, show_time=%s, price=%s WHERE id=%s",
            (request.form['movie_id'], request.form['screen_id'], request.form['show_time'], request.form['price'], show_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    cursor.execute("SELECT * FROM Shows WHERE id=%s", (show_id,))
    show = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_show.html', show=show, movies=movies, screens=screens)


@admin_bp.route('/delete_show/<int:show_id>')
def delete_show(show_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Shows WHERE id=%s", (show_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin')


# -------------------- Snacks CRUD --------------------
@admin_bp.route('/add_snack', methods=['GET', 'POST'])
def add_snack():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Snacks (name, price) VALUES (%s, %s)",
            (request.form['name'], request.form['price'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    return render_template('add_snack.html')


@admin_bp.route('/edit_snack/<int:snack_id>', methods=['GET', 'POST'])
def edit_snack(snack_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute(
            "UPDATE Snacks SET name=%s, price=%s WHERE id=%s",
            (request.form['name'], request.form['price'], snack_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/admin')

    cursor.execute("SELECT * FROM Snacks WHERE id=%s", (snack_id,))
    snack = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_snack.html', snack=snack)


@admin_bp.route('/delete_snack/<int:snack_id>')
def delete_snack(snack_id):
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Snacks WHERE id=%s", (snack_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/admin')
