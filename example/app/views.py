from django.views.generic import View
from django.http import HttpResponse, JsonResponse, Http404, HttpRequest
from django.forms import ModelForm
from app.models import Article, Comment
from django.core.cache import cache
from .lock import DogPileLock

# conn = get_redis_connection("default")

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


class ArticleListView(BaseView):
    model = Article
    form = ArticleFrom

    def get(self, request, *args, **kwargs):
        articles = list(map(article_list_info, Article.objects.all()))  
        return JsonResponse(articles, safe=False)  

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

    def get(self, request, *args, **kwargs):  # cache-aside 读方式

        # 防止缓存失效时，同时有很多个并发请求导致的，数据库压力陡增的问题（dog-pile-effct），通过锁保证。
        with DogPileLock('lock_article:detail:%d' % self.article.id, cache):
            article_detail = cache.get('article:detail:%d' % self.article.id) # 从缓存中取数据

        if article_detail:  # 命中缓存
            return JsonResponse(article_detail, safe=False)  # 直接返回
        else:  # 未命中缓存 
            article_detail = article_detail_info(self.article)  # 从数据库中去取数据
            cache.set('article:detail:%d' % self.article.id, article_detail, 10)  # 更新缓存，过期时间为10s

        return JsonResponse(article_detail)  # 返回数据

    def post(self, request, *args, **kwargs):  # update更新数据接口.(更新的 HTTP原语为PUT,为使用表单使用了post)
        f = ArticleFrom(request.POST, instance=self.article)  # 更新article数据
        if f.is_valid():
            article = f.save()   # 更新成功
            cache.delete('article:detail:%d' % article.id)  # 失效缓存.
            return HttpResponse(status=201)
        else:
            return JsonResponse(f.errors, status=400)

    def delete(self, request, *args, **kwargs):
        self.article.delete() # 删除成功
        cache.delete('article:detail:%d' % self.article.id)  # 失效缓存.
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
