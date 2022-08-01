from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com")

base_url = "https://twitter.com/"
payload = "search?q=(from:{}) lang:{}&src=typed_query"
tweets = []
un = "sanhabot"
languages = ["en","ko"]
f = open("output.html", "a", encoding="utf-8")

def scrape_profile(username):
   profile_url = base_url + username
   driver.get(profile_url)
   WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Home timeline"]')))
   timeline = driver.find_elements(By.CSS_SELECTOR,'[aria-label="Home timeline"]')[0]
   profile = timeline.find_elements(By.CSS_SELECTOR, 'div.css-1dbjc4n div.css-1dbjc4n.r-16y2uox div.css-1dbjc4n.r-1jgb5lz.r-13qz1uu div.css-1dbjc4n div.css-1dbjc4n.r-1ifxtd0.r-ymttw5.r-ttdzmv')[0]
   f.write(profile.get_attribute('outerHTML'))
   
   user_data = {
      "bio" : profile.find_element(By.CSS_SELECTOR, 'div.css-901oao.r-1nao33i.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0').text,
      "following": profile.find_element(By.CSS_SELECTOR, "div.css-1dbjc4n.r-13awgt0.r-18u37iz.r-1w6e6rj div.css-1dbjc4n.r-1mf7evn a.css-4rbku5.css-18t94o4.css-901oao.r-1nao33i.r-1loqt21.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0 span.css-901oao.css-16my406.r-1nao33i.r-poiln3.r-1b43r93.r-b88u0q.r-1cwl3u0.r-bcqeeo.r-qvutc0"),
      "followers": profile.find_element(By.CSS_SELECTOR, "div.css-1dbjc4n.r-13awgt0.r-18u37iz.r-1w6e6rj div.css-1dbjc4n a.css-4rbku5.css-18t94o4.css-901oao.r-1nao33i.r-1loqt21.r-37j5jr.r-a023e6.r-16dba41.r-rjixqe.r-bcqeeo.r-qvutc0 span.css-901oao.css-16my406.r-1nao33i.r-poiln3.r-1b43r93.r-b88u0q.r-1cwl3u0.r-bcqeeo.r-qvutc0 span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0"),
      "joined": profile.find_element(By.CSS_SELECTOR, '[data-testid="UserJoinDate"]'),
   }
   
   return user_data
   
def scrape_tweets(username):
   for lg in languages:
      load = payload.format(username, lg)
      driver.get(base_url + load) 
      WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Search timeline"]')))
      timeline = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Timeline: Search timeline"]')[0]
      WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='tweet']")))
      tweets = timeline.find_elements(By.CSS_SELECTOR,'[data-testid="tweet"]')
      
      for tweet in tweets:
         print("\n------------------------\n")
         print(tweet.text)
      #soup = BeautifulSoup(driver.page_source, 'lxml')
     
scrape_tweets(un)
driver.quit
