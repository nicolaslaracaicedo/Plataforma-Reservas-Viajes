from pymongo import MongoClient

# Conectar con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['reservas_viajes']

# Definición de las colecciones
users_collection = db['users']
flights_collection = db['flights']
hotels_collection = db['hotels']
cars_collection = db['cars']
reservations_collection = db['reservations']

# Eliminar estas líneas para evitar borrar los datos al iniciar el servidor
# users_collection.delete_many({})
# flights_collection.delete_many({})
# hotels_collection.delete_many({})
# cars_collection.delete_many({})
# reservations_collection.delete_many({})

# Ejemplos de documentos para cada colección
# Solo insertar los datos si las colecciones están vacías
if flights_collection.count_documents({}) == 0:
    flights = [
        {"flight_id": 1, "origin": "New York", "destination": "Los Angeles", "departure_time": "2023-07-10T08:00:00Z", "arrival_time": "2023-07-10T11:00:00Z", "price": 250.0},
        {"flight_id": 2, "origin": "Chicago", "destination": "Miami", "departure_time": "2023-07-11T09:00:00Z", "arrival_time": "2023-07-11T13:00:00Z", "price": 200.0},
        {"flight_id": 3, "origin": "San Francisco", "destination": "New York", "departure_time": "2023-07-12T10:00:00Z", "arrival_time": "2023-07-12T18:00:00Z", "price": 300.0},
        {"flight_id": 4, "origin": "Houston", "destination": "Denver", "departure_time": "2023-07-13T07:00:00Z", "arrival_time": "2023-07-13T09:00:00Z", "price": 150.0},
        {"flight_id": 5, "origin": "Seattle", "destination": "Boston", "departure_time": "2023-07-14T06:00:00Z", "arrival_time": "2023-07-14T14:00:00Z", "price": 280.0},
        {"flight_id": 6, "origin": "Las Vegas", "destination": "Chicago", "departure_time": "2023-07-15T05:00:00Z", "arrival_time": "2023-07-15T11:00:00Z", "price": 220.0},
        {"flight_id": 7, "origin": "Orlando", "destination": "San Francisco", "departure_time": "2023-07-16T04:00:00Z", "arrival_time": "2023-07-16T12:00:00Z", "price": 270.0},
        {"flight_id": 8, "origin": "Boston", "destination": "Los Angeles", "departure_time": "2023-07-17T03:00:00Z", "arrival_time": "2023-07-17T11:00:00Z", "price": 260.0},
        {"flight_id": 9, "origin": "Denver", "destination": "Miami", "departure_time": "2023-07-18T02:00:00Z", "arrival_time": "2023-07-18T10:00:00Z", "price": 230.0},
        {"flight_id": 10, "origin": "Atlanta", "destination": "New York", "departure_time": "2023-07-19T01:00:00Z", "arrival_time": "2023-07-19T05:00:00Z", "price": 180.0}
    ]

    flights_collection.insert_many(flights)

if hotels_collection.count_documents({}) == 0:
    hotels = [
        {"hotel_id": 1, "name": "Hotel California", "location": "Los Angeles", "price_per_night": 150.0, "availability": True},
        {"hotel_id": 2, "name": "The Plaza", "location": "New York", "price_per_night": 350.0, "availability": True},
        {"hotel_id": 3, "name": "Hilton Miami", "location": "Miami", "price_per_night": 200.0, "availability": True},
        {"hotel_id": 4, "name": "Grand Hyatt", "location": "Chicago", "price_per_night": 180.0, "availability": True},
        {"hotel_id": 5, "name": "Four Seasons", "location": "San Francisco", "price_per_night": 400.0, "availability": True},
        {"hotel_id": 6, "name": "Marriott Marquis", "location": "Houston", "price_per_night": 170.0, "availability": True},
        {"hotel_id": 7, "name": "W Seattle", "location": "Seattle", "price_per_night": 220.0, "availability": True},
        {"hotel_id": 8, "name": "Bellagio", "location": "Las Vegas", "price_per_night": 300.0, "availability": True},
        {"hotel_id": 9, "name": "Omni Orlando", "location": "Orlando", "price_per_night": 190.0, "availability": True},
        {"hotel_id": 10, "name": "The Westin", "location": "Boston", "price_per_night": 250.0, "availability": True}
    ]

    hotels_collection.insert_many(hotels)

if cars_collection.count_documents({}) == 0:
    cars = [
        {"car_id": 1, "make": "Toyota", "model": "Camry", "year": 2020, "price_per_day": 40.0, "availability": True},
        {"car_id": 2, "make": "Ford", "model": "Mustang", "year": 2019, "price_per_day": 60.0, "availability": True},
        {"car_id": 3, "make": "Chevrolet", "model": "Impala", "year": 2021, "price_per_day": 50.0, "availability": True},
        {"car_id": 4, "make": "Nissan", "model": "Altima", "year": 2020, "price_per_day": 45.0, "availability": True},
        {"car_id": 5, "make": "BMW", "model": "3 Series", "year": 2021, "price_per_day": 80.0, "availability": True},
        {"car_id": 6, "make": "Audi", "model": "A4", "year": 2020, "price_per_day": 75.0, "availability": True},
        {"car_id": 7, "make": "Mercedes-Benz", "model": "C-Class", "year": 2019, "price_per_day": 90.0, "availability": True},
        {"car_id": 8, "make": "Hyundai", "model": "Elantra", "year": 2021, "price_per_day": 35.0, "availability": True},
        {"car_id": 9, "make": "Kia", "model": "Optima", "year": 2020, "price_per_day": 40.0, "availability": True},
        {"car_id": 10, "make": "Tesla", "model": "Model 3", "year": 2021, "price_per_day": 100.0, "availability": True}
    ]

    cars_collection.insert_many(cars)
