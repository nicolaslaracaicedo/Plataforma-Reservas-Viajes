from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from bson.objectid import ObjectId
from .models import users_collection, flights_collection, hotels_collection, cars_collection, reservations_collection

# Crear Blueprint
bp = Blueprint('main', __name__)

# Definir filtro datetimeformat
@bp.app_template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')  # Formato ISO 8601
        except ValueError:
            return value  # Si el valor no se puede convertir, devuelve la cadena original
    if value is None:
        return ""
    return value.strftime(format)

# Rutas
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/buscar_vuelos')
def buscar_vuelos():
    flights = flights_collection.find()
    return render_template('buscar_vuelos.html', flights=flights)

@bp.route('/buscar_hoteles')
def buscar_hoteles():
    hotels = hotels_collection.find()
    return render_template('buscar_hoteles.html', hotels=hotels)

@bp.route('/buscar_coches')
def buscar_coches():
    cars = cars_collection.find()
    return render_template('buscar_coches.html', cars=cars)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        
        users_collection.insert_one(user)
        flash("Usuario registrado con éxito", 'success')
        session['user_name'] = name
        session['user_email'] = email
        return redirect(url_for('.index'))  # Usar '.index' para referirse a la función dentro del mismo Blueprint
    
    return render_template('register.html')

@bp.route('/reservar', methods=['GET', 'POST'])
def reservar():
    if request.method == 'POST':
        user_email = request.form['user_email']
        flight_id = request.form.get('flight_id')
        hotel_id = request.form.get('hotel_id')
        car_id = request.form.get('car_id')
        
        user = users_collection.find_one({"email": user_email})
        if user:
            reservation = {
                "user_id": str(user['_id']),  # Convertir ObjectId a cadena
                "flight_id": flight_id,
                "hotel_id": hotel_id,
                "car_id": car_id,
                "reservation_date": datetime.utcnow()
            }
            
            reservations_collection.insert_one(reservation)
            flash("Reserva realizada con éxito", 'success')
        else:
            flash("Usuario no encontrado", 'error')
        
        return redirect(url_for('.index'))  # Usar '.index' para referirse a la función dentro del mismo Blueprint
    
    users = users_collection.find()
    flights = flights_collection.find()
    hotels = hotels_collection.find()
    cars = cars_collection.find()
    
    return render_template('reservar.html', users=users, flights=flights, hotels=hotels, cars=cars)

@bp.route('/historial', methods=['GET'])
def historial():
    if 'user_email' not in session:
        flash("Debe iniciar sesión para ver el historial de reservas", 'error')
        return redirect(url_for('.login'))  # Usar '.login' para referirse a la función dentro del mismo Blueprint
    
    email = session['user_email']
    user = users_collection.find_one({"email": email})
    reservations = []
    if user:
        reservations = reservations_collection.find({"user_id": str(user['_id'])})  # Convertir ObjectId a cadena
    return render_template('historial.html', reservations=reservations)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users_collection.find_one({"email": email, "password": password})
        if user:
            session['user_email'] = email
            session['user_name'] = user['name']  # Almacena el nombre de usuario en la sesión
            flash("Inicio de sesión exitoso", 'success')
            return redirect(url_for('.index'))  # Usar '.index' para referirse a la función dentro del mismo Blueprint
        else:
            flash("Credenciales incorrectas. Inténtelo de nuevo.", 'error')
    
    return render_template('login.html', is_login_page=True)

@bp.route('/logout')
def logout():
    session.clear()
    flash('¡Has cerrado sesión exitosamente!', 'success')
    return redirect(url_for('.index'))  # Usar '.index' para referirse a la función dentro del mismo Blueprint

@bp.route('/ingresar_vuelo', methods=['GET', 'POST'])
def ingresar_vuelo():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        price = float(request.form['price'])
        
        flight = {
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "price": price
        }
        
        flights_collection.insert_one(flight)
        flash("Vuelo ingresado exitosamente", 'success')
        return redirect(url_for('.ingresar_vuelo'))  # Usar '.ingresar_vuelo' para referirse a la función dentro del mismo Blueprint
    
    flights = flights_collection.find()
    return render_template('ingresar_vuelo.html', flights=flights)

@bp.route('/editar_vuelo/<string:flight_id>', methods=['GET', 'POST'])
def editar_vuelo(flight_id):
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        price = float(request.form['price'])

        flight = {
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "price": price
        }

        flights_collection.update_one({"_id": ObjectId(flight_id)}, {"$set": flight})
        flash("Vuelo actualizado exitosamente", 'success')
        return redirect(url_for('.buscar_vuelos'))  # Redirigir a la página de búsqueda de vuelos

    flight = flights_collection.find_one({"_id": ObjectId(flight_id)})
    return render_template('editar_vuelo.html', flight=flight)

@bp.route('/eliminar_vuelo/<string:flight_id>', methods=['POST'])
def eliminar_vuelo(flight_id):
    flights_collection.delete_one({"_id": ObjectId(flight_id)})
    flash("Vuelo eliminado exitosamente", 'success')
    return redirect(url_for('.buscar_vuelos'))  # Usar '.buscar_vuelos' para referirse a la función dentro del mismo Blueprint

# Rutas para hoteles
@bp.route('/ingresar_hotel', methods=['GET', 'POST'])
def ingresar_hotel():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        available_from = request.form['available_from']
        available_to = request.form['available_to']
        price_per_night = float(request.form['price_per_night'])
        
        hotel = {
            "name": name,
            "location": location,
            "available_from": available_from,
            "available_to": available_to,
            "price_per_night": price_per_night
        }
        
        hotels_collection.insert_one(hotel)
        flash("Hotel ingresado exitosamente", 'success')
        return redirect(url_for('.ingresar_hotel'))  # Usar '.ingresar_hotel' para referirse a la función dentro del mismo Blueprint
    
    hotels = hotels_collection.find()
    return render_template('ingresar_hotel.html', hotels=hotels)

@bp.route('/editar_hotel/<string:hotel_id>', methods=['GET', 'POST'])
def editar_hotel(hotel_id):
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price_per_night = float(request.form['price_per_night'])
        availability = request.form['availability'] == 'True'

        hotel = {
            "name": name,
            "location": location,
            "price_per_night": price_per_night,
            "availability": availability
        }

        hotels_collection.update_one({"_id": ObjectId(hotel_id)}, {"$set": hotel})
        flash("Hotel actualizado exitosamente")
        return redirect(url_for('.buscar_hoteles'))  # Redirigir a la página de búsqueda de hoteles

    hotel = hotels_collection.find_one({"_id": ObjectId(hotel_id)})
    return render_template('editar_hotel.html', hotel=hotel)


@bp.route('/eliminar_hotel/<string:hotel_id>', methods=['POST'])
def eliminar_hotel(hotel_id):
    hotels_collection.update_one({"_id": ObjectId(hotel_id)}, {"$set": {"availability": False}})
    flash("Hotel marcado como no disponible")
    return redirect(url_for('.buscar_hoteles'))

