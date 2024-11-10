 # Budget App
#### Video Demo: https://youtu.be/0-TaDfnbN6s
#### Description
![Lifecycle:experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)
![GitHub version](https://img.shields.io/badge/version-v0.1.0-blue.svg)

##### Overview:
Provides users with step by step questions and provides an output that shows their cash flow.
##### File structure
```
├── output
├── utils
│   └── alias_lookup.py
├── project.py
├── test_project.py
├── requirements.txt
├── LICENSE
└── README.md
```
##### Current Features
Below is a list of current features:
    - creates a user object which stores their information
    - choice of templates (basic, scholar, pro, accountant) - each with default categories for users
    - prompts users for their budget items [name, value, and frequency (daily, weekly, monthly, annual, etc.)]
    - generates a synthetic output, which shows their expected balance if they follow their budget for 5 years
##### Instructions for Use
1. cd into the directory with budget.py
2. first, install the project requirements
```
    python -m pip install -r requirements.txt
```
3. use the main __project.py__ app to start the tool.
```
    python project.py
```
4. results will be saved in the __output__ folder
5. to test the default app, use pytest
```
    python test_project.py
```
##### Future Improvments
Features that can be completed after submission:
- add tax calculator
- plot the time series and budget items by category
- implement SQL for persistent storage
- GUI (graphical user interface)
##### About the Author
[![Zack Kedida](https://avatars.githubusercontent.com/u/8821474?s=96&v=4)](https://www.linkedin.com/in/zack-kedida/)

Hi there! My name is __Zack (Zekarias) Kedida__. I'm from __Toronto, Canada__.

I have a passion for learning and financial literacy.

I made this app (and CS50 final project!) to help friends and family with budgeting!

If you have any questions, send me a message on LinkedIn!!

##### References (Python):
1. https://pandas.pydata.org/docs/reference/api/pandas.date_range.html
2. https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/
3. https://realpython.com/pandas-read-write-files/
4. https://www.alpharithms.com/generating-artificial-time-series-data-with-pandas-in-python-272321/
5. https://stackoverflow.com/questions/17450313/summing-over-months-with-pandas
6. https://docs.python.org/3/library/json.html
7. https://pypi.org/project/black/
8. https://stackoverflow.com/questions/4326658/how-to-index-into-a-dictionary
9. https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
10. https://peps.python.org/pep-0257/
##### References (Other):
11. Feature Map: https://kissflow.com/project/team/guide-to-product-feature-planning/
12. Markdown: https://github.com/Yilber/readme-boilerplate