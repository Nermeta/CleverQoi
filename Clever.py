
import os.path
import json
from zipfile import ZipFile
from os.path import basename
from AspireApi import *
from parentInfo import DemoReport
import uuid
import random
import paramiko
import var
import numpy




url = var.Cleverurl
username = var.Cleverusername
password = var.Cleverpassword
sy = var.Schoolyear
sy = int(sy)
sp = var.SpecNames
upload = var.Cleverupload
path = var.path + '\Clever\\'
zpath =var.path + '\Clever'





def Cleveras():
    df = Aspireas()
    df = df[['sourcedId', 'title', 'type', 'startDate', 'endDate', 'parent', 'schoolYear']]
    df["startDate"] = pd.to_datetime(df["startDate"], format='%Y-%m-%d')
    df["endDate"] = pd.to_datetime(df["endDate"], format='%Y-%m-%d')
    df.drop(df[df['schoolYear'] < sy].index, inplace = True)
    df = df.rename(columns={"parent": "parentSourcedId"})
    df['sourcedId'] = df['sourcedId'].str.replace('|','-',regex = True)
    df.to_csv( path + 'academicSessions.csv', index = False)




def Clevercl():
    asurl = var.Aspireurl
    rem = str(asurl).replace('https://','' )
    rem = rem + 'terms/'
    df = Aspirecl()
    df = df[['sourcedId', 'title', 'course.sourcedId', 'classCode', 'type', 'location', 'school.sourcedId', 'terms', 'periods']]
    df = df.rename(columns={'course.sourcedId':'courseSourcedId', 'type':'classType', 'school.sourcedId': 'schoolSourcedId', 'terms': 'termSourcedIds'})
    df = df.replace(rem,'', regex=True)
    df['termSourcedIds'] = df['termSourcedIds'].str.replace('|','-', regex=True)
    df.to_csv( path + 'classes.csv', index = False)




def Cleverco():
    df = Aspireco()
    df = df[['sourcedId', 'title', 'courseCode', 'org.sourcedId', 'subjects']]
    df.to_csv( path + 'courses.csv', index = False)




def Cleverdemo():
    df = Aspiredemo()
    df = df[['sourcedId','birthDate','sex', 'americanIndianOrAlaskaNative', 'asian', 'blackOrAfricanAmerican', 'nativeHawaiianOrOtherPacificIslander', 'white', 'demographicRaceTwoOrMoreRaces', 'hispanicOrLatinoEthnicity', 'countryOfBirthCode', 'stateOfBirthAbbreviation', 'publicSchoolResidenceStatus']]
    df.to_csv(path + 'demographics.csv', index = False)


