# ISDN-Python

[ISDN (International Standard Dojin Numbering)](https://isdn.jp/) のPythonライブラリとCLIツール

## Install

```
$ pip install isdn
```

## Example

```python
>>> from isdn import ISDN
>>> isdn = ISDN("2784702901978")
>>> isdn.validate()
True
>>> ISDN.calc_check_digit("2784702901978")
'8'
```

```python
>>> from isdn import ISDNClient
>>> client = ISDNClient()
>>> record = client.get("2784702901978")
>>> record.isdn
ISDN(code='2784702901978', prefix='278', group='4', registrant='702901', publication='97', check_digit='8')
>>> record.product_name
'みほん同人誌'
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
```
