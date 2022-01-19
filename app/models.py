from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class BestTags(models.Manager):
    def best_tags():
        return Tag.objects.all()


class BestUsers(models.Manager):
    def best_users():
        return User.objects.all()


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-id')

    def hot_question(self):
        return self.order_by('-like')

    def tags_question(self, tag_name):
        tag = Tag.objects.get(name= tag_name)
        return self.filter(tags=tag)


class AnswerManager(models.Manager):
    def get_question(self, question):
        return self.filter(question=question)


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(default=500)
    like = models.IntegerField(default=0, blank=True, null=True)
    dislike = models.IntegerField(default=0, blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='questions')
    author = models.ForeignKey('Profile', related_name='questions', on_delete=models.CASCADE)
    objects = QuestionManager()


class Answer(models.Model):
    text = models.TextField(default=5000)
    like_counter = models.IntegerField(default=0)
    dislike_counter = models.IntegerField(default=0)
    checked = models.BooleanField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE)
    author = models.ForeignKey('Profile', related_name='profile_answer', on_delete=models.CASCADE)
    objects = AnswerManager()


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return ' '.join([self.name])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='modefide_user', default=31007)
    avatar = models.ImageField(upload_to='img', default='uploads/img/Anon.jpg', blank=True, null=True)


class LikeQuestion(models.Model):
    user = models.ForeignKey('Profile', related_name='users_like_question', on_delete=models.CASCADE)
    check = models.BooleanField(default=False)
    question = models.ForeignKey('Question', related_name='question', on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = [('user', 'question', 'check'), ]


class LikeAnswer(models.Model):
    user = models.ForeignKey('Profile', related_name='users_like_answer', on_delete=models.CASCADE)
    check = models.BooleanField(default=False)
    answer = models.ForeignKey('Answer', related_name='answer', on_delete=models.CASCADE)

    class Meta:
        unique_together = [('user', 'answer', 'check'), ]
