import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker, aliased
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the connection string (update with your MySQL credentials)
connection_string = "mysql+mysqlconnector://my_user:my_password@localhost/codescraper"

# Create the engine
engine = create_engine(connection_string, echo=False)

# Create a base class for declarative models
Base = declarative_base()

# Define the Data model
class Data(Base):
    __tablename__ = "codescraper"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID
    file_code = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False) #increased lenght from 50 to 100 cause some of them were more that 100
    address = Column(String(200), nullable=False) #increased lenght from 100 to 200 cause some of them were more that 100
    total_price = Column(Float, nullable=True)  
    price_per_meter = Column(Float, nullable=True)
    mortgage = Column(Float, nullable=True)
    rent = Column(Float, nullable=True)
    area = Column(Integer, nullable=True)
    number_of_rooms = Column(Integer, nullable=True)
    year_of_manufacture = Column(Integer, nullable=True)
    facilities = Column(JSON, nullable=True) 
    pictures = Column(JSON, nullable=True)
    is_rental = Column(Boolean, nullable=True)

class Similarity(Base):
    __tablename__ = "similarity"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID
    id_1 = Column(Integer, nullable=True)
    id_2 = Column(Integer, nullable=True)
    similarity = Column(Float, nullable=True)

# Create all tables

Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Context manager for session handling
@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Session error: {e}")
        raise
    finally:
        session.close()

# function to create data with duplicate check
def create_data(dict_data):
    try:
        with session_scope() as session:
            # Check if file_code already exists
            existing_data = session.query(Data).filter(Data.file_code == dict_data.get("file_code", "")).first()
            if existing_data:
                logging.warning(f"Data with file_code {dict_data.get('file_code')} already exists. Skipping insertion.")
                return False
            # Insert new data
            new_data = Data(
                file_code=dict_data.get("file_code", ""),
                title=dict_data.get("title", ""),
                address=dict_data.get("address", ""),
                total_price=dict_data.get("total_price"),
                price_per_meter=dict_data.get("price_per_meter"),
                mortgage=dict_data.get("mortgage"),
                rent=dict_data.get("rent"),
                area=dict_data.get("area"),
                number_of_rooms=dict_data.get("number_of_rooms"),
                year_of_manufacture=dict_data.get("year_of_manufacture"),
                facilities=dict_data.get("facilities", []),
                pictures=dict_data.get("pictures", []),
                is_rental=dict_data.get("is_rental")
            )
            session.add(new_data)
            logging.info(f"Inserted data: {dict_data.get('file_code')}")
            return True
    except SQLAlchemyError as e:
        logging.error(f"Error inserting data: {e}")
        return False

# function to create similarity data with duplicate check
def create_sim(dict_sim):
    try:
        with session_scope() as session:
            # Check if the combination of id_1 and id_2 already exists
            existing_sim = session.query(Similarity).filter(
                Similarity.id_1 == dict_sim.get("property_1"),
                Similarity.id_2 == dict_sim.get("property_2")
            ).first()
            if existing_sim:
                logging.warning(f"Similarity with id_1 {dict_sim.get('property_1')} and id_2 {dict_sim.get('property_2')} already exists. Skipping insertion.")
                return False
            # Insert new similarity data
            new_sim_data = Similarity(
                id_1=dict_sim.get("property_1"),
                id_2=dict_sim.get("property_2"),
                similarity=dict_sim.get("similarity")
            )
            session.add(new_sim_data)
            logging.info(f"Inserted similarity data: {dict_sim.get('property_1')} and {dict_sim.get('property_2')}")
            return True
    except SQLAlchemyError as e:
        logging.error(f"Error inserting similarity data: {e}")
        return False

