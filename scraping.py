import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# Setup WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Start maximized
driver = webdriver.Chrome(options=options)

# List of state transport operators and their URLs
state_transports = {
    "Andhra": "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
    "Rajasthan": "https://www.redbus.in/online-booking/rsrtc",
    "Kerala": "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
    "Kadamba": "https://www.redbus.in/online-booking/ktcl",
    "Bihar": "https://www.redbus.in/online-booking/bihar-state-road-transport-corporation-bsrtc/?utm_source=rtchometile",
    "Himachal": "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
    "South Bengal": "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
    "Telangana": "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
    "Patiala and East Punjab": "https://www.redbus.in/online-booking/pepsu-punjab",
    "West Bengal Surface" : "https://www.redbus.in/online-booking/west-bengal-transport-corporation?utm_source=rtchometile"
}

wait = WebDriverWait(driver, 20)

def scrape_routes(url, xpath):
    driver.get(url)
    print(f"Accessing {url}...")

    state_name = f"{state}"
    print(state_name)
    
    state_names = []
    route_names = []
    bus_links = []
    bus_names = []
    bus_types = []
    bus_froms = []
    bus_from_times = []
    bus_tos = []
    bus_to_times = []
    bus_durations = []
    bus_fares = []
    bus_seats = []
    bus_ratings = []

    while True:
        
        next_page_button = None
        # Wait for route elements to be present
        paths = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        hrefs = [link.get_attribute("href") for link in paths]

        pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
        active_buttons = pagination.find_elements(By.XPATH, './/div[contains(@class, "pageActive")]')
        if active_buttons:
            btnnumber = active_buttons[0].text
            nxtbutton = str(int(btnnumber) + 1)
                                                                
        for href in hrefs:
            driver.get(href)
            time.sleep(10)
            bus_link = href
                        
            while True:
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
            
            time.sleep(10)
            checkload = driver.find_elements(By.XPATH, '//*[@class="bus-items"]')
            if checkload:
                buslinks = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="bus-items"]')))
                bus_infos = buslinks.find_elements(By.XPATH, './/div[contains(@class, "clearfix bus-item-details")]')
                route_src = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "src")]'))).text
                route_dst = wait.until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "dst")]'))).text
                route_name = route_src + " To " + route_dst
                print (route_name)
                
                if bus_infos:
                    for bus_info in bus_infos:
                        bus_name = bus_info.find_element(By.XPATH, './/div[contains(@class, "travels lh-24 f-bold d-color")]').text
                        bus_type = bus_info.find_element(By.XPATH, './/div[contains(@class, "bus-type f-12 m-top-16 l-color evBus")]').text
                        bus_from = bus_info.find_element(By.XPATH, './/div[contains(@class, "dp-loc l-color w-wrap f-12")]').text
                        bus_from_time = bus_info.find_element(By.XPATH, './/div[contains(@class, "dp-time f-19 d-color f-bold")]').text
                        bus_to = bus_info.find_element(By.XPATH, './/div[contains(@class, "bp-loc l-color w-wrap f-12")]').text
                        bus_to_time = bus_info.find_element(By.XPATH, './/div[contains(@class, "bp-time f-19 d-color disp-Inline")]').text
                        bus_duration = bus_info.find_element(By.XPATH, './/div[contains(@class, "dur l-color lh-24")]').text
                        bus_fare = bus_info.find_element(By.XPATH, './/span[contains(@class, "f-19") and contains(@class, "f-bold")]').text
                        bus_seat = bus_info.find_element(By.XPATH, './/div[contains(@class, "seat-left")]').text
                        bus_ratingt = bus_info.find_element(By.XPATH, '//span[@class=""]')
                        if bus_ratingt:
                            bus_rating = bus_ratingt.text
                        else:
                            bus_rating = ""
                        state_names.append(state_name)
                        route_names.append(route_name)
                        bus_links.append(bus_link)
                        bus_names.append(bus_name)
                        bus_types.append(bus_type)
                        bus_froms.append(bus_from)
                        bus_from_times.append(bus_from_time)
                        bus_tos.append(bus_to)
                        bus_to_times.append(bus_to_time)
                        bus_durations.append(bus_duration)
                        bus_fares.append(bus_fare)
                        bus_seats.append(bus_seat)
                        bus_ratings.append(bus_rating)
            else:
                print("Page not loaded...")
                
            time.sleep(10)

        # Handle pagination
        driver.get(url)
        print("LETS CHECK NEXT PAGE...")
        pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="DC_117_paginationTable"]')))
        find_buttons = pagination.find_elements(By.XPATH, './/div[contains(@class, "DC_117_pageTabs")]')
        button_index = 0
        for next_button in find_buttons:
            btnnumbr = find_buttons[button_index].text
            if btnnumbr == nxtbutton:
                next_page_button = find_buttons[button_index]
            button_index += 1        
        if next_page_button:
            print("NEXT PAGE BUTTON FOUND....")
            # Ensure the next page button is in view
            actions = ActionChains(driver)
            actions.move_to_element(next_page_button).perform()
            time.sleep(1)  # Wait for a bit after scrolling 
            next_page_button.click()
        else:
            print("NO NEXT PAGE BUTTON, QUITTING....")
        if next_page_button == None:
            break

    return state_names, route_names, bus_links, bus_names, bus_types, bus_froms, bus_from_times, bus_tos, bus_to_times, bus_durations, bus_fares, bus_seats, bus_ratings


    
for state, url in state_transports.items():
    print(f"Scraping data for {state}...")
    state_name = {state}
    
    # Scrape routes for each state transport
    All_state_names = []
    All_route_names = []
    All_bus_links = []
    All_bus_names = []
    All_bus_types = []
    All_bus_froms = []
    All_bus_from_times = []
    All_bus_tos = []
    All_bus_to_times = []
    All_bus_durations = []
    All_bus_fares = []
    All_bus_seats = []
    All_bus_ratings = []

    try:
        states, routes, blinks, bnames, btypes, bfroms, bftimes, btos, bttimes, bdurations, bfares, bseats, bratings = scrape_routes(url, "//a[contains(@class, 'route')]")
        All_state_names.extend(states)
        All_route_names.extend(routes)
        All_bus_links.extend(blinks)
        All_bus_names.extend(bnames)
        All_bus_types.extend(btypes)
        All_bus_froms.extend(bfroms)
        All_bus_from_times.extend(bftimes)
        All_bus_tos.extend(btos)
        All_bus_to_times.extend(bttimes)
        All_bus_durations.extend(bdurations)
        All_bus_fares.extend(bfares)
        All_bus_seats.extend(bseats)
        All_bus_ratings.extend(bratings)
        
        # Create a DataFrame using the route names and links
        df = pd.DataFrame({"State": All_state_names, "Route": All_route_names, "URL":All_bus_links, "Bus_Name":All_bus_names, "Type":All_bus_types, "Origin":All_bus_froms, "Departure":All_bus_from_times, "Destination":All_bus_tos, "Arrival":All_bus_to_times, "Duration":All_bus_durations, "Fare":All_bus_fares, "Seats":All_bus_seats, "Rating":All_bus_ratings})
        print(df)
        df.to_csv(f'.\\csv\\{state}.csv', index=False)
        
    except Exception as e:
        print(f"Error occurred for {state}: {e}")

driver.quit()

print("ALL DONE.....!!! ")
