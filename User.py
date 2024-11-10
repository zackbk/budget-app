import pandas as pd
from datetime import date
import json
from os.path import isfile as isfile
from utils.alias_lookup import alias_dict
from numpy import where

class User:
    '''
    Object that defines a user for the budget tool
    '''
    def __init__(self):
        '''
        Initialise the default values for the budget user
        '''

        self._sdir = './output'

        self.username = "user"
        with open("templates.json") as file:
            self.templates = json.load(file)
        self.style = "basic"
        self.items = {}
        self.itemkeys = ("name", "category", "value_input", "freq_input","value_float", "freq_alias")

        self.freq = "D"
        self.budget = pd.DataFrame()


    def __str__(self):
        '''
        When print is invoked, print the user's name and that this is a budget file

        :param x:
        :type x:
        :raise ValueError: If
        return: The username
        rtype: str
        '''
        return (
            f"{self.username}'s "
            if self.username[-1] != "s"
            else f"{self.username}' "
        ) + "budget file\n"

    # getters
    @property
    def username(self):
        return self._username

    @property
    def items(self):
        return self._items

    @property
    def budget(self):
        return self._budget

    @property
    def budget_summary(self):
        return self._budget_summary

    @property
    def style(self):
        return self._style

    @property
    def templates(self):
        return self._templates

    # setters
    @username.setter
    def username(self, username):
        if username == "":
            username = "user"
        self._username = username

    @items.setter
    def items(self, items):
        if not items:
            self._items = items
        for item in items:
            yn = "y"
            if type(items[item]) is not dict:
                yn = "invalid"
            for i in items[item]:
                if i not in self.itemkeys:
                    yn = "invalid"
            if yn == "y":
                self._items = items
            else:
                raise ValueError("Invalid item.")

    @budget.setter
    def budget(self, budget):
        self._budget = budget

    @budget_summary.setter
    def budget_summary(self, budget_summary):
        self._budget_summary = budget_summary


    @templates.setter
    def templates(self, templates):
        self._templates = templates

    @style.setter
    def style(self, style):
        style = style.strip().lower()
        if style in self.templates:
            self._style = style
        else:
            raise ValueError("style not found")

    def welcome(self):
        print('''Welcome to the budget app!''')
        self.username = input("Enter your username: ")
        print(f"Hi {self.username}!")

    def load_existing(self):
        '''
        Load items and style
        return true if items loaded
        otherwise return false
        '''
        user_path = f'{self._sdir}/{self.username}'

        if (isfile(user_path + '_items.json') and
        input(f"Existing data will be loaded from [{user_path}]. Continue? [Y/n]").strip().lower() != "n"):
            with open(user_path + '_items.json') as file:
                self.items = json.load(file)
            if isfile(user_path + '_style.txt'):
                with open(user_path + '_style.txt') as file:
                    self.style = file.read()
                print("Loaded existing items.")
            return True
        return False

    def pick_style(self):
        '''
        allows user to pick between different pre-set templates stored in the templates.json file.
        '''
        style = ""
        while not style:
            style = (
                input("Pick a style (" + ", ".join(self.templates) + "):")
                .strip()
                .lower()
                )
            if style in self.templates:
                print("The template style has:", *self.templates[style])
                if input("Confirm use? [Y/n]:").strip().lower() != "n":
                    self.style = style
                    break
                else:
                    style = ""

    def set_item(self, item_category):
        '''
        parses entry to remove or add items
        '''
        items = input(f"Item(s): ").split(",")
        if (items[0] == "") and len(items)==1:
            return False
        else:
            for i in items:
                yn = "y"
                item = i.strip()
                if item in ["total","end_balance","max_bal","min_bal"]:
                    print(item + "is a reserved word, skipping entry")
                    yn = "n"
                if yn == "y" and item.find('-') == 0:
                    yn = "n"
                    self.remove_item(item[1::])
                if yn == "y" and item in self.items:
                    yn = input(
                        item
                        + " is already in "
                        + self.items[item]["category"]
                        + ", replace it? [N/y]: "
                    )
                if yn.lower().strip() == "y":
                    self.add_item(item_category,item)
            return True

    def add_item(self, item_category, item):
        '''
        adds a budget item.
        no pytest coverage.
        '''
        self.items[item] = {
                    "name": item,
                    "category": item_category,
                    "value_input": input(item + " value: "),
                    "freq_input": input(item + """ value frequency D[DAY]/w/m/q/y[year] """),
                }
        try:
            self.convert_inputs(item)
            print("item added.")
        except ValueError:
            self.items.pop(item)
            print("invalid entries. " + item + " was not added.")

    def remove_item(self, item):
        '''
        removes a budget item.
        no pytest coverage.
        '''
        if item in self.items:
            self.items.pop(item)
            print("item removed.")

    def to_freq(self,n: str):
        '''
        finds an appropriate alias for an item
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        first checks for common aliases
        if no alias is found, it will attempt to use the string as is.
        if the name is invalid, it returns a ValueError
        if n is empty, returns "D"
        '''
        if n:
            n = n.strip().lower()
            n_loc = where([n in a for a in alias_dict.values()])[0]
            if len(n_loc)>0:
                return list(alias_dict)[n_loc[0]]
            try:
                pd.date_range('1990-01-01',periods=1,freq=n)
                return n
            except ValueError:
                raise ValueError("invalid frequency")
        else:
            return "D"

    def to_float(self,n: str):
        '''converts user input value to float, otherwise returns a zero float'''
        return (
            float(n.replace(",", "").replace(" ", "").replace("$", ""))
            if len(n) > 0
            else float(0)
        )

    def convert_inputs(self,i: str):
        '''
        convert item entries to their workable data type
        '''
        self.items[i]["value_float"] = self.to_float(self.items[i]["category"][0] + self.items[i]["value_input"])
        self.items[i]["freq_alias"] = self.to_freq(self.items[i]["freq_input"])

    def create_budget(self, forecast_years = 5):
        '''
        creates a budget (timeseries) for the forecast years and a budget summary
        '''

        for i in self.items:
            try:
                self.convert_inputs(i)
            except ValueError:
                self.items.pop(i)
                print("invalid inputs. " + item + " was removed.")

        SD = date.isoformat(
            date(date.today().year, date.today().month, date.today().day)
        )
        ED = date.isoformat(
            date(
                date.today().year + forecast_years, date.today().month, date.today().day
            )
        )

        timeseries = pd.date_range(start=SD, end=ED, freq=self.freq)
        budget = pd.DataFrame(columns=self.items, index=timeseries)

        for i in self.items:
            if self.items[i]["freq_alias"] == "SD":
                item_df = pd.DataFrame(
                    data=self.items[i]["value_float"],
                    columns=[self.items[i]["name"]],
                    index=pd.date_range(start=SD, end=SD, freq="D"),
                )
            else:
                item_df = pd.DataFrame(
                    data=self.items[i]["value_float"],
                    columns=[self.items[i]["name"]],
                    index=pd.date_range(start=SD, end=ED, freq=self.items[i]["freq_alias"]),
                )
            budget = budget.combine_first(item_df)

        budget["total"] = budget.sum(axis=1)

        self.budget = budget

        budget_summary = budget.groupby([lambda x: x.year, lambda x: x.quarter]).sum()

        budget['balance'] = budget["total"].cumsum()
        budget_end = budget.groupby([lambda x: x.year, lambda x: x.quarter]).last()['balance']
        budget_max = budget.groupby([lambda x: x.year, lambda x: x.quarter]).max()['balance']
        budget_min = budget.groupby([lambda x: x.year, lambda x: x.quarter]).min()['balance']

        budget_summary["end_balance"] = budget_end
        budget_summary["max_balance"] = budget_max
        budget_summary["min_balance"] = budget_min
        self.budget_summary = budget_summary
