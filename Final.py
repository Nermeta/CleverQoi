
from HMH import Hmhupload
from Clever import Cleverupload
import os
from var import config



try:
    print("Sync in Progress")
    print("Uploading to HMH")
    Hmhupload()
    print("HMH Upload Completed, Now Uploading to Clever")
    os.chdir(config)
    Cleverupload()
    print("Clever Upload Completed. Now Exiting")
except:
    print("An Error Has Occured please check that all variables are correct in the var.py file and that the ChromeDriver.exe is up to date and then try again")





