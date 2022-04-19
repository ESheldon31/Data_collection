# Data Collection Pipeline

### Overview
In this project, I have created a general webscraper module that uses Selenium and Requests to extract data from a website. This is then stored in an AWS RDS database and accessed using SQLAlchemy and PostgreSQL. 

I will perform unit testing and integration testing before using Docker to containerise the application and deploy it to an EC2 instance. Using GitHub Actions, I will set up a CI/CD pipeline to push a new Docker image. I will monitor the container using Prometheus and create dashboards to visualise those metrics using Grafana.

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


