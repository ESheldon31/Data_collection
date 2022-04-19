# Data Collection Pipeline

### Overview
In this project, I have created a general webscraper module that uses Selenium and Requests to extract data from a website. This is then stored in an AWS RDS database and accessed using SQLAlchemy and PostgreSQL. 

I will perform unit testing and integration testing before using Docker to containerise the application and deploy it to an EC2 instance. Using GitHub Actions, I will set up a CI/CD pipeline to push a new Docker image. I will monitor the container using Prometheus and create dashboards to visualise those metrics using Grafana.

## Web scraper
I created a general Scraper class using Selenium and Requests. In the constructor, the Selenium Chrome webdriver is initialised. 
WebDriverManager, in this case, ChromeDriverManager, is used to automate the management of the drivers required by Selenium WebDriver.

Using Selenium, I created methods to cover the main actions a user performs when browsing a website. The methods of the Scraper class are:

| Method        | Action            |
| --------------|-------------      |
| open_url()    | Opens a webpage
| search()
