from django.db import models

class Page(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    num_links = models.IntegerField(default=0)
    is_processing = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