def Cleveren():
    df = Aspireen()
    df = df[['sourcedId', 'class.sourcedId', 'school.sourcedId', 'user.sourcedId', 'role', 'beginDate', 'endDate']]
    df = df.rename(columns = {'class.sourcedId':'classSourcedId', 'school.sourcedId':'schoolSourcedId', 'user.sourcedId':'userSourcedId'})
    df['beginDate'] = pd.to_datetime(df['beginDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    df.to_csv(path + 'enrollments.csv', index = False)




def Cleverorg():
    df = Aspireo()
    df = df[['sourcedId', 'name', 'type', 'parent.sourcedId']]
    df = df.rename(columns={'parent.sourcedId':'parentSourcedId'})
    df.to_csv(path + 'orgs.csv', index = False)




def parent_info():
    
    link = DemoReport()
    df = pd.read_csv(link)
    rd = random.Random()
    seed = 52
    rd.seed(seed)
    
    df['Student ID'] = 'S' + df["Student ID"].astype(str)
    df1 = df[['Student ID', 'Contact1 Last Name','Contact1 First Name', 'Contact1 Relation', 'Contact1 Restraining Order', 
              'Contact1 Email Address', 'Contact1 Phone Number']]
    df2 = df[['Student ID','Contact2 Last Name','Contact2 First Name', 'Contact2 Relation', 'Contact2 Restraining Order', 
              'Contact2 Email Address', 'Contact2 Phone Number']]
    df3 = df[['Student ID','Contact3 Last Name','Contact3 First Name', 'Contact3 Relation', 'Contact3 Restraining Order', 
              'Contact3 Email Address', 'Contact3 Phone Number']]
    df4 = df[['Student ID','Contact4 Last Name','Contact4 First Name', 'Contact4 Relation', 'Contact4 Restraining Order', 
              'Contact4 Email Address', 'Contact4 Phone Number']]
    
    df1 = df1[df1['Contact1 Restraining Order'] == 'N']
    df1['role'] = 'parent'
    df1['Student ID'] =df1['Student ID'].astype('string')
    grouped = df1.groupby('Contact1 Phone Number')
    grouped = grouped['Student ID'].agg(lambda column: ','.join(column))
    df1 = df1.merge(grouped, how = 'right', on= 'Contact1 Phone Number')
    df1 = df1.drop_duplicates(subset='Student ID_y')
    df1 = df1.rename(columns={'Contact1 First Name':'givenName', 'Contact1 Last Name':'familyName', 'Contact1 Email Address':'email', 
                          'Contact1 Phone Number':'phone', 'Student ID_y': 'agentSourcedId'})
    df1 = df1[['givenName','familyName','email','phone','agentSourcedId','role']]
    
    df2 = df2[df2['Contact2 Restraining Order'] == 'N']
    df2['role'] = 'parent'
    df2['Student ID'] =df2['Student ID'].astype('string')
    grouped = df2.groupby('Contact2 Phone Number')
    grouped = grouped['Student ID'].agg(lambda column:','.join(column))
    df2 = df2.merge(grouped, how = 'right', on= 'Contact2 Phone Number')
    df2 = df2.drop_duplicates(subset='Student ID_y')
    df2 = df2.rename(columns={'Contact2 First Name':'givenName', 'Contact2 Last Name':'familyName', 'Contact2 Email Address':'email', 
                          'Contact2 Phone Number':'phone', 'Student ID_y': 'agentSourcedId'})
    df2 = df2[['givenName','familyName','email','phone','agentSourcedId','role']]
    
    df3 = df3[df3['Contact3 Restraining Order'] == 'N']
    df3['role'] = 'parent'
    df3['Student ID'] =df3['Student ID'].astype('string')
    grouped = df3.groupby('Contact3 Phone Number')
    grouped = grouped['Student ID'].agg(lambda column:','.join(column))
    df3 = df3.merge(grouped, how = 'right', on= 'Contact3 Phone Number')
    df3 = df3.drop_duplicates(subset='Student ID_y')
    df3 = df3.rename(columns={'Contact3 First Name':'givenName', 'Contact3 Last Name':'familyName', 'Contact3 Email Address':'email', 
                          'Contact3 Phone Number':'phone', 'Student ID_y': 'agentSourcedId'})
    df3 = df3[['givenName','familyName','email','phone','agentSourcedId','role']]
    
    df4 = df4[df4['Contact4 Restraining Order'] == 'N']
    df4['role'] = 'parent'
    df4['Student ID'] =df4['Student ID'].astype('string')
    grouped = df4.groupby('Contact4 Phone Number')
    grouped = grouped['Student ID'].agg(lambda column:','.join(column))
    df4 = df4.merge(grouped, how = 'right', on= 'Contact4 Phone Number')
    df4 = df4.drop_duplicates(subset='Student ID_y')
    df4 = df4.rename(columns={'Contact4 First Name':'givenName', 'Contact4 Last Name':'familyName', 'Contact4 Email Address':'email', 
                          'Contact4 Phone Number':'phone', 'Student ID_y': 'agentSourcedId'})
    df4 = df4[['givenName','familyName','email','phone','agentSourcedId','role']]
    
    parent = pd.concat([df1,df2,df3,df4])
    
    parent['sourcedId'] = parent.apply(lambda _: uuid.UUID(int=rd.getrandbits(128)), axis=1)
    parent['username'] = parent['sourcedId']
    
    parent['sourcedId'] = parent.apply(lambda _: uuid.UUID(int=rd.getrandbits(128)), axis=1)
    parent['username'] = parent['sourcedId']
    parent['phone'] = parent['phone'].astype(numpy.int64)


    return parent



def Cleverdemo():
    df = Aspiredemo()
    df = df[['sourcedId','status','dateLastModified','birthDate','sex','americanIndianOrAlaskaNative','asian','blackOrAfricanAmerican',
        "white",'demographicRaceTwoOrMoreRaces','hispanicOrLatinoEthnicity','countryOfBirthCode','stateOfBirthAbbreviation', 'cityOfBirth',
        'publicSchoolResidenceStatus']]
    df['birthDate'] = pd.to_datetime(df['birthDate'])
    df['sex'] = df['sex'].str.lower()
    df['dateLastModified']  = '2000-01-01'
    df.to_csv(path +'demographics.csv', index = False)





def Clevermani():
    data = [['manifest.version', '1.0'], ['oneroster.version', '1.1'], ['file.academicSessions', 'bulk'], ['file.categories', 'absent'], 
        ['file.classes', 'bulk'], ['file.classResources', 'absent'], ['file.courses', 'bulk'], ['file.courseResources', 'absent'], 
        ['file.demographics', 'bulk'], ['file.enrollments', 'bulk'], ['file.lineItems', 'absent'], ['file.orgs','bulk'], 
        ['file.resources', 'absent'], ['file.results', 'absent'], ['file.users', 'bulk'], ['source.systemName', 'Aspire'] ]

    df = pd.DataFrame(data, columns = ['propertyName', 'value'])
    df.to_csv(path +'manifest.csv', index = False)




def Cleverus():
    
    df1 = parent_info()
    df = Aspireus()
    spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–", " "]
    
    tmp = df1.assign(agentId=df1['agentSourcedId'].str.split(',')).explode('agentSourcedId').set_index('agentSourcedId')['sourcedId'].astype(str).groupby(level=0).agg(list).str.join(',').reset_index()
    tmp = tmp.assign(agentSourcedId=tmp.agentSourcedId.str.split(",")).explode('agentSourcedId')
    df['sourcedId'] = df['sourcedId'].astype(str)
    
    df3 = df.merge(tmp, left_on='sourcedId', right_on='agentSourcedId').drop('agentSourcedId',axis=1).rename({'sourcedId_x':'sourcedId', 'sourcedId_y':'agentSourcedId', 'orgs':'orgSourcedIds'},axis=1)
    
    df1 = pd.concat([df3, df1], ignore_index=True)
    df = df.loc[df['role'] == 'teacher']
    df['orgSourcedId'] = df['orgs']
    df = pd.concat([df, df1], ignore_index=True)
    df = df.loc[df['role'] == 'teacher']
    df['orgSourcedId'] = df['orgs']
    df = pd.concat([df, df1], ignore_index=True)
    
    df.loc[df['role'] == 'student', 'givenName'] = df['metadata.preferredFirstName']
    df.loc[df['role'] == 'student', 'familyName'] = df['metadata.preferredLastName']
    df.loc[df['role'] == 'parent', 'orgSourcedIds'] = 'LEA'
    df.loc[df['role'] == 'parent', 'enabledUser'] = 'True'
    
    df = df.rename(columns={'agentSourcedId': 'agentSourcedIds'})
    
    for char in spec_chars:
        df['metadata.preferredFirstName'] = df['metadata.preferredFirstName'].str.replace(char, '', regex=True)
        df['metadata.preferredLastName'] = df['metadata.preferredLastName'].str.replace(char, '', regex=True)
        
    df.loc[df['role'] == 'student', 'email'] = df['metadata.preferredFirstName'] +"." + df['metadata.preferredLastName'] + '@saadragons.org'
    df.loc[df['role'] == 'teacher', 'email'] = df['givenName'].str[0] + df['familyName'] + '@saacharter.org'
    
    for k, i in sp.items():
        df.loc[df['sourcedId'] == k, 'email'] = i
        
    df['orgs'] = df['orgs'].str.replace('syracuse.usoe-dcs.org/api/OneRoster/v1p1/orgs/', '', regex=True)
    df = df[['sourcedId','enabledUser','orgSourcedIds','role','username','givenName','familyName','middleName','identifier','email','phone','agentSourcedIds',
             'grades','metadata.stateId']]
    
    
   
    df.to_csv(path +'users.csv', index = False)




def Cleverupload():
    
    CHECK_FOLDER = os.path.isdir(zpath)
    if not CHECK_FOLDER:
        os.makedirs(zpath)
    files = ['academicSessions.csv','classes.csv','courses.csv', 'demographics.csv','enrollments.csv','manifest.csv','orgs.csv','users.csv']
    print('Creating Users')
    Cleverus()
    print('Creating Manifest')
    Clevermani()
    print('Creating Academic Sessions')
    Cleveras()
    print('Creating Classes')
    Clevercl()
    print('Creating Courses')
    Cleverco()
    print('Creating Enrollments')
    Cleveren()
    print('Creating Organizations')
    Cleverorg()
    print('Creating Demographics')
    Cleverdemo()
    
    print('Creating Zip File and Uploading')
    os.chdir(zpath)
    zipObj = ZipFile('oneroster11.zip', 'w')
    for csv in files:
        zipObj.write(csv)
    zipObj.close()
    
    try:
        ssh_client=paramiko.SSHClient()
        ssh_client.connect(hostname=url, username=username, password=password)
    except:
        ssh_client =paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=url, username=username, password=password)
    
    ftp_client=ssh_client.open_sftp()
    ftp_client.chdir(upload)
    ftp_client.put(r'oneroster11.zip',r'oneroster11.zip')
    ftp_client.close()
          
    print("Upload Complete")




