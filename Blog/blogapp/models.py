from django.db import models

#creates a table(blogapp_post) in database
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

#creates two table(blogapp_comment,blogapp_comment_posts) in database
class Comment(models.Model):
    posts = models.ManyToManyField(Post)
    text = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.posts