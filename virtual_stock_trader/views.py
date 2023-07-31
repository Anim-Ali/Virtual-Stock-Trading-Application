from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
import datetime
from decimal import Decimal
from virtual_stock_trader.models import *
from django.db.models import Sum
from django.db.models.query import QuerySet
import json  
from django.shortcuts import render 
from json import dumps 
from virtual_stock_trader.stocks import *
from virtual_stock_trader.sentiment import *


# Create your views here.

def get_homepage_data(request):
    transactions = Transaction.objects.filter(user=request.user)
    # add stock price and total value and total cash user has
    temp_portfolio = Transaction.objects.values('symbol', 'name').annotate(Sum('shares')).filter(user=request.user)
    #portfolio = portfolio.values.filter(portfolio.shares>0)
    shares = []
    symbols = []
    portfolio = []
    for each in temp_portfolio:
        if each.get('shares__sum') > 0:
            portfolio.append(each)   
            symbols.append(each.get('symbol'))
            shares.append(each.get('shares__sum'))   
    sharesJSON = dumps(shares) 
    symbolsJSON = dumps(symbols) 
    return {
        'transactions': transactions,
        'portfolio': portfolio,
        'shares' : sharesJSON,
        'symbols': symbolsJSON,
    }
        
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
        })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # get user if username and password are valid
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Django's built in login function
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "virtual_stock_trader/login.html", {
                "message": "Invalid Credentials"
            })

    return render(request, "virtual_stock_trader/login.html")

def logout_view(request):
    # Django's built in logout function
    logout(request)
    return render(request, "virtual_stock_trader/login.html", {
        "message": "Logged Out"
    })

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1==password2:
            if User.objects.filter(username=username).exists():
                return render(request, "virtual_stock_trader/register.html", {
                    "message": "Username exists"
                })
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "virtual_stock_trader/register.html", {
                "message": "Passwords do not match"
            })

    return render(request, "virtual_stock_trader/register.html")

def quotation_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        ticker_symbol = request.POST["symbol"]
        closing_price = get_closing_price(ticker_symbol)
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
            "closing_price": closing_price,
            "symbol": ticker_symbol,
        })
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
        })

def purchase_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        ticker_symbol = request.POST["symbol"]
        shares = int(request.POST["shares"])
        try:
            closing_price = Decimal(get_closing_price(ticker_symbol))
        except:
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'failure': "An error occured in the API. Please try again later",
            })
        date = datetime.datetime.now()
        total_cost = closing_price * shares
        prof = Profile.objects.get(user=request.user)
        cash = prof.cash
        if cash >= total_cost and shares > 0:
            name = get_company_name(ticker_symbol)
            if (closing_price == 'API Error' or name == 'API Error'):
                data = get_homepage_data(request)
                return render(request, "virtual_stock_trader/home.html", {
                    'transactions': data.get("transactions"),
                    "portfolio": data.get("portfolio"),
                    'shares' : data.get("shares"),
                    'symbols': data.get("symbols"),
                    'failure': "An error occured in the API. Please try again later",
                })
            transaction = Transaction(user=request.user, symbol=ticker_symbol, name=name, 
                        price=closing_price, shares=shares, date=date)
            transaction.save()
            prof.cash = prof.cash - total_cost
            prof.save()
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'success': "You have successfully bought the share(s)",
            })
        else:
            message = ''
            if cash < total_cost:
                message = "Sorry! You do not have sufficient funds to complete this transaction"
            elif shares <= 0:
                message = "Invalid shares amount! please select again"
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'failure': message,
            })
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
        })
