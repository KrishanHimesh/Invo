import psycopg2

DATABASE_URL = "postgresql://postgres.hhsxuwqumwbjytsiogai:[YOUR-PASSWORD]@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres"

def create_inventory_table():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            price NUMERIC NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

create_inventory_table()
