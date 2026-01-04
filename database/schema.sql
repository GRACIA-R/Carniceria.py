-- =========================
-- PRODUCTOS
-- =========================
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT,
    costo REAL NOT NULL,
    precio REAL NOT NULL,
    stock REAL NOT NULL DEFAULT 0,
    unidad TEXT DEFAULT 'kg'
);

-- =========================
-- CLIENTES
-- =========================
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    tipo TEXT DEFAULT 'general',
    lista_precio_id INTEGER,
    activo INTEGER DEFAULT 1
);

-- =========================
-- PROVEEDORES
-- =========================
CREATE TABLE IF NOT EXISTS proveedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    contacto TEXT,
    telefono TEXT,
    email TEXT,
    activo INTEGER DEFAULT 1
);

-- =========================
-- LISTAS DE PRECIOS
-- =========================
CREATE TABLE IF NOT EXISTS listas_precios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

-- =========================
-- PRECIOS POR PRODUCTO
-- =========================
CREATE TABLE IF NOT EXISTS precios_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    lista_id INTEGER NOT NULL,
    precio REAL NOT NULL,
    UNIQUE(producto_id, lista_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (lista_id) REFERENCES listas_precios(id)
);

-- =========================
-- VENTAS (CABECERA)
-- =========================
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente_id INTEGER,
    total REAL NOT NULL,
    pago REAL NOT NULL,
    cambio REAL NOT NULL,
    metodo_pago TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


-- =========================
-- VENTAS (DETALLE)
-- =========================
CREATE TABLE IF NOT EXISTS venta_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);


-- =========================
-- COMPRAS (CABECERA)
-- =========================
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    proveedor_id INTEGER,
    total REAL NOT NULL,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

-- =========================
-- COMPRAS (DETALLE)
-- =========================
CREATE TABLE IF NOT EXISTS compra_detalle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad REAL NOT NULL,
    costo REAL NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- =========================
-- CAJA
-- =========================
CREATE TABLE IF NOT EXISTS caja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    tipo TEXT NOT NULL,          -- ingreso | egreso
    concepto TEXT NOT NULL,
    monto REAL NOT NULL
);
