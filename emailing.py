# import sys, os
# o_path = os.getcwd()
# sys.path.append(o_path)
# sys.path.append(o_path+r'\hyrobot')
# from hyrobot.common import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import time
# from webui import GSTORE # GSTORE was not initialized when it was imported here.
from readpersonalinfo import getConfigInformation

''' 
To keep from exposing author's personal information, the author puts his personinf.ini file in the following varibles "inifilepath".
If anybody else wants to use his own information in the personinf.ini provided in the project folder, either way below works:
    1. change the path to r"personinf.ini"
    2. remove both "infifilepath" in the function send_mail().
'''
inifilepath = r"C:\Users\Public\personinf.ini"
inifilepath = r"personinf.ini"

def send_mail(subject1= 'name1', receivers:list = getConfigInformation(inifilepath).GetDestinationEmails()):
    '''subject1: It will be the information in the subject of the sent mail. GSTORE[subject1] is the result of clocking-in (True: success & False: failed).
    receivers: By default, it is list that contains all the destination emails from the file named peroninf.ini.
                User may give their own destination emails, like ["receiver1@126.com", "receiver2@163.com", "receiver3@gmail.com"]'''
    
    email_host, sender, password = getConfigInformation(inifilepath).getEmailConfig()
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ';'.join(receivers)
    msg['Subject'] = subject1  + " " + now

    mail_msg = '''
<p>\n\t 这是“学习通”体温打卡结果.</p>
<p>\n\t 自动邮件，无需回复！</p>
<p><a href ="https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com">填写健康打卡.</a></p>
<p>结果截图如下: </p>
<p><img src ="cid:image1"></p>
    '''
    submitSuccessfully = "===>     成功!</p>"
    submitFailed = "===>     失败!</p>"

    from webui import GSTORE # The GSTORE was initialized fully before imported here.
    if GSTORE[subject1]:
        mail_msg= "<p>\n\t" + subject1 + submitSuccessfully +"\n" + mail_msg
    else:
        mail_msg= "<p>\n\t" + subject1 + submitFailed +"\n" + mail_msg
    msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    #Define that the picture is in the current directory.
    fp1 = open("pic\\" + subject1 + r'.PNG','rb')
    msgImage1 = MIMEImage(fp1.read())
    fp1.close()
    # Define the picture ID. Displayed in the content.
    msgImage1.add_header('Content-ID', '<image1>')
    msg.attach(msgImage1)
 


    try:
        ret= True        
        server = smtplib.SMTP(email_host)
        server.login(sender, password)
        server.sendmail(sender, receivers, msg.as_string())
        server.quit()
    except Exception as e:
        ret = False
        print(e)
    return ret

if __name__ == '__main__':
    # If the email was sent successfully, the value will be True, else it will be False.

    
    subject1 = 'finalresult'
    # send_mail(subject)
    
    ret1 = send_mail( subject1)
    if ret1:
        print("Mail 1 邮件发送成功！")
    else:
        print("Mail 1 邮件发送失败！")