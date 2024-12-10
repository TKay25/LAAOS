from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import os
import pickle
import numpy as np
import joblib
import psycopg2
from psycopg2 import sql

# Create Flask app
app = Flask(__name__)
app.secret_key = '011235813'  # Required for flashing messages

# Connection string
DATABASE_URL = "postgresql://laaosdatabase_user:ntDL9GOqaQzq3LmHqvhlHXEHyfj6QzZb@dpg-ctbjr9hu0jms73davdg0-a.oregon-postgres.render.com/laaosdatabase"

try:
    # Connect using the URL
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database successfully!")
    cursor = conn.cursor()

    # SQL query to delete the table if it exists
    drop_table_query = "DROP TABLE IF EXISTS registration;"
    
    # Execute the query to drop the table
    cursor.execute(drop_table_query)

    # SQL query to create a table
    create_table_query = """
    CREATE TABLE registration (
        name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        username VARCHAR(100) NOT NULL,
        IDNo VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL
    );
    """

    # Execute the query
    cursor.execute(create_table_query)
    conn.commit()  # Commit the changes
    print("Table 'registration' created successfully!")
    
    cursor.execute("SELECT * FROM registration;")

    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)  # You can format it as needed

except Exception as e:
    print("Error connecting to the database:", e)


# Sample crop options
crops = {
    "r1": "Coffee, Tea, Bananas, Apples, Potatoes, Peas, Vegetables, Proteas",
    "r2": "Maize, Cotton, Groundnuts, Sunflowers",
    "r3": "Tobacco, Maize, Cotton, Wheat, Soybeans, Sorghum, Groundnuts",
    "r4": "Drought-tolerant Maize, Sorghum, Pearl Millet, Finger Millet",
    "r5": "Cattle, Game-ranching"
}


@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Connect to the database
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()

            # Check if the username and password match any record
            query = sql.SQL("SELECT * FROM registration WHERE username = %s AND password = %s")
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                # User found, login successful
                return redirect(url_for('back_to_index2', username = username))  # Redirect back to login page
           
            else:
                # User not found
                flash("Invalid username or password.", "danger")
                return redirect(url_for('login'))  # Redirect back to login page

        except Exception as e:
            print("Error connecting to the database:", e)
            flash("Error occurred during login. Please try again.", "danger")
            return redirect(url_for('login'))


    elif request.method == "GET":
        try:
            username = session.get('username')  # Get the 'username' from the session
            return render_template('index2.html', username=username)
        except Exception as e:
            print("Error connecting to the database:", e)
            flash("Error occurred during login. Please try again.", "danger")
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    username = session.get('username')  # Retrieve username from the session
    if username:
        session.pop('username', None)  # Remove username from session (logout)
    return redirect(url_for('index'))  # Redirect to the index or home page

@app.route("/home", methods=["GET","POST"])
def back_to_index2():
    username = request.args.get('username')  # Get the 'username' parameter from the URL

    return render_template("index2.html", username = username)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        surname = request.form['surname']
        IDNo = request.form['IDNo']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            # Connect to the database
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            print("Connected to the database successfully!")

            # SQL query to insert data into the 'registration' table
            insert_query = """
            INSERT INTO registration (name, surname, IDNo, username, email, password)
            VALUES (%s, %s, %s, %s, %s, %s);
            """

            # Execute the query with the form data
            cursor.execute(insert_query, (name, surname, IDNo, username, email, password))
            conn.commit()  # Commit the changes
            print("Data inserted successfully!")

            return redirect(url_for('back_to_index2', username = username))  # Redirect back to login page

        except Exception as e:
            print("Error inserting data into the database:", e)

@app.route("/recommendation", methods=["POST"])
def back_to_reco():
    # Handle form submission, if necessary
    return redirect(url_for("index2"))  # Redirect to index2.html

@app.route("/predict", methods=["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)

    # Map the predicted value to the actual crop using if-else statements
    if prediction[0] == 0:
        actual_value = (
            "Coffee, Tea, Bananas, Apples, Potatoes, Peas, Vegetables, Proteas"
        )
    elif prediction[0] == 1:
        actual_value = "Tobacco, Maize, Cotton, Wheat, Soybeans, Sorghum, Groundnuts"
    elif prediction[0] == 2:
        actual_value = "Maize, Cotton, Groundnuts, Sunflowers"
    elif prediction[0] == 3:
        actual_value = "Drought-tolerant Maize, Sorghum, Pearl Millet, Finger Millet"
    elif prediction[0] == 4:
        actual_value = "Cattle, Game-ranching"
    else:
        actual_value = "Unknown crop"

    return render_template(
        "results.html", prediction_text=f"The Predicted Crop is {actual_value}"
    )


@app.route("/allocate", methods=["POST"])
def allocate():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = kmeans.predict(features)

    # Map the predicted value to the actual region using if-else statements
    if prediction[0] == 0:
        actual_value = "NR II ,NR III, NR I"
    elif prediction[0] == 1:
        actual_value = "NR IV, NR V"
    elif prediction[0] == 2:
        actual_value = "NR III, NR IV, NR II"
    elif prediction[0] == 3:
        actual_value = "NR I, NR II"
    else:
        actual_value = "Unknown region"

    return render_template(
        "results.html",
        prediction_text=f"The Allocated Region is {actual_value}",
        crops=crops,
        recommendations = recommendations
    )


@app.route("/optimize_land", methods=["POST"])
def optimize_land():
    recommendations = {}
    crop_livestock = request.form["crop-livestock"]
    total_hectares = int(request.form["total-hectares"])
    farmable_hectares = int(request.form["farmable-hectares"])
    plot_div = ""

    #recommendations = []

    selected_crops = request.form.get('crop-livestock')
    total_hectares = float(request.form.get('total-hectares', 0))
    farmable_hectares = float(request.form.get('farmable-hectares', 0))

    if selected_crops and farmable_hectares > 0:
        crop_list = crops[selected_crops].split(", ")
        hectares_per_crop = farmable_hectares / len(crop_list)
        recommendations = {crop: hectares_per_crop for crop in crop_list}
        
        # Create a pie chart
        fig = px.pie(names=list(recommendations.keys()), values=list(recommendations.values()), title='Crop Distribution on Farmable Hectares')
        plot_div = fig.to_html(full_html=False)
# Add more conditions for other crop/livestock selections

    return render_template(
        "results.html",
        crop_livestock = selected_crops,
        crops=crops,
        recommendations=recommendations,
        total_hectares=total_hectares,
        farmable_hectares=farmable_hectares,
        plot_div=plot_div
    )
    
def past_recommendations():
    # Fetch past recommendations from the database
    #past_recommendations = Recommendation.query.all()
    return render_template('data.html', recommendations=past_recommendations)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
