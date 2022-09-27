
import paramiko
import var
import os.path
from zipfile import ZipFile
from os.path import basename
import json
from AspireApi import *




asurl = var.Aspireurl
sp = var.SpecNames
Hostname = var.HmhHostname
Username = var.HmhUsername
Password = var.HmhPassword



path = var.path + '\HMH\\'
zpath =var.path + '\HMH'




def Hmhas():
    df = Aspireas()
    df= df[['sourcedId','status','dateLastModified','title','startDate','endDate','parent','schoolYear']]
    df = df.rename(columns={'parent':'parentSourcedId'})
    df.to_csv( path + 'academicSessions.csv', index = False)




def Hmhcl():   
    df = Aspirecl()
    df = df.loc[df["school.sourcedId"] == '100']
    df = df[df["title"].str.contains("Grade|Kindergarten")==True]
    rem = str(asurl).replace('https://','' )
    rem = rem + 'terms/'

    df = df[['sourcedId','status','dateLastModified','title','grades','course.sourcedId','classCode',
         'course.type','location','school.sourcedId','terms','subjects','subjectCodes','periods']]
    df.drop_duplicates(subset ="sourcedId", keep = "first", inplace = True)
    df = df.replace(rem,'', regex=True)
    df['terms'] = df['terms'].str.replace('|','-', regex=True)
    df['grades'] = df['grades'].str.replace('K','KG')
    df = df.rename(columns={'course.sourcedId':'courseSourcedId','course.type':'classType',
                            'school.sourcedId':'schoolSourcedId', 'terms':'termSourcedIds'})
    df.to_csv(path + 'classes.csv', index = False)





def Hmhco():   
    df = Aspireco()
    df = df[df["title"].str.contains("Grade")==True]
    df = df.loc[df["org.sourcedId"] == '100']
    df = df[['sourcedId','status','dateLastModified','schoolYear.sourcedId','title','courseCode','grades','org.sourcedId','subjects']]
    df['subjectCodes'] = ""
    df = df.rename(columns={'schoolYear.sourcedId':'schoolYearSourcedId','org.sourcedId':'orgSourcedId'})
    df.to_csv(path + 'courses.csv', index = False)



def Hmhdemo():
    df = Aspiredemo()
    df = df[['sourcedId','status','dateLastModified','birthDate','sex','americanIndianOrAlaskaNative','asian','blackOrAfricanAmerican',
        "white",'demographicRaceTwoOrMoreRaces','hispanicOrLatinoEthnicity','countryOfBirthCode','stateOfBirthAbbreviation', 'cityOfBirth',
        'publicSchoolResidenceStatus']]
    df.to_csv(path + 'demographics.csv', index = False)



