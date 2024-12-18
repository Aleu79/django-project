from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

admin.site.register(Task, TaskAdmin)

class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  

admin.site.register(TaskCategory, TaskCategoryAdmin)

class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(TaskTag, TaskTagAdmin)

class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(TaskStatus, TaskStatusAdmin)

class TaskPriorityAdmin(admin.ModelAdmin):
    list_display = ('level',)  

admin.site.register(TaskPriority, TaskPriorityAdmin)

class TaskReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'reminder_time', 'message')

admin.site.register(TaskReminder, TaskReminderAdmin)
2