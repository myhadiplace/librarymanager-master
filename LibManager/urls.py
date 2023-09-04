from . import views
from django.urls import path

urlpatterns = [
    path("",views.books_list,name='Home'),
    path("new-book",views.add_book,name='AddBook'),
    path('delete_book/<int:id>',views.delete_book,name='DeleteBook'),
    path('new-author',views.add_author,name="AddAuthor"),
    path('register-user',views.register_user,name='RegisterUser'),
    path('login-user',views.login_user,name='LoginUser'),
    path('otp-authentication/<int:user_id>',views.otp_authenticate,name="OtpAuth"),
    path('search/',views.search,name='Search'),
    path('filter-book/',views.book_filters,name='FilterBooks'),
    path('sotr/',views.sorting,name='Sort'),
    path('reserve_book/<int:user_id>/<int:book_id>',views.reserve_book,name='ReserveBook'),
    path('pay/',views.payment,name='Payment'),
    path('reserved_book/<int:user_id>',views.all_reserve_book,name='AllReservedBook'),
    path('logout',views.logout,name='LogOut')
    

]
