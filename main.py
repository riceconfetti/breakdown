from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")

base_url = "https://twitter.com/"
payload = "search?q=(from:{}) lang:{}&src=typed_query&f=live"
tweets = []
un = "sanhabot"
languages = ["en","ko"]

def scrape_profile(username):
   profile_url = base_url + username
   driver.get(profile_url)
   WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Home timeline"]')))
   timeline = driver.find_elements(By.CSS_SELECTOR,'[aria-label="Home timeline"]')[0]
   profile = timeline.find_elements(By.CSS_SELECTOR, 'div.css-1dbjc4n div.css-1dbjc4n.r-16y2uox div.css-1dbjc4n.r-1jgb5lz.r-13qz1uu div.css-1dbjc4n div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv')[0]
   f.write(profile.get_attribute('outerHTML'))
   
   user_data = {
      "bio" : profile.find_element(By.CSS_SELECTOR, '[data-testid="UserDescription"]').text,
      "following": profile.find_element(By.CSS_SELECTOR, 'a[href="/{username}/following"] span span').text,
      "followers": profile.find_element(By.CSS_SELECTOR, 'a[href="/{username}/followers"] span span').text,
      "joined": profile.find_element(By.CSS_SELECTOR, '[data-testid="UserJoinDate"]').text,
   }
   
   return user_data
   
def scrape_tweets(username):
   for lg in languages:
      f = open(username + "_" + lg+".json", "a", encoding="utf-8")
      load = payload.format(username, lg)
      end = False
      y = 0
      tweet_count = 0
      last_tweet = None
      #driver.implicitly_wait(5000)
      driver.get(base_url + load) 
      
      while(~end):
         wait("[data-testid='tweet']")   
         tweets_elem = driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
         
         if (y == driver.execute_script("return document.body.scrollHeight")):
            end = True
         
         tweets_elem = driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
         
         if (last_tweet != None):
            while (tweets_elem[0] != last_tweet):
               tweets_elem.pop(0)
            tweets_elem.pop(0)

         
         for tW in tweets_elem:           
            try:
               wait("[data-testid='tweet']")
               tweet = parse_tweet(tW, lg)
               
               if (tweet["date"] == date.today() - timedelta(weeks=26)):
                  end = True
                  break
               
               tweets.append(tweet)
               print(tweet_count)
               tweet_count += 1
            except(Exception):
               return Exception
               
         if (end):
            break
         
         tweets_elem = driver.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
         last_tweet = tweets_elem[-1]
         res = tweets_elem[-1].rect
         height = res["y"] + res["height"]
         
         driver.execute_script("window.scrollTo(0, {});".format(height))
         y = height
   
      print(tweet_count)

def parse_tweet(tW, lg):
   tweet = {
               "date": tW.find_elements(By.CSS_SELECTOR,'[data-testid="User-Names"] div div div a time')[0].get_attribute("datetime"),
               "content": {tW.find_element(By.CSS_SELECTOR,'[data-testid="tweetText"]').text},
               "language": lg
            }
   return tweet



def wait(value):
   try:
      WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, value)))
   except (NoSuchElementException, TimeoutException):
      print('{} not found'.format(value))
      exit()
    
scrape_tweets(un)
driver.quit
