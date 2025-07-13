import threading
from notify import checker

def main():
    check = checker()
    monitor_thread = threading.Thread(target=check.monitor, args=())
    monitor_thread.start()
    check.command_line()
    monitor_thread.join()
    

if __name__ == "__main__":
    main()