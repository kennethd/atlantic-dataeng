PRAGMA foreign_keys = ON;

CREATE TABLE customers
(
    id INTEGER UNIQUE NOT NULL,
    first_name TEXT NOT NULL ,
    last_name TEXT NOT NULL ,
    address TEXT NOT NULL ,
    state TEXT NOT NULL ,
    zip TEXT NOT NULL ,
    PRIMARY KEY (id ASC)
);

CREATE INDEX idx_customers_name ON customers(last_name, first_name);


CREATE TABLE products
(
    id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL, -- VARCHAR(100)
    price INTEGER NOT NULL DEFAULT 0, -- stored as cents
    PRIMARY KEY (id ASC)
);

CREATE INDEX idx_products_name ON products(name);


CREATE TABLE transactions
(
    id INTEGER UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    dt TEXT NOT NULL, -- iso8601 string format
    action STRING NOT NULL, -- 'new', 'cancelled'
    PRIMARY KEY (id ASC),
    FOREIGN KEY (customer_id) REFERENCES (customers.id),
    FOREIGN KEY (product_id) REFERENCES (products.id)
);


