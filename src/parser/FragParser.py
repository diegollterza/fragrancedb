import os
import sys
import re
from bs4 import BeautifulSoup
import pandas as pd


class FragranticaParser:

    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.name = self.get_name(soup)
        self.company = self.get_company(soup)
        self.perfumer = self.get_perfumer(soup)
        self.accords = self.get_accords(soup)
        self.top_notes = self.get_notes(soup, "top")
        self.middle_notes = self.get_notes(soup, "middle")
        self.base_notes = self.get_notes(soup, "base")
        self.year = self.get_launch_year(soup)
        soup.decompose()

    def get_notes(soup, level):
        notes = []
        notes_soup = soup.find("pyramid-level", notes=level)
        try:
            for div in notes_soup.find_all("div"):
                if div.parent.name == "div" and div.parent.parent.name == "div":
                    if div.text:
                        notes.append(str(div.text))
        except AttributeError:
            return None
        return notes

    def get_name(soup):
        try:
            value = str(soup.find_all("h1", itemprop="name")[0].contents[0])
        except AttributeError:
            value = None
        return value

    def get_company(soup):
        try:
            value = str(soup.find("span", "brand").contents[0])
        except AttributeError:
            value = None
        return value

    def get_perfumer(soup):
        try:
            perfumer = str(soup.find("img", "perfumer-avatar").parent.find("a").contents[0])
        except AttributeError:
            return None

        return perfumer

    def get_accords(soup):
        accords = soup.find_all("div", "accord-bar")
        accord_list = []
        for accord in accords:
            try:
                accord_list.append(str(accord.contents[0]))
            except AttributeError:
                pass

        return accord_list

    def get_launch_year(soup):
        desc = str(soup.find(itemprop="description"))
        match = re.match(r".*was launched in (\d\d\d\d)\.", desc)
        try:
            year = match.group(1)
        except AttributeError:
            return ""
        return year