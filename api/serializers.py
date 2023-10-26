from rest_framework import serializers
from .models import Keyword,Book

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','address','description','image','year','size']

class KeywordsSerializer(serializers.ModelSerializer):
    books_url = serializers.SerializerMethodField()
    class Meta:
        model = Keyword
        fields = ['id','name','books_url']
    def get_books_url(self, obj):
        request = self.context.get('request')
        if request:
            keyword_id = obj.id
            return request.build_absolute_uri(f'/api/keywords/{keyword_id}/books')
        return None