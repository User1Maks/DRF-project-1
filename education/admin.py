from django.contrib import admin

from education.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'owner',)
    search_fields = ('id', 'name', 'owner')
    list_filter = ('name', 'owner',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_to_video', 'course', 'owner',)
    search_fields = ('id', 'name', 'course', 'owner')
    list_filter = ('name', 'owner',)
