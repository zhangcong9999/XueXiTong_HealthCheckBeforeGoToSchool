import pandas as pd
from datetime import date as dt



# Read the excel file and remove the blank rows.
def spreadsheet():
    DATE = dt.today().toordinal()
    # print("Read the exceptions of the special cases.")
    # print("Date today: ", DATE)
    # print("Date type: ", type(DATE))
    
    df = pd.read_excel("Exceptions.xlsx",  index_col=None, sheet_name='exceptions') # dtype=str convert the IP value from float to string. 
    # if GSTORE['network'] == 'vpn':
    #     df = df.loc[df['VPN'] == "Y"]
    # elif GSTORE['network'] == 'lab':
    #     df = df.loc[df['LAB'] == "Y"]
    df = df.loc[ df['duration'] > 0]
    return df

# Return the filtered table as the object of a dataframe.
def DateCheckResult(DATE_TODAY = dt.today()): 
    '''The args should be a date at dt(yyyy,m,d). eg: dt(2022, 4, 16).
    According to the exceptions in the excel file named "exceptions.xlsx, return string "yes" for "go to school" or "no" for not "go to school".
    If the args doesn't meet the condition of the exceptions, the regular rule will be applied:
        Monday to Friday => return "yes" for "go to school";
        Saturday to Sunday => return "no" for not "go to school".'''
    # Filtering by the network and remove the useless columns.
    DATE_START, DATE_END, GO_TO_SCHOOL = "", "", ""
    # DATE_TODAY = dt.today()
    DATE_TODAY_VAL:int = DATE_TODAY.toordinal()
    # print("value of the date today: ", DATE_TODAY_VAL)
    # DATE_TODAY_VAL_VAL = 738278
    df = spreadsheet()
    # df = df[['Name when binding IP in Router', 'IP for router', 'MAC']]     # Remove other columns keeping the ones in the list.
    # df = df.loc[df['IP for router']]
    df = df[['date_start', 'date_end', 'Go_To_School']]
    for item in range(len(df)):
        DATE_START      = df.iloc[item][0].toordinal()
        DATE_END        = df.iloc[item][1].toordinal()
        GO_TO_SCHOOL    = df.iloc[item][2]
        # print("DATE_START type:", type(DATE_START), DATE_START)
        # print("DATE_END type:", type(DATE_END), DATE_END)
        if DATE_START <= DATE_TODAY_VAL <= DATE_END:
            break
        else:
            GO_TO_SCHOOL = RegularResult(DATE_TODAY)
    return GO_TO_SCHOOL

def RegularResult(DATE = dt.today()):
    '''The args should be a date at dt(yyyy,m,d). eg: dt(2022, 4, 16).
    According to the weekday number:
    Monday - Friday: values are 1 - 5 accordingly. ==> return string "yes" ==> means go to school.
    Saturday - Suday: values are 6 - 7 accordingly. ==> return string "no" ==> means not go to school.
    '''
    result = ""
    # print("DATE type: ", type(DATE))
    try:
        DATE_VAL = dt.isoweekday(DATE) # isoweekday(): From Monday to Friday -> 1 ~ 5 and Saturday to Sunday -> 6 ~ 7.
        # print(DATE_VAL)
        if 0 < DATE_VAL <=5:
            result = "yes"
        elif 6 <= DATE_VAL <= 7:
            result = "no"
    except:
        result = "Invalid date!"
    return result


if __name__ == "__main__":
    # GSTORE['network'] = 'lab'
    # table = IP_MAC_Table()
    # print(table)
    
    # for i in range(0, len(table)):
    #     print(table.iloc[i][0], table.iloc[i][1], table.iloc[i][2])
    YEAR = 2022
    MON = 10
    DAY = 16
    excel = DateCheckResult(dt(YEAR, MON, DAY))
    print(excel)
