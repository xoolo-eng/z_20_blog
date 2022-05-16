from django.contrib import admin
from posts.models import Post, Comment, Tags
from django.utils.html import mark_safe


class PostAdmin(admin.ModelAdmin):
    list_display = ("show_img", "title", "is_moderated")
    readonly_fields = ("thumbnail",)
    list_filter = ("is_moderated", "is_updated")
    search_fields = ("title", "author__username", "author__first_name", "author__last_name")

    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 "post_img",
    #                 "author",
    #                 "image",
    #                 "title",
    #                 "text",
    #                 "tags",
    #                 # "created",
    #                 "is_updated",
    #                 "is_moderated",
    #                 "views",
    #                 "rating",
    #                 "thumbnail"
    #             )
    #         },
    #     ),
    # )
    #
    # def post_img(self, instance):
    #     return mark_safe('<img src="/media/{}" width="400px"/>'.format(instance.image))
    # post_img.short_description = "Image post"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "is_moderated")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tags)
