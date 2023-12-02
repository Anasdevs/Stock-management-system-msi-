from django.db import models

DEPARTMENT_CHOICES = [
    ('BCA', 'BCA'),
    ('BBA', 'BBA'),
    ('B.COM', 'B.COM'),
    ('BSC', 'BSC'),
    ('B.ED', 'B.ED'),
]

class Faculty(models.Model):
    name = models.CharField(max_length=50)
    faculty_id=models.IntegerField(unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return (self.name,self.faculty_id,self.department)

class Items(models.Model):
    name = models.CharField(max_length=50)
    Quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    ItemName = models.ForeignKey(Items,max_length=50,on_delete=models.DO_NOTHING,related_name='purchase_itemname')
    Quantity = models.IntegerField()
    Rate = models.IntegerField(default=0)
    Invoice_Number = models.IntegerField()
    Billing_Date = models.DateField()
    Date_of_Entry = models.DateField()
    Total_Amount = models.IntegerField()
    Seller_Name = models.CharField(max_length=50)
    CGST = models.IntegerField(default=0)
    SGST = models.IntegerField(default=0)
    Extra_charges = models.IntegerField(default=0)
    Invoice=models.FileField(upload_to='invoice',null=True,blank=True)

    def __str__(self):
        return (self.ItemName,self.Invoice_Number)

class IssuedItem(models.Model):
    ItemName = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING, related_name='issued_item_itemname') 
    Quantity = models.IntegerField()
    Name_of_Employee = models.ForeignKey(Faculty,max_length=50,on_delete=models.DO_NOTHING,related_name='issued_item_name_of_employee')
    Issue_Date = models.DateField()
    Department = models.ForeignKey(Faculty,max_length=50,choices=DEPARTMENT_CHOICES,on_delete=models.SET("Faculty Not Found"))
    Location = models.CharField(max_length=50)
    physical_verification = models.BooleanField(default=False)

    def __str__(self):
        return (self.ItemName,self.Name_of_Employee,self.Department)
