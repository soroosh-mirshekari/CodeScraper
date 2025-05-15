import time
from maskan_file_new import Maskan_File as MaskanDetcNew
from maskan_file_old import Maskan_File as MaskanDectOld
from maskan_file import RealEstateCleaner, RealEstateScraper
from database_manager import create_data, select_data

def maskan_new():

    # detector_old = MaskanDectOld(https://maskan-file.ir/Site/Default.aspx)

    detector = MaskanDetcNew("https://maskan-file.ir/Site/Default.aspx")
    new_property_codes = detector.run()
    
    for property_code in new_property_codes:

        scraper = RealEstateScraper(property_code)
        property_data = scraper.scrape()

        cleaner = RealEstateCleaner()
        cleaned_data = cleaner.clean(property_data)

        create_data(cleaned_data)

    print("All data have been added to database.")


def menu():
    while True:
        print("""choose the site you want data from:
              1.maskan
              2.melkmun
              """)
        
        user_choice = input("Enter here(1-4): ")

        if user_choice == "1":
            maskan_new()
            

menu()