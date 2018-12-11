# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import sys
import os
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json
import datetime
import numpy as np

class MyspiderbotSpider(scrapy.Spider):
        
    name = 'mySpiderBot'
    allowed_domains = ['http://mca.gov.in']
    start_urls = ['http://mca.gov.in/mcafoportal/companiesRegReport.do']
    errorFileName="error.log"
    dataFileName="Company_Registered_in_Last_30days_"+datetime.datetime.now().strftime("%d_%m_%h")+".xlsx"
    dataFileLocation="/home/digiapt/Desktop/mca_gov_in/mca_gov_in/spiders/fetchedFile/"+dataFileName
    successFileName="success.log"
    
    schemaColumns={
        "COMPANY NAME":"name",
        "LIMITED LIABILITY PARTNERSHIP NAME":"name",
        "FOREIGN LIMITED LIABILITY PARTNERSHIP":"name",
        "CIN":"identityNumber",
        "FCRN":"identityNumber",
        "LLPIN":"identityNumber",
        "FLLPIN":"identityNumber",
        "COUNTRY":"country",
        "COUNTRY OF INCORPORATION":"country",
        "DATE OF INCORPORATION":"dateOfIncorporation",
        "DATE OF REGISTRATION":"dateOfIncorporation",
        "STATE":"state",
        "STATE OF PRINCIPAL PLACE OF BUSINESS IN INDIA":"state",
        "ROC":"ROC",
        "CATEGORY":"category",
        "SUB CATEGORY":"subCategory",
        "CLASS":"class",
        "AUTHORIZED_CAPITAL":"authorizedCapital",
        "PAID CAPITAL":"paidCapital",
        "NUMBER OF PARTNERS":"numberOfPartners",
        "NUMBER OF MEMBERS (Applicable only in case of Co. without share Capital)":"numberOfPartners",
        "NUMBER OF DESIGNATED PARTNERS":"numberOfDesignatedParters",
        "ACTIVITY DESCRIPTION":"activityDiscription",
        "ACTIVITY_DESCRIPTION":"activityDiscription",
        "REGISTERED_OFFICE_ADDRESS":"officeAddressInIndia",
        "FOREIGN COMPANY PRESENT ADDRESS IN INDIA":"officeAddressInIndia",
        "FOREIGN OFFICE ADDRESS":"officeAddressInForeign",
        "TOTAL OBLIGATION OF CONTRIBUTION":"totalObligationOfContribution",
        "TYPE OF OFFICE":"typeOfOffice"}
    schema2sheet={
        "name":0,
        "identityNumber" :0,
        "country":0,
        "dateOfIncorporation":0,
        "state":0,
        "ROC":0,
        "category":0,
        "subCategory":0,
        "class":0,
        "authorizedCapital":0,
        "paidCapital":0,
        "numberOfPartners":0,
        "numberOfDesignatedParters":0,
        "activityDiscription":0,
        "officeAddressInIndia":0,
        "officeAddressInForeign":0,
        "totalObligationOfContribution":0,
        "typeOfOffice":0
        }

    def createDataList(self,df,sheet,dataList,sheetOne,sheetTwo,sheetThree,sheetFour):
        if sheet==sheetOne: #"Indian Companies Registered"
            columns=df.columns.values
            entity={}
            incorporationData={}
            emptyField={}
            registrationData={"registrationData":"null"}
            commonCol={}
            for col in columns:
                commonCol[self.schemaColumns[col]]=0
            for index in range(df.shape[0]):
                tmp={}
                tmp1={}
                tmp2={}
                tmp3={}
                #tmp['isCompany']=True;tmp['isLLP']=False;tmp['isForeign']=False;tmp['isDomestic']=True;tmp['identityLabel']="CIN"
                tmp1['isCompany']=True;tmp1['isLLP']=False;tmp1['isForeign']=False;tmp1['isDomestic']=True;
                tmp1['identityLabel']="CIN"
                tmp1['type']="incorporation"
                row=df.iloc[index]
                for col in columns:
                    if col=="COMPANY NAME" or  col == "ACTIVITY_DESCRIPTION" or col=="ROC" or col=="STATE" or col == "CIN" or col == "DATE OF INCORPORATION" or col == "REGISTERED_OFFICE_ADDRESS" :
                        #tmp[schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                        tmp1[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                    elif col == "CATEGORY" or col == "SUB CATEGORY" or col == "CLASS" or col == "AUTHORIZED_CAPITAL" or col == "PAID CAPITAL" or col is "NUMBER OF MEMBERS":
                        tmp2[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
            
                for unInsertedKey in self.schema2sheet.keys():
                    if unInsertedKey not in commonCol:
                        #tmp[unInsertedKey]="null"
                        tmp3[unInsertedKey]="null"
                entity['entity']=tmp1
                incorporationData['incorporationData']=tmp2
                emptyField['emptyField']=tmp3
                tmp={**entity,**incorporationData,**emptyField,**registrationData}
                dataList.append(tmp)
            
            
            
            
            
        
        elif sheet==sheetTwo: #Foreign Companies Registered
            columns=df.columns.values
            commonCol={}
            entity={}
            registrationData={}
            incorporationData={"incorporationData":"null"}
            emptyField={}
            for col in columns:
                commonCol[self.schemaColumns[col]]=0
            for index in range(df.shape[0]):
                tmp={}
                tmp1={}
                tmp2={}
                tmp3={}
                tmp1['isCompany']=True;tmp1['isLLP']=False;tmp1['isForeign']=True;tmp1['isDomestic']=False;
                tmp1['identityLabel']="FCRN"
                tmp1['type']="registration"
                tmp1['type']="India"
                tmp1['vehicle']="company"
                tmp['isCompany']=True;tmp['isLLP']=False;tmp['isForeign']=True;tmp['isDomestic']=False;tmp['identityLabel']="FCRN"
                row=df.iloc[index]
                for col in columns:
                    if col=="COMPANY NAME" or col == "ACTIVITY_DESCRIPTION" or col=="STATE" or col=="ROC" or col == "FCRN" or col == "DATE OF REGISTRATION" or  col =="FOREIGN COMPANY PRESENT ADDRESS IN INDIA" or col == "REGISTERED_OFFICE_ADDRESS" :
                        #tmp[schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                        tmp1[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                    elif col == "TYPE OF OFFICE" or col == "COUNTRY OF INCORPORATION" or col == "FOREIGN OFFICE ADDRESS":
                        tmp2[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                
                    #tmp[schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                
                
                for unInsertedKey in self.schema2sheet.keys():
                    if unInsertedKey not in commonCol:
                        if unInsertedKey=="COUNTRY":continue
                        #tmp[unInsertedKey]="null"
                        tmp3[unInsertedKey]="null"
                entity['entity']=tmp1
                registrationData['registrationData']=tmp2
                emptyField['emptyField']=tmp3
                tmp={**entity,**registrationData,**incorporationData,**emptyField}
                dataList.append(tmp)
            
        elif sheet==sheetThree: #LLP Registered
            columns=df.columns.values
            commonCol={}
            for col in columns:
                    commonCol[self.schemaColumns[col]]=0
            for index in range(df.shape[0]):
                tmp={}
                tmp['isCompany']=False;tmp['isLLP']=True;tmp['vehicle']="LLP";tmp['isForeign']=False;tmp['isDomestic']=True;tmp['identityLabel']="LLPIN"
                row=df.iloc[index]
                for col in columns:
                    tmp[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                for unInsertedKey in self.schema2sheet.keys():
                    if unInsertedKey not in commonCol:
                        tmp[unInsertedKey]="null"
                dataList.append(tmp)        
        
        elif sheet==sheetFour: #Foreign LLP Registered
            columns=df.columns.values
            commonCol={}
            for col in columns:
                    commonCol[self.schemaColumns[col]]=0
            for index in range(df.shape[0]):
                tmp={}
                tmp['isCompany']=False;tmp['isLLP']=True;tmp['LLP']="company";tmp['isForeign']=True;tmp['isDomestic']=False;tmp['identityLabel']="FLLPIN"
                try:
                    row=df.iloc[index]
                    for col in columns:
                        tmp[self.schemaColumns[col]]=row[col] if row[col] is not pd.np.nan else "null"
                    for unInsertedKey in self.schema2sheet.keys():
                        if unInsertedKey not in commonCol:
                            tmp[unInsertedKey]="null"
                    dataList.append(tmp)
                except Exception as e:
                    pass
        return dataList
    
    
    
    
    def readAndInsert(self,fileLocation):
        excelFile=pd.ExcelFile(fileLocation)

    def errorback(self,res):
        with open(self.errorFileName,"a") as fp:
            fp.write(datetime.datetime.now().strftime("%d-%m-%h (%H:%M:%S)")+" - "+str(res)+"\r\n")
        print("please check error log file for more information")
        
    def callback(self,res):
        content=res.body
        with open(self.dataFileLocation,"wb") as fp:
            fp.write(content)
        print("done writing")
        dataList=[]
        excelFile=pd.ExcelFile(self.dataFileLocation)
        sheetOne="Indian Companies Registered"
        sheetTwo="Foreign Companies Registered"
        sheetThree="LLP Registered"
        sheetFour="Foreign LLP Registered"
        for sheet in ["Indian Companies Registered","Foreign Companies Registered"]:
            df=pd.read_excel(excelFile,sheet_name=sheet)
            df.columns=df.iloc[0]
            df.drop(0,inplace=True)
            dataList=self.createDataList(df,sheet,dataList,sheetOne,sheetTwo,sheetThree,sheetFour)
        meta={}
        meta["dateCreated"]=datetime.datetime.now().strftime("%d/%m/%y")
        meta["source"]="http://mca.gov.in"
        meta["sourceURL"]="http://mca.gov.in/mcafoportal/companiesRegReport.do"
        dataList.append({"metaData":meta})
        mongoClient=MongoClient()
        db=mongoClient.mcaGovIn
        collection=db.companies
        
        try:
            collection.insert_many(dataList)
            with open(self.successFileName,"a") as fp:
                fp.write(datetime.datetime.now().strftime("%d-%m-%h (%H:%M:%S)")+" - "+" Insertion Successful, Successfully Crawled"+"\r\n")
            print("**********************************Successfully Crawled*******************************************")
        except Exception as e:
            with open(self.errorFileName,"a") as fp:
                fp.write(datetime.datetime.now().strftime("%d-%m-%h (%H:%M:%S)")+" - "+" Insertion Failed: - "+str(e)+"\r\n")
            print("**********************************Insertion Failed, Please check error log for more information*******************************************")
        




    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0','Cache-Control': 'max-age=0','referer':'mca.gov.in'}
        for url in self.start_urls:
            yield scrapy.Request(url,headers=headers,errback=self.errorback,callback=self.callback,dont_filter=True)