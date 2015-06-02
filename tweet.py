from collections import namedtuple
import os
import subprocess

from jinja2 import Template
from libpelican import PelicanBlog
from pygit2 import Repository, Signature
import tweepy
from pelicanconf import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, \
    TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET, TWITTER_TEMPLATE, \
    TWITTER_LANGUAGE


Article = namedtuple("Article", ("title", "url", "author"))


def get_new_articles():
    blog = PelicanBlog()
    content_dir = blog.get_content_directory()
    repo = Repository(os.path.abspath(os.path.dirname(__file__)))
    diff = repo.revparse_single("HEAD").tree.diff_to_tree()
    existing_articles = set(os.path.relpath(obj.old_file_path, content_dir)
                            for obj in diff
                            if obj.old_file_path.startswith(content_dir))
    all_articles = set(blog.get_posts())
    new_articles = {art for art in all_articles - existing_articles
                    if blog.get_post_lang(art) in (TWITTER_LANGUAGE, "")}
    new_titles = []
    repo.index.read()
    for newart in new_articles:
        title = blog.get_post_title(newart)
        yield Article(title, blog.get_post_url(newart),
                      blog.get_post_authors(newart))
        new_titles.append(title)
        repo.index.add(os.path.join(content_dir, newart))
    blogger = Signature(repo.config["user.name"], repo.config["user.email"])
    repo.create_commit("HEAD", blogger, blogger,
                       "[BLOG] %s" % ", ".join(new_titles),
                       repo.index.write_tree(), [repo.head.peel().oid])
    repo.index.write()
    # TODO(v.markovtsev): implement git push using pygit2
    subprocess.call(("git", "push", "origin", repo.head.shorthand))


def auto_tweet():
    template = Template(TWITTER_TEMPLATE)
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    for article in get_new_articles():
        status = api.update_status(status=template.render(article=article))
        print("Posted https://twitter.com/%s/status/%d" %
              (status.user.screen_name, status.id))

if __name__ == "__main__":
    auto_tweet()
