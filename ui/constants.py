from dataclasses import dataclass


@dataclass(frozen=True)
class StockOption:
    ticker: str
    name: str
    suggested_start_date: str


COMMON_STOCKS: list[StockOption] = [
    StockOption("AAPL", "Apple Inc.", "1980-12-12"),
    StockOption("MSFT", "Microsoft Corporation", "1986-03-13"),
    StockOption("NVDA", "NVIDIA Corporation", "1999-01-22"),
    StockOption("AMZN", "Amazon.com Inc.", "1997-05-15"),
    StockOption("GOOGL", "Alphabet Inc. Class A", "2004-08-19"),
    StockOption("GOOG", "Alphabet Inc. Class C", "2004-08-19"),
    StockOption("META", "Meta Platforms Inc.", "2012-05-18"),
    StockOption("TSLA", "Tesla Inc.", "2010-06-29"),
    StockOption("BRK-B", "Berkshire Hathaway Inc. Class B", "1996-05-09"),
    StockOption("JPM", "JPMorgan Chase & Co.", "1980-03-17"),
    StockOption("V", "Visa Inc.", "2008-03-19"),
    StockOption("LLY", "Eli Lilly and Company", "1972-06-01"),
    StockOption("UNH", "UnitedHealth Group Inc.", "1984-10-17"),
    StockOption("XOM", "Exxon Mobil Corporation", "1970-01-02"),
    StockOption("MA", "Mastercard Inc.", "2006-05-25"),
    StockOption("AVGO", "Broadcom Inc.", "2009-08-06"),
    StockOption("JNJ", "Johnson & Johnson", "1970-01-02"),
    StockOption("PG", "Procter & Gamble Co.", "1970-01-02"),
    StockOption("HD", "Home Depot Inc.", "1981-09-22"),
    StockOption("COST", "Costco Wholesale Corporation", "1986-07-09"),
    StockOption("MRK", "Merck & Co. Inc.", "1970-01-02"),
    StockOption("ABBV", "AbbVie Inc.", "2013-01-02"),
    StockOption("ADBE", "Adobe Inc.", "1986-08-13"),
    StockOption("CRM", "Salesforce Inc.", "2004-06-23"),
    StockOption("NFLX", "Netflix Inc.", "2002-05-23"),
    StockOption("AMD", "Advanced Micro Devices Inc.", "1972-09-27"),
    StockOption("PEP", "PepsiCo Inc.", "1972-06-01"),
    StockOption("KO", "Coca-Cola Co.", "1962-01-02"),
    StockOption("WMT", "Walmart Inc.", "1972-08-25"),
    StockOption("BAC", "Bank of America Corporation", "1973-02-21"),
    StockOption("ORCL", "Oracle Corporation", "1986-03-12"),
    StockOption("CSCO", "Cisco Systems Inc.", "1990-02-16"),
    StockOption("ACN", "Accenture plc", "2001-07-19"),
    StockOption("MCD", "McDonald's Corporation", "1970-01-02"),
    StockOption("TMO", "Thermo Fisher Scientific Inc.", "1980-03-17"),
    StockOption("INTC", "Intel Corporation", "1980-03-17"),
    StockOption("DIS", "The Walt Disney Company", "1962-01-02"),
    StockOption("ABT", "Abbott Laboratories", "1970-01-02"),
    StockOption("WFC", "Wells Fargo & Company", "1972-06-01"),
    StockOption("QCOM", "Qualcomm Inc.", "1991-12-13"),
    StockOption("IBM", "International Business Machines Corporation", "1962-01-02"),
    StockOption("TXN", "Texas Instruments Inc.", "1972-06-01"),
    StockOption("CAT", "Caterpillar Inc.", "1962-01-02"),
    StockOption("NOW", "ServiceNow Inc.", "2012-06-29"),
    StockOption("AMAT", "Applied Materials Inc.", "1972-10-05"),
    StockOption("GE", "GE Aerospace", "1962-01-02"),
    StockOption("UBER", "Uber Technologies Inc.", "2019-05-10"),
    StockOption("SHOP", "Shopify Inc.", "2015-05-21"),
    StockOption("PLTR", "Palantir Technologies Inc.", "2020-09-30"),
    StockOption("BA", "Boeing Company", "1962-01-02"),
]