"""
def sell_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        ticker_symbol = request.POST["symbol"]
        shares = int(request.POST["shares"])
        date = datetime.datetime.now()
        prof = Profile.objects.get(user=request.user)
        cash = prof.cash
        portfolio = Transaction.objects.values('symbol').annotate(Sum('shares')).filter(user=request.user)
        shares_owned = portfolio.get(symbol=ticker_symbol).get('shares__sum')

        # check if user has enough shares. 
        if shares_owned >= shares and shares > 0:
            try:
                closing_price = Decimal(get_closing_price(ticker_symbol))
            except:
                data = get_homepage_data(request)
                return render(request, "virtual_stock_trader/home.html", {
                    'transactions': data.get("transactions"),
                    "portfolio": data.get("portfolio"),
                    'shares' : data.get("shares"),
                    'symbols': data.get("symbols"),
                    'failure': "An error occured in the API. Please try again later",
                })
            name = get_company_name(ticker_symbol)
            total_cost = closing_price * shares
            shares = -abs(shares)
            if (closing_price == 'API Error' or name == 'API Error'):
                data = get_homepage_data(request)
                return render(request, "virtual_stock_trader/home.html", {
                    'transactions': data.get("transactions"),
                    "portfolio": data.get("portfolio"),
                    'shares' : data.get("shares"),
                    'symbols': data.get("symbols"),
                    'failure': "An error occured in the API. Please try again later",
                })
            transaction = Transaction(user=request.user, symbol=ticker_symbol, name=name, 
                        price=closing_price, shares=shares, date=date)
            transaction.save()
            prof.cash = prof.cash + total_cost
            prof.save()
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'success': "You have successfully sold the share(s)",
            })
        else:
            message = ''
            if shares_owned < shares:
                message = "Sorry! The current number of shares you hold is insufficient to complete this transaction"
            elif shares <= 0:
                message = "Invalid shares amount! please select again"
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'failure': message,
            })
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
        })
"""
def sell_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        ticker_symbol = request.POST["symbol"]
        shares = int(request.POST["shares"])
        date = datetime.datetime.now()
        prof = Profile.objects.get(user=request.user)
        cash = prof.cash
        portfolio = Transaction.objects.values('symbol').annotate(Sum('shares')).filter(user=request.user)
        shares_owned = portfolio.get(symbol=ticker_symbol).get('shares__sum')

        # check if user has enough shares. 
        if shares_owned >= shares and shares > 0:
            data = get_homepage_data(request)
            context = {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'failure': "An error occured in the API. Please try again later",
            }
            try:
                closing_price = Decimal(get_closing_price(ticker_symbol))
            except:
                return render(request, "virtual_stock_trader/home.html", context)
            name = get_company_name(ticker_symbol)
            total_cost = closing_price * shares
            shares = -abs(shares)
            if (closing_price == 'API Error' or name == 'API Error'):
                data = get_homepage_data(request)
                return render(request, "virtual_stock_trader/home.html", context)
            transaction = Transaction(user=request.user, symbol=ticker_symbol, name=name, 
                        price=closing_price, shares=shares, date=date)
            transaction.save()
            prof.cash = prof.cash + total_cost
            prof.save()
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'success': "You have successfully sold the share(s)",
            })
        else:
            message = ''
            if shares_owned < shares:
                message = "Sorry! The current number of shares you hold is insufficient to complete this transaction"
            elif shares <= 0:
                message = "Invalid shares amount! please select again"
            data = get_homepage_data(request)
            return render(request, "virtual_stock_trader/home.html", {
                'transactions': data.get("transactions"),
                "portfolio": data.get("portfolio"),
                'shares' : data.get("shares"),
                'symbols': data.get("symbols"),
                'failure': message,
            })
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
        })
        
def add_cash(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        amount = Decimal(request.POST["amount"])
        prof = Profile.objects.get(user=request.user)
        prof.cash = prof.cash + amount
        prof.save()
        cash = prof.cash
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols"),
            'success': '{amount} has been successfully added to your wallet\n'.format(amount=amount) +
                    'Previous balance: {prev}\n'.format(prev=cash-amount) +
                    'New balance: {cash}\n'.format(cash=cash)
        })
    else:
        data = get_homepage_data(request)
        return render(request, "virtual_stock_trader/home.html", {
            'transactions': data.get("transactions"),
            "portfolio": data.get("portfolio"),
            'shares' : data.get("shares"),
            'symbols': data.get("symbols")
        })

def sentiment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        sentimentCount, sentiment_scores = get_data(request.POST["keyword"])
        sentimentJSON = dumps(sentimentCount)
        scoresJSON = dumps(sentiment_scores)
        return render(request, "virtual_stock_trader/sentiment.html", {
            'sentimentCount': sentimentJSON,
            'sentimentScores': scoresJSON
        })
    else:
        return render(request, "virtual_stock_trader/sentiment.html")