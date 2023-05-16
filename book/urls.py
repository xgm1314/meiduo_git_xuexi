from django.urls import path
from book import views

urlpatterns = [
    path('books/', views.BookListView.as_view()),
    path('books/<int:pk>/', views.BookDetailView.as_view()),

    path('apiviewbooks/', views.BookListAPIView.as_view()),
    path('genericapiviewbooks/', views.BookInfoGenericAPIView.as_view()),
    path('genericapiviewbooks/<pk>/', views.BookInfoDetailGenericAPIView.as_view()),
    path('retrieveapiviewbooks/<pk>/', views.BookInfoRetrieveModelMixinAPIView.as_view()),
    path('genericapimixinviewbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    path('listcreatapiviewbooks/', views.BookInfoListCreateAPIView.as_view()),
    path('retrievesapiviewbooks/<pk>/', views.BookInfoRetrieveMixinAPIView.as_view()),

]
