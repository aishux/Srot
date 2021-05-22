from django.contrib import admin
from .models import *

# Register your models here.

class FilterAdmin(admin.ModelAdmin):
    list_filter = ['volunteer_deleted','volunteer_verify']

admin.site.register(Discussion)
admin.site.register(Plasma,FilterAdmin)
admin.site.register(Oxygen,FilterAdmin)
admin.site.register(Injection,FilterAdmin)
admin.site.register(Food,FilterAdmin)
admin.site.register(Beds,FilterAdmin)
admin.site.register(DiscussionComment)
admin.site.register(Volunteer)