from DataCrap import * 
from datetime import datetime
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
from datetime import date
import time
import pyarrow.parquet as pq
import uuid
FD = finmind_data()
PD = patent_data()
GD = googlenews_data()
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
   stock_financial_info_fin = None
   stock_balance_info_fin = None
   stock_cashflow_info_fin = None
   stock_InvestorsBuy_info_fin = None
   
   for i in stockbasedata['StockCode']:
      stock_price_info = FD.stock_price_info(i,start_date=startdate,end_date=enddate)
      stock_revene_info = FD.stock_revene_info(i,start_date=startdate,end_date=enddate)
      stock_Dividend_info = FD.stock_Dividend_info(i,start_date=startdate,end_date=enddate)
      stock_PER_info = FD.stock_PER_info(i,start_date=startdate,end_date=enddate)
      
      stock_financial_info = FD.stock_financial_info(i,start_date=startdate,end_date=enddate)
      stock_balance_info = FD.stock_balance_info(i,start_date=startdate,end_date=enddate)
      stock_cashflow_info = FD.stock_cashflow_info(i,start_date=startdate,end_date=enddate)
      stock_InvestorsBuy_info = FD.stock_InvestorsBuy_info(i,start_date=startdate,end_date=enddate)
      
      
      if stock_price_info_fin is None:
         stock_price_info_fin = stock_price_info
         stock_revene_info_fin = stock_revene_info
         stock_Dividend_info_fin = stock_Dividend_info
         stock_PER_info_fin = stock_PER_info
         
         stock_financial_info_fin = stock_financial_info
         stock_balance_info_fin = stock_balance_info
         stock_cashflow_info_fin = stock_cashflow_info
         
         stock_InvestorsBuy_info_fin = stock_InvestorsBuy_info
      else:
         stock_price_info_fin = pd.concat([stock_price_info_fin,stock_price_info])
         stock_revene_info_fin = pd.concat([stock_revene_info_fin,stock_revene_info])   
         stock_Dividend_info_fin = pd.concat([stock_Dividend_info_fin,stock_Dividend_info])
         stock_PER_info_fin = pd.concat([stock_PER_info_fin,stock_PER_info])
   
         stock_financial_info_fin = pd.concat([stock_financial_info_fin,stock_financial_info])
         stock_balance_info_fin = pd.concat([stock_balance_info_fin,stock_balance_info])
         stock_cashflow_info_fin = pd.concat([stock_cashflow_info_fin,stock_cashflow_info])
         stock_InvestorsBuy_info_fin = pd.concat([stock_InvestorsBuy_info_fin,stock_InvestorsBuy_info])
   
   #建立dataid
   stock_price_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_price_info_fin['stock_id']))]
   stock_revene_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_revene_info_fin['stock_id']))]
   stock_Dividend_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_Dividend_info_fin['stock_id']))]
   stock_PER_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_PER_info_fin['stock_id']))]
   stock_financial_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_financial_info_fin['stock_id']))]
   stock_balance_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_balance_info_fin['stock_id']))]
   stock_cashflow_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_cashflow_info_fin['stock_id']))]
   stock_InvestorsBuy_info_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(stock_InvestorsBuy_info_fin['stock_id']))]
         
   #資料清理
   stock_Dividend_info_fin = stock_Dividend_info_fin.loc[stock_Dividend_info_fin['CashDividendPaymentDate']!='']
   
   #股票股價資訊
   stock_price_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_price_info_fin['Dataid'],dtype='str'),
      'StockCode' : pd.Series(stock_price_info_fin['stock_id'],dtype='str'),
      'StockDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_price_info_fin['date']],
      'StockClose' : pd.Series(stock_price_info_fin['close'],dtype='float'),
      'TradingVolume':pd.Series(stock_price_info_fin['Trading_Volume'],dtype='float'),
      'Tradingmoney':pd.Series(stock_price_info_fin['Trading_money'],dtype='float'),
      'RSV' : pd.Series(stock_price_info_fin['RSV_value'],dtype='float'),
      'KValue' : pd.Series(stock_price_info_fin['K_value'],dtype='float'),
      'DValue' : pd.Series(stock_price_info_fin['D_value'],dtype='float')
      }).reset_index(drop=True)
   #股票收益資訊
   stock_revene_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_revene_info_fin['Dataid'],dtype='str'),
      'StockCode' : pd.Series(stock_revene_info_fin['stock_id'],dtype='str'),
      'RevenueYear' : pd.Series(stock_revene_info_fin['revenue_year'],dtype='int'),
      'RevenueMonth' : pd.Series(stock_revene_info_fin['revenue_month'],dtype='int'),
      'TotalRevenue' : pd.Series(stock_revene_info_fin['revenue'],dtype='float')
      }).reset_index(drop=True)
   #股票股息資訊
   stock_Dividend_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_Dividend_info_fin['Dataid'],dtype='str'),
      'StockCode' : pd.Series(stock_Dividend_info_fin['stock_id'],dtype='str'),
      'DateInfo' : pd.Series(stock_Dividend_info_fin['year'],dtype='str'),
      'CashDividends' : pd.Series(stock_Dividend_info_fin['StockEarningsDistribution'] + stock_Dividend_info_fin['StockStatutorySurplus'],dtype='float'),
      'StockDividend' : pd.Series(stock_Dividend_info_fin['CashEarningsDistribution']	+ stock_Dividend_info_fin['CashStatutorySurplus'],dtype='float'),
      'ExDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashExDividendTradingDate']],
      'CashDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashDividendPaymentDate']]
      }).reset_index(drop=True)
   #股票PER資訊
   stock_PER_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_PER_info_fin['Dataid'],dtype='str'),
      'StockCode' : pd.Series(stock_PER_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_PER_info_fin['date']],
      'YieldRate' : pd.Series(stock_PER_info_fin['dividend_yield'],dtype='float'),
      'PER' : pd.Series(stock_PER_info_fin['PER'],dtype='float'),
      'PBR' : pd.Series(stock_PER_info_fin['PBR'],dtype='float')
      }).reset_index(drop=True) 
   #股票損益資訊
   stock_financial_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_financial_info_fin['Dataid'],dtype='str'),
      'StockCode' :  pd.Series(stock_financial_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_financial_info_fin['date']],
      'Types' : pd.Series(stock_financial_info_fin['type'],dtype='str'),
      'DataValue' : pd.Series(stock_financial_info_fin['value'],dtype='float'),
      'OriginName' : pd.Series(stock_financial_info_fin['origin_name'],dtype='str')
      }).reset_index(drop=True) 
   #股票資產負債資訊
   stock_balance_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_balance_info_fin['Dataid'],dtype='str'),
      'StockCode' :  pd.Series(stock_balance_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_balance_info_fin['date']],
      'Types' : pd.Series(stock_balance_info_fin['type'],dtype='str'),
      'DataValue' : pd.Series(stock_balance_info_fin['value'],dtype='float'),
      'OriginName' : pd.Series(stock_balance_info_fin['origin_name'],dtype='str')
      }).reset_index(drop=True) 

   #股票現金流量資訊
   stock_cashflow_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_cashflow_info_fin['Dataid'],dtype='str'),
      'StockCode' :  pd.Series(stock_cashflow_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_cashflow_info_fin['date']],
      'Types' : pd.Series(stock_cashflow_info_fin['type'],dtype='str'),
      'DataValue' : pd.Series(stock_cashflow_info_fin['value'],dtype='float'),
      'OriginName' : pd.Series(stock_cashflow_info_fin['origin_name'],dtype='str')
      }).reset_index(drop=True) 
   
   #股票法人買賣表
   stock_InvestorsBuy_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(stock_InvestorsBuy_info_fin['Dataid'],dtype='str'),
      'StockCode' :  pd.Series(stock_InvestorsBuy_info_fin['stock_id'],dtype='str'),
      'DateInfo' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_InvestorsBuy_info_fin['date']],
      'Buy' : pd.Series(stock_InvestorsBuy_info_fin['buy'],dtype='float'),
      'Names' : pd.Series(stock_InvestorsBuy_info_fin['name'],dtype='str'),
      'Sell' : pd.Series(stock_InvestorsBuy_info_fin['sell'],dtype='float')
      })
   
   return {'stock_price_info_to_DB':stock_price_info_fin,
           'stock_revene_info_to_DB':stock_revene_info_fin,
           'stock_Dividend_info_to_DB':stock_Dividend_info_fin,
           'stock_PER_info_to_DB':stock_PER_info_fin,
           'stock_financial_info_fin_to_DB' : stock_financial_info_fin,
           'stock_balance_info_fin_to_DB' : stock_balance_info_fin,
           'stock_cashflow_info_fin_to_DB' : stock_cashflow_info_fin,
           'stock_InvestorsBuy_info_fin_to_DB' : stock_InvestorsBuy_info_fin
           }
   
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
   
   #建立Dataid
   patent_main_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(patent_main_fin['patentnumber']))]
   patnet_cpc_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(patnet_cpc_fin['patent_id']))]
   patent_text_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(patent_text_fin['PatentNumber']))]
   
         
   #專利號碼、專利申請日與專利公開公告日      
   patent_main_fin = pd.DataFrame({
      'Dataid': pd.Series(patent_main_fin['Dataid'],dtype='str'),
      'StockCode' : pd.Series(patent_main_fin['stockid'],dtype='str'), 
      'PatentNumber' : pd.Series(patent_main_fin['patentnumber'],dtype='str'),
      'PatentApplicationDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentapplicationdate']],
      'PatentPubDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentpubdate']],
      'PatentApplicationDateYear' : pd.Series(patent_main_fin['patentapplicationdateyear'],dtype='int'),
      'PatentPubDateYear' : pd.Series(patent_main_fin['patentpubdateyear'],dtype='int')
      }).dropna().reset_index(drop=True)
   #專利技術分類號資訊
   patnet_cpc_fin = pd.DataFrame({
      'Dataid': pd.Series(patnet_cpc_fin['Dataid'],dtype='str'),
      'PatentNumber' : pd.Series(patnet_cpc_fin['patent_id'],dtype='str'),
      'PatnetCPCCode' : pd.Series(patnet_cpc_fin['CPC'],dtype='str')
      }).dropna().reset_index(drop=True)
   #專利標題與摘要資訊
   patent_text_fin = pd.DataFrame({
      'Dataid': pd.Series(patent_text_fin['Dataid'],dtype='str'),
      'PatentNumber' : pd.Series(patent_text_fin['PatentNumber'],dtype='str'),
      'PatnetTitle' : pd.Series(patent_text_fin['PatnetTitle'],dtype='str'),
      'PatentAbs' : pd.Series(patent_text_fin['PatentAbs'],dtype='str')
      }).dropna().reset_index(drop=True)
   
   return {'patent_main_to_DB':patent_main_fin, 
           'patnet_cpc_to_DB':patnet_cpc_fin,
           'patent_text_to_DB':patent_text_fin}

