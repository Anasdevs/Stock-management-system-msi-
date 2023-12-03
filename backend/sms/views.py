from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib import messages
from .models import Purchase, IssuedItem, Items, Faculty

def index(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item = get_object_or_404(Items, name=item_name)
        quantity = request.POST.get('quantity')
        rate = request.POST.get('rate')
        invoice_number = request.POST.get('invoice_number')
        billing_date = request.POST.get('billing_date')
        date_of_entry = request.POST.get('date_of_entry')
        total_amount = request.POST.get('total_amount')
        seller_name = request.POST.get('seller_name')
        cgst = request.POST.get('cgst')
        sgst = request.POST.get('sgst')
        extra_charges = request.POST.get('extra_charges')

        Purchase.objects.create(
            ItemName=item,
            Quantity=quantity,
            Rate=rate,
            Invoice_Number=invoice_number,
            Billing_Date=billing_date,
            Date_of_Entry=date_of_entry,
            Total_Amount=total_amount,
            Seller_Name=seller_name,
            CGST=cgst,
            SGST=sgst,
            Extra_charges=extra_charges
        )

        messages.success(request, 'Data submitted!')
        return redirect('index')

    submitted = False
    purchases = Purchase.objects.all()
    message_list = messages.get_messages(request)

    return render(request, 'home.html', {
        'purchases': purchases,
        'submitted': submitted,
        'messages': message_list,
        'item_names': Items.objects.values_list('name', flat=True).all()
    })


def issued(request):
    return render(request, 'Issued.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def reports(request):
    return render(request, 'reports.html')



