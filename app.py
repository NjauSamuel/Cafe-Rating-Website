from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/')
def home():
    # Fetch the JSON data from the /all route
    response = requests.get('http://127.0.0.1:5000/all')
    cafes_data = response.json()
    cafes = cafes_data.get('cafes', [])

    # Passing data to the HTML template
    query_location = request.args.get('loc', '')
    return render_template('index.html', cafes=cafes, query_location=query_location)


@app.route('/search', methods=['GET'])
def search():
    query_location = request.args.get('loc')
    if not query_location:
        return render_template('search.html', cafes=[], query_location=query_location)

    response = requests.get(f'http://127.0.0.1:5000/search?loc={query_location}')
    if response.status_code == 200:
        cafes_data = response.json()
        cafes = cafes_data.get('cafes', [])
    else:
        cafes = []

    return render_template('search.html', cafes=cafes, query_location=query_location)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe_data = {
            "name": request.form.get("name"),
            "map_url": request.form.get("map_url"),
            "img_url": request.form.get("img_url"),
            "loc": request.form.get("loc"),
            "sockets": request.form.get("sockets"),
            "toilet": request.form.get("toilet"),
            "wifi": request.form.get("wifi"),
            "calls": request.form.get("calls"),
            "seats": request.form.get("seats"),
            "coffee_price": request.form.get("coffee_price"),
        }
        response = requests.post('http://127.0.0.1:5000/add', data=new_cafe_data)
        if response.status_code == 200:
            return redirect(url_for('home'))
        else:
            return "Error adding cafe"
    return render_template('add_cafe.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_cafe():
    if request.method == 'POST':
        cafe_id = request.form.get("cafe_id")
        api_key = request.form.get("api_key")
        response = requests.delete(f'http://127.0.0.1:5000/report-closed/{cafe_id}?api-key={api_key}')
        if response.status_code == 200:
            return redirect(url_for('home'))
        elif response.status_code == 403:
            return "Forbidden: Incorrect API Key"
        elif response.status_code == 404:
            return "Not Found: Cafe with the given ID does not exist"
        else:
            return "Error deleting cafe"

    response = requests.get('http://127.0.0.1:5000/all')
    cafes_data = response.json()
    cafes = cafes_data.get('cafes', [])
    return render_template('delete_cafe.html', cafes=cafes)


@app.route('/update', methods=['GET', 'POST'])
def update_price():
    if request.method == 'POST':
        cafe_id = request.form.get("cafe_id")
        new_price = request.form.get("new_price")
        response = requests.patch(f'http://127.0.0.1:5000/update-price/{cafe_id}?new_price={new_price}')
        if response.status_code == 200:
            return redirect(url_for('home'))
        elif response.status_code == 404:
            return "Not Found: Cafe with the given ID does not exist"
        else:
            return "Error updating price"

    response = requests.get('http://127.0.0.1:5000/all')
    cafes_data = response.json()
    cafes = cafes_data.get('cafes', [])
    return render_template('update_price.html', cafes=cafes)


if __name__ == '__main__':
    app.run(port=8000)
