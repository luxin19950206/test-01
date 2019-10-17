# encoding: UTF-8

import sys
sys.path.append('..')
from ctaAlgo.datayesClient import DatayesClient


def demo():
    datayes_client = DatayesClient()

    path = 'api/market/getMktFutd.json'

    params = {}
    params['ticker'] = 'rb1705'
    params['beginDate'] = '20170301'
    params['endDate'] = '20170321'

    result = datayes_client.downloadData(path, params)

    print result

if __name__ == '__main__':
    demo()