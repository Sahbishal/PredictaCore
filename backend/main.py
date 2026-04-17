from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import json
import os
from backend.agents import SensorAnalysisAgent, MaintenanceRecommendationAgent

app = FastAPI(title="PredictaCore API")

# Load data and agents
data_path = os.getenv('DATA_PATH', 'data/turbine_data.csv')
procedures_path = os.getenv('PROCEDURES_PATH', 'data/maintenance_procedures.json')
model_path = os.getenv('MODEL_PATH', 'data/isolation_forest.joblib')

# Global agent instances (in-memory)
sensor_agent = SensorAnalysisAgent(data_path, model_path)
maintenance_agent = MaintenanceRecommendationAgent(procedures_path)

class MachineStatusRequest(BaseModel):
    machine_id: str

class MachineStatusResponse(BaseModel):
    machine_id: str
    status: str
    latest_stats: dict
    anomalies: List[str]
    recommendations: Optional[dict] = None

class QuestionRequest(BaseModel):
    machine_id: str
    question: str
    status: dict
    recommendations: dict

@app.get("/machines")
async def get_machines():
    df = pd.read_csv(data_path)
    return list(df['machine_id'].unique())

@app.get("/history/{machine_id}")
async def get_machine_history(machine_id: str, limit: int = 50):
    df = pd.read_csv(data_path)
    machine_history = df[df['machine_id'] == machine_id].tail(limit)
    if machine_history.empty:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine_history.to_dict(orient='records')

@app.post("/status", response_model=MachineStatusResponse)
async def get_machine_status(request: MachineStatusRequest):
    status_info = sensor_agent.get_machine_status(request.machine_id)
    recommendations = maintenance_agent.get_recommendations(status_info['anomalies'])
    
    return MachineStatusResponse(
        machine_id=status_info['machine_id'],
        status=status_info['status'],
        latest_stats=status_info['latest_stats'],
        anomalies=status_info['anomalies'],
        recommendations=recommendations
    )

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    response = maintenance_agent.answer_question(
        question=request.question,
        machine_status=request.status,
        recommendations=request.recommendations
    )
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
