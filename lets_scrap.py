import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from termcolor import colored


def print_header(config):
    print(colored("\n---- Let's Scrap these images ----\n", attrs=["bold"]))
    print(colored(f"config : {config}\n", "yellow", attrs=["bold"]))


def hub(config):
    print_header(config)
