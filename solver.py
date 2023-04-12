from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sympy
from sympy.parsing.latex import parse_latex
from time import sleep
import re


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

    pattern = r'\\answer\s*{([^{}]*(?:{(?:[^{}]*(?:{[^{}]*})*[^{}]*)*})*[^{}]*)}'
    answer_matches = re.findall(pattern, answer_text)

    answers = [tex_to_unicode(answer) for answer in answer_matches]
    for index, input_area in enumerate(input_areas):
        input_area.clear()
        input_area.send_keys(answers[index])
        input_area.send_keys(u'\ue007')


def tex_to_unicode(tex_expression) -> str:
    expr = parse_latex(tex_expression)
    if '|' in tex_expression:
        expr = sympy.pretty(expr, use_unicode=False)
    return str(expr)


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

