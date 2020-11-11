from dotenv import find_dotenv, load_dotenv
import os

from portfolio_tools import PortfolioDataRequest
from portfolio_tools import PortfolioOptimization
from portfolio_tools import PortfolioReturns


"""
    Script for portfolio optimization pipeline research
    https://medium.com/swlh/automatic-portfolio-optimization-3a50558fd7e8
    By: Roman Paolucci
"""

if __name__ == '__main__':

    load_dotenv(find_dotenv())
    PORTFOLIO = 'AAPL MSFT JNJ JPM XOM WMT UNH PFE VZ V BA'  # os.getenv('PORTFOLIO')
    stocks = PORTFOLIO.split()
    data = PortfolioDataRequest(
            stocks,
            '2010-01-01',
            '2017-01-01'
            )
    print(data.table)
    optimization = PortfolioOptimization(data.table)
    optimization.report_discrete_allocation()
    returns = PortfolioReturns(
            stocks,
            optimization.allocation,
            '2017-01-01',
            '2018-01-01'
            )
    returns.report_returns()
