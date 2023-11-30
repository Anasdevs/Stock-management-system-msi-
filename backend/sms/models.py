from django.db import models

DEPARTMENT_CHOICES = [
    ('BCA', 'BCA'),
    ('BBA', 'BBA'),
    ('B.COM', 'B.COM'),
    ('BSC', 'BSC'),
    ('B.ED', 'B.ED'),
]

class Purchase(models.Model):
    ItemName = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    Invoice_Number = models.IntegerField()
    Reference_Number = models.IntegerField( unique=True)
    Billing_Date = models.DateField()
    Date_of_Entry = models.DateField()
    Total_Amount = models.IntegerField()
    Seller_Name = models.CharField(max_length=50)

class IssuedItem(models.Model):
    ItemName = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='issued_item_itemname') 
    Quantity = models.IntegerField()
    Name_of_Employee = models.CharField(max_length=50)
    Reference_Number = models.ForeignKey(Purchase, to_field='Reference_Number', on_delete=models.CASCADE)
    Issue_Date = models.DateField()
    Department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    Location = models.CharField(max_length=50)
