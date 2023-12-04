from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib import messages
from .models import Purchase, IssuedItem, Items, Faculty
from django.db.models import Sum
from django.db import models


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


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import IssuedItem, Faculty, Purchase

def issued(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')
        employee_name = request.POST.get('employee_name')
        issue_date = request.POST.get('issue_date')
        # department_name = request.POST.get('department')
        location = request.POST.get('location')

        try:
            purchase_item = Purchase.objects.filter(ItemName__name=item_name).first()

            if not purchase_item:
                return HttpResponse("Item not found in Purchase table")

            employee = get_object_or_404(Faculty, name=employee_name)

            # department = get_object_or_404(Faculty, department=department_name)

            # Create and save IssuedItem
            issued_item = IssuedItem.objects.create(
                ItemName=purchase_item,
                Quantity=quantity,
                Name_of_Employee=employee,
                Issue_Date=issue_date,
                # Department=department,
                Location=location,
            )

            # Update the quantity in the Items model
            purchase_item.ItemName.Quantity -= int(quantity)
            purchase_item.ItemName.save()

            # Add a success message
            message = "Item issued successfully."
            return render(request, 'Issued.html', {'message': message})

        except Purchase.MultipleObjectsReturned:
            return HttpResponse("Error: Multiple purchases found for the given item. Please check your data.")

    issued_items = IssuedItem.objects.all()
    faculty_names = Faculty.objects.all()
    items = Purchase.objects.values_list('ItemName__name', flat=True).distinct()
    return render(request, 'Issued.html', {'faculty_names': faculty_names, 'items': items, 'issued_items': issued_items})








 
def dashboard(request):
    item = Items.objects.first() 

    total_purchased = Purchase.objects.filter(ItemName=item).aggregate(total=models.Sum('Quantity'))['total'] or 0
    total_issued = IssuedItem.objects.filter(ItemName__ItemName=item).aggregate(total=models.Sum('Quantity'))['total'] or 0
    inventory = item.Quantity - total_issued

    context = {
        'item': item,
        'total_purchased': total_purchased,
        'total_issued': total_issued,
        'inventory': inventory,
    }

    return render(request, 'dashboard.html', context)










def reports(request):
    return render(request, 'reports.html')
