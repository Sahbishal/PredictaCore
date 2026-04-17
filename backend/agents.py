import pandas as pd
import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest
import joblib
load_dotenv()

class SensorAnalysisAgent:
    def __init__(self, data_path='data/turbine_data.csv', model_path='data/isolation_forest.joblib'):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.model_path = model_path
        
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = IsolationForest(contamination=0.05, random_state=42)
            self._train_model()
    
    def _train_model(self):
        # Select numeric features for anomaly detection
        features = ['temperature', 'vibration', 'pressure', 'oil_pressure', 'rpm']
        X = self.df[features]
        self.model.fit(X)
        joblib.dump(self.model, self.model_path)
    
    def get_machine_status(self, machine_id):
        machine_data = self.df[self.df['machine_id'] == machine_id].sort_values('timestamp', ascending=False)
        
        if machine_data.empty:
            return {"error": "Machine ID not found"}
            
        latest = machine_data.iloc[0]
        
        # ML-based anomaly detection
        features = ['temperature', 'vibration', 'pressure', 'oil_pressure', 'rpm']
        current_features = latest[features].values.reshape(1, -1)
        is_anomaly = self.model.predict(current_features)[0] == -1
        
        anomalies = []
        if is_anomaly:
            # Additional heuristic to provide human-readable anomaly types
            if latest['temperature'] > 900: anomalies.append('high_temperature')
            if latest['vibration'] > 0.75: anomalies.append('high_vibration')
            if latest['oil_pressure'] < 2.8: anomalies.append('low_oil_pressure')
            if not anomalies:
                anomalies.append('system_anomaly_detected')
        
        return {
            "machine_id": machine_id,
            "latest_stats": latest.to_dict(),
            "anomalies": anomalies,
            "status": "Warning" if anomalies else "Normal"
        }

class MaintenanceRecommendationAgent:
    def __init__(self, procedures_path='data/maintenance_procedures.json'):
        with open(procedures_path, 'r') as f:
            self.procedures = json.load(f)
        
        # Initialize LLM for follow-up questions
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        
    def get_recommendations(self, anomalies):
        recs = {}
        for anomaly in anomalies:
            if anomaly in self.procedures:
                recs[anomaly] = self.procedures[anomaly]
        return recs

    def answer_question(self, question, machine_status, recommendations):
        prompt = ChatPromptTemplate.from_template("""
        You are a turbine maintenance expert. Based on the machine status and recommendations provided, answer the user's follow-up question.
        
        Machine Status: {status}
        Recommendations: {recs}
        
        Question: {question}
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"status": json.dumps(machine_status), "recs": json.dumps(recommendations), "question": question})
        return response.content
