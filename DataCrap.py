import requests
import pandas as pd
import json
from sidepro.baseENV import *
class finmind_data:
    def __init__(self):
        self.token = login_data['token'] 
    def stock_price_info(self,stock_id : str,start_date : str,end_date : str):
        price_parameter = {
          "dataset": "TaiwanStockPrice",
          "data_id": stock_id,
          "start_date": start_date,
          "end_date": end_date,
          "token":  self.token
        }
        stock_price = requests.get(data_url, params=price_parameter)
        price_data = stock_price.json()
        price_data = pd.DataFrame(price_data["data"])
        
        try :   
          price_data = price_data[['date','stock_id','close']]
          price_data[['date_year','date_month','date_date']] = price_data['date'].str.split('-',n=2,expand=True)
          
          RSV_value=[]
          K_value=[]
          D_value=[]
          date_def=9

          for i in range(0,len(price_data['close'])):
              if i < date_def-1:
                RSV_value.append(0)
                K_value.append(0)
                D_value.append(0)
              elif i < date_def :
                RSV_value.append(0)
                K_value.append(50)
                D_value.append(50)
              else:
                RSV = (price_data['close'][i] - price_data['close'][i-date_def:i].min())/(price_data['close'][i-date_def:i].max()-price_data['close'][i-date_def:i].min())*100
                K = (RSV/3) + (K_value[i-1]*2/3)
                D = (K/3) + (D_value[i-1]*2/3)
                RSV_value.append(RSV)
                K_value.append(K)
                D_value.append(D)

          price_data['RSV_value']=RSV_value
          price_data['K_value']=K_value
          price_data['D_value']=D_value

          return price_data
        except:
          price_data = pd.DataFrame({
            'date' : 'nodata',
            'stock_id' : 'nodata',
            'close' : 'nodata',
            'date_year' : 'nodata',
            'date_month' : 'nodata',
            'date_date' : 'nodata',
            'RSV_value' : 'nodata',
            'K_value' : 'nodata',
            'D_value' : 'nodata'
          })
          
          return price_data
          
    def stock_revene_info(self,stock_id: str,start_date: str,end_date: str):
      revenue_parameter = {
        "dataset": "TaiwanStockMonthRevenue",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": self.token  
        }
      stock_revenue = requests.get(data_url, params=revenue_parameter)
      revenue_data = stock_revenue.json()
      try:
        revenue_data = pd.DataFrame(revenue_data["data"]).drop(['date','country'],axis=1)
        return revenue_data
      except:
        revenue_data = pd.DataFrame({
          'stock_id':'nodata',
          'revenue':'nodata',
          'revenue_month':'nodata',
          'revenue_year':'nodata'
        })
        return revenue_data
    
    def stock_Dividend_info(self,stock_id: str,start_date: str,end_date: str):
      Dividend_parameter = {
        "dataset": "TaiwanStockDividend",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": self.token  
        }
      stock_Dividend = requests.get(data_url, params=Dividend_parameter)
      Dividend_data = stock_Dividend.json()
      try:
        Dividend_data = pd.DataFrame(Dividend_data["data"])
        Dividend_data=Dividend_data[['stock_id', 
                                    'year', 
                                    'StockEarningsDistribution',
                                    'StockStatutorySurplus',
                                    'CashEarningsDistribution', 
                                    'CashStatutorySurplus',
                                    'CashExDividendTradingDate', 
                                    'CashDividendPaymentDate']]
        return Dividend_data
      except:
        Dividend_data = pd.DataFrame({
          'stock_id':'nodata', 
          'year':'nodata', 
          'StockEarningsDistribution':'nodata',
          'StockStatutorySurplus':'nodata',
          'CashEarningsDistribution':'nodata', 
          'CashStatutorySurplus':'nodata',
          'CashExDividendTradingDate':'nodata', 
          'CashDividendPaymentDate':'nodata'
        })
        
    def stock_PER_info(self,stock_id: str,start_date: str,end_date: str):
      PER_parameter = {
        "dataset": "TaiwanStockPER",
        "data_id": stock_id,
        "start_date": start_date,
        "end_date": end_date,
        "token": self.token  
        }
      stock_PER = requests.get(data_url, params=PER_parameter)
      PER_data = stock_PER.json()
      try:
        PER_data = pd.DataFrame(PER_data["data"])
        return PER_data
      except:
        PER_data = pd.DataFrame({
          'date':'nodata',	
          'stock_id':'nodata',	
          'dividend_yield':'nodata',	
          'PER':'nodata',	
          'PBR':'nodata'
        })
        return PER_data


