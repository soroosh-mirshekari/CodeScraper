import time, random
from maskan_file_new import Maskan_File as MaskanDetcNew
from maskan_file_old import Maskan_File as MaskanDectOld
from maskan_file import RealEstateCleaner, RealEstateScraper
from database_manager import create_data, select_data

def maskan():
    # fetch old data
    detector_old = MaskanDectOld("https://maskan-file.ir/Site/Default.aspx")
    old_property_codes = detector_old.run()

    # put old data in database
    for old_property_code in old_property_codes:
        scraper = RealEstateScraper(old_property_code)
        property_data = scraper.scrape()

        cleaner = RealEstateCleaner()
        cleaned_data = cleaner.clean(old_property_code)

        # TODO:  algorythm moshabeh here

        create_data(cleaned_data)
    
    print("Old data have been added to database.")

    while True:
        
        time.sleep(random.uniform(20, 30)) #Use random delays to mimic human browsing patterns

        print("new scraping started.")
        detector = MaskanDetcNew("https://maskan-file.ir/Site/Default.aspx")
        new_property_codes = detector.run()
        
        for property_code in new_property_codes:

            scraper = RealEstateScraper(property_code)
            property_data = scraper.scrape()

            cleaner = RealEstateCleaner()
            cleaned_data = cleaner.clean(property_data)

            # TODO:  algorythm moshabeh here

            create_data(cleaned_data)

def melkmun():
    pass

def menu():
    while True:
        print("""choose the site you want data from:
              1.maskan
              2.melkmun
              """)
        
        user_choice = input("Enter here(1-4): ")

        if user_choice == "1":
            maskan()
        elif user_choice == "2":
            melkmun()
        else: print("please enter correctly.")
        

menu()