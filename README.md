### cache aside

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
            先从缓存中获取数据，如果获取到数据（命中缓存），就直接返回数据。
            如果未获取到数据就从数据库中获取数据，并更新缓存，然后返回数据。
        更新数据：
            save_update_data_to_sor(id, update_data)
            delete_data_of_cache(id)
            将数据更新过的数据保存到数据库中，
            然后失效对应缓存。
    next ----> 消除dog pile effect
### cache as SoR
#### read through
#### write through
#### write behind

    