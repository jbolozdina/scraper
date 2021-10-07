import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.rdveikals.lv/categories/lv/417/sort/1/filter/0_0_0_161000.171851.161359.167608.161233/page/1/Videokartes.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
productGrids = soup.find_all(True, {'class':[
    'product-list product-list--grid product-list--with-overlay row row--pad block-top block-none-bottom', # top row
    'product-list product-list--grid product-list--with-overlay row row--pad block' # remaining grid
    ]})

productBlocks = []
for gridElement in productGrids:
    productBlocks += gridElement.find_all("li", class_="col col--xs-4 product js-product js-touch-hover")

products = dict()
for product in productBlocks:
    productTitle = product.find(class_="product__info").find(class_="product__title").text.strip()
    productTitle = productTitle.replace("\r\n                                ", " ") # clear spaces
    productPrice = product.find(class_="product__info").find(class_="price").get_text(strip=True)
    productPrice = productPrice.replace("€", "") # get rid of euro sign
    products[productTitle] = float(productPrice)

for product, price in products.items():
    print("Product Name:", product, "\nProduct Price:", price)

with open("products.json", "w") as outfile:
    json.dump(products, outfile, indent = 4)