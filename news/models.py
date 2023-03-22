from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Max


# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_posts = Post.objects.filter(author=self.pk).aggregate(post_rating=Sum('post_rating'))['post_rating']
        sum_rating_author_comment = Comment.objects.filter(user=self.pk).aggregate(comment_rating=Sum('comment_rating'))[
            'comment_rating']
        sum_rating_all_comment = Comment.objects.filter(post__author=self.id).aggregate(comment_rating=Sum('comment_rating'))[
            'comment_rating']
        all_rating = sum_rating_posts * 3 + sum_rating_author_comment + sum_rating_all_comment
        self.user_rating = all_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(unique=True, max_length=128)


class Post(models.Model):
    post = 'Post'
    news = 'News'

    POSITION = [
        (post, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_or_news = models.CharField(max_length=4, choices=POSITION)
    date_add = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=128)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return self.content[:124] + '...'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
