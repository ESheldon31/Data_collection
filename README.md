# Data Collection Pipeline

### Overview
In this project, I have created a general webscraper module that uses Selenium and Requests to extract data from a website. This is then stored in an AWS RDS database and accessed using SQLAlchemy and PostgreSQL. 

I will perform unit testing and integration testing before using Docker to containerise the application and deploy it to an EC2 instance. Using GitHub Actions, I will set up a CI/CD pipeline to push a new Docker image. I will monitor the container using Prometheus and create dashboards to visualise those metrics using Grafana.

## Websites
The two websites I wanted to scrape were:
- https://inspirassion.com/es/
  
  This website is a collocations dictionary. Collocations are combinations of words that sound natural to a native speaker, e.g. in English, we say 'heavy rain', not 'strong rain.' As a former English teacher, I understand the value of learning collocations and as a current Spanish student, I was interested in scraping this website to get a collection of verbs and adjectives that collocate with a particular noun. I have decided to focus my search on abstract nouns, such as 'libertad' (freedom) and 'curiosidad' (curiosity), as I felt this was a gap in my knowledge at my current level.  
- https://ideas.lego.com 
  
  This is the Lego Ideas website. Anyone can submit an idea for a Lego project and if it receives enough support, it will get made into a real Lego set. I love browsing this website and seeing all the amazing designs. 
  
## Web scraper
I created a general Scraper class using Selenium and Requests. In the constructor, the Selenium Chrome webdriver is initialised. WebDriverManager, in this case ChromeDriverManager, is used to automate the management of the drivers required by Selenium WebDriver.

Using Selenium, I created methods to cover the main actions a user performs when browsing a website. The methods of the Scraper class are:

| Methods that replicate user behaviour    | Methods for 'behind-the-scenes' actions              |
| --------------| -------------
| open_url()    | wait_for()   |
| search()      | get_img_links() 
| click_button() | get_list_links() 
| scroll_up_top() | download_raw_data() |
| scroll_down_bottom() | download_images
|  accept_cookies() | create_uuid() |
| infinite_scroll() | switch_frame()     |
| see_more() | get_html() (uses Requests and BeautifulSoup)|
| next_page() | find_in_html() (uses Requests and BeautifulSoup)|
| quit() | |

Making use of inheritance, I made a child class for each website I wanted to scrape. These inherited all the methods above and allowed me to make some methods specific to each website. 

| Methods specific to LegoScraper | Methods specific to CollocationsScraper |
| -----                           | -------                                 |
| get_info_from_java() | create_dict() |
| create_id() | get_words() |
| get_info_from_html() | get_infinitives() |
| collate_info() | get_frequency() |
| explore_product_ideas() | get_phrases()    |
