import pandas as pd
import numpy as np

# Create synthetic sensor data for turbine engines
def generate_turbine_data(num_samples=1000):
    np.random.seed(42)
    
    # Sensors
    data = {
        'timestamp': pd.date_range(start='2026-01-01', periods=num_samples, freq='H'),
        'machine_id': np.random.choice(['T1', 'T2', 'T3', 'T4', 'T5'], num_samples),
        'temperature': np.random.normal(800, 50, num_samples),  # °C
        'pressure': np.random.normal(20, 2, num_samples),      # bar
        'vibration': np.random.normal(0.5, 0.1, num_samples),   # mm/s
        'rpm': np.random.normal(12000, 500, num_samples),       # revolutions per minute
        'oil_pressure': np.random.normal(4, 0.5, num_samples),  # bar
    }
    
    df = pd.DataFrame(data)
    
    # Introduce failures based on sensor thresholds (simulating anomaly detection)
    # T > 920, P < 15, V > 0.8, OP < 2.5
    df['failure'] = 0
    df.loc[(df['temperature'] > 920) | (df['vibration'] > 0.8) | (df['oil_pressure'] < 2.5), 'failure'] = 1
    
    return df

df = generate_turbine_data()
df.to_csv('data/turbine_data.csv', index=False)
