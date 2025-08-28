from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import google.generativeai as genai
from sidepro.baseENV import googleapikey

engine = sqlalchemy.create_engine('sqlite:///stock_database.db', echo=False)

companybasedata = pd.read_sql('SELECT * FROM CompanyBaseInfo',engine)

stockdata_price_all = pd.read_sql('SELECT * FROM StockPriceInfo',engine)
stockdata_revenue = pd.read_sql('SELECT * FROM stockRevenue',engine)
stockdata_Dividend = pd.read_sql('SELECT * FROM stockDividend',engine)
stockdata_PER = pd.read_sql('SELECT * FROM stockPERIndex',engine)

patentcpc = pd.read_sql('SELECT * FROM PatentClass',engine) 
patentmain = pd.read_sql('SELECT * FROM PatentMain',engine)
patenttext = pd.read_sql('SELECT * FROM PatentText',engine)

def companybaseinfo(stock_id : str):
    companybasedata_info = companybasedata[companybasedata['StockCode']==stock_id]
    companybasedata_info = companybasedata_info.T.reset_index()
    companybasedata_info = companybasedata_info.rename(columns={'index': 'stat',0 : 'value'})
    return companybasedata_info

def stockinfo(stock_id : str):
    stock_price_all = stockdata_price_all[stockdata_price_all['StockCode']==stock_id]
    stock_price_all = stock_price_all[['StockDate','StockClose']]
    stock_price_all['StockDate'] = pd.to_datetime(stock_price_all['StockDate'])
    
    stock_revenue = stockdata_revenue[stockdata_revenue['StockCode']==stock_id]
    stock_revenue = stock_revenue[['RevenueYear','RevenueMonth','TotalRevenue']]
    
    stock_dividend = stockdata_Dividend[stockdata_Dividend['StockCode']==stock_id]
    stock_dividend = stock_dividend[['Dateinfo','CashDividends','StockDividend','ExDividendDate','CashDividendDate']]
    
    stock_per = stockdata_PER[stockdata_PER['StockCode']==stock_id]
    stock_per = stock_per[['DateInfo','YieldRate','PER','PBR']].sort_values('DateInfo',ascending=False)
    return stock_price_all,stock_revenue,stock_dividend,stock_per
    
def patentinfo(stock_id : str):
    patentmaindata = patentmain[patentmain['StockCode']==stock_id]

    patentmaindata_app = patentmaindata[['PatentNumber','PatentApplicationDateYear']]
    patentmaindata_app = patentmaindata_app.groupby('PatentApplicationDateYear').count().reset_index()
    patentmaindata_app = patentmaindata_app.sort_values('PatentApplicationDateYear')
    patentmaindata_app['PatentApplicationDateYear'] = [str(i) for i in patentmaindata_app['PatentApplicationDateYear']]

    patentmaindata_new = patentmaindata.sort_values(by=['PatentApplicationDate'],ascending=False).head(30)
    patentmaindata_new = pd.merge(patentmaindata_new,patenttext,left_on='PatentNumber',right_on='PatentNumber')[['PatentNumber','PatentApplicationDate','PatentPubDate','PatnetTitle','PatentAbs']]
    
    patentmaindata_cpc = pd.merge(patentmaindata,patentcpc,left_on='PatentNumber',right_on='PatentNumber')[['PatentNumber','PatnetCPCCode']]
    patentmaindata_cpc = patentmaindata_cpc.groupby('PatnetCPCCode').count().reset_index()
    patentmaindata_cpc = patentmaindata_cpc.sort_values('PatentNumber',ascending=False).head(12)
    return patentmaindata_app,patentmaindata_new,patentmaindata_cpc

