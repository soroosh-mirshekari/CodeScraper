import time, random
from maskan_file_new import Maskan_File as MaskanDetcNew
from maskan_file_old import Maskan_File as MaskanDectOld
from maskan_file import RealEstateCleaner, RealEstateScraper
from melkemun import EstateManager
from melkemun_cleaner import MelkemunEstateCleaner
from database_manager import create_data, select_data, create_sim, select_similarity_pairs
from similarity_algorithm import PropertySimilarity
from tabulate import tabulate

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
        
        print("new scraping started.")
        detector = MaskanDetcNew("https://maskan-file.ir/Site/Default.aspx")
        new_property_codes = detector.run()
        
        # scrap data and put new data in database
        maskan_scraper(new_property_codes)

        time.sleep(random.uniform(20, 30)) #Use random delays to mimic human browsing patterns

def melkmun_scraper(n):
    manager = EstateManager()
    for n in range(0,n):
        estate_data = manager.get_estate_by_index(n)

        cleaner = MelkemunEstateCleaner()
        cleaned_data = cleaner.clean(estate_data)

        # TODO:  algorithm here

        create_data(cleaned_data)

def melkmun():
    # getting the old data (old scraper) and save in database
    melkmun_scraper(20)

    print("Old data have been added to database.")

    while True:
        time.sleep(random.uniform(20, 30)) #Use random delays to mimic human browsing patterns
        print("new scraping started.")

        # getting the new data (new scraper) and save in database
        melkmun_scraper(10)

def similarity_checker():
    all_data = select_data()
    similarity_check = PropertySimilarity()
    check_results = similarity_check.compare_properties(properties=all_data)
    return check_results

def similarity():
    datas = similarity_checker() 
    for data in datas:
        create_sim(data)

    print("sim data added to database")

def print_similiar_files():
    pairs = select_similarity_pairs()

    # Define table headers for all Data fields
    headers = [
        "Similarity ID", "Similarity Score",
        "Data 1 ID", "Data 1 File Code", "Data 1 Title",
        "Data 1 Total Price", "Data 1 Price/Meter", "Data 1 Mortgage", "Data 1 Rent",
        "Data 1 Area", "Data 1 Rooms", "Data 1 Year",
        "Data 2 ID", "Data 2 File Code", "Data 2 Title",
        "Data 2 Total Price", "Data 2 Price/Meter", "Data 2 Mortgage", "Data 2 Rent",
        "Data 2 Area", "Data 2 Rooms", "Data 2 Year",    ]

    # Prepare table rows
    rows = []
    for pair in pairs:
        row = [
            pair["similarity_id"],
            pair["similarity_score"],
            pair["data_1"]["id"] if pair["data_1"] else None,
            pair["data_1"]["file_code"] if pair["data_1"] else None,
            pair["data_1"]["title"] if pair["data_1"] else None,
            pair["data_1"]["total_price"] if pair["data_1"] else None,
            pair["data_1"]["price_per_meter"] if pair["data_1"] else None,
            pair["data_1"]["mortgage"] if pair["data_1"] else None,
            pair["data_1"]["rent"] if pair["data_1"] else None,
            pair["data_1"]["area"] if pair["data_1"] else None,
            pair["data_1"]["number_of_rooms"] if pair["data_1"] else None,
            pair["data_1"]["year_of_manufacture"] if pair["data_1"] else None,
            pair["data_2"]["id"] if pair["data_2"] else None,
            pair["data_2"]["file_code"] if pair["data_2"] else None,
            pair["data_2"]["title"] if pair["data_2"] else None,
            pair["data_2"]["total_price"] if pair["data_2"] else None,
            pair["data_2"]["price_per_meter"] if pair["data_2"] else None,
            pair["data_2"]["mortgage"] if pair["data_2"] else None,
            pair["data_2"]["rent"] if pair["data_2"] else None,
            pair["data_2"]["area"] if pair["data_2"] else None,
            pair["data_2"]["number_of_rooms"] if pair["data_2"] else None,
            pair["data_2"]["year_of_manufacture"] if pair["data_2"] else None,
        ]
        rows.append(row)
    
    # Print the table using tabulate
    print(tabulate(rows, headers=headers,tablefmt="github", stralign="right", floatfmt=".2f"))
    
def menu():
    while True:
        print("""choose the site you want data from:
              1.maskan
              2.melkmun
              3.similarity check
              4.show similar files information
              0.exit
              """)
        
        user_choice = input("Enter here(1-4): ")

        if user_choice == "1":
            maskan()
        elif user_choice == "2":
            melkmun()
        elif user_choice == "3":
            similarity()
        elif user_choice == "4":
            print_similiar_files()
        elif user_choice == "0":
            break
        else: print("please enter correctly.")
        
menu()