import psycopg

# ⚠️ If your PostgreSQL user or database name is different,
# change "dbname" and "user" below accordingly.
# Since you use peer authentication, no password is needed.
conn = psycopg.connect("dbname=masato user=masato")

with conn.cursor() as cur:
    # Insert sample products
    cur.execute("INSERT INTO products (name) VALUES (%s) RETURNING id;", ("Laptop",))
    laptop_id = cur.fetchone()[0]

    cur.execute("INSERT INTO products (name) VALUES (%s) RETURNING id;", ("Smartphone",))
    smartphone_id = cur.fetchone()[0]

    # Insert sample options
    cur.execute("INSERT INTO options (name) VALUES (%s) RETURNING id;", ("16GB RAM",))
    ram_id = cur.fetchone()[0]

    cur.execute("INSERT INTO options (name) VALUES (%s) RETURNING id;", ("256GB Storage",))
    storage_id = cur.fetchone()[0]

    cur.execute("INSERT INTO options (name) VALUES (%s) RETURNING id;", ("5G Connectivity",))
    connectivity_id = cur.fetchone()[0]

    # Insert relations (products ↔ options)
    cur.execute(
        "INSERT INTO product_options (product_id, option_id, description) VALUES (%s, %s, %s);",
        (laptop_id, ram_id, "Laptop with upgraded memory")
    )
    cur.execute(
        "INSERT INTO product_options (product_id, option_id, description) VALUES (%s, %s, %s);",
        (laptop_id, storage_id, "Laptop with extra storage")
    )
    cur.execute(
        "INSERT INTO product_options (product_id, option_id, description) VALUES (%s, %s, %s);",
        (smartphone_id, connectivity_id, "Smartphone with 5G support")
    )

conn.commit()
conn.close()

print("✅ Sample data inserted successfully!")

