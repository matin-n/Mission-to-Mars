# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# Scrape Articles
def mars_news(browser):
    try:
        # Visit the Mars news site
        url = 'https://redplanetscience.com'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Parse the HTML
        html = browser.html
        news_soup = soup(html, 'html.parser')
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the content title
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    return news_title, news_p


# Space Images Featured Images
def featured_image(browser):
    try:
        # Visit URL
        url = 'https://spaceimages-mars.com'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    except AttributeError:
        return None
    return img_url


# Scrape Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df.columns = ['Description', 'Mars', 'Earth']
        df.set_index('Description', inplace=True)
    except BaseException:
        return None
    # Convert dataframe into HTML format
    return df.to_html(classes="table table-bordered")


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
