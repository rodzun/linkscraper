# Web Scraper API with DRF

This is a simple web scraper API that allows users to add a URL to a web page and scrape a list of all the links on the page. The API is built using Django Rest Framework (DRF).

## Features

- Users can see a list of all pages that have been scraped, along with the number of links found.
- Users can see the details of all links on a particular page, including the URL and name.
- Users can add a URL and the system will check for all the links and add them to the database.
- Pagination is available for the list of pages and links.
- Users can see which pages are currently being processed.

## Implementation

- The API is built using Django Rest Framework (DRF).
- Database: SQLite
- Test Suite: PyTest
- Scraping Tool: Beautiful Soup
- Concurrency: Threading library. 

## Installation

1. Clone this repository to your local machine.
    ```
    $ git clone https://github.com/rodzun/linkscraper.git
    ```
2. Install the required dependencies using `pip install -r requirements.txt` using a virtual environment.
3. Run migrations using `python manage.py migrate`.
4. Start the server using `python manage.py runserver`.
5. Endpoints:

    # GET
    * To see the list of scraped pages.
    ```
    http://localhost:8000/api/scraped_pages/
    ``` 
    * To see the list of links in the page number 1. Just change the number to see the list according to the page id.
   ```
   http://localhost:8000/api/scraped_pages/1/links
   ```

   # POST

    * To request scraping a url.
    ```
    http://localhost:8000/api/add_page/
    ```

## Usage

1. Once the project is running after following the steps in the previous point it can be used using different tools like Postman or other similars.
2. The GET endpoints are listed in the previous part. To see the response, different tools can be used. I used Google Chrome with the JSON Formatter Extension (https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en) in order to clean and proper formmating in the web browser.
3. The POST endpoint was tested using **httpie** library to use the following command to scrape https://www.google.com/ web page. Just change that parameter to test other urls.
    ```consolo
    $ http POST http://localhost:8000/api/add_page/ url=https://www.google.com/ 
    ```
4. To run the Test Suite:
- Inside *Tests* folder run the following command:
    ```
    $ pytest
    ```
    or the following to see a more verbose output:
    ```
    $ pytest --verbose
    ```

## Main Dependencies

- Django for web framework.
- Django Rest Framework for API development.
- Requests for HTTP requests.
- BeautifulSoup4 for scraping web pages.
- PyTest for unit testing.
- Threading for concurrency.

For full list of dependencies see requirements.txt file.

## Commentaries

- The Test Suite doesn't cover all posible scenarios. It mainly cover most important points and the idea was to show my skills using different test tools and logic, like patch, mock, etc. This was because of the time constraint.

