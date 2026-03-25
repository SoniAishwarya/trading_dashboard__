from django.shortcuts import render
import yfinance as yf
from .models import Trade

balance = 10000
portfolio = {}


from django.contrib.auth.decorators import login_required


def home(request):
    global balance, portfolio

    stock_price = None  # पहले define करो

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

        # BUY
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

        # SELL
        elif action == "sell":
            if portfolio.get(stock, 0) >= quantity:
                balance += total
                portfolio[stock] -= quantity

                profit = quantity * 10  # (temporary)
                Trade.objects.create(
                    stock=stock,
                    quantity=quantity,
                    price=price,
                    trade_type="SELL",
                    profit=profit
                )

    trades = Trade.objects.all().order_by('-date')
    total_profit = sum(t.profit for t in trades)
    portfolio_value = sum(qty * 100 for qty in portfolio.values())
    return render(request, 'home.html', {
        'balance': balance,
        'trades': trades,
        'profit': total_profit,
        'stock_price': stock_price ,  # ✅ FIX
        'portfolio_value': portfolio_value

    })