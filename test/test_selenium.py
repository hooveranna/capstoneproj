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

    def test_blns3(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns4(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("0xffffffff")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns5(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("Ω≈ç√∫˜µ≤≥÷")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns6(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็ ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็ ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns7(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("<foo val=“bar” />")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns8(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("部落格")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns9(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("בְּרֵאשִׁית, בָּרָא אֱלֹהִים, אֵת הַשָּׁמַיִם, וְאֵת הָאָרֶץ" )
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns10(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("・(￣∀￣)・:*:")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns11(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys("Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳ ̞̥̱̳̭r̛̗̘e͙p͠r̼̞̻̭̗e̺̠̣͟s̘͇̳͍̝͉e͉̥̯̞̲͚̬͜ǹ̬͎͎̟̖͇̤t͍̬̤͓̼̭͘ͅi̪̱n͠g̴͉ ͏͉ͅc̬̟h͡a̫̻̯͘o̫̟̖͍̙̝͉s̗̦̲.̨̹͈̣")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns12(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys(
            "'; EXEC sp_MSForEachTable 'DROP TABLE ?'; --̨̹͈̣")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def test_blns13(self):
        self.driver.find_element_by_id("name").send_keys("Test")
        self.driver.find_element_by_id("usertext").send_keys(
            "{% print 'x' * 64 * 1024**3 %}")
        self.driver.find_element_by_id("matchMe").click()
        print(self.driver.title)
        assert "Personality Match -" in self.driver.title

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        print("Test Completed")

# if __name__ == "__main__":
#     unittest.main()