from rest_framework.viewsets import ModelViewSet
from .models import Book,Keyword
from .serializers import KeywordsSerializer,BooksSerializer
from rest_framework.filters import SearchFilter 
from .utils import search
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

# search("ahmed ali shah")
class KeyWordViewSet(ModelViewSet):
    queryset=Keyword.objects.filter(is_deleted=False)
    serializer_class=KeywordsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    def filter_queryset(self, queryset):
        search_query = self.request.query_params.get('search', None)
        if search_query:
            if len(search_query) <= 3:
                raise ValidationError("Search query must be longer than 3 characters.")
            queryset = queryset.filter(name=search_query)
            if not queryset:
                 search(search_query)
            queryset = queryset.filter(name=search_query)
        return queryset

class BookViewSet(ModelViewSet):
    serializer_class = BooksSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    page_size_query_param = 'page_size'
    def get_queryset(self):
        keyword_pk = self.kwargs.get('keyword_pk')
        if keyword_pk is not None:
            keyword = Keyword.objects.filter(id=keyword_pk).first()
            if keyword:
                return keyword.books.all()
        return Book.objects.none()
    def get_serializer_context(self):
        return {'keyword_pk': self.kwargs.get('keyword_pk')}