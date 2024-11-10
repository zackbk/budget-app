from User import User
from tabulate import tabulate
import sys
import os
import json
import matplotlib.pyplot as plt

# for potential future use:
# import re,argparse,pickle
# import matplotlib.pyplot as plt

def main():
    '''
    Main app
    '''
    try:
        user = User()
        user.welcome()

        if user.load_existing():
            pass
        else:
            user.pick_style() # pick style

        get_budget_fun1(user)
        save_budget_fun2(user)
        show_budget_fun3(user)

    except EOFError:
        sys.exit("Budget Terminated")

    print("Here is your budget:")
    print(tabulate(user.budget_summary,headers=user.budget_summary.columns,tablefmt="rounded_grid"))
    print('''\rCheck the output folder for more results.
          \rThanks for using the budget app. See you soon!''')


def get_budget_fun1(user):
    '''
    Enables users to set budget items
    '''
    if input("show entry guide? [y/N]") == "y":
        input(
        '''
        \rIn this section you will be prompted to add items by each category
        - to add an item, type it's name. eg. car
            - the following item names are reserved: "total","end_balance","max_bal","min_bal"
        - to remove a previously added item, use '-' before the name. eg. -car
        - to add multiple items efficiently, use ','. eg. car,house,cat
            Note: you will be prompted to add costs individually.
        - to move on to the next category, press [Enter] when prompted for an item
        ...
        ''')

    for i in user.templates[user.style]:
        print("------------------")
        print("Category: " + i[::])
        try:
            while user.set_item(i):
                pass
        except KeyboardInterrupt:
            print("\n-- end " + i + " --")
    user.create_budget()


def save_budget_fun2(user):
    '''
    Saves results in the output folder
    '''
    if not os.path.exists("output"): os.mkdir("output");
    user.budget.to_csv(f"output/{user.username}_timeseries.csv")
    user.budget_summary.to_csv(f"output/{user.username}_summary.csv")
    with open(f"output/{user.username}_items.json","w") as file:
        json.dump(user.items,file)
    with open(f"output/{user.username}_style.txt","w") as file:
        file.write(user.style)

def show_budget_fun3(user):
    '''
    creates a time series plot of the total budget
    '''
    fig, ax = plt.subplots(1,1)
    ax.plot(user.budget.index.to_numpy(),user.budget['balance'])
    ax.xaxis_date()
    fig.savefig(f'output/{user.username}_plot.jpg')


if __name__ == "__main__":
    main()
