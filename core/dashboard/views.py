from django.shortcuts import render
import yfinance as yf
from .models import Trade

balance = 10000
portfolio = {}

def home(request):
    global balance, portfolio

    stock_price = None

    if request.method == "POST":
        stock = request.POST.get("stock")
        quantity = int(request.POST.get("quantity"))
        action = request.POST.get("action")

        # 🔥 LIVE PRICE
        data = yf.Ticker(stock)
        try:
            price = data.info.get("regularMarketPrice", 100)
        except:
            price = 100

        stock_price = price
        total = quantity * price

        # ✅ BUY
        if action == "buy":
            if balance >= total:
                balance -= total
                portfolio[stock] = portfolio.get(stock, 0) + quantity

                Trade.objects.create(
                    stock=stock,
                    quantity=quantity,
                    price=price,
                    trade_type="BUY"
                )

        # ✅ SELL
        elif action == "sell":
            if portfolio.get(stock, 0) >= quantity:
                balance += total
                portfolio[stock] -= quantity

                # 🔥 अगर 0 हो गया तो remove करो
                if portfolio[stock] == 0:
                    del portfolio[stock]

                # 🔥 last buy price
                buy_trade = Trade.objects.filter(
                    stock=stock, trade_type="BUY"
                ).order_by('-date').first()

                if buy_trade:
                    buy_price = buy_trade.price
                else:
                    buy_price = price

                profit = (price - buy_price) * quantity

                Trade.objects.create(
                    stock=stock,
                    quantity=quantity,
                    price=price,
                    trade_type="SELL",
                    profit=profit
                )

    trades = Trade.objects.all().order_by('-date')
    total_profit = sum(t.profit for t in trades)

    # 🔥 LIVE portfolio value
    portfolio_value = 0
    for stock, qty in portfolio.items():
        data = yf.Ticker(stock)
        try:
            live_price = data.info.get("regularMarketPrice", 100)
        except:
            live_price = 100

        portfolio_value += live_price * qty

    return render(request, 'home.html', {
        'balance': balance,
        'trades': trades,
        'profit': total_profit,
        'stock_price': stock_price,
        'portfolio_value': portfolio_value
    })