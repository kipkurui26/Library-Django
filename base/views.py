from django.shortcuts import render, redirect
from .models import Book_Reg, Borrowed_Books, LostBooks, LogDetails
from django.contrib import messages

# Create your views here.
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get("userName", '')
        password = request.POST.get('userPassword', '')
        if LogDetails.objects.filter(userName=username, userPassword=password).exists():
            messages.info(request, "Login Success. Welcome to Leagues Library", extra_tags="messages_show")
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect Username or Password. Please try again.", extra_tags="messages_show")
            return render(request, "base/user_login.html")
        
    return render(request, "base/user_login.html")

def Dashboard(request):
    total_books = Book_Reg.objects.all().count()
    lost_books = LostBooks.objects.all().count()
    borrowed_books = Borrowed_Books.objects.all().count()

    context = {
        "total_books"  : total_books,
        "lost_books"  : lost_books,
        "borrowed_books"  : borrowed_books,
    }

    return render(request, "base/dashboard.html", context)

def DisplayBooks(request):
    books = Book_Reg.objects.all()
    total_books = books.count()

    b_books = Borrowed_Books.objects.all()
    context = {
        "books": books,
        "total_books": total_books,
        "b_books": b_books
    }


    return render(request, "base/display_books.html", context)

def AddBook(request):
    if request.method == "POST":
        bookStatus = request.POST.get("bookStatus")
        bookId = request.POST.get("bookId")
        bookTitle = request.POST.get("bookTitle")
        bookAuthor = request.POST.get("bookAuthor")
        bookPublisher = request.POST.get("bookPublisher")
        bookEdition = request.POST.get("bookEdition")
        bookForm = request.POST.get("bookForm")
        bookSubject = request.POST.get("bookSubject")
        bookCondition = request.POST.get("bookCondition")
        dateAdded = request.POST.get("dateAdded")
        addedBy = request.POST.get("addedBy")

        if Book_Reg.objects.filter(bookId=bookId).exists():
            messages.error(request, "ERROR: Book with the same id already exists!", extra_tags="messages_show")
            return redirect("addBook")

        book = Book_Reg(bookStatus=bookStatus, bookId=bookId, bookTitle=bookTitle, bookAuthor=bookAuthor, bookPublisher=bookPublisher, bookEdition=bookEdition, bookForm=bookForm, bookSubject=bookSubject, bookCondition=bookCondition, dateAdded=dateAdded, addedBy=addedBy)
        book.save()

        messages.success(request, "Successfully Registered", extra_tags="messages_show")
        return redirect("displayBooks")
    return render(request, "base/add_book.html")

def UpdateBook(request, id):
    if request.method == "POST":
        bookId = request.POST["bookId"]
        bookTitle = request.POST["bookTitle"]
        bookAuthor = request.POST["bookAuthor"]
        bookPublisher = request.POST["bookPublisher"]
        bookEdition = request.POST["bookEdition"]
        bookForm = request.POST["bookForm"]
        bookSubject = request.POST["bookSubject"]
        bookCondition = request.POST["bookCondition"]
        dateAdded = request.POST["dateAdded"]
        addedBy = request.POST["addedBy"]

        book = Book_Reg.objects.get(bookId=id)
        book.bookId = bookId
        book.bookTitle = bookTitle
        book.bookAuthor = bookAuthor
        book.bookPublisher = bookPublisher
        book.bookEdition = bookEdition
        book.bookForm = bookForm
        book.bookSubject = bookSubject
        book.bookCondition = bookCondition
        book.dateAdded = dateAdded
        book.addedBy = addedBy
        book.save()

        messages.success(request, "Successfully Updated", extra_tags="messages_show")
        return redirect("displayBooks")
    u_book = Book_Reg.objects.get(bookId=id)
    context = {
        "u_book": u_book
    }
    return render(request, "base/update_book.html", context)

def DeleteBook(request, id):
    book = Book_Reg.objects.get(bookId=id)
    book.delete()

    messages.info(request, "Successfully Deleted", extra_tags="messages_show")
    return redirect("displayBooks")

