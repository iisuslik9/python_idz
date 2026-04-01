import pandas as pd
from typing import Dict, Any

class WarehouseModel:
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set_data(self, key: str, value: Any):
        self.data[key] = value

    def calculate_area(self) -> float:
        Pa = float(self.data['Pa'])  # т
        p = int(self.data['p'])      # сут, ЦЕЛОЕ число
        V = float(self.data['V'])    # сут
        capacity = float(self.data['capacity'])
        Ka = 0.33 if capacity <= 500 else 0.5
        qa_map = {
            'бухты/мотки': 1.2, 
            'прутки': 3.2, 
            'полосовая': 2.1, 
            'сетки': 0.4, 
            'бухты в бункерах': 3.0
        }
        qa = qa_map[self.data['type']]
        S = (Pa * p) / (V * Ka * qa)
        return round(S, 2)

    def save_to_xlsx(self, filename: str, S: float):
        capacity = float(self.data['capacity'])
        Ka = 0.33 if capacity <= 500 else 0.5
        qa_map = {
            'бухты/мотки': 1.2, 'прутки': 3.2, 'полосовая': 2.1, 
            'сетки': 0.4, 'бухты в бункерах': 3.0
        }
        qa = qa_map[self.data['type']]
        
        df = pd.DataFrame({
            'Параметр': [
                'Годовая потребность Па, т', 
                'Запас п, сут', 
                'Фонд времени В, сут', 
                'Вместимость, т', 
                'Коэффициент Ka', 
                'Масса на 1м² qa, т/м²', 
                'Площадь S, м²'
            ],
            'Значение': [
                self.data['Pa'], 
                self.data['p'], 
                self.data['V'], 
                self.data['capacity'],
                Ka, 
                qa, 
                S
            ]
        })
        df.to_excel(filename, index=False)