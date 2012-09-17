import brevisurl.settings


def brevisurl_data(request):
    return {
        # Still present due to historic reasons. Now deprecated.
        'BREVIS_BACKEND': brevisurl.settings.DEFAULT_BACKEND,
        'BREVIS_BACKEND_LOCAL_DOMAIN': brevisurl.settings.LOCAL_BACKEND_DOMAIN,
        # Up-to-date context variables.
        'BREVISURL_BACKEND': brevisurl.settings.DEFAULT_BACKEND,
        'BREVISURL_BACKEND_LOCAL_DOMAIN': brevisurl.settings.LOCAL_BACKEND_DOMAIN,
        'BREVISURL_LOCAL_BACKEND_TOKEN_CHARS': brevisurl.settings.LOCAL_BACKEND_TOKEN_CHARS,
        'BREVISURL_LOCAL_BACKEND_TOKEN_LENGTH': brevisurl.settings.LOCAL_BACKEND_TOKEN_LENGTH,
        'BREVISURL_LOCAL_BACKEND_URL_PATTERN': brevisurl.settings.LOCAL_BACKEND_URL_PATTERN,
        'BREVISURL_LOCAL_BACKEND_DOMAIN_PROTOCOL': brevisurl.settings.LOCAL_BACKEND_DOMAIN_PROTOCOL
    }