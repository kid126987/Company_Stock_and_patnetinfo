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
    MainBusinessActivities varchar(50) --主要業務
);

CREATE TABLE StockPriceInfo(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),
    StockDate date,
    StockClose decimal,
    RSV decimal,
    KValue decimal,
    DValue decimal, 
    PRIMARY KEY (StockCode, StockDate)
);


CREATE TABLE stockRevenue(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),
    RevenueYear int,
    RevenueMonth int,
    TotalRevenue decimal,
    PRIMARY KEY (StockCode,RevenueYear,RevenueMonth)
);

CREATE TABLE stockDividend(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),
    Dateinfo varchar(20),
    CashDividends decimal,
    StockDividend decimal,
    ExDividendDate Date,
    CashDividendDate Date,
    PRIMARY KEY (StockCode, DateInfo)
);

CREATE TABLE stockPERIndex(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),
    DateInfo date,
    YieldRate decimal,
    PER decimal,
    PBR decimal,
    PRIMARY KEY (StockCode, DateInfo)
);

CREATE TABLE PatentMain(
    StockCode varchar(10) REFERENCES CompanyBaseInfo(StockCode),
    PatentNumber varchar(30),
    PatentApplicationDate date,
    PatentPubDate date,
    PatentApplicationDateYear int,
    PatentPubDateYear int,
    PRIMARY KEY (StockCode, PatentNumber)
);

CREATE TABLE PatentClass(
    PatentNumber varchar(30) REFERENCES PatentMain(PatentNumber),
    PatnetCPCCode varchar(30),
    PRIMARY KEY (PatentNumber, PatnetCPCCode)
);

CREATE TABLE PatentText(
    PatentNumber varchar(30) PRIMARY KEY REFERENCES PatentMain(PatentNumber),
    PatnetTitle varchar,
    PatentAbs varchar
);







