# ReactPy-NetWorth

Built with ReactPy, Bootstrap, SQLModel and Pandas, shows a summary of assets, liabilities and net worth. Deals or transactions are saved in sqlite database.

The modules `networth.py` and `sqlmodeldb.py` should be on the same folder. This app will create a folder called `data` in the directory where `networth.py` is located. Under this data folder, it creates a file called `networth.db`. The `networth.db` is an sqlite file that stores saved deals by the users.

![image](https://github.com/fsmosca/ReactPy-NetWorth/assets/22366935/6f983de0-172f-4c6d-a0c5-beb15753990e)

This repository is linked to my [blog](https://energybeam.blogspot.com/2023/08/how-to-create-income-and-expense-app-in.html) in blogspot.

## Setup

1. Install Python version 3.9 or newer

2. Clone the repository from command line.

```
git clone https://github.com/fsmosca/ReactPy-NetWorth.git
```

3. Change directory to reactpy-networth.

```
cd reactpy-networth
```

4. Install requirements.

```
pip install -r requirements.txt
```

5. Run the app.

```
uvicorn networth:app
```

6. Follow instruction from the console. Paste the given url to browser to open the app.

## Credits

* [ReactPy Github](https://github.com/reactive-python/reactpy)
* [ReactPy Docs](https://reactpy.dev/docs/guides/getting-started/index.html)
* [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
* [SQLModel](https://sqlmodel.tiangolo.com/)
* [Pandas](https://pandas.pydata.org/getting_started.html)
