# MYPlatE by Team willCodeForFood

Michael: Project Manager

Emily: Frontend

Yaru: Backend

Our website is all about food :hamburger:	 We will utilize the [Recipe Puppy](https://docs.google.com/document/d/13OUDMV2C-yqZqcLTVC5xLgo9W4p5XKlCxfD6u3MtNrI/edit) API to present a searchable recipe book, the [Zomato API](https://docs.google.com/document/d/1ptuOtfx2B46Yl87aNOniRa-M4qJFGq0HjFpTniAma80/edit) for a restaurant search engine, and the [FoodData Central](https://docs.google.com/document/d/10ByyAa4DtXPNJD1E3Nd-qjbd3W9ZhN6FQc-We5B95C4/edit) API in a food diary.

## How to run

Install all the dependencies for this project by running this from the command line:

```shell
    pip3 install -r requirements.txt
```

After installing all the dependencies, run the program by running:

```shell
    python3 app.py
```
## Obtaining API keys
The Zomato and FoodData Central APIs require a key to use them

#### FoodData Central
1. Sign up for an API key at [FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html)
2. The API key should show up on the screen and it is also emailed to you
3. Open the "keys.json" file and replace "YOUR_API_KEY_HERE" next to "fooddata" with the API key you obtained

#### Zomato
1. Go to [Zomato](https://developers.zomato.com/api) and scroll down to the bottom
2. Click "Generate API key" and sign up for an account.
3. Open the "keys.json" file and replace "YOUR_API_KEY_HERE" next to "zomato" with the API key you obtained

