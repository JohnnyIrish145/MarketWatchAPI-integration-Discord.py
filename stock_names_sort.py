import requests

def sort(company_name): # Takes the name, for example "Apple"
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    # Returns 'NOT FOUND' if yahoo finance database can not find that specific name
    if len(data["quotes"]) == 0:
        return 'NOT FOUND'
        
    company_code = data['quotes'][0]['symbol']
    return company_code # Returns a company code, for example "AAPL"