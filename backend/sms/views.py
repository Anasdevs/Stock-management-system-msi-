from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Purchase, IssuedItem, Items, Faculty, Department
from django.db.models import Sum
from django.db import transaction
from datetime import datetime


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

    return render(request, 'Purchase.html', {
        'purchases': purchases,
        'submitted': submitted,
        'messages': message_list,
        'item_names': Items.objects.values_list('name', flat=True).all()
    })


def issued(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        quantity = int(request.POST.get('quantity'))
        employee_name = request.POST.get('employee_name')
        issue_date_str = request.POST.get('issue_date')
        department_name = request.POST.get('department')
        location = request.POST.get('location')

        try:
            # Get the item from the Items table
            item = get_object_or_404(Items, name=item_name)

            # Check if there are enough items in inventory
            if item.QuantityInInventory < quantity:
                messages.error(request, 'Not enough items in inventory.')
                return redirect('issued')

            # Get the employee from the Faculty table
            employee = get_object_or_404(Faculty, name=employee_name)

            # Get the department from the Department table
            department = get_object_or_404(Department, department=department_name)

            # Convert issue_date string to a datetime object
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Create and save IssuedItem
                issued_item = IssuedItem.objects.create(
                    ItemName=item,
                    Quantity=quantity,
                    Name_of_Employee=employee,
                    Issue_Date=issue_date,
                    Department=department,
                    Location=location,
                )

                # Update the quantity in the Items model
                item.QuantityInInventory -= quantity
                item.ItemsIssued += quantity
                item.save()

            # Add a success message
            messages.success(request, 'Item issued!')
            return redirect('issued')

        except Items.DoesNotExist:
            return HttpResponse("Item not found in Items table")

        except Faculty.DoesNotExist:
            return HttpResponse("Employee not found in Faculty table")

        except Department.DoesNotExist:
            return HttpResponse("Department not found in Department table")

    # Fetch data to be displayed in the template
    issued_items = IssuedItem.objects.all()
    faculty_names = Faculty.objects.all()
    items = Items.objects.values_list('name', flat=True).distinct()
    departments = Department.objects.all()
    message_list = messages.get_messages(request)

    return render(request, 'Issued.html', {'faculty_names': faculty_names, 'items': items, 'issued_items': issued_items, 'departments': departments, 'messages': message_list})
 



def dashboard(request):
    # Fetch all unique item names from the Purchase table
    items = Purchase.objects.values_list('ItemName__name', flat=True).distinct()

    # Create a list to store information for each item
    item_info_list = []

    # Calculate total purchased and total issued quantities for each item
    for item_name in items:
        total_purchased = Purchase.objects.filter(ItemName__name=item_name).aggregate(Sum('Quantity'))['Quantity__sum'] or 0
        total_issued = IssuedItem.objects.filter(ItemName__name=item_name).aggregate(Sum('Quantity'))['Quantity__sum'] or 0

        # Calculate items in inventory for each item
        inventory = total_purchased - total_issued

        # Save or update the data in the Items model
        item, created = Items.objects.get_or_create(name=item_name)
        item.totalPurchased = total_purchased
        item.ItemsIssued = total_issued
        item.QuantityInInventory = inventory
        item.save()

        # Append item information to the list
        item_info_list.append({
            'name': item_name,
            'total_purchased': total_purchased,
            'total_issued': total_issued,
            'inventory': inventory,
        })

    return render(request, 'dashboard.html', {'item_info_list': item_info_list})
def reports(request):
    return render(request, 'reports.html')

def home(request):
    return render(request, 'landing.html')


def profile(request):
    return render(request,'Profile.html')