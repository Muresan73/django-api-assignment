from django.db import models


class Link(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.SlugField(unique=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)

    @property
    def get_score(self):
        return self.upvotes - self.downvotes

    def save(self, *args, **kwarg):
        self.score = self.get_score
        super(Link, self).save(*args, **kwarg)
