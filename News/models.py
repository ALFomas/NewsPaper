from django.db import models
from django.contrib.auth.models import User
from News.resourses import POST_TYPE, news


class Author(models.Model):
    """ Model containing objects from all authors """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """ Method for update rating """
        post_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        comment_post_rating = self.post_set.aggregate(models.Sum('comment__rating'))['comment__rating__sum'] or 0
        comment_author = Comment.objects.filter(post__author=self)
        comment_rating = 0
        for comment in comment_author:
            comment_rating += comment.rating
        self.rating = post_rating * 3 + comment_post_rating + comment_rating
        self.save()

    def __str__(self):
        """ String generation method """
        return self.user.username


class Category(models.Model):
    """ Model News/Article Categories """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """ String generation method """
        return self.name


class Post(models.Model):
    """ Model containing articles and news """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=news)
    data_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        """ Preview method """
        if len(self.text) > 124:
            return self.text[:124] + "..."
        else:
            return self.text

    def like(self):
        """Method to make like"""
        self.rating += 1
        self.save()

    def dislike(self):
        """Method to make dislike"""
        self.rating -= 1
        self.save()

    def __str__(self):
        """ String generation method """
        return self.title


class PostCategory(models.Model):
    """Model for many-to-many Post - Category"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        """ String generation method """
        return f"{self.post.title} - {self.category.name}"


class Comment(models.Model):
    """Model containing comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    data_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        """Method to make like"""
        self.rating += 1
        self.save()

    def dislike(self):
        """Method to make dislike"""
        self.rating -= 1
        self.save()

    def __str__(self):
        """ String generation method """
        return f"{self.user.username} - {self.post.title}"
