from django.contrib import admin
from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer


admin.site.register(Question)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
