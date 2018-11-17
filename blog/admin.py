from django.contrib import admin
from blog.models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['STATUS_CHOICES','title','slug','author','body','publish','created','updated','status']
    list_filter = ('status','created','author','publish')
    search_fields = ('title','body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug':('title',)}
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','body','created','updated','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
