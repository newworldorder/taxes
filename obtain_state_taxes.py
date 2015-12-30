from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # source  http://taxfoundation.org/article/state-individual-income-tax-rates-and-brackets-2015
    r = requests.get('https://docs.google.com/spreadsheets/d/1RNmhCqUwrJQX85UQ3OWvP0dODtD_Xh-nWwYW0EwnXmo/pubhtml')

    # parse content of interest 
    tbody = BeautifulSoup(r.content, 'html.parser')
    trs = tbody.find_all('tr')
    acc = ''
    for tr in trs:
        tds_text = [td.text for td in tr.find_all('td')]
        row = '|'.join(tds_text)
        acc += row + '\n'
    acc = acc[:acc.rfind('|||||||||||')]
    # output to a file 
    with open('state_tax_parsed.output', 'w') as f:
        f.write(acc.encode('utf8'))
    
        


