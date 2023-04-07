# ISDN-Python

[![PyPI version](https://badge.fury.io/py/isdn.svg)](https://badge.fury.io/py/isdn)
[![Test](https://github.com/Babibubebon/isdn-python/actions/workflows/test.yml/badge.svg)](https://github.com/Babibubebon/isdn-python/actions/workflows/test.yml)

[ISDN (International Standard Dojin Numbering)](https://isdn.jp/) のPythonライブラリとCLIツール

## Install

```
$ pip install isdn
```

## Example

ISDNを[番号の仕様](https://isdn.jp/about.html)に従って検証

```python
>>> from isdn import ISDN
>>> isdn = ISDN("2784702901978")
>>> isdn.validate()
True
>>> ISDN.calc_check_digit("2784702901978")
'8'
```

isdn.jp が提供している書誌情報を取得 ([Web からの情報取得](https://isdn.jp/about.html))

```python
>>> from isdn import ISDNClient
>>> client = ISDNClient()
>>> record = client.get("2784702901978")
>>> record.isdn
ISDN(code='2784702901978', prefix='278', group='4', registrant='702901', publication='97', check_digit='8')
>>> record.product_name
'みほん同人誌'
>>> record
ISDNRecord(
    isdn=ISDN(
        code='2784702901978',
        prefix='278',
        group='4',
        registrant='702901',
        publication='97',
        check_digit='8'
    ),
    region='日本',
    class_='オリジナル',
    type='同人誌',
    rating_gender='区別なし',
    rating_age='一般',
    product_name='みほん同人誌',
    product_yomi='みほんどうじんし',
    publisher_code='14142139',
    publisher_name='見本サークル',
    publisher_yomi='みほんさーくる',
    issue_date=datetime.date(2008, 3, 12),
    genre_code='106',
    genre_name='評論・情報',
    genre_user=None,
    c_code='C3055',
    author='専門',
    shape='単行本',
    contents='電子通信',
    price=Decimal('100'),
    price_unit='JPY',
    barcode2='2923055001007',
    product_comment=None,
    product_style=None,
    product_size=None,
    product_capacity=None,
    product_capacity_unit=None,
    sample_image_uri=HttpUrl('https://isdn.jp/images/thumbs/2784702901978.png', ),
    useroptions=[
        UserOption(property='執筆者', value='みほん執筆者1'),
        UserOption(property='執筆者', value='みほん執筆者2'),
        UserOption(property='執筆者', value='みほん執筆者3'),
        UserOption(property='執筆者', value='みほん執筆者4'),
        UserOption(property='執筆者', value='みほん執筆者5'),
        UserOption(property='執筆者', value='みほん執筆者6')
    ],
    external_links=[
        ExternalLink(title='国際標準同人誌番号', uri=HttpUrl('http://isdn.jp/', )),
        ExternalLink(
            title='mixiコミュニティ',
            uri=HttpUrl('http://mixi.jp/view_community.pl?id=3188828', )
        )
    ]
)
```

## CLI

指定したISDNの形式を検証

```
$ isdn validate 2784702901978
```

指定したISDNの書誌情報を isdn.jp から取得

```
$ isdn get 2784702901978
$ isdn get 2784702901978 --format json
```

ISDNの一覧を isdn.jp から取得

```
$ isdn list
```

すべての書誌情報を isdn.jp から取得してファイルに保存

```
$ isdn bulk-download /path/to/download
$ isdn bulk-download /path/to/download --write-image
```
