from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the data from Excel
df = pd.read_excel('sampledatafoodsales_analysis.xlsx', sheet_name='FoodSales')

@app.route('/')
def home():
    with open('index.html', 'r') as file:
        return file.read()

@app.route('/get_filters', methods=['GET'])
def get_filters():
    unique_dates = sorted(df['Date'].astype(str).unique())
    unique_cities = sorted(df['City'].unique())
    unique_categories = sorted(df['Category'].unique())
    return jsonify({'dates': unique_dates, 'cities': unique_cities, 'categories': unique_categories})

@app.route('/filter_data', methods=['POST'])
def filter_data():
    start_date = request.form.get('startDate')
    end_date = request.form.get('endDate')
    city = request.form.get('city')
    category = request.form.get('category')

    filtered_df = df.copy()

    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= end_date]
    if city:
        filtered_df = filtered_df[filtered_df['City'] == city]
    if category:
        filtered_df = filtered_df[filtered_df['Category'] == category]

    return jsonify(filtered_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run()
