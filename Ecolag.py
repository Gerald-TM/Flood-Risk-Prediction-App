import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = os.path.join(os.path.dirname(__file__), 'Datasets/Lagos_data_set.csv')

lag_df = pd.read_csv(DATA_PATH)
raw_df = {'Waste': (lag_df['POPULATION'] * lag_df['PER CAPITA WASTE']) / 1000,
          'Population': lag_df['POPULATION'] / lag_df['LAND AREA'],
          'Rainfall': lag_df['ANNUAL RAINFALL'],
          'Inefficiency': 1 - lag_df['COLLECTION EFFICIENCY']}

data = pd.DataFrame({
    "Waste": raw_df['Waste'],
    "Population": raw_df['Population'],
    "Rainfall": raw_df['Rainfall']
})
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(data)
normalized_df = pd.DataFrame(normalized_data, columns=data.columns)
normalized_df['Inefficiency'] = raw_df['Inefficiency']
normalized_df['LGA'] = lag_df['LGA']

normalized_df['Risk'] = ((
                                 0.35 * normalized_df['Waste'] +
                                 0.25 * normalized_df['Population'] +
                                 0.25 * normalized_df['Rainfall'] +
                                 0.15 * normalized_df['Inefficiency']
                         ) * 100)

normalized_df = normalized_df[['LGA', 'Risk', 'Waste', 'Population', 'Inefficiency', 'Rainfall']].round(2)

def risk_level(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


normalized_df['Risk_Level'] = normalized_df['Risk'].apply(risk_level)

normalized_df = normalized_df[['LGA', 'Risk', 'Waste', 'Inefficiency', 'Rainfall', 'Risk_Level', 'Population']]
normalized_df = normalized_df.sort_values(by='Risk', ascending=False)
