import requests
import pandas as pd
from config import BLS_API_KEY

class DollarConverter:
    def __init__(self):
        self.inflation_data = self.fetch_inflation_data()

    def fetch_inflation_data(self):
        url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        series_id = 'CUUR0000SA0'  # CPI for All Urban Consumers (CPI-U)
        headers = {'Content-type': 'application/json'}
        data = {
            "seriesid": [series_id],
            "startyear": "1913",  # Start year of data
            "endyear": "2023",
            "catalog": False,
            "calculations": False,
            "annualaverage": True,
            "registrationkey": BLS_API_KEY
        }

        response = requests.post(url, json=data, headers=headers)

        # Debugging output
        print("API Response Status Code:", response.status_code)
        print("API Response JSON:", response.json())

        if response.status_code != 200:
            raise ValueError(f"API request failed with status code {response.status_code}")

        json_data = response.json()
        if 'Results' not in json_data or 'series' not in json_data['Results']:
            raise ValueError("Invalid data structure from API response.")

        inflation_data = {
            entry['year']: float(entry['value'])
            for entry in json_data['Results']['series'][0]['data']
            if entry['period'] == 'M13'  # Only take the annual average (M13)
        }

        if not inflation_data:
            raise ValueError("No inflation data was retrieved from the API.")

        # Normalize to make the most recent year's CPI equal to 1.0
        most_recent_year = max(inflation_data.keys())
        most_recent_cpi = inflation_data[most_recent_year]
        for year in inflation_data:
            inflation_data[year] /= most_recent_cpi

        return inflation_data

    def convert(self, amount, from_year, to_year):
        from_year, to_year = str(from_year), str(to_year)
        if from_year not in self.inflation_data or to_year not in self.inflation_data:
            raise ValueError("Year not found in inflation data.")

        from_index = self.inflation_data[from_year]
        to_index = self.inflation_data[to_year]

        return amount * (to_index / from_index)
