# 🚀 PredictaCore: Turbine Engine Predictive Maintenance

**PredictaCore** is an AI-powered predictive maintenance application designed to monitor turbine engine health, detect sensor anomalies, and provide actionable maintenance recommendations.

## 🛠 Features
- **Real-time Monitoring**: Track critical turbine metrics like Temperature, Vibration, and RPM.
- **AI-Powered Diagnostics**: Specialized agents analyze sensor data to detect anomalies and identify potential failures.
- **Maintenance Recommendations**: Automated procedure suggestions based on detected issues.
- **Interactive Assistant**: Ask follow-up questions about machine status and maintenance steps via a natural language interface.
- **Sensor Trends Visualization**: Interactive charts for historical data analysis.

## 🏗 Project Structure
- **[./backend/](./backend/)**: FastAPI server implementing the core logic and AI agents.
- **[./frontend/](./frontend/)**: Streamlit-based user dashboard for real-time visualization.
- **[./data/](./data/)**: Contains turbine sensor data (CSV) and maintenance procedure guidelines (JSON).
- **[./run.py](./run.py)**: Unified entry point to launch both backend and frontend services.

## 🚀 Getting Started
 
### Prerequisites
- Python 3.8+
- An OpenAI API key (configured in `.env`)

### Running the Application
To start both the FastAPI backend and the Streamlit frontend, run:
```bash
python run.py
```
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Frontend Dashboard**: [http://localhost:8501](http://localhost:8501) (Streamlit default)
- 

  ## 📦 Tech Stack
 - **Backend**: FastAPI, LangChain, Pydantic
- **Frontend**: Streamlit, Altair
- **Data Analysis**: Pandas, Scikit-learn
- **API**: OpenAI GPT-4o-mini



