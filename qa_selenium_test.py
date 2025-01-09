import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Test case for validating search functionality
@pytest.fixture(scope="class")
def driver_setup(request):
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)  # Implicit wait
    
    # Attach the driver to the test class instance
    request.cls.driver = driver
    yield
    driver.quit()  # Clean up after tests

@pytest.mark.usefixtures("driver_setup")
class TestTableSearchDemo:
    def test_search_new_york(self):
        # Navigate to the Selenium Playground page
        url = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"
        self.driver.get(url)
        
        logger.info(f"Navigated to {url}")

        # Locate and interact with the search box
        search_box = self.driver.find_element(By.CSS_SELECTOR, "#example_filter input")
        search_box.send_keys("New York")

        logger.info("Entered 'New York' in the search box")

        # Validate the number of search results
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#example tbody tr")
        result_count = sum(1 for row in rows if row.is_displayed())
        assert result_count == 5, f"Expected 5 results for 'New York', found {result_count}"
        
        logger.info(f"Search results for 'New York': {result_count} entries")

        # Validate total entries in the footer text
        footer_text = self.driver.find_element(By.ID, "example_info").text
        assert "24 total entries" in footer_text, f"Expected '24 total entries' in footer, but got '{footer_text}'"

        logger.info(f"Footer text: {footer_text}")


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--capture=sys"])
