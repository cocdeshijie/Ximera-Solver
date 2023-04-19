from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sympy
from pylatexenc.latex2text import LatexNodes2Text
from time import sleep
import regex


def dropdown_solver(element, driver) -> None:
    dropdown_menu = element.find_element(By.XPATH, ".//div[contains(@class, 'dropdown-menu')]")
    open_menu = element.find_element(By.XPATH, ".//button[contains(@data-toggle, 'dropdown')]").click()
    correct_choice = dropdown_menu.find_element(By.XPATH, ".//button[contains(@class, 'correct')]").click()


def fill_in_solver(element, driver) -> None:
    inner_mathjax = element.find_element(By.XPATH, ".//nobr[contains(@aria-hidden, 'true')]")
    input_areas = inner_mathjax.find_elements(By.XPATH, ".//input[contains(@class, 'form-control')]")
    input_area = input_areas[0]

    # magic, get answers from new window
    action_chains = ActionChains(driver)
    driver.execute_script("arguments[0].scrollIntoView();", input_area)
    driver.execute_script("window.scrollBy(0, -200);")
    # right click on input
    action_chains.context_click(input_area).perform()
    sleep(0.1)
    # find mathjax menu
    mathjax_menu = driver.find_elements(By.CLASS_NAME, "MathJax_ContextMenu")[0]
    # find menu item with text "Show Math As"
    show_math_as = mathjax_menu.find_elements(By.XPATH, "//div[contains(text(), 'Show Math As')]")[0]
    # hover over menu item
    action_chains.move_to_element(show_math_as).perform()
    sleep(0.1)
    # find menu item with text "TeX Commands"
    tex_commands = mathjax_menu.find_elements(By.XPATH, "//div[contains(text(), 'TeX Commands')]")[0]
    # click on menu item
    tex_commands.click()
    # get content from popup tab opened
    popup = driver.window_handles[1]
    driver.switch_to.window(popup)
    # get all text from popup
    answer_text = driver.find_elements(By.TAG_NAME, "pre")[0].text
    # close popup
    driver.close()
    # switch back to main tab
    driver.switch_to.window(driver.window_handles[0])

    answer_matches = extract_answer_brackets(answer_text)

    cleaned_answers = clean_answers(answer_matches)

    answers = [tex_to_string(answer) for answer in cleaned_answers]

    for index, input_area in enumerate(input_areas):
        input_area.clear()
        input_area.send_keys(answers[index])
        input_area.send_keys(u'\ue007')


def tex_to_string(tex_expression) -> str:

    result = LatexNodes2Text().latex_to_text(latex=tex_expression)
    result = result.replace("√", "sqrt")
    result = result.replace("cos", " cos")
    result = result.replace("sin", " sin")
    result = result.replace("tan", " tan")
    result = result.replace("cot", " cot")
    result = result.replace("sec", " sec")
    result = result.replace("csc", " csc")
    return str(result)


def extract_answer_brackets(text) -> list:
    result = []
    stack = []
    index = 0

    while index < len(text):
        if text[index:index + 8] == '\\answer ':
            index += 8
            if text[index] == '{':
                stack.append(index)
                level = 1
                index += 1
                start = index

                while index < len(text) and level > 0:
                    if text[index] == '{':
                        level += 1
                    elif text[index] == '}':
                        level -= 1
                    index += 1

                if level == 0:
                    result.append(text[start:index - 1])
        else:
            index += 1

    return result


def clean_answers(answers) -> list:
    result = []
    for answer in answers:
        # Define the regex pattern
        pattern = r'(?<!\\[a-zA-Z]+)\{([^\{\}]+)\}'
        # Replace the matched pattern with the desired format
        result.append(regex.sub(pattern, r'{(\1)}', answer))
    return result


def multiple_choice_solver(element, driver) -> None:
    options_group = element.find_element(By.CLASS_NAME, "btn-group-vertical")
    # get all buttons under the options group
    options = options_group.find_elements(By.TAG_NAME, "button")
    # loop through all options with correct class and click correct one
    for option in options:
        if "correct" in option.get_attribute("class"):
            option.send_keys(Keys.SPACE)
    check_work_button = element.find_element(By.CLASS_NAME, "btn-ximera-submit")
    check_work_button.send_keys(Keys.SPACE)

