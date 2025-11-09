# Winch Project

Development in real time.

## Mime Types

It's a Python syntax instead of string literals and is helpful for:

- Avoiding misprints
- Using of IDE hints

Usage:

```python
>>> from winch import mime_types

>>> str(mime_types.application.x_www_form_urlencoded())
'application/x-www-form-urlencoded'

>>> str(mime_types.text.html(charset='utf-8'))
'text/html;charset=utf-8'
```

Basically for usage with HTTP headers


## HTTP Headers