def IssueBook(request, id):
    if request.method == "POST":
        bookId = request.POST.get("bookId")
        bookTitle = request.POST.get("bookTitle")
        studentId = request.POST.get("admissionNo")
        studentName = request.POST.get("studentName")
        bookCondition = request.POST.get("bookCondition")
        issuedBy = request.POST.get("issuedBy")
        issueDate = request.POST.get("issueDate")
        returnDate = request.POST.get("returnDate")

        if Borrowed_Books.objects.filter(bookId=bookId).exists():
            messages.error(request, "Error: Book Already Issued!", extra_tags="messages_show")
            return redirect("displayBooks")

        bookId_instance = Book_Reg.objects.get(bookId=bookId)

        if bookId_instance.bookStatus == "Lost":
            messages.error(request, "Error: Lost books cannot be issued!", extra_tags="messages_show")
            return redirect("displayBooks")
        
        issueBook = Borrowed_Books(bookId=bookId_instance, bookTitle=bookTitle, studentId=studentId, studentName=studentName, bookCondition=bookCondition, issuedBy=issuedBy, issueDate=issueDate, returnDate=returnDate)
        issueBook.save()

        bookId_instance.bookStatus = "Issued"
        bookId_instance.save()

        messages.info(request, "Book Successfully Issued", extra_tags="messages_show")
        return redirect("displayBooks")

    book = Book_Reg.objects.filter(bookId=id)
    context = {"book": book}
    return render(request, "base/issue_book.html", context)

def BorrowedBooks(request):
    borrowed_book = Borrowed_Books.objects.all()
    context = {
        "borrowed_book": borrowed_book
    }
    return render(request, "base/borrowed_books.html", context) 

def ReportLostBook(request, id):
    if request.method == "POST":
        bookId = request.POST.get("bookId")
        bookTitle = request.POST.get("bookTitle")
        studentId = request.POST.get("admissionNo")
        studentName = request.POST.get("studentName")
        bookFine = request.POST.get("bookFine")
        filledBy = request.POST.get("filledBy")

        bookId_instance = Book_Reg.objects.get(bookId=bookId)

        lBook = LostBooks(bookId=bookId_instance, bookTitle=bookTitle, studentId=studentId, studentName=studentName, bookFine=bookFine, filledBy=filledBy)
        lBook.save()

        bookId_instance.bookStatus = "Lost"
        bookId_instance.save()

        borrow_book = Borrowed_Books.objects.get(bookId=bookId)
        borrow_book.delete()

        messages.info(request, f"Book with id: {bookId} has been marked lost", extra_tags="messages_show")
        return redirect("displayBooks")

    lostBook = Borrowed_Books.objects.filter(bookId=id)
    context = {
        "lostBook": lostBook
    }
    return render(request, "base/lost_books.html", context)

def LostBooksList(request):
    lost_books = LostBooks.objects.all()
    context = {
        "lost_books": lost_books
    }
    return render(request, "base/display_lost.html", context)

def DelLostBooks(request, id):
    lost_book = LostBooks.objects.get(bookId=id)
    lost_book.delete()

    book_instance = Book_Reg.objects.get(bookId=id)
    
    book_instance.bookStatus = 'Available'
    book_instance.save()

    messages.info(request, "Book is repaid and now available for re-issuing", extra_tags="messages_show")
    return redirect("displayBooks")

def ReturnBook(request, id): 
    bookId_instance = Book_Reg.objects.get(bookId=id)
    return_book = Borrowed_Books.objects.get(bookId=id)
    return_book.delete()

    bookId_instance.bookStatus = "Available"
    bookId_instance.save()

    messages.info(request, "Book Successfully Returned", extra_tags="messages_show")
    return redirect("displayBooks")
    
def SearchBooks(request):
    search_query = request.POST.get('search', '')

    if search_query:
        search_books = Book_Reg.objects.filter(bookTitle__icontains=search_query)
        borrowed_books = Borrowed_Books.objects.filter(bookTitle__icontains=search_query)
        f_lost_books = LostBooks.objects.filter(bookTitle__icontains=search_query)

        referer = request.META.get('HTTP_REFERER')

        if "display-books" in referer:
            if search_books.exists():
                context = {'search_books': search_books}
                return render(request, 'base/display_books.html', context)
            else:
                messages.error(request, "No books found matching the search query.", extra_tags="messages_show")
                return redirect('displayBooks')
    
        elif "borrowed-books" in referer:
            if borrowed_books.exists():
                context = {'borrowed_books': borrowed_books}
                return render(request, 'base/borrowed_books.html', context)
            else:
                messages.error(request, "No books found matching the search query.", extra_tags="messages_show")
                return redirect('borrowedBooks')
        
        elif "lost-books-list" in referer:
            if f_lost_books.exists():
                context = {'f_lost_books': f_lost_books}
                return render(request, 'base/display_lost.html', context)
            else:
                messages.error(request, "No books found matching the search query.", extra_tags="messages_show")
                return redirect('lostBooksList')
        else:
            messages.error(request, "Please enter a valid search query.", extra_tags="messages_show")
            return redirect('displayBooks')
            
    else:
        messages.error(request, "Please enter a valid search query.", extra_tags="messages_show")
        return redirect('displayBooks')

def error_404(request):
    return render(request, "base/error.html")