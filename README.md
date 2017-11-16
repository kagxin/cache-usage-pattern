### cache aside

##### 读取数据伪代码:
```
    data = get_data_form_cache(identify)
    if data:
        return data
    else:
        data = get_data_form_sor(identify)
        set_data_to_cache(identify, data, expire)
        return data
```
* 先从缓存中获取数据，如果获取到数据（命中缓存），就直接返回数据。
* 如果未获取到数据就从数据库中获取数据，并更新缓存，然后返回数据。

##### 更新数据：
```
    save_update_data_to_sor(identify, update_data)
    delete_data_of_cache(identify)
```
* 将数据更新过的数据保存到数据库中,然后失效对应缓存。

##### dog-pile-effect:
* 防止缓存失效时，同时有很多个并发请求导致的，数据库压力陡增的问题（dog-pile-effect)
* 通过cache中的key锁保证。


### cache as SoR
#### read through
#### write through
#### write behind

    