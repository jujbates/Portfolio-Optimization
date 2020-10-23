import os
import pandas as pd
from bs4 import BeautifulSoup
from yahooquery import Ticker
import logging


from api_sockets import WikipediaSocket, SlickSocket

CURRENT_DIR = os.getcwd()
PROJECT_DIR = os.path.abspath(os.path.join(os.path.join(CURRENT_DIR, os.pardir), os.pardir))

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)

DATA_RAW_DIR = '/data/raw/'
DATA_INTERIM_DIR = '/data/interim/'


class WikipediaData:
    """
        Socket for Wikipedia's S&P 500 data
    """

    def __init__(self):
        self.url = None
        self.df = None
        self.raw_file_name = 'wiki_sp500_raw.csv'
        self.interim_file_name = 'wiki_sp500_interim.csv'
        self.get_raw_data()
        self.clean_data()

    def get_raw_data(self):
        try:
            self.df = pd.read_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.raw_file_name}')
            logger.info(f'Creating now...')
            self.url = WikipediaSocket().input_url
            wiki_tables = pd.read_html(self.url)
            self.df = wiki_tables[0]
            self.save_raw_data()

    def clean_data(self):
        try:
            self.df = pd.read_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.interim_file_name}')
            logger.info(f'Creating now...')
            self.df['Symbol'] = self.df['Symbol'].str.replace('.', '-', regex=False)
            self.save_clean_data()

    def save_raw_data(self):
        logger.info(f'Saving now...')
        self.df.to_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_file_name, index=False)

    def save_clean_data(self):
        logger.info(f'Saving now...')
        self.df.to_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_file_name, index=False)


class SlickData:
    """
        Socket for Slick's S&P 500 data
    """

    def __init__(self):
        self.res = None
        self.df = None
        self.raw_file_name = 'slick_sp500_raw.csv'
        self.interim_file_name = 'slick_sp500_interim.csv'
        self.get_raw_data()
        self.clean_data()

    def get_raw_data(self):
        try:
            self.df = pd.read_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.raw_file_name}')
            logger.info(f'Creating now...')
            self.res = SlickSocket().get()
            soup = BeautifulSoup(self.res.content, 'lxml')
            tables = soup.find_all('table')
            self.df = pd.read_html(str(tables[0]))[0]
            self.save_raw_data()

    def clean_data(self):
        try:
            self.df = pd.read_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.interim_file_name}')
            logger.info(f'Creating now...')
            self.save_clean_data()

    def save_raw_data(self):
        logger.info(f'Saving now...')
        self.df.to_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_file_name, index=False)

    def save_clean_data(self):
        logger.info(f'Saving now...')
        self.df.to_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_file_name, index=False)


