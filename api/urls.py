from rest_framework_nested import routers
from .views import KeyWordViewSet,BookViewSet
router = routers.DefaultRouter()
keyword_router=router.register('keywords', KeyWordViewSet, basename='keywords')
books_router = routers.NestedDefaultRouter(router , 'keywords', lookup='keyword') # in lookup means product_pk
books_router.register('books', BookViewSet , basename='keyword-books')

urlpatterns = router.urls + books_router.urls