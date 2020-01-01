{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "import pandas as pd\n",
    "import datetime as dt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "!which chromedriver"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "NASA MARS NEWS"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape():\n",
    "    \n",
    "    # Set executable Path and initialize Chrome Browser (fo Mac)\n",
    "    executable_path = {\"executable_path\": \"/usr/local/bin/chromedriver\"}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "    news_title, news_p = nasa_mars_news(browser)\n",
    "    \n",
    "    # Run all scraping functions and store in dictionary.\n",
    "    results = {\n",
    "        'news_title': news_title,\n",
    "        'news_paragraph': news_p,\n",
    "        'featured_image': featured_img_url(browser),\n",
    "        'facts': table_facts(),\n",
    "        'weather': mars_twitter_weather(browser),\n",
    "        'hemispheres': hemisphere_image_urls(browser)\n",
    "    }\n",
    "    \n",
    "    # Quit browser and return scraped results\n",
    "    browser.quit()\n",
    "    return results\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "def nasa_mars_news(browser):\n",
    "    mars_url = 'https://mars.nasa.gov/news/'\n",
    "    browser.visit(mars_url)\n",
    "    mars_html = browser.html\n",
    "    mars_soup = soup(mars_html, 'html.parser')\n",
    "    \n",
    "    #Scrape the first article title and teaser paragraph text\n",
    "    news_title = mars_soup.find('div', class_='content_title').get_text()\n",
    "    news_p = mars_soup.find('div', class_='article_teaser_body').get_text()\n",
    "    return news_title, news_p    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def featured_image(browser):\n",
    "    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(jpl_url)\n",
    "    \n",
    "    #Find and click the Full Image button\n",
    "    full_image_button = browser.find_by_id(\"full_image\")\n",
    "    full_image_button.click()\n",
    "    \n",
    "    # Find the More Info button and click that\n",
    "    browser.is_element_present_by_text(\"more info\", wait_time=1)\n",
    "    more_info_element = browser.find_link_by_partial_text(\"more info\")\n",
    "    more_info_element.click()\n",
    "    \n",
    "    # Parse the html with BeautifulSoup\n",
    "    jpl_html = browser.html\n",
    "    jpl_img_soup = soup(jpl_html, 'html.parser')\n",
    "    \n",
    "    # Find the image url\n",
    "    featured_img_url = jpl_img_soup.select_one('figure.lede a img').get('src')\n",
    "    \n",
    "    #Use base url to create complete url\n",
    "    featured_img_url = f'https://www.jpl.nasa.gov{featured_img_url}'\n",
    "    \n",
    "    return featured_img_url\n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "def table_facts():\n",
    "    mars_facts_df = pd.read_html('https://space-facts.com/mars/')\n",
    "    table_facts = mars_facts_df[0]\n",
    "        \n",
    "    table_facts.columns = ['Description', 'Value']\n",
    "    table_facts.set_index('Description', inplace=True)\n",
    "    \n",
    "    table_facts.to_html(classes='table table-striped')\n",
    "            "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "def mars_twitter_weather(browser):\n",
    "    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'\n",
    "    browser.visit(mars_weather_url)\n",
    "    \n",
    "    mars_weather_html = browser.html\n",
    "    mars_weather_soup = soup(mars_weather_html, 'html.parser')\n",
    "    \n",
    "    # Scrape tweet info and return\n",
    "    mars_twitter_weather = mars_weather_soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()\n",
    "    return mars_twitter_weather\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (<ipython-input-11-da860e893946>, line 25)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-11-da860e893946>\"\u001b[0;36m, line \u001b[0;32m25\u001b[0m\n\u001b[0;31m    if__name__== '__main__':\u001b[0m\n\u001b[0m                            ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "def hemisphere_image_urls(browser):\n",
    "    hemi_image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(hemi_image_url)\n",
    "    \n",
    "    # Parse the html with BeautifulSoup\n",
    "    hemisphere_html = browser.html\n",
    "    hemisphere_soup = soup(hemisphere_html, 'html.parser')\n",
    "    \n",
    "    hemi_strings = []\n",
    "    links = hemisphere_soup.find_all('h3')\n",
    "\n",
    "    for hemi in links:\n",
    "        hemi_strings.append(hemi.text)\n",
    "        \n",
    "    # Initialize hemisphere_image_urls list\n",
    "    hemisphere_image_urls = []\n",
    "    \n",
    "    hemisphere_image_urls.append({\n",
    "                    'title': link['title'].replace(' Enhanced', ''),\n",
    "                    'img_url': img_url,\n",
    "            })\n",
    "    \n",
    "    return hemisphere_image_urls\n",
    "\n",
    "if__name__== '__main__':\n",
    "    \n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
