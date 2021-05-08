from .models import Post


def get_simple_table_data():
    data = Post.objects.all()
    return data
