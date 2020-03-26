# 阿里云对象存储-oss

oss 是阿里云对外提供的基于网络的数据存储服务，可以用来存储和获取各种文件，包括文本，图片，视频，音频等

## 控制台

1. 开通 oss，在阿里云官网搜索 oss，可以找到 oss 产品的入口，点击折扣套餐，可以先购买个体验套餐标准 LRS 存储包，40G * 半年 / 3.6￥
2. 创建 bucket，bucket 可以类比为一块磁盘，任何数据都会存储在一个特定的 bucket 中，一个 bucket 下也可以建立文件目录
   - 打开 oss 控制台: <https://oss.console.aliyun.com/overview>
   - 【Bucket 管理】 → 【创建 Bucket】，填写 bucket 名称，选择 bucket 所在的地区

控制台上还有 bucket 的管理，文件的上传下载等功能，都比较直观

## ossutil

安装

```
curl -o /usr/local/bin/ossutilmac64 http://gosspublic.alicdn.com/ossutil/1.6.10/ossutilmac64
chmod 755 /usr/local/bin/ossutilmac64
ln -s /usr/local/bin/ossutilmac64 /usr/local/bin/ossutil
```

配置

```
ossutil config
```

- endpoint: 地域(region)信息，比如：oss-cn-beijing.aliyuncs.com，地域和 region 对照表 <https://help.aliyun.com/document_detail/31837.html?spm=a2c4g.11186623.2.19.566f448avXOpXk#concept-zt4-cvy-5db>
- accessKeyID 和 accessKeySecret: <https://help.aliyun.com/document_detail/53045.html?spm=a2c4g.11186623.2.20.566f448avXOpXk#task-1715673>
- stsToken: 可选项，STS临时授权，<https://help.aliyun.com/document_detail/31852.html?spm=a2c4g.11186623.2.22.566f448avXOpXk#section-dvv-hkb-5db>

配置文件保存在 `~/.ossutilconfig` 目录，这个文件可以手动编辑修改

列出对象

```
ossutil ls
ossutil ls oss://hatlonely-test-bucket
ossutil ls oss://hatlonely-test-bucket --limited-num=1
```

上传下载

```
echo "hello oss" > hello.txt
ossutil cp hello.txt oss://hatlonely-test-bucket/
ossutil cp hello.txt oss://hatlonely-test-bucket/123/
ossutil cp oss://hatlonely-test-bucket/hello.txt .
```

查看文件

```
ossutil stat oss://hatlonely-test-bucket/hello.txt  # 文件元数据信息
ossutil cat oss://hatlonely-test-bucket/hello.txt   # 查看文件数据
```

删除

```
ossutil rm oss://hatlonely-test-bucket/hello.txt    # 删除单个文件
ossutil rm -r oss://hatlonely-test-bucket/123       # 删除目录
```

## 链接

- oss 帮助文档: <https://help.aliyun.com/document_detail/31883.html?spm=5176.8466029.0.0.697a1450iKedXW>
