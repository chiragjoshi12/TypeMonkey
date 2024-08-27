import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard

class MonkeyTyper:
    def __init__(self) -> None:
        # Disable all notifications from selenium
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")

        # Set up webdriver
        self.driver = webdriver.Chrome(options=options)

        # Open MonkeyType
        self.driver.get("https://monkeytype.com/")
        self._switch_to_words()

    def _switch_to_words(self):
        """
        Switches to words tab
        Basically just clicks buttons and refreshes the page
        """
        try:
            # Wait until the elements with the class name "text-button" are present
            f = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "text-button"))
            )

            if len(f) < 4:
                print(f"Expected at least 4 elements, but found {len(f)}.")
                return

            time.sleep(2)
            f[3].click()
            time.sleep(2)

            f = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "text-button"))
            )
            found = False
            for element in f:
                if element.get_attribute("wordcount") == "10":
                    element.click()
                    found = True
                    break

            if not found:
                print("Could not find the element with wordcount = 10.")

            # Reload the page
            self.driver.refresh()

        except Exception as e:
            print(f"An error occurred: {e}")

    def _get_sentence(self):
        """
        Gets the sentence
        All sentences in MonkeyType are in `word`
        In every word, there are <letter> tags

        This function collects everything into one sentence and returns it
        """
        time.sleep(2)
        # Clicks on wordsWrapper
        wordsWrapper = self.driver.find_element(by="id", value="wordsWrapper")
        try:
            wordsWrapper.click()
        except:
            pass

        # gets all the words and make a sentence
        words = self.driver.find_elements(by="class name", value="word")
        sentence = ""

        for word in words:
            # Retry finding letters in case of a stale element exception
            while True:
                try:
                    letters = word.find_elements(by="tag name", value="letter")
                    break  # Exit the loop if successful
                except selenium.common.exceptions.StaleElementReferenceException:
                    letters = word.find_elements(by="tag name", value="letter")

            for letter in letters:
                if not "correct" in letter.get_attribute("class"):
                    sentence += letter.text
            sentence += " "

        return sentence

    def start(self):
        """
        Gets the sentence and starts typing
        """
        sentence = self._get_sentence()

        keyboard.write(sentence, delay=0.04)
        keyboard.press_and_release("enter")
        keyboard.press_and_release("tab")


if __name__ == "__main__":
    typer = MonkeyTyper()
    time.sleep(10)  # Sleeping to allow the user to do stuff before starting
    i = 0
    while True:
        typer.start()
        i += 1
