import brevisurl.settings


def brevisurl_data(request):
    return {
        'BREVIS_BACKEND': brevisurl.settings.DEFAULT_BACKEND,
        'BREVIS_BACKEND_LOCAL_DOMAIN': brevisurl.settings.LOCAL_BACKEND_DOMAIN
    }