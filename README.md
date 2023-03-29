# ChessGod
A Discord bot that authenticates and displays player data for lichess.org accounts. Users' lichess profiles
are stored in a MongoDB database for easy access in servers to compare stats among friends!

## Authentication
Discord users must request a personal API access token from [lichess](https://lichess.org/account/oauth/token) and
register the lichess account by sending a `register auth-code` private message to ChessGod. The token is unique to
the account and should not be shared with anyone else.

## APIs
- [Discord](https://discordpy.readthedocs.io/en/stable/api.html) 
- [Berserk](https://berserk.readthedocs.io/en/master/)
- [Pymongo](https://pymongo.readthedocs.io/en/stable/)

## To Run

### (Optional) Set up [virtual environment](https://virtualenv.pypa.io/en/latest/)

1. Install virtualenv `pip install virtualenv`

2.  Run `virtualenv env`

3.  Run `source flask/bin/activate`


### Run 
1. Create .env file and add your discord bot API token

2. Install Requirements
```pip install -r requirements.txt```

3. Run main app
```python chess-god.py```

4. Run your bot commands in your discord server :)
