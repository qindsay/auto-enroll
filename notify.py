from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup
import requests as rq
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import os
from dotenv import load_dotenv

class notify:
    def __init__(self):
        load_dotenv()
        self.dest = os.getenv('DEST')
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
    
    def send_email(self, class_name, link):
        SMTPserver = 'smtp.gmail.com'
        sender = self.email
        destination = self.dest

        # typical values for text_subtype are plain, html, xml
        text_subtype = 'html'
        try:
            content=f"""
                <html>
                <body>
                    <p>{class_name} is open! Enroll  
                    <a href="{link}">here</a>.
                    </p>
                </body>
                </html>
                """
            msg = MIMEText(content, text_subtype)
            msg['Subject']= f"{class_name} OPEN"
            msg['From']   = "sender" # some SMTP servers will do this automatically, not all
            
            conn = SMTP(SMTPserver, 465)
            conn.set_debuglevel(False)
            conn.login(self.email, self.password)
            try:
                conn.sendmail(sender, destination, msg.as_string())
                print("Successfully sent email.")
            finally:
                conn.quit()
        except Exception as e:
            print("Error:", e)  

class enroll:
    def __init__(self):
        self.notif = notify()
    
    def extract_count_status(self, row, waitlist):
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
    
    def save_count(self, url):
        r = rq.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        id_tags = soup.find("div", id="class_id_textbook")
        class_id = str(id_tags.find_all("p")[1])[13:22]
        
        candidates = soup.find_all("td")
        row = candidates[0]
        waitlist = candidates[1]
        
        seats, status = self.extract_count_status(row.string, waitlist.string)
        
        if class_id not in previous:
            previous[class_id] = [seats, status]
        else:
            if seats < previous[class_id][0]:
                self.notif.send_email(class_id, url) 
                
    
# urlOpen = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=EC%20ENGR&crs_catlg_no=0116C%20M%20&class_id=439398100&class_no=%20001%20%20"
# urlWaitlist = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=COM%20SCI&crs_catlg_no=0181%20%20%20%20&class_id=187787200&class_no=%20001%20%20"
# urlClosed = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassDetail?term_cd=25F&subj_area_cd=COM%20SCI&crs_catlg_no=0163%20%20%20%20&class_id=187699200&class_no=%20001%20%20"
# urls = [urlOpen, urlWaitlist, urlClosed]

# previous = {'439398100': [54, 0], '187787200': [14, 1], '187699200': [120, 2]}



# for url in urls:
#     save_count(url)
    





