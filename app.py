import requests
import pandas as pd

##########
# CONFIG #
##########

# This is not secure but whatever idc
API_KEY = "API_KEY_HERE"

# Energy Network Code
# NEM, WEM, AEMO_ROOFTOP, APVI
NETWORK_CODE = "NEM"

# Data interval
# Available options: 5m, 1h, 1d, 7d, 1M, 3M, season, 1y, fy
INTERVAL = "1d"

# Data time period (Max 1 year)
DATE_START = "2024-01-01"
DATE_END = "2024-12-31"
# DATE_START = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
# DATE_END = datetime.now().strftime("%Y-%m-%d")

'''
POWER: Instantaneous power output/consumption (MW)
ENERGY: Energy generated/consumed over time (MWh)
PRICE: Price per unit of energy ($/MWh)
DEMAND: Demand for energy (MW)
MARKET_VALUE: Total market value ($)
EMISSIONS: CO2 equivalent emissions (tonnes)
RENEWABLE_PROPORTION: Percentage of renewable energy (%)
'''
METRIC = "market_value"

# List of facility codes to get data for (Get from the website idk how else)
FACILITY_CODES = ["BAYSW", "BANGOWF"]

##############
# END CONFIG #
##############

url = f"https://api.openelectricity.org.au/v4/data/facilities/{NETWORK_CODE}"

headers = { "Authorization": f"Bearer {API_KEY}" }

params = {
    "facility_code": FACILITY_CODES,
    "metrics": METRIC,
    "interval": INTERVAL,
    "date_start": DATE_START,
    "date_end": DATE_END
}

response = requests.request("GET", url, headers=headers, params=params)

# Parse the JSON response
response_json = response.json()
facility_data = {}
for result in response_json['data'][0]['results']:
    facility_name = result['name']
    facility_data[facility_name] = result['data']

# Convert to df
df = pd.DataFrame()

# Add timestamp column
if facility_data:
    first_facility = list(facility_data.keys())[0]
    df['timestamp'] = [row[0] for row in facility_data[first_facility]]
    
    # Add value columns for each facility
    for facility_name, data in facility_data.items():
        df[facility_name] = [row[1] for row in data]

df.to_csv('data.csv', index=False)