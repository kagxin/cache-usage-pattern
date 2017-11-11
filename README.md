### cache aside

#### 1、读操作
```buildoutcfg
        @命中缓存：直接从cache中取出数据返回。
        @缓存失效：应用程序从cache中读取数据，没有等到对应的数据，则从SoR中读取对应数据，放入cache中，然后返回数据。
```
#### 2、写数据
```buildoutcfg
        @将数据存入数据库，成功后使cache失效。
```
### cache as SoR
#### read through
#### write through
#### write behind

    