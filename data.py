import pandas as pd
import random

# Define the base data with coordinates and additional attributes
base_data = {
    "Region": ["NR I", "NR II", "NR III", "NR IV", "NR V"],
    "Min Temperature (°C)": [10, 15, 20, 25, 30],
    "Max Temperature (°C)": [20, 25, 30, 35, 40],
    "Min Rainfall (mm)": [1000, 750, 500, 450, 300],
    "Max Rainfall (mm)": [2000, 1000, 750, 650, 500],
    "Fertilizer_Usage": [10, 20, 30, 40, 50],  # Updated values
    "Pest_Incidence": [5, 15, 25, 35, 45],  # Updated values
    "Labor_Availability": [50, 40, 30, 20, 10],  # Updated values
    "Market_Access": [50, 40, 30, 20, 10],  # Updated values
    "Suitable Plants": [
        "Coffee, Tea, Bananas, Apples, Potatoes, Peas, Vegetables, Proteas",
        "Tobacco, Maize, Cotton, Wheat, Soybeans, Sorghum, Groundnuts",
        "Maize, Cotton, Groundnuts, Sunflowers",
        "Drought-tolerant Maize, Sorghum, Pearl Millet, Finger Millet",
        "Cattle, Game-ranching",
    ],
    "Latitude": [-20.0725, -18.6108, -19.0892, -20.1314, -20.9194],
    "Longitude": [30.8303, 27.2331, 29.4219, 28.5950, 28.9117],
    "Crop Yield (tons/ha)": [8, 6, 4, 2, 1],  # Based on region productivity
    "Humidity (%)": [75, 70, 65, 60, 55],  # Based on region climate
    "Soil pH": [6.5, 6.0, 5.5, 5.0, 4.5],  # Based on region soil quality
}

# Create a list to hold the extended data
extended_data = []

# Generate 2000 rows of data
for _ in range(400):
    # Randomize the order of regions
    regions = list(base_data["Region"])
    random.shuffle(regions)

    for region in regions:
        index = base_data["Region"].index(region)
        row = {
            "Region": region,
            "Min Temperature (°C)": base_data["Min Temperature (°C)"][index] + random.gauss(0, 3),
            "Max Temperature (°C)": base_data["Max Temperature (°C)"][index] + random.gauss(0, 3),
            "Min Rainfall (mm)": base_data["Min Rainfall (mm)"][index] + random.gauss(0, 100),
            "Max Rainfall (mm)": base_data["Max Rainfall (mm)"][index] + random.gauss(0, 200),
            "Suitable Plants": base_data["Suitable Plants"][index],
            "Fertilizer_Usage": base_data["Fertilizer_Usage"][index] + random.gauss(0, 5),
            "Pest_Incidence": base_data["Pest_Incidence"][index] + random.gauss(0, 10),
            "Labor_Availability": base_data["Labor_Availability"][index] + random.gauss(0, 10),
            "Market_Access": base_data["Market_Access"][index] + random.gauss(0, 10),
            "Latitude": base_data["Latitude"][index] + random.gauss(0, 0.2),
            "Longitude": base_data["Longitude"][index] + random.gauss(0, 0.2),
            "Crop Yield (tons/ha)": base_data["Crop Yield (tons/ha)"][index] + random.gauss(0, 1),
            "Humidity (%)": base_data["Humidity (%)"][index] + random.gauss(0, 5),
            "Soil pH": base_data["Soil pH"][index] + random.gauss(0, 0.3),
        }
        extended_data.append(row)

# Create a DataFrame
df = pd.DataFrame(extended_data)
# Display the first few rows of the DataFrame
print(df.head())
# Save the DataFrame to a CSV file
df.to_csv("Data2.csv", index=False)