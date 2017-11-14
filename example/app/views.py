from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404
from django.forms import ModelForm
from app.models import Article, Comment
from django.core import serializers
# Create your views here.

class ArticleFrom(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']

class CommentFrom(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'article']

class ArticleListView(View):
    model = Article
    form = ArticleFrom

    def get(self, *args, **kwargs):
        articles = serializers.serialize('json', self.model.objects.all(), fields=('title', 'text', 'create_time'))
        return HttpResponse(articles, content_type='application/json')

    def post(self, request, *args, **kwargs):
        print(request.POST.get('title'))

        f = ArticleFrom(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse(f.errors, status=400)

class ArticleDetail(View):
    model = Article

    def get(self, request, *args, **kwargs):
        try:
            article = self.model.objects.get(pk=kwargs.pop('pk', 0))
        except Article.DoesNotExist:
            raise Http404('未找到对应文章.')
#         article_s = serializers.serialize('json', [article])

        return HttpResponse(status=201)

class TestView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('test')


