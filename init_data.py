from app.database import SessionLocal
from app.models import models

def init_cities_and_cinemas():
    db = SessionLocal()
    
    try:
        if db.query(models.City).count() > 0:
            print("Города уже есть в базе.")
            return
        
        cities_data = [
            {"name": "Москва"},
            {"name": "Санкт-Петербург"},
            {"name": "Владивосток"},
            {"name": "Волгоград"},
            {"name": "Новосибирск"}
        ]
        
        cities = []
        for city_data in cities_data:
            city = models.City(**city_data)
            db.add(city)
            cities.append(city)
        
        db.commit()
        print(f"Добавлено {len(cities_data)} городов")
        
        moscow = db.query(models.City).filter(models.City.name == "Москва").first()
        saint_petersburg = db.query(models.City).filter(models.City.name == "Санкт-Петербург").first()
        vladivostok = db.query(models.City).filter(models.City.name == "Владивосток").first()
        volgograd = db.query(models.City).filter(models.City.name == "Волгоград").first()
        novosibirsk = db.query(models.City).filter(models.City.name == "Новосибирск").first()
        

        
        cinemas_data = [
            {"city_id": moscow.id, "name": "Октябрь", "address": "ул. Новый Арбат, 24"},
            {"city_id": moscow.id, "name": "Каро 11 Охотный Ряд", "address": "Охотный Ряд, 2"},
            {"city_id": moscow.id, "name": "Формула Кино Европа", "address": "пл. Киевского Вокзала, 2"},
            {"city_id": saint_petersburg.id, "name": "Аврора", "address": "Невский пр., 60"},
            {"city_id": saint_petersburg.id, "name": "Великан Парк", "address": "пр. Тореза, 9"},
            {"city_id": vladivostok.id, "name": "Океан IMAX", "address": "ул. Набережная, 9"},
            {"city_id": vladivostok.id, "name": "Уссури", "address": "ул. Светланская, 49"},
            {"city_id": volgograd.id, "name": "Пять Звёзд", "address": "пр. Ленина, 86"},
            {"city_id": volgograd.id, "name": "Киномакс", "address": "ул. Землячки, 110"},
            {"city_id": novosibirsk.id, "name": "Победа", "address": "ул. Ленина, 7"},
            {"city_id": novosibirsk.id, "name": "Синема Парк", "address": "ул. Ватутина, 107"},
        ]
        
        for cinema_data in cinemas_data:
            cinema = models.Cinema(**cinema_data)
            db.add(cinema)
        
        db.commit()
        print(f"Добавлено {len(cinemas_data)} кинотеатров")
        
    except Exception as error:
        print(f"Ошибка: {error}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Начало инициализации данных")
    init_cities_and_cinemas()
    print("Инициализация завершена")