#google_news 資料
def googledata(Companynamedata):
   Newsdata_fin = None
   for i in range(len(Companynamedata['CompanyNameC'])):
      time.sleep(1)
      TWNews = GD.googlenewssearch(Companynamedata['CompanyNameC'][i],"TW")
      JPNews = GD.googlenewssearch(Companynamedata['CompanyNameE'][i].replace(" ",""),"JP")
      USNews = GD.googlenewssearch(Companynamedata['CompanyNameE'][i].replace(" ",""),"US")
      EPNews = GD.googlenewssearch(Companynamedata['CompanyNameE'][i].replace(" ",""),"EP")
      Newsdata = pd.concat([TWNews,JPNews,USNews,EPNews])
      Newsdata['StockCode']=Companynamedata['StockCode'][i]
      
      if Newsdata_fin is None:
         Newsdata_fin = Newsdata
      else:
         Newsdata_fin = pd.concat([Newsdata_fin,Newsdata])
   Newsdata_fin = Newsdata_fin[Newsdata_fin['title'] != 'nodata'].reset_index(drop=True)
     
   #建立Dataid
   Newsdata_fin['Dataid'] = [str(uuid.uuid4()) for i in range(len(Newsdata_fin['StockCode']))]
     
   stock_news_info_fin = pd.DataFrame({
      'Dataid' : pd.Series(Newsdata_fin['Dataid'],dtype='str'),
      'StockCode' :  pd.Series(Newsdata_fin['StockCode'],dtype='str'),
      'Title': pd.Series(Newsdata_fin['title'],dtype='str'),
      'PublishTime': pd.Series(Newsdata_fin['published'],dtype='str'),
      'NewsLink': pd.Series(Newsdata_fin['link'],dtype='str'),
      })
   return stock_news_info_fin
   


