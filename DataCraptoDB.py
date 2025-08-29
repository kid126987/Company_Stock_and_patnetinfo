from sidepro.DataCrap import * 
from datetime import datetime
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
from datetime import date
FD = finmind_data()
PD = patent_data()

#公司檢索專利表格，以十間公司為範例
stockbasedata = pd.DataFrame({
   'StockCode' : ['2330','2317','2454','2308','2382','2891','2881','3711','2882','2412'],
   'companyname' : ['TAIWAN SEMICONDUCTOR MANUFACTURING COMPANY',
                    'HON HAI PRECISION INDUSTRY CO',
                    'MEDIATEK INC',
                    'Delta Electronics',
                    'QUANTA COMPUTER',
                    '',
                    '',
                    '',
                    '',
                    'Chunghwa Telecom Co., Ltd.']
   })

#透過Findmind抓取各公司的DATA後，並針對預計要呈現的表格進行資料型態轉換
def DBStockData(enddate :str):
   #以程式運行的當下為基準點，回推抓取五年的資料
   startdate = enddate.replace(enddate.split('-')[0],str(int(enddate.split('-')[0])-5))
   stock_price_info_fin = None
   stock_revene_info_fin = None
   stock_Dividend_info_fin = None
   stock_PER_info_fin = None
   
   for i in stockbasedata['StockCode']:
      stock_price_info = FD.stock_price_info(i,start_date=startdate,end_date=enddate)
      stock_revene_info = FD.stock_revene_info(i,start_date=startdate,end_date=enddate)
      stock_Dividend_info = FD.stock_Dividend_info(i,start_date=startdate,end_date=enddate)
      stock_PER_info = FD.stock_PER_info(i,start_date=startdate,end_date=enddate)
      
      
      if stock_price_info_fin is None:
         stock_price_info_fin = stock_price_info
         stock_revene_info_fin = stock_revene_info
         stock_Dividend_info_fin = stock_Dividend_info
         stock_PER_info_fin = stock_PER_info
         
      else:
         stock_price_info_fin = pd.concat([stock_price_info_fin,stock_price_info])
         stock_revene_info_fin = pd.concat([stock_revene_info_fin,stock_revene_info])   
         stock_Dividend_info_fin = pd.concat([stock_Dividend_info_fin,stock_Dividend_info])
         stock_PER_info_fin = pd.concat([stock_PER_info_fin,stock_PER_info])
   
   stock_Dividend_info_fin = stock_Dividend_info_fin.loc[stock_Dividend_info_fin['CashDividendPaymentDate']!='']
   #股票股價資訊
   stock_price_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_price_info_fin['stock_id'],dtype='str'),
      'StockDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_price_info_fin['date']],
      'StockClose' : pd.Series(stock_price_info_fin['close'],dtype='float'),
      'RSV' : pd.Series(stock_price_info_fin['RSV_value'],dtype='float'),
      'KValue' : pd.Series(stock_price_info_fin['K_value'],dtype='float'),
      'DValue' : pd.Series(stock_price_info_fin['D_value'],dtype='float')
      }).reset_index(drop=True)
   #股票收益資訊
   stock_revene_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_revene_info_fin['stock_id'],dtype='str'),
      'RevenueYear' : pd.Series(stock_revene_info_fin['revenue_year'],dtype='int'),
      'RevenueMonth' : pd.Series(stock_revene_info_fin['revenue_month'],dtype='int'),
      'TotalRevenue' : pd.Series(stock_revene_info_fin['revenue'],dtype='float')
      }).reset_index(drop=True)
   #股票股息資訊
   stock_Dividend_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_Dividend_info_fin['stock_id'],dtype='str'),
      'Dateinfo' : pd.Series(stock_Dividend_info_fin['year'],dtype='str'),
      'CashDividends' : pd.Series(stock_Dividend_info_fin['StockEarningsDistribution'] + stock_Dividend_info_fin['StockStatutorySurplus'],dtype='float'),
      'StockDividend' : pd.Series(stock_Dividend_info_fin['CashEarningsDistribution']	+ stock_Dividend_info_fin['CashStatutorySurplus'],dtype='float'),
      'ExDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashExDividendTradingDate']],
      'CashDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashDividendPaymentDate']]
      }).reset_index(drop=True)
   #股票PER資訊
   stock_PER_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_PER_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_PER_info_fin['date']],
      'YieldRate' : pd.Series(stock_PER_info_fin['dividend_yield'],dtype='float'),
      'PER' : pd.Series(stock_PER_info_fin['PER'],dtype='float'),
      'PBR' : pd.Series(stock_PER_info_fin['PBR'],dtype='float')
      }).reset_index(drop=True) 
   
   return {'stock_price_info_to_DB':stock_price_info_fin,
           'stock_revene_info_to_DB':stock_revene_info_fin,
           'stock_Dividend_info_to_DB':stock_Dividend_info_fin,
           'stock_PER_info_to_DB':stock_PER_info_fin}
   
