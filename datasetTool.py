import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
n_samples = 10000

# Generate synthetic data for crop yield prediction
X, y = make_classification(n_samples=n_samples, n_features=10, n_informative=5, n_redundant=2, n_clusters_per_class=2, random_state=42)

# Create a DataFrame
columns = ['Temperature', 'Rainfall', 'Humidity', 'Soil_pH', 'Soil_Nutrients', 'Water_Availability', 'Fertilizer_Usage', 'Pest_Incidence', 'Labor_Availability', 'Market_Access']
df = pd.DataFrame(X, columns=columns)
df['Crop_Yield'] = y

# Add some noise to make the data more realistic
df['Temperature'] = df['Temperature'] * 10 + 20  # Scale and shift temperature
df['Rainfall'] = df['Rainfall'] * 50 + 100  # Scale and shift rainfall
df['Humidity'] = df['Humidity'] * 10 + 50  # Scale and shift humidity
df['Soil_pH'] = df['Soil_pH'] * 0.5 + 6  # Scale and shift soil pH
df['Soil_Nutrients'] = df['Soil_Nutrients'] * 10 + 50  # Scale and shift soil nutrients
df['Water_Availability'] = df['Water_Availability'] * 10 + 50  # Scale and shift water availability
df['Fertilizer_Usage'] = df['Fertilizer_Usage'] * 5 + 20  # Scale and shift fertilizer usage
df['Pest_Incidence'] = df['Pest_Incidence'] * 5  # Scale pest incidence
df['Labor_Availability'] = df['Labor_Availability'] * 10 + 50  # Scale and shift labor availability
df['Market_Access'] = df['Market_Access'] * 10 + 50  # Scale and shift market access

# Add latitudes and longitudes for farming regions
regions = {
    'Region I': {'Latitude': 18.9, 'Longitude': 32.7},
    'Region II': {'Latitude': 17.8, 'Longitude': 31.0},
    'Region III': {'Latitude': 19.0, 'Longitude': 30.0},
    'Region IV': {'Latitude': 20.0, 'Longitude': 29.0},
    'Region V': {'Latitude': 21.0, 'Longitude': 28.0}
}

# Randomly assign regions to each sample
df['Region'] = np.random.choice(list(regions.keys()), n_samples)
df['Latitude'] = df['Region'].apply(lambda x: regions[x]['Latitude'])
df['Longitude'] = df['Region'].apply(lambda x: regions[x]['Longitude'])

# Display the first few rows of the dataset
print(df.head())

# Save the dataset to a CSV file
df.to_csv('synthetic_agriculture_data_with_geo.csv', index=False)
