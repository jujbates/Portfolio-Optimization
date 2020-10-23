# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from get_data import WikipediaData, SlickData,YahooFinanceData


def main():
    """
        Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed) and then finally
        data processed, features developed features ready to be modeled (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Starting Data Wrangling...')

    # Get data ready for EDA and Feature development
    start = "2019-01-01"
    end = "2020-01-01"

    wd = WikipediaData()
    w_df = wd.df
    ticker_list = w_df.Symbol
    SlickData()
    YahooFinanceData(ticker_list, 'sp500', start, end)
    YahooFinanceData(['^GSPC'], 'sp500_index', start, end)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
