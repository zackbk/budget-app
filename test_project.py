from project import User,get_budget_fun1,save_budget_fun2,show_budget_fun3
from pytest import raises
import os, json

mock_user = User()
mock_user.username = "test"
mock_user.style = "basic"
mock_user.items = {'office' : {"name" : 'office',"category" : '+income',"value_input" : "300","freq_input" : 'week'},
              'home' : {"name" : 'home',"category" : '-expenses',"value_input" : "900","freq_input" : 'month'},
              }

def test_fun1():
    '''
    test if budget math checks out
    The budget should not be off by a significant amount
    '''
    mock_user.create_budget(17)
    assert mock_user.items['office']['value_float'] == 300
    assert mock_user.items['home']['value_float'] == -900
    assert abs(sum(mock_user.budget['total']) - (300*365.25/7 + -900*12)*len(mock_user.budget.index)/365) <= 300
    mock_user.create_budget(5)
    assert abs(sum(mock_user.budget['total']) - (300*365.25/7 + -900*12)*len(mock_user.budget.index)/365) <= 300


def test_fun2_output():
    '''
    test output functions which are created through the functions
    '''
    test_items = f"output/test_items.json"

    if os.path.isfile(test_items):
        os.remove(test_items)
    save_budget_fun2(mock_user)
    assert os.path.exists(f"output/") == True
    assert os.path.isfile(test_items) == True
    with open(test_items) as file:
        items_2 = json.load(file)
    assert items_2 == mock_user.items
    with open("output/test_style.txt") as file:
        style_2 = file.read()
    assert style_2 == mock_user.style
    test_plot = f"output/test_plot.jpg"
    if os.path.isfile(test_plot):
        os.remove(test_plot)
    show_budget_fun3(mock_user)
    assert os.path.isfile(test_plot) == True # checks that a jpg file is created.

def test_fun3_aux():
    assert mock_user.to_freq("weekly") == "W"
    assert mock_user.to_freq("February Start ") == "AS-FEB"
    assert mock_user.to_freq("5D") == "5d"
    assert mock_user.to_freq("2w") == "2w"
    with raises(ValueError):
        mock_user.to_freq("fortnight")
    assert mock_user.to_float("-300") == -300
    assert mock_user.to_float("1,900") == 1900
    assert mock_user.to_float("-12,000") == -12000
    assert mock_user.to_float("-$12,000") == -12000

def test_User():
    with raises(ValueError):
        mock_user.style = "blank"