from datetime import date
from webui import *
from exceptions import DateCheckResult

class CLOCK_IN:
    def __init__(self):
        pass
        # self.emaildestinations:list = [""]
        
    def setup(self):
        url = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com'
        wd = open_browser()
        wd.maximize_window()
        login(url)
    
    def teardown(self):
        wd = get_global_webdriver()
        wd.quit()

    def steps(self):        
        applications()
        pop_up_clockin_page()
        switch_to_clockin_tab()
        fillTemperature(bodyTemperature())
        # CheckHealth()
        # Go2School()
        # Submit()
        # clickConfirmButton()
        # ContinueAdding()
        ToRecords()
        checkFinalResult()
        
        

def clockIn():
    clockin = CLOCK_IN()
    clockin.setup()
    clockin.steps()
    clockin.teardown()


if __name__ == '__main__':
    # YEAR = 2022
    # MON = 10
    # DAY = 5
    # CHECK_GO_TO_SCHOOL = DateCheckResult(date(YEAR, MON, DAY))
    CHECK_GO_TO_SCHOOL = DateCheckResult(date.today())
    if CHECK_GO_TO_SCHOOL == "yes":
        clockIn()
    elif CHECK_GO_TO_SCHOOL == "no":
        print("not clock in this day!")
