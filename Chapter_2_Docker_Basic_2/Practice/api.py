from blog import query_all, add_user, add_post


def all():
    posts = query_all()
    return [
        {
            'id': post.id,
            'key': post.key,
            # 'title': post.title,
            # 'author': post.user,
            # 'content': post.content
        } for post in posts
    ]

def add_new_user(username: str, password: str):
    return add_user(username, password)

def add_new_post(title: str, content: str, username: str, password: str):
    return add_post(title, content, username, password)