class patent_data:
    def __init__(self):
        self.key = patentkey
    def patent_basic(self,stockid:str ,company_name : list,gte_patentdate : str):
        special_keys = {
            'api/v1/ipc'                      : 'ipcr',
            'api/v1/wipo'                     : 'wipo',
            'api/v1/publication/rel_app_text' : 'rel_app_text_publications'
            }
        def response_key(endpoint:str) -> str:
            endpoint = endpoint.rstrip('/')
            leaf = endpoint.split('/')[-1]
            if leaf in special_keys:
                return special_keys[leaf]
            elif leaf.endswith('s'):
                return leaf + 'es'
            else:
                return leaf + 's'
        base_url = 'https://search.patentsview.org'
        endpoint = 'api/v1/patent'   

        param_dict = {
            "f" : ["patent_id", "patent_title", "patent_earliest_application_date","patent_date","patent_abstract","assignees.assignee_organization","cpc_current.cpc_group_id"],
            "o" : {"size":1000},
            "q" : {"_and":[{"_contains":{"assignees.assignee_organization":company_name}},{"_lte":{"patent_earliest_application_date":gte_patentdate}}]},
            "s" : [{"patent_earliest_application_date":"desc"}]
                      }

        param_string = "&".join([f"{param_name}={json.dumps(param_val)}" for param_name, param_val in param_dict.items()])
        query_url = f"{base_url}/{endpoint.strip('/')}/?{param_string}"    
        response = requests.get(query_url, headers={"X-Api-Key": self.key})
        response_unpacked = pd.DataFrame(response.json()[response_key(endpoint)])
        
        patent_main_data = pd.DataFrame({
            'stockid' : stockid,
            'patentnumber' : response_unpacked['patent_id'],
            'patentapplicationdate' : response_unpacked['patent_earliest_application_date'],
            'patentpubdate' : response_unpacked['patent_date'],
            'patentapplicationdateyear' : [date.split('-')[0] for date in response_unpacked['patent_earliest_application_date']],
            'patentpubdateyear' : [date.split('-')[0] for date in response_unpacked['patent_date']],
        })
        patent_text_data = pd.DataFrame({
            'PatentNumber' : response_unpacked['patent_id'],
            'PatnetTitle' : response_unpacked['patent_title'],
            'PatentAbs' : response_unpacked['patent_abstract']
        })
        patnet_cpc_data=None
        org_data = response_unpacked[['patent_id','cpc_current']]
        org_data = org_data.dropna().reset_index(drop=True)

        for i in range(len(org_data['patent_id'])):
            if i==0 :
                CPC_data = pd.DataFrame({
                'patent_id' : org_data['patent_id'][i],
                'CPC'   :   pd.DataFrame(org_data['cpc_current'][i])['cpc_group_id']})
                patnet_cpc_data=CPC_data
            else :
                CPC_data = pd.DataFrame({
                'patent_id' : org_data['patent_id'][i],
                'CPC'   :   pd.DataFrame(org_data['cpc_current'][i])['cpc_group_id']})
                patnet_cpc_data=pd.concat([patnet_cpc_data,CPC_data],axis=0)

        return {'patent_main_data' : patent_main_data,'patent_text_data' : patent_text_data,'patnet_cpc_data' : patnet_cpc_data}
        
        