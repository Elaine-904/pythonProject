Web scrape & data convert
========================================

-   Backend application built with Python and Flask framework. 
-   The purpose of this application is to scrape data from a user-provided URL and export the data to a CSV, JSON, or TXT file. Additionally, the application allows the user to import their Excel file and automatically convert it to a JSON file.

Prerequisites
-------------

To run this application, you need to have Python 3.x installed on your machine, as well as the following Python libraries:

-   Flask
-   BeautifulSoup

You can install these libraries using pip

`pip install flask`

Running the Application
-----------------------

Run `app.py` file:

`python app.py`

This will start the Flask development server and the application will be available at `http://localhost:5000`.

Usage
-----

The application provides two main functionalities:

1.  Scraping Data: To scrape data from a URL
Enter the URL you want to scrape in the input field and select the output format (CSV, JSON, or TXT) from the dropdown. Click on the "Scrape" button to start scraping. The scraped data will be exported to a file with the chosen format and downloaded to your computer.

2.  Importing Excel Files: To import an Excel file and convert it to JSON
Click on the "Choose File" button and select the Excel file you want to import. Click on the "Upload" button to start the import process. The Excel file will be converted to JSON and downloaded to your computer.

Contributing
------------

If you find any issues with the application or would like to contribute to its development, feel free to create an issue or submit a pull request on the GitHub repository.

License
-------

This application is licensed under the MIT license. See the LICENSE file for more details.
