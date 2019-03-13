from django.contrib import admin
from MAIN.models import Project, Task, TaskComment, TimeLog
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TimeLog)