def gptinfo(stock_id : str):
        
    stockmain = stockinfo(stock_id)
    revenue_info = stockmain[1]
    dividend_info = stockmain[2]
       
    for i in revenue_info.columns:
        revenue_info[i] = [str(j) for j in revenue_info[i]]
    revenue_info = ";".join(revenue_info.columns[0]+':'+ revenue_info[revenue_info.columns[0]]+','+revenue_info.columns[1]+':'+ revenue_info[revenue_info.columns[1]]+','+revenue_info.columns[2]+':'+ revenue_info[revenue_info.columns[2]])
    for k in dividend_info.columns:
        dividend_info[k] = [str(l) for l in dividend_info[k]]
   
    dividend_info = ";".join(dividend_info.columns[0]+':'+dividend_info[dividend_info.columns[0]]+','+dividend_info.columns[1]+':'+dividend_info[dividend_info.columns[1]]+','+dividend_info.columns[2]+':'+dividend_info[dividend_info.columns[2]]+','+dividend_info.columns[3]+':'+dividend_info[dividend_info.columns[3]]+','+dividend_info.columns[4]+':'+dividend_info[dividend_info.columns[4]])
    
    techinfo = patentinfo(stock_id)
    techinfo = ';'.join(techinfo[1]['PatnetTitle'].head(20))
    requests_text = f'你是一位投資分析專家,請根據以下技術描述, 摘要目前公司的技術發展趨勢,並綜合營收資訊與配息資訊，進行基本面分析。技術描述:{techinfo}, 營收資訊:{revenue_info}, 配息資訊:{dividend_info}'
    
    client = genai.configure(api_key=googleapikey)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(requests_text)
    
    return response.text
 
 
 

import gradio as gr
with gr.Blocks() as demo:
   with gr.Column():
      id_input = gr.Dropdown(label='input stock id',choices=['2330','2317','2454','2308','2382','2891','2881','3711','2882','2412'])
      search_btn = gr.Button("continue")
   
   with gr.Tab('company_base_info'):
      output1 = gr.Dataframe()
      search_btn.click(fn=companybaseinfo,inputs=id_input,outputs=output1)
   
   with gr.Tab('stock_info'):
      with gr.Column():
         with gr.Row():
            start = gr.DateTime("2024-08-15", label="Start",include_time=False)
            end = gr.DateTime("2025-08-15", label="End",include_time=False)
            apply_btn = gr.Button("Apply", scale=0)
         with gr.Row():
            group_by = gr.Radio(["None", "30d", "60d", "90d"], 
                                value="None", 
                                label="Group by")
         
         stock_price_alls = gr.LinePlot(
            label='sttock_price_all',
            x="StockDate",
            y="StockClose",
         )
                 
         time_graphs = stock_price_alls
         group_by.change(
            lambda group: gr.LinePlot(x_bin=None if group == "None" else group,y_aggregate='mean'),
            group_by,
            time_graphs
         )
         apply_btn.click(lambda start, end: gr.LinePlot(x_lim=[start, end]), [start, end], time_graphs)
         
         stock_revenues = gr.Dataframe(label='stock_recenue_info')
         stock_dividends = gr.Dataframe(label='stock_dividend_info')
         stock_pers = gr.Dataframe(label='stock_per_info')
       
      search_btn.click(fn=stockinfo,inputs=id_input,outputs=[stock_price_alls,stock_revenues,stock_dividends,stock_pers])      
   
   
   with gr.Tab('patnet_info'):      
      patentmaindata_apps = gr.LinePlot(
               label='patentmaindata_app',
               x="PatentApplicationDateYear",
               y="PatentNumber",
         )
      patentmaindata_news = gr.Dataframe(label='patentmaindata_new')
      patentmaindata_cpcs = gr.BarPlot(
               label='patentmaindata_cpc',
               x="PatnetCPCCode",
               y="PatentNumber"
      )

      search_btn.click(fn=patentinfo,inputs=id_input,outputs=[patentmaindata_apps,patentmaindata_news,patentmaindata_cpcs])
   
   with gr.Tab('Techreport'):
      con_btn = gr.Button("continue")
      text_output = gr.Textbox(label='output')
      con_btn.click(fn=gptinfo,inputs=id_input,outputs=text_output)

if __name__=="__main__":
   demo.launch(share=False)