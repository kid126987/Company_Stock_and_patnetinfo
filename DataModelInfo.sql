DROP TABLE IF EXISTS CompanyBaseInfo;
DROP TABLE IF EXISTS StockPriceInfo;
DROP TABLE IF EXISTS StockRevenue;
DROP TABLE IF EXISTS StockDividend;
DROP TABLE IF EXISTS StockPERIndex;
DROP TABLE IF EXISTS StockNews;
DROP TABLE IF EXISTS StockInvestorsBuy;
DROP TABLE IF EXISTS StockCashflow;
DROP TABLE IF EXISTS StockBalance;
DROP TABLE IF EXISTS StockFinancial;
DROP TABLE IF EXISTS PatentMain;
DROP TABLE IF EXISTS PatentClass;
DROP TABLE IF EXISTS PatentText;


CREATE TABLE CompanyBaseInfo(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode VARCHAR(10) , --股票號碼
    CompanyNameC VARCHAR(50), --公司名稱
    CompanyNameE VARCHAR(50), --英文簡稱
    ChairmanName VARCHAR(10), --董事長
    EstablishmentDate date, --成立時間
    ListingDate date, --掛牌日期
    CompanyClass VARCHAR(10), --產業類別
    Webside varchar(50), --公司網站
    CompanyEmail varchar(50), --電子郵件
    GeneralManager varchar(50), --總經理
    CompanyAddress varchar(50), --公司住址
    MarketClass varchar(10), --市場別
    MainBusinessActivities varchar(50) --主要業務說明
);

CREATE TABLE StockPriceInfo(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode), --台灣股票代號
    StockDate date, --股價時間點
    StockClose decimal, --股票收盤價
    TradingVolume decimal,
    Tradingmoney decimal,
    RSV decimal, --RSV value
    KValue decimal, --KValue value
    DValue decimal  --DValue value
);


CREATE TABLE StockRevenue(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    RevenueYear int,--收益年分
    RevenueMonth int,--收益月份
    TotalRevenue decimal--公司總收益
);

CREATE TABLE StockDividend(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo varchar(20), --年度與季度
    CashDividends decimal, --現金股息
    StockDividend decimal, --股票股息
    ExDividendDate Date, --除息日資訊
    CashDividendDate Date --股息或股利發送時間點
);

CREATE TABLE StockPERIndex(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    YieldRate decimal, --殖利率
    PER decimal, --本益比
    PBR decimal  --股價淨值比
);

CREATE TABLE StockFinancial(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    Types varchar(30), --損益類別
    DataValue decimal, --損益數值
    OriginName varchar(30) --損益類別原始名稱
);

CREATE TABLE StockBalance(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    Types varchar(30), --資產負債類別
    DataValue decimal, --負債數值
    OriginName varchar(30) --資產負債類別原始名稱
);

CREATE TABLE StockCashflow(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    Types varchar(30), --現金流量類別
    DataValue decimal, --流量數值
    OriginName varchar(30) --流量類別原始名稱
);

CREATE TABLE StockInvestorsBuy(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    Buy decimal, --購買量
    Names varchar(30), --法人名稱
    Sell decimal --賣出量
);

CREATE TABLE StockNews(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    Title varchar(1000), --新聞標題
    PublishTime varchar(100), -- 新聞發布時間
    NewsLink varchar(1000) --新聞連結
);



CREATE TABLE PatentMain(
    Dataid VARCHAR(50) PRIMARY KEY ,
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    PatentNumber varchar(30),--專利號碼
    PatentApplicationDate date, --專利申請日
    PatentPubDate date, -- 專利公開公告日
    PatentApplicationDateYear int, --專利申請年分
    PatentPubDateYear int --專利公開公告年分
);

CREATE TABLE PatentClass(
    Dataid VARCHAR(50) PRIMARY KEY ,
    PatentNumber varchar(30) REFERENCES PatentMain(PatentNumber), --專利號碼
    PatnetCPCCode varchar(30) --專利技術分類號
);

CREATE TABLE PatentText(
    Dataid VARCHAR(50) PRIMARY KEY ,
    PatentNumber varchar(30) REFERENCES PatentMain(PatentNumber), --專利號碼
    PatnetTitle varchar, --專利標題
    PatentAbs varchar --專利摘要
);








