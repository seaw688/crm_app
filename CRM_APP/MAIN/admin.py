from django.contrib import admin
from MAIN.models import Project, Task, TaskComment, TimeLog ,TaskFile
from django.contrib.auth.models import Permission


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 2

class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TaskFileInline, ]



admin.site.register(Permission)
admin.site.register(Project)
admin.site.register(Task,TaskAdmin)
admin.site.register(TaskComment)
admin.site.register(TimeLog)