PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS cafe_tables (
  id INTEGER PRIMARY KEY,
  table_number VARCHAR(20) NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS menu_items (
  id INTEGER PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(50) NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  rating NUMERIC(3,1) DEFAULT 0,
  reviews INTEGER DEFAULT 0,
  image TEXT NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_images (
  id INTEGER PRIMARY KEY,
  menu_item_id INTEGER NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS addons (
  id INTEGER PRIMARY KEY,
  menu_item_id INTEGER NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
  name VARCHAR(150) NOT NULL,
  price NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  order_number VARCHAR(30) NOT NULL UNIQUE,
  table_id INTEGER NOT NULL REFERENCES cafe_tables(id),
  user_id INTEGER REFERENCES users(id),
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  subtotal NUMERIC(10,2) NOT NULL,
  tax NUMERIC(10,2) NOT NULL,
  total NUMERIC(10,2) NOT NULL,
  special_instructions TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  menu_item_id INTEGER NOT NULL REFERENCES menu_items(id),
  item_name VARCHAR(150) NOT NULL,
  unit_price NUMERIC(10,2) NOT NULL,
  quantity INTEGER NOT NULL,
  instructions TEXT
);

CREATE TABLE IF NOT EXISTS order_item_addons (
  id INTEGER PRIMARY KEY,
  order_item_id INTEGER NOT NULL REFERENCES order_items(id) ON DELETE CASCADE,
  addon_id INTEGER NOT NULL REFERENCES addons(id),
  addon_name VARCHAR(150) NOT NULL,
  addon_price NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY,
  table_id INTEGER NOT NULL REFERENCES cafe_tables(id),
  rating INTEGER NOT NULL,
  message TEXT,
  created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS waiter_requests (
  id INTEGER PRIMARY KEY,
  table_id INTEGER NOT NULL REFERENCES cafe_tables(id),
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS bill_requests (
  id INTEGER PRIMARY KEY,
  table_id INTEGER NOT NULL REFERENCES cafe_tables(id),
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL
);