todayinfo = date.today().strftime('%Y-%m-%d')
engine = sqlalchemy.create_engine('sqlite:///stock_database.db', echo=False)
#讀取公司基本資訊
print('getting company data')
companydata = pq.read_table('company_baseinfo.parquet')
companydata = companydata.to_pandas()
print('company data get!')
#透過公司表格與時間抓取股票資訊
print('getting stock data')
STOCK_data = DBStockData(todayinfo)
print('stock data get!')
#透過公司表格與時間抓取專利資訊
print('getting patent data')
PTAENT_data = DBPatnetData(todayinfo)
print('patent data get!')
#透過公司名稱找google news
print('getting google news data')
News_data = googledata(companydata[['CompanyNameC','CompanyNameE','StockCode']])
print('google news data get!')

def DatatoDB():
   #匯入公司資訊進入先前建立的Data Base
   companydata.to_sql('CompanyBaseInfo', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   print('companytoDB_OK!')
   #匯入股票資訊進入先前建立的Data Base
   STOCK_data['stock_price_info_to_DB'].to_sql('StockPriceInfo', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_revene_info_to_DB'].to_sql('StockRevenue', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_Dividend_info_to_DB'].to_sql('StockDividend', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_PER_info_to_DB'].to_sql('StockPERIndex', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_financial_info_fin_to_DB'].to_sql('StockFinancial', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_balance_info_fin_to_DB'].to_sql('StockBalance', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_cashflow_info_fin_to_DB'].to_sql('StockCashflow', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   STOCK_data['stock_InvestorsBuy_info_fin_to_DB'].to_sql('StockInvestorsBuy', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   
   print("stockdatatoDB_OK!")
   #匯入專利資訊進入先前建立的Data Base
   PTAENT_data['patent_main_to_DB'].to_sql('PatentMain', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   PTAENT_data['patnet_cpc_to_DB'].to_sql('PatentClass', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   PTAENT_data['patent_text_to_DB'].to_sql('PatentText', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   print("patentdatatoDB_OK!")
   
   #匯入新聞資訊進入先前建立的Data Base
   News_data.to_sql('StockNews', con=engine, if_exists='append',index=False,method='multi', chunksize=1000)
   print("newsdatatoDB_OK!")
   
   return print('allDB_OK!!')

if __name__ == "__main__":
   DatatoDB()
   