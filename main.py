import requests, schedule, time, os, smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = "mypassword"
username = "mylogin"

data = {}

url = "https://www.lamoda.ru/p/mp002xw0yzrn/shoes-remonte-botinki/"
data["price_wanted"] = 6500

def scrape():
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        prices = soup.find_all("span", {"class": "x-premium-product-prices__price"})
        good_price = False
        price = {}
        
        if len(prices) == 1:
            price = prices[0]
        elif len(prices) == 2:
            price = prices[1]
        elif len(prices) == 0: # no price at all - item out of stock
            return good_price 
        
        data["price_now"] = int(float(price["content"]))
        
        if data["price_wanted"] >= data["price_now"]:
            good_price = True

        print(data["price_now"])
        
    except Exception as err: # request returns error
        print(err) 
        
    return good_price


def send_mail():
    if not scrape():
        return
        
    email = f"""<p><a href='{url}'> This item </a> is now {data['price_now']} and you wanted to buy in at least for {data['price_wanted']} </p>"""
    
    server = "smtp.gmail.com"
    port = 587
    s = smtplib.SMTP(host=server, port=port)
    s.starttls()
    s.login(username, password)
    
    msg = MIMEMultipart()
    msg["To"] = username
    msg["From"] = username
    msg["Subject"] = "Good chance to buy some stuff"
    msg.attach(MIMEText (email, "html"))
    s.send_message(msg)
    del(msg)
    print(f"Email notification has been sent. Price now is {data['price_now']}. Price that you wanted is {data['price_wanted']}.")


schedule.every().day.at("12:00").do(send_mail)

while True:
    schedule.run_pending()
    time.sleep(1)