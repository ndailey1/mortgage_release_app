from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_release_data(volume, page):
    # Set up headless Chrome (runs without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get('https://recordhub.cottsystems.com/WindsorLocksCT/Search/Records')
        # Wait for the username field to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="UserName"]'))
        )

        # Login
        driver.find_element("xpath", '//*[@id="UserName"]').send_keys('czapiga24@gmail.com')
        driver.find_element("xpath", '//*[@id="Password"]').send_keys('Quas06248!')
        driver.find_element("xpath", '//*[@id="submit"]').click()

        # Wait for the search type button to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSearchType"]'))
        )

        # Select Book/Page search
        driver.find_element("xpath", '//*[@id="btnSearchType"]').click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="Type"]/ul/li[4]/a'))
        )
        driver.find_element("xpath", '//*[@id="Type"]/ul/li[4]/a').click()

        # Wait for the Book field to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Book"]'))
        )

        # Input Volume and Page
        driver.find_element("xpath", '//*[@id="Book"]').send_keys(volume)
        driver.find_element("xpath", '//*[@id="Page"]').send_keys(page)
        driver.find_element("xpath", '//*[@id="search-btn"]').click()

        # Wait for search results
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="search-results-table"]/tbody/tr[1]/td[3]/a[3]'))
            )
            driver.find_element("xpath", '//*[@id="search-results-table"]/tbody/tr[1]/td[3]/a[3]').click()

            # Wait for related documents
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'td[class="childData"]'))
            )
            child_elements = driver.find_elements(By.CSS_SELECTOR, 'td[class="childData"]')
            for child_element in child_elements:
                if 'REL' in child_element.text:
                    date_filed = child_element.text.split('Filed:')[1].split(' ')[1]
                    volume_data = child_element.text.split('Volume:')[1].split(' ')[1]
                    page_data = child_element.text.split('Page:')[1].split(' ')[1]
                    return {
                        "Date Filed": date_filed,
                        "Volume": volume_data,
                        "Page": page_data,
                        "Mortgage Volume": volume,
                        "Mortgage Page": page
                    }
            # No release found
            return {
                "Date Filed": "No Release",
                "Volume": "N/A",
                "Page": "N/A",
                "Mortgage Volume": volume,
                "Mortgage Page": page
            }
        except:
            return {
                "Date Filed": "No Release",
                "Volume": "N/A",
                "Page": "N/A",
                "Mortgage Volume": volume,
                "Mortgage Page": page
            }
    finally:
        driver.quit()

if __name__ == "__main__":
    # Test the function
    result = get_release_data("115", "341")
    print(result)