# Function to fetch all similarity pairs with their corresponding Data table info
def select_similarity_pairs():
    try:
        with session_scope() as session:
            # Create aliases for the Data table
            Data1 = aliased(Data, name='data1')
            Data2 = aliased(Data, name='data2')
            
            # Join Similarity with Data for id_1 and id_2 using aliases
            results = []
            sim_data = session.query(Similarity, Data1, Data2).\
                join(Data1, Similarity.id_1 == Data1.id, isouter=True).\
                join(Data2, Similarity.id_2 == Data2.id, isouter=True).\
                all()
            
            for sim, data1, data2 in sim_data:
                pair = {
                    "similarity_id": sim.id,
                    "similarity_score": sim.similarity,
                    "data_1": None,
                    "data_2": None
                }
                if data1:
                    pair["data_1"] = {
                        "id": data1.id,
                        "file_code": data1.file_code,
                        "title": data1.title,
                        "address": data1.address,
                        "total_price": data1.total_price,
                        "price_per_meter": data1.price_per_meter,
                        "mortgage": data1.mortgage,
                        "rent": data1.rent,
                        "area": data1.area,
                        "number_of_rooms": data1.number_of_rooms,
                        "year_of_manufacture": data1.year_of_manufacture,
                        "facilities": data1.facilities,
                        "pictures": data1.pictures,
                        "is_rental": data1.is_rental,
                    }
                else:
                    logging.warning(f"No data found for id_1: {sim.id_1}")
                if data2:
                    pair["data_2"] = {
                        "id": data2.id,
                        "file_code": data2.file_code,
                        "title": data2.title,
                        "address": data2.address,
                        "total_price": data2.total_price,
                        "price_per_meter": data2.price_per_meter,
                        "mortgage": data2.mortgage,
                        "rent": data2.rent,
                        "area": data2.area,
                        "number_of_rooms": data2.number_of_rooms,
                        "year_of_manufacture": data2.year_of_manufacture,
                        "facilities": data2.facilities,
                        "pictures": data2.pictures,
                        "is_rental": data2.is_rental,
                    }
                else:
                    logging.warning(f"No data found for id_2: {sim.id_2}")
                results.append(pair)
            
            return results
    except SQLAlchemyError as e:
        logging.error(f"Error fetching similarity pairs: {e}")
        return []

# Function to fetch all data into a dict
def select_data():
    try:
        with session_scope() as session:
            all_data = session.query(Data).all()
            result = [{
                "id": data.id,
                "file_code": data.file_code,
                "title": data.title,
                "address": data.address,
                "total_price": data.total_price,
                "price_per_meter": data.price_per_meter,
                "mortgage": data.mortgage,
                "rent": data.rent,
                "area": data.area,
                "number_of_rooms": data.number_of_rooms,
                "year_of_manufacture": data.year_of_manufacture,
                "facilities": data.facilities,
                "pictures": data.pictures,
                "is_rental": data.is_rental,
            } for data in all_data]
            return result
    except SQLAlchemyError as e:
        logging.error(f"Error fetching data: {e}")
        return []

# Function to delete data by ID
def delete_data(data_id):
    try:
        with session_scope() as session:
            data = session.query(Data).filter(Data.id == data_id).first()
            if data:
                session.delete(data)
                logging.info(f"Deleted data with ID: {data_id}")
                return True
            else:
                logging.warning(f"No data found with ID: {data_id}")
                return False
    except SQLAlchemyError as e:
        logging.error(f"Error deleting data with ID {data_id}: {e}")
        return False

if __name__ == "__main__":
    test_data = [
        {
            'file_code': '2886670',
            'title': 'هاشمیه 79 کوهسار 8',
            'address': 'منطقه 9 محله هنرستان خیابان هاشمیه 79 کوهسار 8',
            'total_price': None,
            'price_per_meter': None,
            'mortgage': 300000000.0, 
            'rent': 2000000.0,  
            'area': 60,
            'number_of_rooms': 1,
            'year_of_manufacture': 1,
            'facilities': ["حیاط دار", "بازسازی شده", "کمد دیواری"], 
            'pictures': [],  
            'is_rental': True
        },
        {
            'file_code': '2881482', 
            'title': 'مشکینی 45', 
            'address': 'منطقه 10 محله قاسم آباد خیابان مشکینی 45', 
            'total_price': None, 
            'price_per_meter': None, 
            'mortgage': 350000000, 
            'rent': 4500000, 
            'area': 80, 
            'number_of_rooms': 2, 
            'year_of_manufacture': 14, 
            'facilities': ['آیفون تصویری', 'کمد دیواری', 'خط تلفن'], 
            'pictures': ['https://maskan-file.ir/img/FilesImages/2881482_3.jpg?v=5/15/2025', 'https://maskan-file.ir/img/FilesImages/2881482_1.jpg?v=5/15/2025', 'https://maskan-file.ir/img/FilesImages/2881482_2.jpg?v=5/15/2025'], 
            'is_rental': True
         }
    ]

    # sim = [
    #     {
    #         'property_1': 1,
    #         'property_2': 2,
    #         'similarity': 66.6,
    #     }
    # ]

    # # Insert test data
    # for data in test_data:
    #     create_data(data)
    
    # # Insert test similarity data
    # for data in sim:
    #     create_sim(data)

    # Test selecting similarity pairs
    results = select_similarity_pairs()
    for result in results:
        print(result)