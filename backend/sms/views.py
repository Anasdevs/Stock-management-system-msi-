from django.shortcuts import render, redirect
from django.http import request
from django.contrib import messages
from .models import Purchase

def index(request):

    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')
        invoice_number = request.POST.get('invoice_number')
        billing_date = request.POST.get('billing_date')
        date_of_entry = request.POST.get('date_of_entry')
        total_amount = request.POST.get('total_amount')
        seller_name = request.POST.get('seller_name')

        Purchase.objects.create(
            ItemName=item_name,
            Quantity=quantity,
            Invoice_Number=invoice_number,
            Billing_Date=billing_date,
            Date_of_Entry=date_of_entry,
            Total_Amount=total_amount,
            Seller_Name=seller_name
        )

        messages.success(request, 'Data submitted!')
        return redirect('index')

    submitted = False
    message_list = messages.get_messages(request)

    return render(request, 'home.html', {'submitted': submitted, 'messages': message_list})


def issued(request):
    return render(request, 'Issued.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def reports(request):
    return render(request, 'reports.html')



