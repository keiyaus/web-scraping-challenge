from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from config import host_name

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=f'mongodb://{host_name}/mars_app')

@app.route('/')
def home():

    # Find one record of data from the mongo database
    latest_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", data=latest_data)

@app.route('/scrape')
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)