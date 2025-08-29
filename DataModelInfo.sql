DROP TABLE IF EXISTS CompanyBaseInfo;
DROP TABLE IF EXISTS StockPriceInfo;
DROP TABLE IF EXISTS stockRevenue;
DROP TABLE IF EXISTS stockDividend;
DROP TABLE IF EXISTS stockPERIndex;
DROP TABLE IF EXISTS PatentMain;
DROP TABLE IF EXISTS PatentClass;
DROP TABLE IF EXISTS PatentText;


CREATE TABLE CompanyBaseInfo(
    StockCode VARCHAR(10) PRIMARY KEY,
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
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode), --台灣股票代號
    StockDate date, --股價時間點
    StockClose decimal, --股票收盤價
    RSV decimal, --RSV value
    KValue decimal, --KValue value
    DValue decimal, --DValue value
    PRIMARY KEY (StockCode, StockDate)
);


CREATE TABLE stockRevenue(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    RevenueYear int,--收益年分
    RevenueMonth int,--收益月份
    TotalRevenue decimal,--公司總收益
    PRIMARY KEY (StockCode,RevenueYear,RevenueMonth)
);

CREATE TABLE stockDividend(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    Dateinfo varchar(20), --年度與季度
    CashDividends decimal, --現金股息
    StockDividend decimal, --股票股息
    ExDividendDate Date, --除息日資訊
    CashDividendDate Date, --股息或股利發送時間點
    PRIMARY KEY (StockCode, DateInfo)
);

CREATE TABLE stockPERIndex(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    DateInfo date, --每日時間
    YieldRate decimal, --殖利率
    PER decimal, --本益比
    PBR decimal, --股價淨值比
    PRIMARY KEY (StockCode, DateInfo)
);

CREATE TABLE PatentMain(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),--台灣股票代號
    PatentNumber varchar(30),--專利號碼
    PatentApplicationDate date, --專利申請日
    PatentPubDate date, -- 專利公開公告日
    PatentApplicationDateYear int, --專利申請年分
    PatentPubDateYear int, --專利公開公告年分
    PRIMARY KEY (StockCode, PatentNumber)
);

CREATE TABLE PatentClass(
    PatentNumber varchar(30) REFERENCES PatentMain(PatentNumber), --專利號碼
    PatnetCPCCode varchar(30), --專利技術分類號
    PRIMARY KEY (PatentNumber, PatnetCPCCode)
);

CREATE TABLE PatentText(
    PatentNumber varchar(30) PRIMARY KEY REFERENCES PatentMain(PatentNumber), --專利號碼
    PatnetTitle varchar, --專利標題
    PatentAbs varchar --專利摘要
);







