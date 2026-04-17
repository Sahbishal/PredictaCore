import pytest
import os
import json
import pandas as pd
from backend.agents import SensorAnalysisAgent, MaintenanceRecommendationAgent

# Mock data for testing
DATA_PATH = 'data/turbine_data.csv'
PROCEDURES_PATH = 'data/maintenance_procedures.json'

@pytest.fixture
def sensor_agent():
    return SensorAnalysisAgent(DATA_PATH)

@pytest.fixture
def maintenance_agent():
    return MaintenanceRecommendationAgent(PROCEDURES_PATH)

def test_sensor_analysis_agent_load(sensor_agent):
    assert not sensor_agent.df.empty
    assert 'machine_id' in sensor_agent.df.columns

def test_sensor_analysis_agent_status(sensor_agent):
    machine_id = sensor_agent.df['machine_id'].iloc[0]
    status = sensor_agent.get_machine_status(machine_id)
    assert 'status' in status
    assert 'anomalies' in status
    assert status['machine_id'] == machine_id

def test_maintenance_recommendation_agent_load(maintenance_agent):
    assert isinstance(maintenance_agent.procedures, dict)

def test_maintenance_recommendation_agent_recs(maintenance_agent):
    anomalies = ['high_temperature']
    recs = maintenance_agent.get_recommendations(anomalies)
    assert 'high_temperature' in recs
    assert isinstance(recs['high_temperature'], list)
