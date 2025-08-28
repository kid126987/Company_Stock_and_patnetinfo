from sidepro.DataCrap import * 
from datetime import datetime
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
from datetime import date
FD = finmind_data()
PD = patent_data()


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


def DBStockData(enddate :str):
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
   
   stock_price_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_price_info_fin['stock_id'],dtype='str'),
      'StockDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_price_info_fin['date']],
      'StockClose' : pd.Series(stock_price_info_fin['close'],dtype='float'),
      'RSV' : pd.Series(stock_price_info_fin['RSV_value'],dtype='float'),
      'KValue' : pd.Series(stock_price_info_fin['K_value'],dtype='float'),
      'DValue' : pd.Series(stock_price_info_fin['D_value'],dtype='float')
      }).reset_index(drop=True)
   stock_revene_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_revene_info_fin['stock_id'],dtype='str'),
      'RevenueYear' : pd.Series(stock_revene_info_fin['revenue_year'],dtype='int'),
      'RevenueMonth' : pd.Series(stock_revene_info_fin['revenue_month'],dtype='int'),
      'TotalRevenue' : pd.Series(stock_revene_info_fin['revenue'],dtype='float')
      }).reset_index(drop=True)
   stock_Dividend_info_fin = pd.DataFrame({
      'StockCode' : pd.Series(stock_Dividend_info_fin['stock_id'],dtype='str'),
      'Dateinfo' : pd.Series(stock_Dividend_info_fin['year'],dtype='str'),
      'CashDividends' : pd.Series(stock_Dividend_info_fin['StockEarningsDistribution'] + stock_Dividend_info_fin['StockStatutorySurplus'],dtype='float'),
      'StockDividend' : pd.Series(stock_Dividend_info_fin['CashEarningsDistribution']	+ stock_Dividend_info_fin['CashStatutorySurplus'],dtype='float'),
      'ExDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashExDividendTradingDate']],
      'CashDividendDate' : [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in stock_Dividend_info_fin['CashDividendPaymentDate']]
      }).reset_index(drop=True)
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
      
         
   patent_main_fin = pd.DataFrame({
      'StockCode' : pd.Series(patent_main_fin['stockid'],dtype='str'), 
      'PatentNumber' : pd.Series(patent_main_fin['patentnumber'],dtype='str'),
      'PatentApplicationDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentapplicationdate']],
      'PatentPubDate' : [datetime.strptime(date_str, '%Y-%m-%d') for date_str in patent_main_fin['patentpubdate']],
      'PatentApplicationDateYear' : pd.Series(patent_main_fin['patentapplicationdateyear'],dtype='int'),
      'PatentPubDateYear' : pd.Series(patent_main_fin['patentpubdateyear'],dtype='int')
      }).dropna().reset_index(drop=True)
   
   patnet_cpc_fin = pd.DataFrame({
      'PatentNumber' : pd.Series(patnet_cpc_fin['patent_id'],dtype='str'),
      'PatnetCPCCode' : pd.Series(patnet_cpc_fin['CPC'],dtype='str')
      }).dropna().reset_index(drop=True)
   
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
print('DB_OK')
companydata = pd.read_parquet('company_baseinfo.parquet')
print('companydata_OK')
STOCK_data = DBStockData(todayinfo)
print('stockdata_OK')
PTAENT_data = DBPatnetData(todayinfo)
print('patdata_OK')


if __name__ == "__main__":
   companydata.to_sql('CompanyBaseInfo', con=engine, if_exists='append',index=False)
   print('companytoDB_OK')
   
   STOCK_data['stock_price_info_to_DB'].to_sql('StockPriceInfo', con=engine, if_exists='append',index=False)
   STOCK_data['stock_revene_info_to_DB'].to_sql('stockRevenue', con=engine, if_exists='append',index=False)
   STOCK_data['stock_Dividend_info_to_DB'].to_sql('stockDividend', con=engine, if_exists='append',index=False)
   STOCK_data['stock_PER_info_to_DB'].to_sql('stockPERIndex', con=engine, if_exists='append',index=False)
   print("stockdatatoDB_OK!")
   
   PTAENT_data['patent_main_to_DB'].to_sql('PatentMain', con=engine, if_exists='append',index=False)
   PTAENT_data['patnet_cpc_to_DB'].to_sql('PatentClass', con=engine, if_exists='append',index=False)
   PTAENT_data['patent_text_to_DB'].to_sql('PatentText', con=engine, if_exists='append',index=False)
   print("patentdatatoDB_OK!")