class YahooFinanceData:
    """
        Socket for Slick's S&P 500 data
    """

    def __init__(self, ticker_list, ticker_set_name, start_date, end_date):
        self.ticker_list = ticker_list
        self.start_date = start_date
        self.end_date = end_date
        self.raw_adj_close_file_name = f'yahoo_{ticker_set_name}_adj_close_raw.csv'
        self.interim_adj_close_file_name = f'yahoo_{ticker_set_name}_adj_close_interim.csv'
        self.raw_shares_outstanding_file_name = f'yahoo_{ticker_set_name}_shares_outstanding_raw.csv'
        self.interim_shares_outstanding_file_name = f'yahoo_{ticker_set_name}_shares_outstanding_interim.csv'
        self.tickers = None
        self.adj_close_df = None
        self.shares_outstanding_df = None
        self.error_tickers = {}

    def get_raw_data(self):
        # Adjusted Closing Price
        save = False
        try:
            self.adj_close_df = pd.read_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_adj_close_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.raw_adj_close_file_name}')
            logger.info(f'Creating now...')
            self.get_raw_data_adj_close()
            save = True

        # Other Price Date
        try:
            self.shares_outstanding_df = pd.read_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_shares_outstanding_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.raw_shares_outstanding_file_name}')
            logger.info(f'Creating now...')
            self.get_raw_data_shares_outstanding()
            save = True
        if save:
            self.save_raw_data()

    def get_raw_data_adj_close(self):
        # Adjusted Closing Price
        if self.tickers is None:
            self.tickers = Ticker(self.ticker_list, asynchronous=True)

        yf_data = self.tickers.history(start=self.start_date, end=self.end_date)
        if isinstance(yf_data, dict):
            good_tickers = []
            error_tickers = {}
            for k, v in yf_data.items():
                if isinstance(v, pd.DataFrame):
                    adj_close_df = pd.DataFrame(v.adjclose)
                    adj_close_df.rename(columns={'adjclose': k}, inplace=True)
                    good_tickers.append(adj_close_df)
                else:
                    error_tickers[k] = v
            self.adj_close_df = pd.concat(good_tickers, axis=1)
            self.adj_close_df.index.name = 'date'
        else:
            adj_close_df = yf_data.adjclose
            adj_close_df.index.name = 'date'
            adj_close_df = adj_close_df.reset_index(level='symbol')
            adj_close_df = adj_close_df.pivot(columns='symbol')
            adj_close_df.columns = [col[1] for col in adj_close_df.columns]
            self.adj_close_df = adj_close_df.copy()

    def get_raw_data_shares_outstanding(self):
        if self.tickers is None:
            self.tickers = Ticker(self.ticker_list, asynchronous=True)
        yf_data_key_stats = self.tickers.key_stats
        bad_ticker_stats = [k for k, v in yf_data_key_stats.items() if isinstance(v, str)]
        [yf_data_key_stats.pop(key) for key in bad_ticker_stats]
        if len(yf_data_key_stats.keys()) > 0:
            sp500_yf_df = pd.DataFrame.from_dict(yf_data_key_stats).T
            self.shares_outstanding_df = sp500_yf_df[['sharesOutstanding']]
            self.shares_outstanding_df.index.name = 'symbol'
        else:
            logger.info(f'No Shares Outstanding for list of symbols.')




    def clean_data(self):
        save = False
        try:
            self.adj_close_df = pd.read_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_adj_close_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.interim_adj_close_file_name}')
            logger.info(f'Creating now...')
            self.clean_data_adj_close()
            save = True

        try:
            self.shares_outstanding_df = pd.read_csv(PROJECT_DIR + DATA_INTERIM_DIR
                                                     + self.interim_shares_outstanding_file_name)
        except FileNotFoundError:
            logger.info(f'File does not exist: {self.interim_shares_outstanding_file_name}')
            logger.info(f'Creating now...')
            self.clean_data_shares_outstanding()
            save = True

        if save:
            self.save_clean_data()

    def clean_data_adj_close(self):
        error_tickers_list = list(self.error_tickers.keys())
        tickers_with_nan_values = self.adj_close_df.columns[self.adj_close_df.isna().any()].tolist()
        [error_tickers_list.append(x) for x in tickers_with_nan_values]
        self.adj_close_df = self.adj_close_df.drop(columns=tickers_with_nan_values)

    def clean_data_shares_outstanding(self):
        if self.shares_outstanding_df is not None:
            error_tickers_list = list(self.error_tickers.keys())
            tickers_with_nan_values = self.shares_outstanding_df.columns[self.shares_outstanding_df.isna().any()].tolist()
            [error_tickers_list.append(x) for x in tickers_with_nan_values]
            self.shares_outstanding_df = self.shares_outstanding_df.drop(columns=tickers_with_nan_values)
        else:
            logger.info(f'No Shares Outstanding for list of symbols.')

    def save_raw_data(self):
        logger.info(f'Saving all raw data now...')
        self.adj_close_df.to_csv(PROJECT_DIR + DATA_RAW_DIR + self.raw_adj_close_file_name, index=True)

        if self.shares_outstanding_df is not None:
            self.shares_outstanding_df.to_csv(PROJECT_DIR + DATA_RAW_DIR
                                              + self.raw_shares_outstanding_file_name, index=True)

    def save_clean_data(self):
        logger.info(f'Saving all clean data now...')
        self.adj_close_df.to_csv(PROJECT_DIR + DATA_INTERIM_DIR + self.interim_adj_close_file_name, index=True)
        if self.shares_outstanding_df is not None:
            self.shares_outstanding_df.to_csv(PROJECT_DIR + DATA_INTERIM_DIR
                                              + self.interim_shares_outstanding_file_name, index=True)