#透過patentsview抓取各公司的DATA後，並針對預計要呈現的表格進行資料型態轉換   
def DBPatnetData(nowdate : str):
   patent_main_fin = None
   patnet_cpc_fin = None
   patent_text_fin = None
   
   for i,j in zip(stockbasedata['StockCode'],stockbasedata['companyname']):
      if j=='':
         continue
      elif patent_main_fin is None:
         patent_main_data = PD.patent_basic(i,j,nowdate)
         patent_main_fin = patent_main_data['patent_main_data']
         patnet_cpc_fin = patent_main_data['patnet_cpc_data']
         patent_text_fin = patent_main_data['patent_text_data']
      else:
         patent_main_data = PD.patent_basic(i,j,nowdate)
         patent_main_fin = pd.concat([patent_main_fin,patent_main_data['patent_main_data']])
         patnet_cpc_fin = pd.concat([patnet_cpc_fin,patent_main_data['patnet_cpc_data']])
         patent_text_fin = pd.concat([patent_text_fin,patent_main_data['patent_text_data']])
      
   #專利號碼、專利申請日與專利公開公告日      
   patent_main_fin = pd.DataFrame({
      'StockCode' : pd.Series(patent_main_fin['stockid'],dtype='str'), 
      'PatentNumber' : pd.Series(patent_main_fin['patentnumber'],dtype='str'),
      'PatentApplicationDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentapplicationdate']],
      'PatentPubDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentpubdate']],
      'PatentApplicationDateYear' : pd.Series(patent_main_fin['patentapplicationdateyear'],dtype='int'),
      'PatentPubDateYear' : pd.Series(patent_main_fin['patentpubdateyear'],dtype='int')
      }).dropna().reset_index(drop=True)
   #專利技術分類號資訊
   patnet_cpc_fin = pd.DataFrame({
      'PatentNumber' : pd.Series(patnet_cpc_fin['patent_id'],dtype='str'),
      'PatnetCPCCode' : pd.Series(patnet_cpc_fin['CPC'],dtype='str')
      }).dropna().reset_index(drop=True)
   #專利標題與摘要資訊
   patent_text_fin = pd.DataFrame({
      'PatentNumber' : pd.Series(patent_text_fin['PatentNumber'],dtype='str'),
      'PatnetTitle' : pd.Series(patent_text_fin['PatnetTitle'],dtype='str'),
      'PatentAbs' : pd.Series(patent_text_fin['PatentAbs'],dtype='str')
      }).dropna().reset_index(drop=True)
   
   return {'patent_main_to_DB':patent_main_fin, 
           'patnet_cpc_to_DB':patnet_cpc_fin,
           'patent_text_to_DB':patent_text_fin}



todayinfo = date.today().strftime('%Y-%m-%d')
engine = sqlalchemy.create_engine('sqlite:///stock_database.db', echo=False)
#讀取公司基本資訊
companydata = pd.read_parquet('company_baseinfo.parquet')
#透過公司表格與時間抓取股票資訊
STOCK_data = DBStockData(todayinfo)
#透過公司表格與時間抓取專利資訊
PTAENT_data = DBPatnetData(todayinfo)



def DatatoDB():
   #匯入公司資訊進入先前建立的Data Base
   companydata.to_sql('CompanyBaseInfo', con=engine, if_exists='append',index=False)
   print('companytoDB_OK')
   #匯入股票資訊進入先前建立的Data Base
   STOCK_data['stock_price_info_to_DB'].to_sql('StockPriceInfo', con=engine, if_exists='append',index=False)
   STOCK_data['stock_revene_info_to_DB'].to_sql('stockRevenue', con=engine, if_exists='append',index=False)
   STOCK_data['stock_Dividend_info_to_DB'].to_sql('stockDividend', con=engine, if_exists='append',index=False)
   STOCK_data['stock_PER_info_to_DB'].to_sql('stockPERIndex', con=engine, if_exists='append',index=False)
   print("stockdatatoDB_OK!")
   #匯入專利資訊進入先前建立的Data Base
   PTAENT_data['patent_main_to_DB'].to_sql('PatentMain', con=engine, if_exists='append',index=False)
   PTAENT_data['patnet_cpc_to_DB'].to_sql('PatentClass', con=engine, if_exists='append',index=False)
   PTAENT_data['patent_text_to_DB'].to_sql('PatentText', con=engine, if_exists='append',index=False)
   print("patentdatatoDB_OK!")
   
   return print('allDB_OK')

if __name__ == "__main__":
   DatatoDB()
   