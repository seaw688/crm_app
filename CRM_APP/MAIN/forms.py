from django.forms import ModelForm,fields,forms
from .models import Project
from slugify import slugify

class ProjectForm(ModelForm):
    #slug = fields.SlugField(required=False,widget=fields.HiddenInput())

    class Meta:
        model = Project
        fields = ['title','description','users','logo']


    def clean(self):
        super().clean()

        slug=self.cleaned_data['title']
        i = 0
        while i < 9999999:
            i += 1
            if Project.objects.filter(slug=slug).exists():
                slug = slug + "-" + str(i)
            else:
                break

        self.cleaned_data['slug']=slug


    def save(self, commit=True):
        project = super().save(commit=False)
        project.slug = self.cleaned_data['slug']
        project.save()
        return project



    # def clean_slug(self):
    #     slug=self.cleaned_data['title']
    #     i = 0
    #     while i < 9999999:
    #         i += 1
    #         if Project.objects.filter(slug=slug).exists():
    #             slug = slug + "-" + str(i)
    #         else:
    #             break
    #
    #     self.cleaned_data['slug']=slug
    #     data = self.cleaned_data['slug']
    #     return data



    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     slug = slugify(cleaned_data['title'])
    #
    #     print(slug)
    #     if Project.objects.filter(slug=slug).exists():
    #         print('x')
    #
    #     else:
    #         print('y')
    #
    #     i=0
    #     while i < 1000 :
    #         print('we in cycle')
    #         i += 1
    #         if Project.objects.filter(slug=slug).exists():
    #             slug = slug + "-"+str(i)
    #             print(slug)
    #         else:
    #             break
    #
    #     cleaned_data['slug']=slug