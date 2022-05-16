import pathlib
from random import randrange
from datetime import datetime
from django.db import models
from django.dispatch.dispatcher import receiver
from user.models import User
from django.conf import settings
from django.utils.html import mark_safe
from PIL import Image


class Post(models.Model):
    def file_path(self, filename):
        file = pathlib.Path(filename)
        ext = file.suffix or ".png"
        path = (
                datetime.strftime(datetime.now(), "post/%Y/%m/%d/%H/%M%S")
                + str(round(datetime.now().timestamp() * 1000000))
                + str(randrange(1, 100000000))
        )
        return path + ext

    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=file_path)
    thumbnail = models.ImageField(upload_to=file_path, blank=True, null=True)
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField("Tags", related_name="posts")
    created = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    rating = models.SmallIntegerField(validators=[])
    slug = models.SlugField(blank=True)  # TODO: autoset

    def show_img(self):
        return mark_safe('<img src="/media/{}"/>'.format(self.thumbnail))

    show_img.short_description = "Head img"
    show_img.allow_tags = True

    class Meta:
        db_table = "posts"

    def save(self, **kwargs):
        super().save(**kwargs)
        # если что то менялось
        self.create_thumbnail()

    def create_thumbnail(self):
        img_path = pathlib.Path(self.image.path)
        thum_path = pathlib.Path(img_path.parent, "min_" + str(img_path.name))
        if not thum_path.exists():
            img = Image.open(self.image.path).convert("L")
            height = 100
            width = round(img.size[0] * height / img.size[1])
            img.thumbnail((width, height), Image.ANTIALIAS)
            new_path = thum_path.as_posix()
            media_path = settings.MEDIA_ROOT.as_posix()
            new_path = new_path.replace(media_path, "")
            new_path = new_path.strip("/")
            self.thumbnail = new_path
            img.save(thum_path)
            self.save()

    def __str__(self):
        return self.title[:20]


@receiver(models.signals.pre_save, sender=Post)
def is_update_comment(sender, instance, **kwargs):
    if instance.id is not None:
        instance.is_updated = True


@receiver(models.signals.pre_save, sender=Post)
def create_slug(sender, instance, **kwargs):
    if instance.id is None:
        instance.slug = str(hash(str(instance.title).encode("utf-8")))[1:]


@receiver(models.signals.pre_delete, sender=Post)
def clean_image(sender, instance, **kwargs):
    path_to_img = settings.BASE_DIR / str(instance.image.path)
    path_to_tmb = settings.BASE_DIR / str(instance.thumbnail.path)
    try:
        path_to_img.unlink()
        path_to_tmb.unlink()
    except Exception as error:
        print(error)


class Comment(models.Model):
    def file_path(self, filename):
        file = pathlib.Path(filename)
        ext = file.suffix or ".png"
        path = (
                datetime.strftime(datetime.now(), "post/comment/%Y/%m/%d/%H/%M%S")
                + str(round(datetime.now().timestamp() * 1000000))
                + str(randrange(1, 100000000))
        )
        return path + ext

    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    image = models.ImageField(upload_to=file_path, null=True, blank=True)
    parent = models.ForeignKey("Comment", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f"Comment for {self.post.title}: {self.id}"


@receiver(models.signals.pre_save, sender=Comment)
def is_update_comment(sender, instance, **kwargs):
    if instance.id is not None:
        instance.is_updated = True
        # instance.is_moderated = False
        # send_email_to_moderator()


@receiver(models.signals.pre_delete, sender=Comment)
def clean_image(sender, instance, **kwargs):
    path_to_img = settings.BASE_DIR / str(instance.image.path)
    try:
        path_to_img.unlink()
    except Exception as error:
        print(error)


class Tags(models.Model):
    # TODO: validators for name
    name = models.CharField(max_length=25, verbose_name="#tag")
    slug = models.SlugField(max_length=24, blank=True)

    class Meta:
        db_table = "tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


@receiver(models.signals.pre_save, sender=Tags)
def edit_tag(sender, instance, **kwargs):
    if not instance.name.startswith("#"):
        instance.name = "#" + instance.name

    instance.slug = instance.name.strip("#")
