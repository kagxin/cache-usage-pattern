
"""
cache-aside-pattern

伪代码:
    读取数据:
        data = get_data_form_cache(id)
        if data:
            return data
        else:
            data = get_data_form_sor(id)
            set_data_to_cache(id, data, expire)
            return data
        先从缓存中获取数据，如果获取到数据（命中缓存），就直接放回数据。
        如果未获取到数据就从数据库中获取数据，并更新缓存，然后返回数据。
    更新数据：
        id = save_update_data_to_sor(data)
        delete_data_of_cache(id)
        将数据更新过的数据保存到数据库中，
        然后失效对应缓存。

dog-pile-effect:
    防止缓存失效时，同时有很多个并发请求导致的，数据库压力陡增的问题（dog-pile-effct），通过cache中的key锁保证。
"""



## example 中的详情view
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

"""
缓存粒度，可以是整个网站，单个view，单个函数返回值，数据库一条数据，单个数据
这里缓存的是返回文章数据函数的返回值。
"""
