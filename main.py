from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

from solver import dropdown_solver, fill_in_solver, multiple_choice_solver

# set up options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option("detach", True)

# set up chrome webdriver
driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

# set up action chains
action_chains = ActionChains(driver)

# open the Ximera
driver.get("https://ximera.osu.edu/")

input("Please navigate to the first Ximera page you want to solve and press enter...")

sleep(0.5)
driver.switch_to.window(driver.window_handles[0])
sleep(0.5)


def parse_questions() -> dict:
    """
    Parses the questions on the page and returns a dictionary of the question type and the question element
    :return:
    """
    parsed_questions = []
    # Dropdown questions
    dropdown_questions = driver.find_elements(By.XPATH, "//div[contains(@class, 'dropdown word-choice btn-ximera-submit')]")
    for dropdown_question in dropdown_questions:
        parsed_questions.append(("dropdown_solver", dropdown_question))

    # Fill in the blank questions
    fill_in_questions = driver.find_elements(By.XPATH, "//*[contains(@class, 'MathJax')]")
    for fill_in_question in fill_in_questions:
        parsed_questions.append(("fill_in_solver", fill_in_question))

    # Multiple choice questions
    multiple_choice_questions = driver.find_elements(By.XPATH, "//div[contains(@class, 'ximera-horizontal')]")
    for multiple_choice_question in multiple_choice_questions:
        parsed_questions.append(("multiple_choice_solver", multiple_choice_question))

    return parsed_questions


def do_questions() -> None:
    next_page = True
    while next_page:
        # make all hidden elements visible
        css_style = '''
            div {
                visibility: visible !important;
            }
        '''
        driver.execute_script("""
            (function(css) {
                const style = document.createElement('style');
                style.type = 'text/css';
                style.innerHTML = css;
                document.head.appendChild(style);
            })(arguments[0]);
        """, css_style)
        sleep(0.5)
        progress = driver.find_element(By.XPATH, "//div[contains(@class, 'progress-bar bg-success h-100')]").get_attribute("aria-valuenow")
        while int(progress) < 100:
            parsed_questions = parse_questions()
            for item in parsed_questions:
                solver, question = item
                solve = globals()[solver]
                try:
                    solve(question, driver)
                except Exception:
                    pass
            sleep(2)
            progress = driver.find_element(By.XPATH, "//div[contains(@class, 'progress-bar bg-success h-100')]").get_attribute("aria-valuenow")
            sleep(1)
        next_button = driver.find_element(By.XPATH, "//li[contains(@id, 'next-activity')]")
        if "disabled" in next_button.get_attribute("class"):
            next_page = False
        else:
            next_button.click()
            sleep(0.5)


do_questions()
