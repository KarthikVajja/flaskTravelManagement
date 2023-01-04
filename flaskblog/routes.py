import secrets, os
from PIL import Image
from flask import abort, jsonify, render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AeroBookingForm, BusBookingForm, HotelBookingForm
from flaskblog import app, bcrypt, db
from flaskblog.models import Users, Post
from flask_login import login_user, current_user, logout_user, login_required
import psycopg2
from flaskblog import sqlScripts

conn = psycopg2.connect(database="DMQL",
                        host="localhost",
                        user="postgres",
                        password="",
                        port="5432")
cursor = conn.cursor()
def get_booking_id():
    cursor.execute("select max(id) from bookings")
    booking_id = cursor.fetchone()
    booking_id = booking_id[0]+1 if booking_id[0] else 1
    return booking_id
def get_hotel_id():
    cursor.execute("select max(id) from hotel")
    hotel_id = cursor.fetchone()
    hotel_id = hotel_id[0] if hotel_id[0] else 1
    return hotel_id
def get_flight_id():
    cursor.execute("select max(id) from flight")
    flight_id = cursor.fetchone()
    flight_id = flight_id[0] if flight_id[0] else 1
    return flight_id
def get_bus_id():
    cursor.execute("select max(id) from bus")
    bus_id = cursor.fetchone()
    bus_id = bus_id[0] if bus_id[0] else 1
    return bus_id

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page[1:]))
            return redirect(url_for('home', username=current_user.username))
        else:
            flash('Unsuccessful Login! Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        user = Users(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/home/<string:username>")
@login_required
def home(username):
    # page = request.args.get('page', 1, type=int)
    
    user = Users.query.filter_by(username=username).first()
    curr_user_id = user.id
    cursor.execute("select * from bookings where user_id='" + str(curr_user_id) + "'")
    bookings = cursor.fetchall()
    print(bookings)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    posts = None
    return render_template('home.html', posts=posts, bookings=bookings)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.name)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.data.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture:
            picture_fn = save_picture(form.picture)
            current_user.image_file = picture_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


states = ['Andhra', 'Telangana', 'Tamilnadu', 'Karnataka']
cities = {'Andhra': ['Vijayawada', 'Vizag', 'Tirupati'], 
            'Telangana': ['Hyderabad', 'Adilabad', 'Warangal'],
            'Tamilnadu': ['Chennai', 'Katpadi', 'Selam'],
            'Karnataka': ['Banglore', 'Mysore', 'Gulbarga']
        }

@app.route("/booking/new/hotel", methods=['GET', 'POST'])
@login_required
def new_booking_hotel():
    form = HotelBookingForm()
    form.state.choices = [(i,i) for i in states]
    form.city.choices= [(i,i) for i in cities['Andhra']]
    if form.validate_on_submit():
        booking_id = get_booking_id()
        query = sqlScripts.insertBooking(booking_id, 'Hotel', current_user.id)
        cursor.execute(query)
        conn.commit()
        hotel_id = get_hotel_id()
        query = sqlScripts.insertHotel(hotel_id, form.state.data, form.city.data, str(form.start_date.data), str(form.end_date.data), booking_id)
        cursor.execute(query)
        conn.commit()
        flash('Your stay has been successfully booked!', 'success')
        return redirect(url_for('home', username=current_user.username))
    else:
        print(form.state.data, form.city.data)
    return render_template('new_booking_hotel.html', title='New Post', form=form, legend='Book Your Stay')

@app.route('/booking/new/<state>')
@login_required
def fetch_city_hotel(state):
    cities = {'Andhra': ['Vijayawada', 'Vizag', 'Tirupati'], 
            'Telangana': ['Hyderabad', 'Adilabad', 'Warangal'],
            'Tamilnadu': ['Chennai', 'Katpadi', 'Selam'],
            'Karnataka': ['Banglore', 'Mysore', 'Gulbarga']
        }
    cities = [{'id':i,'name':i} for i in cities[state]]
    return jsonify({'cities':cities})

@app.route("/booking/new/flight", methods=['GET', 'POST'])
@login_required
def new_booking_aero():
    form = AeroBookingForm()
    form.sourceState.choices = [(i,i) for i in states]
    form.sourceCity.choices= [(i,i) for i in cities['Andhra']]
    form.destState.choices = [(i,i) for i in states][::-1]
    form.destCity.choices= [(i,i) for i in cities[list(cities.keys())[-1]]]
    if form.validate_on_submit():
        booking_id = get_booking_id()
        query = sqlScripts.insertBooking(booking_id, 'Flight', current_user.id)
        cursor.execute(query)
        conn.commit()
        flight_id = get_flight_id()
        query = sqlScripts.insertFlight(flight_id, form.sourceState.data, 
                    form.sourceCity.data, form.destState.data, form.destCity.data,
                    booking_id, str(form.travelDate.data))
        cursor.execute(query)
        conn.commit()
        flash('Your flight has been successfully booked!', 'success')
        return redirect(url_for('home', username=current_user.username))
    return render_template('new_booking_aero.html', title='New Post', form=form, legend='Book Your Flight')

@app.route("/booking/new/bus", methods=['GET', 'POST'])
@login_required
def new_booking_bus():
    form = BusBookingForm()
    form.sourceState.choices = [(i,i) for i in states]
    form.sourceCity.choices= [(i,i) for i in cities['Andhra']]
    form.destState.choices = [(i,i) for i in states][::-1]
    form.destCity.choices= [(i,i) for i in cities[list(cities.keys())[-1]]]
    if form.validate_on_submit():
        booking_id = get_booking_id()
        query = sqlScripts.insertBooking(booking_id, 'Bus', current_user.id)
        cursor.execute(query)
        conn.commit()
        bus_id = get_bus_id()
        query = sqlScripts.insertBus(bus_id, form.sourceState.data, 
                    form.sourceCity.data, form.destState.data, form.destCity.data,
                    booking_id, str(form.travelDate.data))
        cursor.execute(query)
        conn.commit()
        flash('Your Bus has been successfully booked!', 'success')
        return redirect(url_for('home', username=current_user.username))
    return render_template('new_booking_bus.html', title='New Post', form=form, legend='Book Your Bus')







@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # post = Post(title = form.title.data, content = form.content.data, author = current_user)
        # db.session.add(post)
        # db.session.commit()
        flash('Post has been successfully created!', 'success')
        return redirect(url_for('home', username=current_user.username))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home', username=current_user.username))

@app.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        print('get request')
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)