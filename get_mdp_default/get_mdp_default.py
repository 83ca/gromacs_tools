import urllib3
from bs4 import BeautifulSoup

url = "http://manual.gromacs.org/online/mdp_opt.html"

http = urllib3.PoolManager()
req = http.request('GET', url)

soup = BeautifulSoup(req.data, 'html.parser')
