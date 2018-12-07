from dulwich import porcelain
import time

def clone(repodir, repo_url):
    repo = porcelain.clone(repo_url, repodir)
    return repo
    # TODO: Progress Indicator?