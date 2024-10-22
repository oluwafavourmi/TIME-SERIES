import pandas as pd
import requests
import bs4

url = 'https://coincodex.com/crypto/bitcoin/historical-data/'

req = requests.get(url)
soup = bs4.BeautifulSoup(req.content, 'html.parser')
table = soup.find('table')
table_rows = soup.find_all('tr')
rows = table.find_all('tr')

table_data = []
for row in table_rows:
    cells = row.find_all("td")  # Or "th" for header cells
    row_data = [cell.text.strip() for cell in cells]
    table_data.append(row_data)
    
col = ['Date Start', 'Date End', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
df = pd.DataFrame(table_data, columns=col)

df = df.iloc[1:]
df2 = df.drop('Date End', axis='columns')
df3 = df2.reindex(index=df2.index[::-1])
df3['Date'] = pd.to_datetime(df['Date Start'], format='%b %d, %Y')
df4 = df3.drop(['Date Start'], axis='columns')
df5 = df4.reset_index()
df6 = df5.drop('index', axis='columns')

open = pd.DataFrame(df6['Open'].str.replace('$', ''))
high = pd.DataFrame(df6['High'].str.replace('$', ''))
low = pd.DataFrame(df6['Low'].str.replace('$', ''))
close = pd.DataFrame(df6['Close'].str.replace('$', ''))
volume = pd.DataFrame(df6['Volume'].str.replace('$', ''))
market = pd.DataFrame(df6['Market Cap'].str.replace('$', ''))
date = df6['Date']

columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap', 'Date']
df7 = pd.concat([date, open, high, low, close, volume, market ], axis='columns')