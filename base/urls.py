from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.UserLogin, name="userLogin"),
    path("dashboard/", views.Dashboard, name="dashboard"),
    path("display-books/", views.DisplayBooks, name="displayBooks"),
    path("add-book/", views.AddBook, name="addBook"),
    path("update-book/<str:id>", views.UpdateBook, name="updateBook"),
    path("delete-book/<int:id>/", views.DeleteBook, name="deleteBook"),
    path("issue-book/<int:id>/", views.IssueBook, name="issueBook"),
    path("borrowed-books/", views.BorrowedBooks, name="borrowedBooks"),
    path("lost-books/<str:id>/", views.ReportLostBook, name="lostBooks"),
    path("lost-books-list/" , views.LostBooksList, name="lostBooksList"),
    path("del-lost-books/<str:id>/", views.DelLostBooks, name="delLostBooks"),
    path("return-book/<str:id>/", views.ReturnBook, name="returnBook"),
    path("search-books/", views.SearchBooks, name="searchBooks"),

    path("<path:unknown>", TemplateView.as_view(template_name='error.html')),
]