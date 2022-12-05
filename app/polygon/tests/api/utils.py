def urljoin(root_url: str, *urls: str) -> str:
    return f'{"/".join((root_url.rstrip("/"), *(url.lstrip("/") for url in urls)))}/'
