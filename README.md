# Crypto_Bot
 An experimental trading bot for cryptocurrencies
 
This bot isn't intended to be used for live trading. Rather, it's an experimental program designed to teach me, the crater, how trade automation works and what an automated program looks like. It also has helped me hone my coding skills. 

Some big takeaways are:
• Crypto markets are incredibly chaotic. That is, the random walk is particularly random in the crypto space. Which, obviously, makes a lot of sense and the coins are somewhere between penny stocks and ponzi schemes in the scope of assets.
• Bots are easy to make but will almost always loose money over the short run and, will always lose money over the long run.

How this thing works:
1: warehouse imports data from my MondoDB cloud. The cloud is updated by a python script running on ASW that uses coin market cap api to fetch data.
2: Basic metrics like RSI and z scores are calculated for the data.
3: The data is run through the backtester which has triggers based off of user inputs. 