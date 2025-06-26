from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time

from bs4 import BeautifulSoup
import requests as rq

# chrome_options = Options()

# # chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options) 
# driver.get("https://sa.ucla.edu/ro/Public/SOC")

# time.sleep(5)
# selection = driver.find_element("id", "search_by")
# select_menu = Select(selection)
# select_menu.select_by_value('classidnumber')

urlOpen = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=EC%20ENGR&crs_catlg_no=0116C%20M%20&class_id=439398100&class_no=%20001%20%20"
urlWaitlist = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=COM%20SCI&crs_catlg_no=0181%20%20%20%20&class_id=187787200&class_no=%20001%20%20"
urlClosed = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=COM%20SCI&crs_catlg_no=0163%20%20%20%20&class_id=187699200&class_no=%20001%20%20"
urls = [urlOpen, urlWaitlist, urlClosed]

previous = {'439398100': [54, 0], '187787200': [14, 1], '187699200': [120, 2]}
def extract_count_status(row, waitlist):
    if "Open" in row:
        of_index = row.index("of")
        spots = int(row[6:of_index-1])
        return spots, 0
    elif "Waitlist" in row:
        print("row", row)
        print("waitlist", waitlist)
        of_index = waitlist.index("of")
        spots = int(waitlist[:of_index-1])
        return spots, 1
    else:
        open_index = row.index("(")
        close_index = row.index(")")
        spots = int(row[open_index+1:close_index])
        return spots, 2

def save_count(url):
    r = rq.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    id_tags = soup.find("div", id="class_id_textbook")
    class_id = str(id_tags.find_all("p")[1])[13:22]
    
    candidates = soup.find_all("td")
    row = candidates[0]
    waitlist = candidates[1]
    
    seats, status = extract_count_status(row.string, waitlist.string)
    
    if class_id not in previous:
        previous[class_id] = [seats, status]
    else:
        if seats < previous[class_id][0]:
            print("notify")
    
        
    
for url in urls:
    save_count(url)




