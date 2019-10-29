# Faker - 为生成虚假数据而生:smirk:

去年为了生成一些人员信息的测试数据，包括姓名、性别、地址、电话号码、身份证号等信息，我挨个写了函数来进行随机生成。当时，就想有空了要写一个Python包来自动化生成这些数据，最好是能用上LSTM等神经网络，通过读入一系列的真实数据，便能够自动生成“以假乱真”的虚假数据。现在想想还觉得这个功能挺诱人的，是不是可以再好好考虑考虑？:blush:

Faker是最近发现的一个可以快速方便地生成虚假数据的Python包，看了它的文档，就知道当时轮子又白造了。在工作中，如果有生成虚假数据做一些测试或者演示的需求的，可以考虑使用一下。下面是一些利用Faker生成中文虚假数据实例，详细的文档强烈推荐官方文档[^1]。

## 安装引用

```python
pip install Faker
########################
from faker import Faker
fake = Faker('zh_CN')
```

## 地址

```python
fake.address()
# '云南省哈尔滨市东丽巢湖街I座 754201'

fake.city_name()
# '沈阳'
```

## 人名

```python
fake.name()
#'雷桂香'

fake.name_female()
#'陈小红'

fake.name_male()
#'尹慧'
```

## 公司

```python
fake.company()
# '晖来计算机科技有限公司'
```

## 电话号码

```python
fake.phone_number()
# '13290223533'
```

## 用户资料

```python
fake.profile()
# {'job': '营业部大堂经理', 'company': '方正科技网络有限公司', 'ssn': '410421199901249884', 'residence': '西藏自治区福州县普陀邯郸路b座 300649', 'current_location': (Decimal('58.033016'), Decimal('-99.820126')), 'blood_group': 'O-', 'website': ['http://min.cn/'], 'username': 'leihao', 'name': '姚琳', 'sex': 'F', 'address': '吉林省萍县黄浦荆门路A座 402305', 'mail': 'tlu@yahoo.com', 'birthdate': datetime.date(1972, 11, 26)}
```

## 地理位置

```python
fake.latitude()
# Decimal('-69.002703')

fake.longitude()
# Decimal('71.104808')
```

## 大段文字

```python
fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
# '参加浏览如何不要.起来到了管理投资设计工具孩子.安全中心大学运行经济.'

fake.text(max_nb_chars=200, ext_word_list=None)
#'很多空间她的.网络提供程序规定.生活都是大学社会应用报告.\n程序发布会员中心希望标题.论坛行业怎么非常.密码您的不过日期资源用户.\n学校北京商品一切现在.现在首页规定.这些没有行业.\n相关可是推荐欢迎.制作他们事情产品经营研究.\n但是数据其实软件.\n网站如果决定业务.合作那些全部系列质量.\n一种安全如此研究起来.朋友发展可是手机.不同责任推荐威望安全拥有市场是否.'
```

## 浏览器信息

```python
fake.chrome(version_from=13, version_to=63, build_from=800, build_to=899)
#'Mozilla/5.0 (Windows 98; Win 9x 4.90) AppleWebKit/5362 (KHTML, like Gecko) Chrome/28.0.816.0 Safari/5362'
```

## 其他

```python
fake.md5(raw_output=False)
# '47ebdf4d67740d0c9f68819e850ddb50'

fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
# 'pD0ZTvUz!1'
```

除了上面展示的这些，利用Faker还可以生成**二进制文件**、**文件名**、**IP地址**、**MAC地址**、**邮箱**、**URL**、**银行卡**、**车牌号**、**条形码**、**颜色值**、**年月日**、**Python内置数据**等信息。官方文档[^1]提供了非常详细的说明，一定要浏览一下。造数据也是一个技术活。:joy:

------

### 参考链接

[^1]:  <https://faker.readthedocs.io/en/master/>

