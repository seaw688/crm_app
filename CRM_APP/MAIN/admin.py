from django.contrib import admin
from MAIN.models import Project, Task, TaskComment, TimeLog

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TimeLog)