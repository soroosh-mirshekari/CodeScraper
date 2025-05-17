import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
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

# Function to create data
def create_data(dict_data):
    # if 
        try:
            with session_scope() as session:
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
        except SQLAlchemyError as e:
            logging.error(f"Error inserting data: {e}")

# Function to create similarity data
def create_sim(dict_sim):
    try:
        with session_scope() as session:
            new_sim_data = Similarity(
                id_1 = dict_sim.get("property_1"),
                id_2 = dict_sim.get("property_2"),
                similarity = dict_sim.get("similarity")
            )
            session.add(new_sim_data)
            logging.info(f"Inserted data: {dict_sim.get('property_1')} and {dict_sim.get('property_2')}")
    except SQLAlchemyError as e:
        logging.error(f"Error inserting data: {e}")

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

    sim = [
        {
            'property_1' : 1,
            'property_2' : 2,
            'similarity' : 66.6,
        }
    ]
    

    # # Insert test data
    for data in sim:
        create_sim(data)

    # # Fetch and print all data
    # results = select_data()
    # for result in results:
    #     print(result)