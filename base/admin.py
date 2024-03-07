from django.contrib import admin
from .models import Book_Reg, Borrowed_Books, LostBooks, LogDetails

# Register your models here.

dbList = [
    Book_Reg, 
    Borrowed_Books,
    LostBooks,
    LogDetails,
] 

admin.site.register(dbList)