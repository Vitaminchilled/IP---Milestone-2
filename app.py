from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1111",
    "database": "sakila"
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def index():
    return 'Index Page'

@app.route("/api/top-films")
def get_top_films():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT f.film_id, f.title, COUNT(r.rental_id) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.film_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

