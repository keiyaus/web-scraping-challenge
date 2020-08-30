# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

# Create scrape function
def scrape():
    
    # ------------ Scrape latest Mars news ------------ 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)

    # Create BautifulSoup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the title of the latest article
    step1 = soup.select_one('ul.item_list li.slide')
    news_title = step1.find('div', class_='content_title').get_text()

     # Find the teaser of the latest article
    news_p = step1.find('div', class_='article_teaser_body').get_text()

    # Close the browser after scraping
    browser.quit()

    #  ------------ Scrape JPL Mars space images ------------ 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Navigate to desired page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Create BeautifulSoup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find and extract the current featured image
    step1 = soup.find('figure', class_='lede')
    img = step1.find('a')['href']

    # Create url of the image
    featured_image_url = 'https://www.jpl.nasa.gov' + img

    # Close the browser after scraping
    browser.quit()

    # ------------ Scrape Mars facts ------------ 
    # Visit url and scrape tabular data from webpage
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Convert table into dataframe
    df = tables[0]

    # Read dataframe into html and export codes to file
    table_html = df.to_html(index=False, header=False)
    
    # ------------ Scrape Mars hemisphers data ------------ 
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
   
    # Create list to store scrapped data
    hemisphere_img_urls = []

    # Create list of hemispheres
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    # Create for loop to scrape data from each of the urls
    for h in hemispheres:
        
        # Navigate to each hemisphere's webpage
        browser.click_link_by_partial_text(h)
        
        # Create BeautifulSoup object
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find hemisphere image
        img = soup.find('img', class_='wide-image')['src']
        img_url = f'https://astrogeology.usgs.gov{img}'
        
        # Find title of image
        title = soup.find('div', class_='content').h2.text
        
        # Store data in a dictionary
        hemisphere_img_urls.append({
        'title': title,
        'img_url': img_url
        })
    
        mars_data = {
            'news_title': news_title,
            'news_p': news_p,
            'featured_image': featured_image_url,
            'table_html': table_html,
            'hemisphere': hemisphere_img_urls
        }

    # Close the browser after scraping
    browser.quit()

    return mars_data

if __name__ == "__main__":
    print(scrape())
