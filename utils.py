import pandas as pd
import numpy as np
import json
import pickle
import warnings
warnings.filterwarnings('ignore')
import config

class CarPrice:
    def __init__(self):
        self.column_data = None
        self.model = None
        self.columns_name = None
        self.feature_count = None

    def load_data(self):
        with open(config.MODEL_FILE_NAME, 'rb') as f:
            self.model = pickle.load(f)

        with open(config.COLUMN_DATA_JSON_FILE, 'r') as f:
            self.column_data = json.load(f)

        self.columns_name = self.model.feature_names_in_
        self.feature_count = self.model.n_features_in_

    def get_predicted_price(self, Year, Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner):
        self.load_data()

        Fuel_Type = self.column_data['Fuel_Type'][Fuel_Type]
        Seller_Type = "Seller_Type_" + Seller_Type
        Transmission = "Transmission_" + Transmission

        Seller_Type_index = np.where(self.columns_name == Seller_Type)[0][0]
        Transmission_index = np.where(self.columns_name == Transmission)[0][0]

        test_array = np.zeros((1, self.feature_count))
        test_array[0, 0] = Year
        test_array[0, 1] = Present_Price
        test_array[0, 2] = Kms_Driven
        test_array[0, 3] = Fuel_Type
        test_array[0, 4] = Owner
        test_array[0, Seller_Type_index] = 1
        test_array[0, Transmission_index] = 1

        predicted_price = self.model.predict(test_array)[0]
        return predicted_price

def load_dataset():
    df = pd.read_csv(config.CSV_FILE_NAME)
    return df