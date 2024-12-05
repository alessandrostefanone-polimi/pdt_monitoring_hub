from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Endpoint of the API
API_URL = "http://localhost:8000/api/"

# Function to fetch fridge data from the API
def get_fridge_data(fridge_id):
    response = requests.get(API_URL + fridge_id)
    response.raise_for_status()
    return response.json()

# Main page
@app.route('/')
def index():
    fridges = ['fridge1', 'fridge2', 'fridge3']
    return render_template('index.html', fridges=fridges)

# Dynamic route for each fridge (e.g., /fridge1, /fridge2)
@app.route('/<fridge_id>')
def fridge(fridge_id):
    try:
        # Fetch fridge data
        fridge_data = get_fridge_data(fridge_id)
        return render_template('fridge.html', fridge_id=fridge_id, fridge_data=fridge_data)
    except requests.exceptions.RequestException as e:
        return f"Error fetching data for {fridge_id}: {str(e)}", 404
    
# API endpoint to fetch fridge data in JSON format
@app.route('/api/<fridge_id>')
def api_fridge_data(fridge_id):
    try:
        # Fetch fridge data
        fridge_data = get_fridge_data(fridge_id)
        return jsonify(fridge_data)  # Return data as JSON
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
