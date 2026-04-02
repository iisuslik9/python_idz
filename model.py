class ArmatureWarehouseModel:
    def is_number(self, s):
        if isinstance(s, (int, float)):
            return True
        if not s or s.strip() == "":
            return False
        temp = s.replace('.', '', 1).replace('-', '', 1).replace(',', '')
        return temp.replace('.', '', 1).isdigit()

    def calculate_area(self, annual_demand, storage_days, work_days, capacity_type, metal_type):
        
        if not self.is_number(annual_demand):
            return "Ошибка: годовая потребность должна быть числом"
        
        pga = float(annual_demand)
        if pga <= 0:
            return "Ошибка: годовая потребность должна быть положительным числом"
        
        na = float(storage_days)
        
        # Проверка годового фонда времени
        if not self.is_number(work_days):
            return "Ошибка: годовой фонд времени должен быть числом"
        
        ba = float(work_days)
        if ba <= 0:
            return "Ошибка: годовой фонд времени должен быть положительным числом"

        # Коэффициент использования площади Kиа
        kia = 0.33 if capacity_type == "до 500т" else 0.5

        # Нормы заготовки qa, т/м2
        qa_dict = {
            "сталь в бухтах": 1.2,
            "сталь в прутках": 3.2,
            "полосовая сталь": 2.1,
            "сетки в рулонах": 0.4,
            "бухты в бункерах": 3.0
        }
        qa = qa_dict.get(metal_type, 3.2)

        # Расчет площади
        s = (pga * na) / (ba * kia * qa)
        
        return {
            "area": round(s, 2),
            "details": f"S = ({pga} × {na}) / ({ba} × {kia} × {qa}) = {s:.2f} м\u00B2",
            "input_data": {
                "Годовая потребность (Пга), т": pga,
                "Запас (nа), сут": na,
                "Фонд времени (Bр), сут": ba,
                "Вместимость склада": capacity_type,
                "Коэффициент использования (Kиа)": kia,
                "Тип арматуры": metal_type,
                "Норма загрузки (qa), т/м²": qa
            }
        }