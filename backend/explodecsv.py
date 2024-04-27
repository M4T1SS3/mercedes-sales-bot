# import pandas as pd

# # Read CSV file into pandas DataFrame
# df = pd.read_csv('personas.csv')
# print(df)

# # List of columns containing lists to be exploded_
# # Split rows with multiple values in certain columns
# df = df.assign(
#     STRONG_LOCATION=df['STRONG LOCATION'].str.split(', '),
#     LOCATION_TYPE=df['LOCATION TYPE'].str.split(', '),
#     VEHICLE_PREFERENCES=df['VEHICLE PREFERENCES'].str.split(', '),
#     SERVICE_PREFERENCES=df['SERVICE PREFERENCES'].str.split(', '),
#     BRAND_LOYALTY=df['BRAND LOYALTY'].str.split(', '),
#     PSYCHOLOGICAL_TRAITS=df['PSYCHOLOGICAL TRAITS'].str.split(', ')
# )

# df = df.explode('STRONG_LOCATION').explode('LOCATION_TYPE').explode('VEHICLE_PREFERENCES').explode('SERVICE_PREFERENCES').explode('BRAND_LOYALTY').explode('PSYCHOLOGICAL_TRAITS')

# # save to new csv file
# df.to_csv('personas_exploded.csv', index=False)


import pandas as pd

# READ CSV
df = pd.read_csv('personas.csv')

# Columns to explode (all columns except 'PERSONA')
columns_to_explode = [col for col in df.columns if col != 'PERSONA']

# Function to explode DataFrame based on a specified column
def explode_dataframe(df, column):
    df[column] = df[column].apply(lambda x: x.split(', ') if isinstance(x, str) else x)
    return df.explode(column).reset_index(drop=True)

# Explode the DataFrame for each specified column
for col in columns_to_explode:
    df = explode_dataframe(df, col)

columns_to_remove = [col for col in columns_to_explode if len(set(df[col])) > 1]
print(columns_to_remove)

# Display the exploded DataFrame
print(df)

#Save to csv file
df.to_csv('personas_exploded.csv', index=False)
