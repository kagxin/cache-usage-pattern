from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404
from django.forms import ModelForm
from app.models import Article, Comment
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection

con = get_redis_connection("default")

# Create your views here.

class ArticleFrom(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']


class CommentFrom(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'article']


class BaseView(View):
    def init_request(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        self.init_request(request, *args, **kwargs)
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class ArticleListView(View):
    model = Article
    form = ArticleFrom

    def get(self, *args, **kwargs):
        articles = map(article_list_info, Article.objects.all())
        return JsonResponse(list(articles), safe=False)

    def post(self, request, *args, **kwargs):

        f = ArticleFrom(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse(f.errors, status=400)


class ArticleDetailView(BaseView):
    model = Article

    def init_request(self, request, *args, **kwargs):
        super(ArticleDetailView, self).init_request(request, *args, **kwargs)
        try:
            self.article = Article.objects.get(pk=kwargs.pop('pk', 0))
        except Article.DoesNotExist:
            raise Http404('未找到对应文章.')

    def get(self, request, *args, **kwargs):

        return JsonResponse(article_detail_info(self.article), status=201)

    def delete(self, request, *args, **kwargs):
        self.article.delete()
        return HttpResponse(status=201) 

class CommentView(BaseView):

    def init_request(self, request, *args, **kwargs):
        super(CommentView, self).init_request(request, *args, **kwargs)
        try:
            self.article = Article.objects.get(pk=kwargs.pop('pk', 0))
        except Article.DoesNotExist:
            raise Http404('未找到对应文章.')

    def get(self, request, *args, **kwargs):
        comments = list(map(article_comments_info, self.article.comments.all()))
        return JsonResponse(comments, safe=False) 

    def post(self, request, *args, **kwargs):
        f = CommentFrom(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponse(status=201)
        else:
            return JsonResponse(f.errors, status=400)


class TestView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('test')


def article_list_info(article):
    article = {
            'pk': article.id,
            'title': article.title,
            'text': article.text,
            'create_time': article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
    return article

def article_detail_info(article):
    article = {
        'pk': article.id,
        'title': article.title,
        'text': article.text,
        'create_time': article.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'comments':list(map(article_comments_info, article.comments.all()))
        }
    return article

def article_comments_info(comment):
    comment = {
            'pk':comment.id,
            'text':comment.text,
            'article_id':comment.article.id,
        }
    return comment