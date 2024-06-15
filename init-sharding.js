// Iniciar el servidor de configuración
rs.initiate({
    _id: "configRS",
    configsvr: true,
    members: [
        { _id: 0, host: "config-server:27019" }
    ]
});

// Iniciar el shard1
rs.initiate({
    _id: "shard1RS",
    members: [
        { _id: 0, host: "shard1-server:27018" }
    ]
});

// Iniciar el shard2
rs.initiate({
    _id: "shard2RS",
    members: [
        { _id: 0, host: "shard2-server:27017" }
    ]
});

// Añadir shards al router
sh.addShard("shard1RS/shard1-server:27018");
sh.addShard("shard2RS/shard2-server:27017");

// Crear las colecciones e insertar datos de prueba
db = db.getSiblingDB('reservas_viajes');

// Colección de usuarios
db.createCollection('usuarios');
db.usuarios.insertMany([
    { nombre: "Juan Perez", email: "juan@example.com", telefono: "1234567890", password: "password123" },
    { nombre: "Maria Gomez", email: "maria@example.com", telefono: "0987654321", password: "password456" }
]);

// Colección de vuelos
db.createCollection('vuelos');
db.vuelos.insertMany([
    { origen: "Lima", destino: "Buenos Aires", fecha_salida: new Date("2024-07-01"), fecha_llegada: new Date("2024-07-01"), precio: 200, aerolinea: "LATAM" },
    { origen: "Lima", destino: "Santiago", fecha_salida: new Date("2024-07-05"), fecha_llegada: new Date("2024-07-05"), precio: 150, aerolinea: "Avianca" }
]);

// Colección de hoteles
db.createCollection('hoteles');
db.hoteles.insertMany([
    { nombre: "Hotel Lima", ubicacion: "Lima", precio_por_noche: 100, amenidades: ["WiFi", "Desayuno"] },
    { nombre: "Hotel Buenos Aires", ubicacion: "Buenos Aires", precio_por_noche: 120, amenidades: ["Piscina", "Gimnasio"] }
]);

// Colección de coches
db.createCollection('coches');
db.coches.insertMany([
    { marca: "Toyota", modelo: "Corolla", año: 2020, precio_por_dia: 50, disponibilidad: true },
    { marca: "Honda", modelo: "Civic", año: 2019, precio_por_dia: 45, disponibilidad: true }
]);

// Colección de reservas
db.createCollection('reservas');
db.reservas.insertMany([
    { usuario_id: ObjectId("607c191e810c19729de860ea"), tipo_reserva: "vuelo", detalle_reserva: { vuelo_id: ObjectId("607c191e810c19729de860eb"), fecha_inicio: new Date("2024-07-01"), fecha_fin: new Date("2024-07-01"), precio_total: 200 }, fecha_reserva: new Date() },
    { usuario_id: ObjectId("607c191e810c19729de860ea"), tipo_reserva: "hotel", detalle_reserva: { hotel_id: ObjectId("607c191e810c19729de860ec"), fecha_inicio: new Date("2024-07-02"), fecha_fin: new Date("2024-07-05"), precio_total: 300 }, fecha_reserva: new Date() }
]);
