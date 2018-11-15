PRAGMA foreign_keys = ON;

CREATE TABLE customers
(
    id INTEGER UNIQUE NOT NULL,
    first_name TEXT NOT NULL ,
    last_name TEXT NOT NULL ,
    address TEXT NOT NULL ,
    state TEXT NOT NULL ,
    zip TEXT NOT NULL ,
    created STRING DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id ASC)
);

CREATE INDEX idx_customers_name ON customers(last_name, first_name);
CREATE INDEX idx_customers_created ON customers(created);


CREATE TABLE products
(
    id INTEGER UNIQUE NOT NULL,
    name TEXT NOT NULL, -- VARCHAR(100)
    created STRING DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id ASC)
);

CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_created ON products(created);

 -- outputs 1
PRAGMA foreign_keys;

CREATE TABLE customers_products
(
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    status STRING NOT NULL, -- 'new', 'cancelled'
    created STRING DEFAULT CURRENT_TIMESTAMP,
    last_modified STRING DEFAULT CURRENT_TIMESTAMP --,
    --FOREIGN KEY (customer_id) REFERENCES (customers.id),
    --FOREIGN KEY (product_id) REFERENCES (products.id)
);

CREATE UNIQUE INDEX idx_customers_products_customer_id_product_id ON customers_products(customer_id, product_id);
CREATE INDEX idx_customers_products_created ON customers_products(created);
CREATE INDEX idx_customers_products_last_modified ON customers_products(last_modified);

--CREATE TRIGGER update_customers_products AFTER UPDATE ON customers_products
--BEGIN
--UPDATE customers_products SET last_modified = CURRENT_TIMESTAMP WHERE rowid = OLD.rowid;
--END


CREATE TABLE transactions
(
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    dt TEXT NOT NULL, -- iso8601 string format supplied from 3rd party
    action STRING NOT NULL, -- 'new', 'cancelled'
    amount INTEGER NOT NULL DEFAULT 0, -- stored as cents
    created STRING DEFAULT CURRENT_TIMESTAMP --,
    --FOREIGN KEY (customer_id) REFERENCES (customers.id),
    --FOREIGN KEY (product_id) REFERENCES (products.id)
);

CREATE INDEX idx_transactions_customer_id ON transactions(customer_id);
CREATE INDEX idx_transactions_product_id ON transactions(product_id);
CREATE INDEX idx_transactions_dt ON transactions(dt);
CREATE INDEX idx_transactions_action ON transactions(action);
CREATE INDEX idx_transactions_created ON transactions(created);

