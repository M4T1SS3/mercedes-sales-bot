import pandas as pd
import numpy as np

def generate_persona_data(persona, num_records, deviation_prob=0.05, age_prob=0.2):
    base_distributions = {
        'Franz': {
            'STRONG_LOCATION': ['USA', 'UK', 'Germany'],
            'AGE': (39, 10),  # mean, std
            'INCOME_LEVEL': ['HIGHEST'],
            'LOCATION_TYPE': ['rural', 'small', 'suburbs'],
            'VEHICLE_PREFERENCES': ['large', 'luxury'],
            'SERVICE_PREFERENCES': ['phone', 'click'],
            'BRAND_LOYALTY': ['high', 'low'],
            'DIGITAL_ENGAGEMENT': ['traditional', 'digital'],
            'PSYCHOLOGICAL_TRAITS': ['luxury', 'convenience', 'quality']
        },
        'Sally': {
            'STRONG_LOCATION': ['China', 'France', 'Switzerland'],
            'AGE': (32, 5),
            'INCOME_LEVEL': ['HIGH'],
            'LOCATION_TYPE': ['urban', 'megacity'],
            'VEHICLE_PREFERENCES': ['entry', 'luxury', 'modern', 'executive'],
            'SERVICE_PREFERENCES': ['contract'],
            'BRAND_LOYALTY': ['high'],
            'DIGITAL_ENGAGEMENT': ['digital'],
            'PSYCHOLOGICAL_TRAITS': ['validation', 'trends']
        },
        'Peter': {
            'STRONG_LOCATION': ['China', 'Brazil', 'Canada'],
            'AGE': (34, 5),
            'INCOME_LEVEL': ['HIGH'],
            'LOCATION_TYPE': ['urban', 'large'],
            'VEHICLE_PREFERENCES': ['urban', 'large'],
            'SERVICE_PREFERENCES': ['digital'],
            'BRAND_LOYALTY': ['low'],
            'DIGITAL_ENGAGEMENT': ['digital'],
            'PSYCHOLOGICAL_TRAITS': ['luxury', 'experience']
        },
        'Viola': {
            'STRONG_LOCATION': ['Sweden', 'Switzerland', 'Germany'],
            'AGE': (47, 8),
            'INCOME_LEVEL': ['LOW'],
            'LOCATION_TYPE': ['rural', 'small'],
            'VEHICLE_PREFERENCES': ['used', 'mid'],
            'SERVICE_PREFERENCES': ['phone'],
            'BRAND_LOYALTY': ['low'],
            'DIGITAL_ENGAGEMENT': ['digital'],
            'PSYCHOLOGICAL_TRAITS': ['price', 'quality', 'service']
        }
    }

    #Create a dictionary with all possibilities for each attribute:
    all_posibilities = {
        'STRONG_LOCATION': ['USA', 'UK', 'Germany', 'China', 'France', 'Switzerland', 'Brazil', 'Canada', 'Sweden'],
        'AGE': np.arange(18, 101),
        'INCOME_LEVEL': ['HIGHEST', 'HIGH', 'LOW'],
        'LOCATION_TYPE': ['rural', 'small', 'suburbs', 'urban', 'megacity', 'large'],
        'VEHICLE_PREFERENCES': ['large', 'luxury', 'entry', 'modern', 'executive', 'urban', 'mid', 'used'],
        'SERVICE_PREFERENCES': ['phone', 'click', 'contract'],
        'BRAND_LOYALTY': ['high', 'low'],
        'DIGITAL_ENGAGEMENT': ['traditional', 'digital'],
        'PSYCHOLOGICAL_TRAITS': ['luxury', 'convenience', 'quality', 'validation', 'trends', 'experience', 'price', 'service']
    }
    
    data = pd.DataFrame()
    
    for attribute, distribution in base_distributions[persona].items():
        if attribute == 'AGE':
            if persona == 'Franz' and np.random.rand() < age_prob:
                age_mean, age_std = distribution
                ages = np.random.normal(loc=age_mean, scale=age_std, size=num_records).astype(int)
                ages = np.clip(ages, 18, 100)
                ages[np.random.rand(num_records) < 0.2] += 20
            else:
                ages = np.random.normal(loc=distribution[0], scale=distribution[1], size=num_records).astype(int)
                ages = np.clip(ages, 18, 100)
            data[attribute] = ages
        elif attribute in ['VEHICLE_PREFERENCES', 'PSYCHOLOGICAL_TRAITS']:
            # Check if there are enough unique items for sampling
            num_items = 2 if attribute == 'VEHICLE_PREFERENCES' else 2  # Choose number of items per attribute
            if len(distribution) < num_records * num_items:
                # If not enough unique items, sample with replacement
                item_samples = np.random.choice(distribution, size=(num_records, num_items), replace=True)
            else:
                # Enough unique items, sample without replacement
                item_samples = np.random.choice(distribution, size=(num_records, num_items), replace=False)
            
            for i in range(num_items):
                data[f'{attribute}_{i+1}'] = item_samples[:, i]
        else:
            data[attribute] = np.random.choice(distribution, num_records)
    
    # Add noise to the data
    

    
    data['PERSONA'] = persona
    
    return data

# Generate sample data for each persona
num_records_per_persona = 1000
deviation_prob = 0.30
age_prob = 0.2

franz_data = generate_persona_data('Franz', int(num_records_per_persona * 0.04), deviation_prob, age_prob)
sally_data = generate_persona_data('Sally', int(num_records_per_persona * 0.14), deviation_prob)
peter_data = generate_persona_data('Peter', int(num_records_per_persona * 0.08), deviation_prob)
viola_data = generate_persona_data('Viola', int(num_records_per_persona * 0.33), deviation_prob)

# Combine all persona data into a single dataset
sample_data = pd.concat([franz_data, sally_data, peter_data, viola_data], ignore_index=True)

# Save the generated sample data to a CSV file
sample_data.to_csv('generated_clusters.csv', index=False)

# Display the first few rows of the generated sample data
print(sample_data.head())
