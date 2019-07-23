from app.posts.models import Posts
from app.users.models import Users

def test_posts_init():
    test_post = Posts("a", "b", "c")
    assert type(test_post.author_id) is str
    assert type(test_post.title) is str
    assert type(test_post.body) is str

def test_users_init():
    test_user = Users("a", "b", "c")
    assert type(test_user.user_id) is str
    assert type(test_user.user_password) is str
    assert type(test_user.user_email) is str
