from django.contrib import admin
from .models import *

from .models import Thread, ChatMessage

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Category)