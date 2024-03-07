from django.db import models

# Create your models here.
class Book_Reg(models.Model):
    bookStatus = models.CharField(max_length=100, null=True, blank=True)
    bookId = models.CharField(primary_key=True, max_length=150)
    bookTitle = models.CharField(max_length=150)
    bookAuthor = models.CharField(max_length=100)
    bookPublisher = models.CharField(max_length=100)
    bookEdition = models.CharField(max_length=100)
    bookForm = models.CharField(max_length=100)
    bookSubject = models.CharField(max_length=100)
    bookCondition = models.CharField(max_length=100)
    dateAdded = models.DateField()
    addedBy = models.CharField(max_length=100)

    def __str__(self):
        return str(self.bookId)
    
class Borrowed_Books(models.Model):
    bookId = models.ForeignKey(Book_Reg, on_delete=models.CASCADE)
    bookTitle = models.CharField(max_length=200)
    studentId = models.CharField(max_length=200)
    studentName = models.CharField(max_length=200)
    bookCondition = models.CharField(max_length=200)
    issuedBy = models.CharField(max_length=200)
    issueDate = models.DateField()
    returnDate = models.DateField()

    def __str__(self):
        return str(self.bookId)
    
class LostBooks(models.Model):
    bookId = models.ForeignKey(Book_Reg, on_delete=models.CASCADE)
    bookTitle = models.CharField(max_length=200)
    studentId = models.CharField(max_length=200)
    studentName = models.CharField(max_length=200)
    bookFine = models.CharField(max_length=200)
    filledBy = models.CharField(max_length=200)

    def __str__(self):
        return str(self.bookId)


class LogDetails(models.Model):
    userName = models.CharField(max_length=200)
    userPassword = models.CharField(max_length=200)

    def __str__(self):
        return str(self.userName)
