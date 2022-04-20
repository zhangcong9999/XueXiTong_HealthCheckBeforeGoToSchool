import configparser
"""
To keep from committing the personal information to the github, the personinf.ini of the author is stored in a different path.
By default, the codes below can only get the dummy information in the project directory.
"""
class getConfigInformation:
    def __init__(self, inifilepath:str =  r"personinf.ini"): 
        """The inifilepath could be a customized path of the personinf.ini"""       
        self.config = configparser.ConfigParser()
        self.config.read(inifilepath)

    def getPersonalInformation(self):
        """The personal information is stored in another directory so that 
        the author's information won't be committed to the git hub.
        username is the user ID of the 超星学习通.
        password is the password of the 超星学习通."""        
        username:str = self.config.get("USER", 'username')
        password:str = self.config.get("USER", 'password')
        return username, password

    def getEmailConfig(self):
        """The personal information is stored in another directory so that 
        the author's information won't be committed to the git hub.
        emailhost is the smtp address for sending email. eg: smtp.126.com
        senderEmailAddr is the email address of the sender. eg: sender@126.com.
        authentication: Usually, the email server doesn't allow the 3rd party client to send email with the email password.
                        The authentication is specially provided the 3rd party client to send email without email password."""        
        emailhost:str       = self.config.get("EMAILCONFIG", 'emailhost')
        senderEmailAddr:str = self.config.get("EMAILCONFIG", 'senderEmailAddr')
        authentication:str  = self.config.get("EMAILCONFIG", 'authentication')
        return emailhost, senderEmailAddr, authentication

    def GetDestinationEmails(self):
        """The personal information is stored in another directory so that 
        the author's information won't be committed to the git hub.
        emailhost is the smtp address for sending email. eg: smtp.126.com
        senderEmailAddr is the email address of the sender. eg: sender@126.com.
        authentication: Usually, the email server doesn't allow the 3rd party client to send email with the email password.
                        The authentication is specially provided the 3rd party client to send email without email password."""
        SECTION = "RECEIVEREMAILS"
        RECEIVER_INDEXES = self.config.options(SECTION)
        return [self.config.get(SECTION, receiver) for receiver in RECEIVER_INDEXES ]


if __name__ == "__main__":    
    inifilepath = r"C:\Users\Public\personinf.ini"    
    userID, Passcode = getConfigInformation(inifilepath).getPersonalInformation()
    emailhost, senderEmailAddr,authentication = getConfigInformation(inifilepath).getEmailConfig()
    print("username:\t", userID , "\npassword:\t", Passcode)
    print("email host:\t", emailhost,"\nEmail Address of the sender:\t\t", senderEmailAddr,"\nauthentication key of the sender email:\t", authentication)    
    emails = (getConfigInformation(inifilepath).GetDestinationEmails())
    print(emails)