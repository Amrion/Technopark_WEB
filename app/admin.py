from django.contrib import admin

# Register your models here.


from app.models import Question, Answer, Tag, Profile, LikeQuestion, LikeAnswer


admin.site.register(Question)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)