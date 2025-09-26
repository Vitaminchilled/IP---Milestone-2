from flask import Flask, jsonify, request, redirect, render_template
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
    return render_template('./first-project/index.html')

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

@app.route("/api/search")
def search_films():
    search_query = request.args.get('q', '')
    
    if not search_query:
        return jsonify([])
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Search in film titles, descriptions, actor names, and category names
    query = """
        SELECT DISTINCT f.film_id, f.title, f.description
        FROM film f
        LEFT JOIN film_actor fa ON f.film_id = fa.film_id
        LEFT JOIN actor a ON fa.actor_id = a.actor_id
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        WHERE f.title LIKE %s 
           OR f.description LIKE %s
           OR a.first_name LIKE %s 
           OR a.last_name LIKE %s
           OR c.name LIKE %s
        ORDER BY f.title
    """
    
    search_pattern = f"%{search_query}%"
    cursor.execute(query, (search_pattern, search_pattern, search_pattern, 
                          search_pattern, search_pattern))
    
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(results)

@app.route("/api/films/<int:film_id>")
def get_film_details(film_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT f.film_id, f.title, f.description, f.release_year, l.name as language, f.rating
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        WHERE f.film_id = %s
    """
    cursor.execute(query, (film_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify(result)

@app.route("/api/top-actors")
def get_top_actors():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT a.actor_id, a.first_name, a.last_name, COUNT(r.rental_id) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        JOIN actor a ON fa.actor_id = a.actor_id
        GROUP BY a.actor_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(results)


@app.route("/api/actors/<int:actor_id>")
def get_actor_details(actor_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # actor info
    cursor.execute("SELECT actor_id, first_name, last_name FROM actor WHERE actor_id = %s", (actor_id,))
    actor = cursor.fetchone()

    # top 5 films for actor
    query = """
        SELECT f.film_id, f.title, COUNT(r.rental_id) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_actor fa ON f.film_id = fa.film_id
        WHERE fa.actor_id = %s
        GROUP BY f.film_id
        ORDER BY rental_count DESC
        LIMIT 5;
    """
    cursor.execute(query, (actor_id,))
    films = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify({"actor": actor, "top_films": films})


@app.route("/api/rent", methods=["POST"])
def rent_film():
    from flask import request
    data = request.get_json()
    customer_id = data.get("customer_id")
    inventory_id = data.get("inventory_id")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO rental (rental_date, inventory_id, customer_id, staff_id) VALUES (NOW(), %s, %s, 1)"
    cursor.execute(query, (inventory_id, customer_id))
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"message": "Film rented successfully"})

@app.route("/api/customers")
def get_customers():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT customer_id, first_name, last_name, email
        FROM customer
        ORDER BY last_name, first_name
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
