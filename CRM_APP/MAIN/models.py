from django.db import models
from CRM_APP import settings
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def project_logo_upload_path(instance, filename):
    return str(settings.MEDIA_ROOT + '/projects/{0}/logo/{1}'.format(instance.slug, filename))


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=2000)
    logo = models.ImageField(upload_to=project_logo_upload_path )
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.slug)


TASK_TYPES = (
    ("OTHER", "Other"),
    ("BUG", "Bug"),
    ("FEATURE", "Feature"),
)

TASK_STATUSES = (
    ("TO-DO", "To do"),
    ("IN-PROGRESS", "In progress"),
    ("DONE", "Task done"),
    ("TEST", "In testing"),
    ("CLOSED", "Closed"),
    ("SUSPENDED", "Suspended")
)

TASK_PRIORITY = (
    ("NORMAL", "Normal priority"),
    ("HIGH", "High priority"),
    ("URGENT", "Urgent priority"),
    ("LOW", "Low priority"),
)


class Task(models.Model):
    title = models.CharField(max_length=100, )
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=2000)
    kind = models.CharField(max_length=20, choices=TASK_TYPES, default=TASK_TYPES[0][0])
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default=TASK_STATUSES[0][0])
    priority = models.CharField(max_length=20, choices=TASK_PRIORITY, default=TASK_PRIORITY[0][0])
    estimation = models.DecimalField(max_digits=5, decimal_places=1, default=0, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tasks')
    created = models.DateTimeField(auto_now=True)
    executor = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='user_tasks')

    def __str__(self):
        return 'Task: {0} № {1}'.format(self.slug,self.pk)