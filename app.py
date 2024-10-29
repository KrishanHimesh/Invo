from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "Krishan@2022"

# Database configuration using ElephantSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.hhsxuwqumwbjytsiogai:[YOUR-PASSWORD]@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Home route
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM inventory')
    items = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('inventory.html', items=items)

# Add item route
@app.route('/add', methods=('POST',))
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']

    if not name or not quantity or not price:
        flash("Please fill all fields!")
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)',
                (name, quantity, price))
    conn.commit()
    cur.close()
    conn.close()
    flash("Item added successfully!")
    return redirect(url_for('index'))

# Delete item route
@app.route('/delete/<int:item_id>', methods=('POST',))
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM inventory WHERE id = %s', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Item deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