def Hmhen():
    df= Aspireen()
    df2 = Aspirecl()
    df2 = df2.loc[df2["school.sourcedId"] == '100']
    df2 = df2[df2["title"].str.contains("Grade|Kindergarten")==True]
    df = df.merge(df2,left_on="class.sourcedId",right_on='sourcedId')
    df['sourcedId_x'] = df['sourcedId_x'].str.replace('|','-', regex=True)
    df= df.rename(columns = {'sourcedId_x': 'sourcedId','status_x':'status','dateLastModified_x':'dateLastModified', 
                         'class.sourcedId':'classSourcedId', 'school.sourcedId_x':'schoolSourcedId','user.sourcedId':'userSourcedId'})
    df.drop_duplicates(subset ="sourcedId", keep = "first", inplace = True)
        
    df['beginDate'] = pd.to_datetime(df['beginDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    df = df[['sourcedId','status','dateLastModified','classSourcedId','schoolSourcedId','userSourcedId','role','primary','beginDate','endDate']]
    df.to_csv(path + 'enrollments.csv', index = False)
    return df



def Hmhman():
    data = [['manifest.version', "1.0"], ['oneroster.version', "1.1"], ['file.academicSessions', "bulk"] , ['file.classes', "bulk"] , ['file.courses', "bulk"] , ['file.demographics', "bulk"] , ['file.enrollments', "bulk"], ['file.orgs', "bulk"], 
        ['file.users', "bulk"] , ['file.catagories', "absent"], ['file.classResources', "absent"], ['file.courseResources', "absent"] , ['file.lineItems', "absent"], ['file.resources', "absent"], ['file.results', "absent"]]
    manifest =  pd.DataFrame(data, columns = ['propertyName', 'value'])
    manifest.to_csv(path + "manifest.csv",mode='w',index=False)



def Hmhorg():
    df = Aspireo()
    df = df[['sourcedId','status','dateLastModified','name','type','identifier','parent.sourcedId']]
    df = df.rename(columns={'parent.sourcedId':'parentSourcedId'})
    df.to_csv(path + 'orgs.csv', index = False)




def Hmhus():
    df = Aspireus()
    df1 = Hmhen()
    df3 = Aspireus()
    
    df['grades'] = df['grades'].str.replace('K','0')
    df['grades'] = pd.to_numeric(df['grades'])
    rem = str(asurl).replace('https://','' )
    rem = rem + 'orgs/'
    df['orgs'] = df.replace(rem,'', regex=True)['orgs'].astype(int)
    df3['orgs'] = 100
    df = df[df['orgs'] == 100]
    dfs = df[df['grades'] < 7]
    
    df1 = df1.loc[df1['role'] == 'teacher']
    df1.drop_duplicates(subset ="sourcedId", keep = "first")
    df1 = df1['userSourcedId']
    a = df1.tolist()
    df2 = df3[df3.sourcedId.isin(a)]

    df = pd.concat([dfs,df2])
    
    spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–", " "]
    for char in spec_chars:
        df['metadata.preferredFirstName'] = df['metadata.preferredFirstName'].str.replace(char, '', regex=True)
        df['metadata.preferredLastName'] = df['metadata.preferredLastName'].str.replace(char, '', regex=True)
    
    df.loc[df['role'] == 'student', 'email'] = df['metadata.preferredFirstName'] +"." + df['metadata.preferredLastName'] + '@saadragons.org'
    df.loc[df['role'] == 'teacher', 'email'] = df['givenName'].str[0] + df['familyName'] + '@saacharter.org'
    for k, i in sp.items():
        df.loc[df['identifier'] == k, 'email'] = i
    df = df.rename(columns={'orgs':'orgSourcedIds'})
    df.insert(1,'agentSourcedIds','',False)
    df.insert(1,'password','',False)
    df['grades'] = "IT-Other"
    
    df= df[['sourcedId','status','dateLastModified','enabledUser','orgSourcedIds','role','username','userIds','givenName','familyName','middleName',
        'identifier', 'email','sms','phone','agentSourcedIds','grades','password']]
    df.to_csv(path + 'users.csv', index = False)



def HmhZip():
    print("Creating Academic Sessions")
    Hmhas()
    print("Creating Classes")
    Hmhcl()
    print("Creating Courses")
    Hmhco()
    print("Creating Demographics")
    Hmhdemo()
    print("Creating Manifest")
    Hmhman()
    print("Creating Organazations")
    Hmhorg()
    print("Creating Users")
    Hmhus()
    files = ['academicSessions.csv','classes.csv','courses.csv', 'demographics.csv','enrollments.csv','manifest.csv','orgs.csv','users.csv']
    print('Zipping and Uploading')
    os.chdir(zpath)
    zipObj = ZipFile('oneroster11.zip', 'w')
    for csv in files:
        zipObj.write(csv)
    zipObj.close()
   




def Hmhupload():
    CHECK_FOLDER = os.path.isdir(zpath)
    if not CHECK_FOLDER:
        os.makedirs(zpath)
        
    HmhZip()
    try:
        ssh_client=paramiko.SSHClient()
        ssh_client.connect(hostname=Hostname, username=Username, password=Password)
    except:
        ssh_client =paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=Hostname, username=Username, password=Password)
    
    ftp_client=ssh_client.open_sftp()
    ftp_client.put(r'oneroster11.zip',r'oneroster11.zip')
    ftp_client.close()
    print('Done')







