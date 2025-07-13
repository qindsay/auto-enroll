from bs4 import BeautifulSoup
import requests as rq
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import os
from dotenv import load_dotenv

import threading
import time

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

class checker:
    def __init__(self, check_interval=5):
        self.notif = notify()
        
        self.urls_ids = {}
        
        #both dictionaries use class ids as keys
        self.status_seats = {}
        self.class_names = {}
        
        self.lock = threading.Lock()
        self.is_running = True
        
        self.CHECK_INTERVAL = check_interval #seconds
        self.OPEN = 0
        self.WAITLIST = 1
        self.CLOSED = 2
    
    def add_class(self, url):
        r = rq.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        id_tags = soup.find("div", id="class_id_textbook")
        class_id = str(id_tags.find_all("p")[1])[13:22]
        
        class_block = str(soup.find("div", id="subject_class"))
        br_index_end = class_block.index("<br/>") + 5
        length = len(class_block)
        class_name = class_block[br_index_end:length-10].strip()

        self.urls_ids[url] = class_id
        self.class_names[class_id] = class_name
        
        print("Added " + self.get_info_string(url))
    
    def remove_class(self, url):
        if url in self.urls:
            class_id = self.urls_ids[url]
            del self.urls_ids[url]
            del self.class_names[class_id]
            del self.seats_status[class_id]
            
            print("Removed " + self.get_info_string(url))
        else:
            print("URL not found:", url)
        
    def extract_count_status(self, row, waitlist):
        if "Open" in row:
            of_index = row.index("of")
            spots = int(row[6:of_index-1])
            return spots, self.OPEN
        elif "Waitlist" in row:
            print("row", row)
            print("waitlist", waitlist)
            of_index = waitlist.index("of")
            spots = int(waitlist[:of_index-1])
            return spots, self.WAITLIST
        else:
            open_index = row.index("(")
            close_index = row.index(")")
            spots = int(row[open_index+1:close_index])
            return spots, self.CLOSED
    
    def get_info_string(self, url):
        id = self.urls_ids[url]
        info_string = f"{self.class_names[id]}. {id} ({url})"
        return info_string
    
    def check_count(self, url):
        r = rq.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        class_id = self.urls_ids[url]
        
        candidates = soup.find_all("td")
        row = candidates[0]
        waitlist = candidates[1]
        
        seats, status = self.extract_count_status(row.string, waitlist.string)
                    
        if class_id in self.status_seats:
            if status < self.seats_status[class_id][1]: #status changed to be open or waitlist
                self.notif.send_email(class_id, url)
            elif seats > self.seats_status[class_id][0]: #seats increased
                self.notif.send_email(class_id, url)
        
        self.seats_status[class_id] = [seats, status]
    
    def monitor(self):
        while self.is_running:
            with self.lock:
                current_sites = self.urls_ids.copy()
            for url in current_sites:
                self.check_count(url)
            time.sleep(self.CHECK_INTERVAL)
    
    def command_line(self):
        print("Type commands: add <url>, remove <url>, list, quit")
        while True:
            cmd = input("> ").strip()
            if cmd.startswith("add "):
                url = cmd[4:].strip()
                with self.lock:
                    if url in self.urls_ids:
                        print("Already monitoring:", self.class_names[self.urls_ids[url]])
                    else:
                        self.add_class(url)
            elif cmd.startswith("remove "):
                url = cmd[7:].strip()
                with self.lock:
                    if url in self.urls_ids:
                        self.remove_class(url)
                    else:
                        print("URL not found:", url)
            elif cmd == "list":
                with self.lock:
                    print("Currently monitoring:")
                    for id in self.class_names:
                        print(" •", self.class_names[id])
            elif cmd == "quit":
                print("Exiting...")
                self.is_running = False
                break
            else:
                print("Unknown command.")

    





