from django.urls import path
from book import views

urlpatterns = [
    # path('books/', views.BookListView.as_view()),
    # path('books/<int:pk>/', views.BookDetailView.as_view()),
    #
    # path('apiviewbooks/', views.BookListAPIView.as_view()),
    # path('genericapiviewbooks/', views.BookInfoGenericAPIView.as_view()),
    # path('genericapiviewbooks/<pk>/', views.BookInfoDetailGenericAPIView.as_view()),
    # path('retrieveapiviewbooks/<pk>/', views.BookInfoRetrieveModelMixinAPIView.as_view()),
    # path('genericapimixinviewbooks/', views.BookInfoGenericMixinAPIView.as_view()),
    # path('listcreatapiviewbooks/', views.BookInfoListCreateAPIView.as_view()),
    # path('retrievesapiviewbooks/<pk>/', views.BookInfoRetrieveMixinAPIView.as_view()),
    # # 视图集路由
    # path('bookviewset/', views.BookViewSet.as_view({'get': 'list'})),
    # path('bookviewset/<pk>/', views.BookViewSet.as_view({'get': 'retrieve'})),
]

from rest_framework.routers import DefaultRouter, SimpleRouter

"""
DefaultRouter, SimpleRouter：共同点是都可以帮助视图集生成路由
不同点：DefaultRouter ：http://127.0.0.1:8000/ 跟路由可以访问
       SimpleRouter  ：http://127.0.0.1:8000/ 跟路由不可以访问
"""

router = DefaultRouter()  # 创建路由实例对象
# router = SimpleRouter()  # 创建路由实例对象
# prefix：列表视图和详情视图公共部分；
# viewset：视图集；
# basename：给列表视图和详情视图的路由设置别名，一般设置为prefix，命名规则：列表视图basename-list；详情视图basename-detail
router.register(prefix='book', viewset=views.BookModelViewSet, basename='book')
router.register(prefix='people', viewset=views.PeopleModelViewSet, basename='people')

urlpatterns += router.urls  # 将router生成的路由追加到urlpatterns
