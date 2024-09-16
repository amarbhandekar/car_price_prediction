from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import config
from utils import CarPrice, load_dataset

car_price = CarPrice()
df = load_dataset()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/year_options')
def year_options():
    year_list=list(df['Year'].unique())
    int_list_year=[int(x) for x in year_list]
    return jsonify(int_list_year)

@app.route('/fuel_options')
def fuel_options():
    # df['Fuel_Type'] = df['Fuel_Type'].apply(lambda x: x.lower())
    return jsonify(list(df['Fuel_Type'].unique()))

@app.route('/seller_options')
def seller_options():
    return jsonify(list(df['Seller_Type'].unique()))

@app.route('/transmission_options')
def transmission_options():
    return jsonify(list(df['Transmission'].unique()))

@app.route('/prediction', methods=['POST'])
def prediction():
    data = request.form
    print(data)

    Year = data['Year']
    Present_Price = data['Present_Price']
    Kms_Driven = data['Kms_Driven']
    Fuel_Type = data['Fuel_Type']
    Seller_Type = data['Seller_Type']
    Transmission = data['Transmission']
    Owner = data['Owner']

    pred_price = car_price.get_predicted_price(Year, Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner)
    print("predicted price:", pred_price)

    return jsonify({'Predicted Car Price': pred_price})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.FLASK_PORT_NUMBER, debug=True)