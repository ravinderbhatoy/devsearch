from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def image_url(self):  
        try:
            url = self.featured_image.url
        except:
            url = '/images/default.jpg'
        return url

    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_vote = reviews.filter(value='up').count()
        total_votes = reviews.count()
        if total_votes == 0:
            ratio = 0
        else:
            ratio = (up_vote/total_votes) * 100
        self.vote_total = total_votes
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set

class Review(models.Model):
    VOTE_TYPE = (("up", "Vote up"), ("down", "Vote down"))
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )

    def __str__(self) -> str:
        return self.name
