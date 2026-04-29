from datetime import datetime

class OccupancyPredictor:
    def __init__(self, model_path='app/ai_models/occupancy_model.joblib'):
        self.model_path = model_path
        self._model = None
    
    def _load_model(self):
        import joblib
        self._model = joblib.load(self.model_path)
    
    @property
    def model(self):
        if self._model is None:
            self._load_model()
        return self._model
    
    def predict_single(self, session_data: dict) -> float:
        import pandas as pd
        dt = datetime.strptime(session_data['date'], '%Y-%m-%d')
        
        features = pd.DataFrame([{
            'day_of_week': dt.weekday(),
            'is_weekend': 1 if dt.weekday() >= 5 else 0,
            'session_hour': session_data['session_hour'],
            'ticket_price': session_data['ticket_price'],
            'capacity': session_data['capacity']
        }])
        
        return float(self.model.predict(features)[0])