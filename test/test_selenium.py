from selenium import webdriver
import unittest

#driver = webdriver.Chrome(executable_path='/Users/sijialuo/Documents/chromedriver')
#
# driver.get("http://127.0.0.1:5000/")
# driver.find_element_by_id("name").send_keys("Test")
# driver.find_element_by_id("usertext").send_keys("null")
# driver.find_element_by_id("matchMe").click()
# time.sleep(5)
# print("Test Completed")
# driver.quit()

class SeleniumTest(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/Users/sijialuo//Documents/chromedriver')
        self.driver.get("http://127.0.0.1:5000")

    def test_blns1(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("null")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns2(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("hasOwnProperty")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title


    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        print("Test Completed")

# if __name__ == "__main__":
#     unittest.main()