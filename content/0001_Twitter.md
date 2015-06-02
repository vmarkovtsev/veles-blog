Title: Pelican + Twitter
Date: 2015-06-02 12:00
Modified: 2015-06-02 12:00
Category: Programming
Tags: twitter,git,pygit2,tweepy
Slug: twitter
Authors: Vadim Markovtsev
Summary: Pelican and Twitter can be integrated better

We picked [Pelican](http://blog.getpelican.com/) as the static blog generator after studying a somewhat outdated article about such generators ([in Russian](http://habrahabr.ru/post/93499/)). It appeared that there are many of them, and one can choose any which looks good. We've had a Python background, some experience with [Jinja2](http://jinja.pocoo.org/) templates (used in e.g. in publishers) and [GitHub flavored Markdown](https://help.github.com/articles/markdown-basics/) markup. Although our docs are made up with [Sphinx](http://sphinx-doc.org/) which adopts [reStructuredText](http://docutils.sourceforge.net/rst.html) markup, we like Markdown better for it's cleaner syntax and general availability (GitHub, StackOverflow, etc.). Personally, reStructuredText makes me suffer, and it is one of the reasons perhaps why Veles documentation currently sucks. Anyway, that Habrahabr article showed that Pelican perfectly suited our tastes.

It appeared to be really nice and easy to understand, and the docs are good. There is one feature that miss out of the box - automatic Twitter updates after publishing. I found [pelican_auto_tweet](https://github.com/quack1/pelican_auto_tweet) project on GitHub which seemed relevant,
but it does not support Python 3 and the code looked untidy. Then I recalled how I used excellent [tweepy](http://www.tweepy.org/) package for sending tweets and [pygit2](http://www.pygit2.org/) for Git scripting and the solution came.

Basically, I took ```libpelican.py``` from pelican_auto_tweet and the mentioned packages together with Jinja2. Refer to [tweet.py](https://github.com/vmarkovtsev/veles-blog/blob/master/tweet.py). ```auto_tweet()``` function is called on the script execution, which initializes ```tweepy.API``` instance and triggers ```status_update()``` with the rendered template for each new article (of class ```Article```). ```get_new_articles()``` is a generator (I love generators) which compares the current set of Pelican articles with those committed in Git, takes only one language in case of a multilingual blog, yields the constructed objects and finally does ```git commit``` followed by ```git push```. I added a new Makefile target "twitter" and set "ssh_upload" as the dependency.
 
 Thus ```make twitter``` publishes Pelican blog on disk, uploads it through SSH to velesnet.ml, creates the tweets pointing to new articles and finally pushes the changes back to my Git repository on GitHub. Sweet.