from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import TradeItem, TradeRequest, BoardRoom
from .forms import TradeItemForm, TradeRequestForm

@login_required
def trade_home(request):
    return render(request, 'trade/trade_home.html')

@login_required
def list_items(request):
    items = TradeItem.objects.all()
    return render(request, 'trade/list_items.html', {'items': items})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(TradeItem, pk=pk)
    return render(request, 'trade/item_details.html', {'item': item})

@login_required
def create_item(request):
    if request.method == 'POST':
        form = TradeItemForm(request.POST, request.FILES)
        if form.is_valid():
            trade_item = form.save(commit=False)
            trade_item.owner = request.user
            trade_item.save()
            return redirect('trade:list_items')
    else:
        form = TradeItemForm()
    return render(request, 'trade/create_item.html', {'form': form})

@login_required
def boardroom(request):
    boardrooms = BoardRoom.objects.all()
    return render(request, 'trade/boardroom.html', {'boardrooms': boardrooms})
