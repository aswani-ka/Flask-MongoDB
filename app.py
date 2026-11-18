import json
import os
import pymongo
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI')

try:
    client = pymongo.MongoClient(MONGO_URI)

    db = client.flask_sample_db

    collection = db["users"]

except Exception as e:
    print(f"Intial MongoDB Connection Error: , {e}")


@app.route("/api", methods=['GET'])

def get_api_data():
    file_path = os.path.join(app.root_path, "data.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Backend data not found."}), 404
    except json.JSONDecodeError:
        return  jsonify({"error": "Invalid JSON format in backend file."}), 500


@app.route('/', methods=['GET', 'POST'])

def signup():
    error_message = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            error_message = "All fields are required"
            return render_template("index.html", error=error_message)

        form_data = {
            "name": name,
            "email": email,
            "password": password
        }

        try:
            collection.insert_one(form_data)
            return redirect(url_for("success"))
        except PyMongoError as e:
            error_message = f"Database Error: {str(e)}"
        except Exception as e:
            error_message = f"An unexpected error occured: {str(e)}"

    return render_template("index.html", error=error_message)


@app.route("/success", methods=['GET'])

def success():
    return render_template("success.html")



if __name__ == "__main__":
    app.run(debug=True)