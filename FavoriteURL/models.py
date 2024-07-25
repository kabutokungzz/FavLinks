from django.db import models

class Category(models.Model):
    type_name = models.CharField(max_length=128 , blank=True , null=True, unique=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-id']),
        ]
        ordering = ['type_name']

    def __str__(self):
        return '%s' % (self.type_name)


# FavoriteURL 
class Favorite_Url(models.Model):
    statuses = (
        ("valid ", "valid "),
        ("invalid ", "invalid "),
    )
    
    url_favorite = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='favorite_url', null=True, blank=True
    )
    status = models.TextField(default="valid", choices=statuses)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]
        ordering = ['-id']

    def __str__(self):
        return '%s' % (self.url_favorite,)


class Tags(models.Model):
    tage_name = models.CharField(max_length=128 , blank=True , null=True, unique=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['-id']),
        ]
        ordering = ['tage_name']

    def __str__(self):
        return '%s' % (self.tage_name)

# M<->M
class LinkData(models.Model):

    favorite_url = models.ForeignKey(
        Favorite_Url, on_delete=models.CASCADE, related_name='link_data', null=True, blank=True
    )
    # category = models.ForeignKey(
    #     Category, on_delete=models.CASCADE, related_name='link_data', null=True, blank=True
    # )
    tags = models.ForeignKey(
        Tags, on_delete=models.CASCADE, related_name='link_data', null=True, blank=True
    )
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['-id']),
        ]
        ordering = ['id']

    def __str__(self):
        return '%s - %s - %s' % (self.favorite_url  , self.tags)

class CheckUrlsLog(models.Model):

    datecheck = models.DateField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['-id']),
        ]
        ordering = ['id']

    def __str__(self):
        return '%s - %s - %s' % (self.favorite_url  , self.tags)