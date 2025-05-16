import time, random
from maskan_file_new import Maskan_File as MaskanDetcNew
from maskan_file_old import Maskan_File as MaskanDectOld
from maskan_file import RealEstateCleaner, RealEstateScraper
from melkemun import EstateManager
from database_manager import create_data, select_data

def maskan_scraper(property_codes):
    for property_code in property_codes:
            scraper = RealEstateScraper(property_code)
            property_data = scraper.scrape()

            cleaner = RealEstateCleaner()
            cleaned_data = cleaner.clean(property_data)

            # TODO:  algorythm moshabeh here

            create_data(cleaned_data)
            print("One data added")

def maskan():
    # fetch old data
    detector_old = MaskanDectOld("https://maskan-file.ir/Site/Default.aspx")
    old_property_codes = detector_old.run()

    # scrap data and put old data in database
    maskan_scraper(old_property_codes)
    print("Old data have been added to database.")

    while True:
        
        time.sleep(random.uniform(20, 30)) #Use random delays to mimic human browsing patterns

        print("new scraping started.")
        detector = MaskanDetcNew("https://maskan-file.ir/Site/Default.aspx")
        new_property_codes = detector.run()
        
        # scrap data and put new data in database
        maskan_scraper(new_property_codes)

def melkmun_scraper(n):
    manager = EstateManager()
    for n in range(0,n):
        estate_data = manager.get_estate_by_index(n)

        # TODO: cleaner and algorithm

        create_data(estate_data)

def melkmun():
    # getting the old data (old scraper) and save in database
    melkmun_scraper(20)

    print("Old data have been added to database.")

    while True:
        time.sleep(random.uniform(20, 30)) #Use random delays to mimic human browsing patterns
        print("new scraping started.")

        # getting the new data (new scraper) and save in database
        melkmun_scraper(10)

def menu():
    while True:
        print("""choose the site you want data from:
              1.maskan
              2.melkmun
              0.exit
              """)
        
        user_choice = input("Enter here(1-4): ")

        if user_choice == "1":
            maskan()
        elif user_choice == "2":
            melkmun()
        elif user_choice == "0":
            break
        else: print("please enter correctly.")
        
menu()