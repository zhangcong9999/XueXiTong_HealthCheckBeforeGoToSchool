from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from readpersonalinfo import getConfigInformation
from emailing import send_mail

global GSTORE
GSTORE = {} 

def open_browser():
    '''Open the web browser of the google chrome.'''
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome(options=options)    
    wd.implicitly_wait(20) # timeout value for each page

    # global GSTORE
    # GSTORE = {}    
    GSTORE['global_webdriver'] = wd

    return wd

def get_global_webdriver():
    return GSTORE['global_webdriver']


def login(url='http://www.baidu.com'):
    ''' fill the url and log in with an existing username and password.'''
    
    inifilepath = r"C:\Users\Public\personinf.ini"
    username, password = getConfigInformation(inifilepath).getPersonalInformation()
    wd = get_global_webdriver()
    wd.get(url)
    wd.find_element(By.XPATH, "//input[@id='phone']").send_keys(username) # fill username
    wd.find_element(By.XPATH, '//*[@id="pwd"]').send_keys(password) # fill password
    wd.find_element(By.XPATH, '//*[@id="loginBtn"]').click() # click the button "login"

def applications():
    '''Click the button named "应用中心".'''
    wd = get_global_webdriver()
    wd.find_element(By.XPATH, '//*[@id="first123953"]/h5').click()

def pop_up_clockin_page():
    # Click the button "入校前健康登记" to open another tab named "入校前健康登记"
    wd = get_global_webdriver()
    wd.switch_to.frame("frame_content")
    wd.find_element(By.XPATH, '//span[@title="入校前健康登记"]').click()



def switch_to_clockin_tab():
    ''' Switch to the tab titled "入校前健康登记".'''
    wd = get_global_webdriver()
    global recording
    for handle in wd.window_handles:
        # 先切换到该窗口
        wd.switch_to.window(handle)
        # 得到该窗口的标题栏字符串，判断是不是我们要操作的那个窗口
        if '入校前健康登记' in wd.title:
            # 如果是，那么这时候WebDriver对象就是对应的该该窗口，正好，跳出循环，
            break
    

def fillTemperature(temp:float = 36.3):
    '''Fill number of the given temperature to the box.'''
    wd = get_global_webdriver()
    wd.find_element(By.XPATH, '//li[@id="2"] //input[@class="inputM"]').send_keys(str(temp))

def CheckHealth (health:bool = True):
    '''
    health = True (default): check the "健康".
    health = False: check the "异常".
    '''
    wd = get_global_webdriver()
    express:str = ""
    if health:
        express = '//li[@id="3"]/div[@class="fsw-ul-check"]/div[1]/i'
    else:
        express = '//li[@id="3"]/div[@class="fsw-ul-check"]/div[2]/i'
    wd.find_element(By.XPATH, express).click()

def Go2School (present:bool = True):
    ''' present = True default: Check the "到校".
    present = False: Check the "请假".'''
    wd = get_global_webdriver()
    express:str = ""
    if present:
        express = '//li[@id="5"]/div[@class="fsw-ul-check"]/div[1]/i'
    else:
        express = '//li[@id="5"]/div[@class="fsw-ul-check"]/div[2]/i'
    wd.find_element(By.XPATH, express).click()

def Submit ():
    ''' Click the "提交" button and the confirm  button when prompting.'''
    wd = get_global_webdriver()   
    express = '//*[@id="forms"]//p[@class="appyl_btm_submit fr"]'
    wd.find_element(By.XPATH, express).click() # Click the "提交" button.
    # wd.switch_to.alert.accept() # Click the Yes when prompt.

def saveScreenshot(filename:str = "screenshot"):
    ''' 
    Save the screenshot in the folder named pic.
    The saved file name depends on the given args.
    '''
    wd = get_global_webdriver()
    filepath = ".\\pic\\" + filename + ".png"
    print(filepath)
    wd.get_screenshot_as_file(filepath)

def ToRecords():
    # Click the button "提交记录" to view all submitted records.
    wd = get_global_webdriver()
    express = '//p[@class="go_rec_btn"]'
    wait_count = 6
    for sequ in range(wait_count): # try up to 6 times if the button is not reachable.
        try:
            wd.find_element(By.XPATH, express).click() 
            break
        except:
            if sequ == wait_count - 1: # Doesn't wait if it is the last time.
                break
            else:
                sleep(1)


def CheckUpdatedRecord():
    ''' Check 2 items with the current date at format YYYY-MM-DD.
    Return True if there are more than 1 item else return False if not.'''
    import datetime
    checkpoint:str = datetime.datetime.now().strftime("%Y-%m-%d") # eg: checkpoint: 2022-04-08
    wd = get_global_webdriver()
    express = ('//td[contains(text(), \"%s\")]' %checkpoint)
    recordcount = 0
    TRY_COUNT = 3
    for try_num in range(TRY_COUNT):
        recordcount = len(wd.find_elements(By.XPATH, express))
        if recordcount > 1:
            break
        elif try_num == TRY_COUNT-1:
            break
        else:
            sleep(2)      
    return True if  recordcount > 1 else False


def bodyTemperature():    
    ''' pick a temperature value at random to return.'''
    import random
    return random.choice([36.2, 36.3])

def clickConfirmButton():
    ''' Click the confirm button named "确定".'''
    wd = get_global_webdriver()
    wd.find_element(By.XPATH, '//span[@class="form_submit_sure ml10"]').click()

def ContinueAdding():
    ''' Click the button named "继续添加".'''
    wd = get_global_webdriver()
    wd.find_element(By.XPATH, '//span[contains(text(), "继续添加")]').click()

def checkFinalResult():
    '''Take a screenshot of the final page no matter it fails or passes.
    Check the submit records by the characters of the submit date.
    send the final result and the saved screenshot to destination email stored in the personinf.ini file.'''
    SCREENSHOTNAME = "finalresult"
    saveScreenshot(SCREENSHOTNAME)
    GSTORE[SCREENSHOTNAME] = CheckUpdatedRecord()
    send_mail(SCREENSHOTNAME)

if __name__ == '__main__':
    url = 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com'
    wd = open_browser()
    wd.maximize_window()
    login(url)
    applications()
    pop_up_clockin_page()
    switch_to_clockin_tab()  
    fillTemperature(bodyTemperature())
    try:
        wd.switch_to.alert.accept()
    except:
        pass
    # CheckHealth()
    # Go2School()
    # Submit()
    # clickConfirmButton()
    # ContinueAdding()
    ToRecords()
    if CheckUpdatedRecord():
        print("Yes")
    else:
        print("No")
    saveScreenshot("finalresult")
    wd.quit()

