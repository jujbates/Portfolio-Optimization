import requests


class WikipediaSocket:
    """
        Socket for Wikipedia's S&P 500 data
    """
    def __init__(self):
        self.input_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


class SlickSocket:
    """
        Socket for Slick's S&P 500 data
    """
    def __init__(self):
        self.input_url = 'https://www.slickcharts.com/sp500'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/50.0.2661.102 '
                                      'Safari/537.36'}

    def get(self):
        return requests.get(self.input_url, headers=self.headers)
