DEFAULT_SERVER = "http://ftp.luminlinux.ru"
AVAILABLE_REPOSITORIES = [ "core", "stable", "testing" ]

def check_repository_available(repository):
    if repository in AVAILABLE_REPOSITORIES:
        return True
    else:
        return False

def get_repository_url(repository):
    if not check_repository_available(repository=repository):
        return ""
    return f"{DEFAULT_SERVER}/{repository}"