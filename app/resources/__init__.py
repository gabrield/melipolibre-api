import jsonschema


def validate_http_https_url(instance):
    import re
    url_pattern = re.compile(r'^https?://[\w\-\.]+\.\w+(:\d+)?(/\S*)?$')
    return url_pattern.match(instance) is not None


# Register the custom format with jsonschema
jsonschema \
    .FormatChecker(
    ).validators['http-https-url'] = validate_http_https_url
