**Activate the virtual environment**

```
$ blockchain_env\Scripts\activate
```

**install all pachages**

```
pip3 install -r requirements.txt
```

**Run the application and API**

Make sure to activate the virtual environment. $ blockchain_env\Scripts\Activate

```
set FLASK_APP=app
flask run
```

**Run a peer instance**
Make sure to activate the virtual environment. $ blockchain_env\Scripts\Activate

```
export PEER=True && python -m backend.app
```
