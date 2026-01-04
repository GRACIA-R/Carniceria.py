CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE,
    costo_kg REAL,
    precio_kg REAL,
    stock_kg REAL
);

CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    producto_id INTEGER,
    kg REAL,
    total REAL
);

CREATE TABLE compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    proveedor TEXT,
    kg REAL,
    costo_total REAL
);

CREATE TABLE caja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    tipo TEXT,
    monto REAL,
    descripcion TEXT
);
