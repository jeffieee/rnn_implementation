import numpy as np
from keras.models import load_model
import pickle
import mysql.connector

import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Full paths to the model and encoders
model_path = os.path.join(current_dir, 'rnn_recommendation_model.h5')
encoders_path = os.path.join(current_dir, 'label_encoders (3).pkl')
scaler_path = os.path.join(current_dir, 'scaler (3).pkl')


model = load_model(model_path)

with open(encoders_path, 'rb') as f:
    label_encoders = pickle.load(f)

with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)


# Function to preprocess data from database
def preprocess_data_from_db(data):
    # Encode categorical features
    for col, le in label_encoders.items():
        data[col] = le.transform(data[col])

    # Normalize numerical features
    data['Age'] = scaler.transform(data[['Age']])

    # Convert to a NumPy array
    X = data[['Age', 'Gender', 'Student', 'PWD', 'isOccupation', 'isBeneficiaries']].values

    return X

def recommend_program(new_resident_array):
    # Get the model's prediction
    prediction = model.predict(new_resident_array)[0]
    recommended_program_index = np.argmax(prediction)
    recommended_program_id = recommended_program_index + 1  # Adjust for 0-based indexing

    return recommended_program_id

if __name__ == '__main__':
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="data"
    )

    # Check if the connection was successful
    if conn.is_connected():
        print("Connected to MySQL database")

        # Specify the query
        query = "SELECT Age, Gender, Student, PWD, isOccupation, isBeneficiaries FROM sample"

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch all rows
        data = cursor.fetchall()

        import pandas as pd
        df = pd.DataFrame(data, columns=['Age', 'Gender', 'Student', 'PWD', 'isOccupation', 'isBeneficiaries'])

        # Preprocess the data
        X = preprocess_data_from_db(df)

        # Get recommendation
        recommended_program_id = recommend_program(X)

        # Print the recommended program ID
        print(f"Recommended program ID for the new resident: {recommended_program_id}")

        # Close cursor and connection
        cursor.close()
        conn.close()
    else:
        print("Connection to MySQL database failed")

