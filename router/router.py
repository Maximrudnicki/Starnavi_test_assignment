from controllers.user_controller import router as router_users
from controllers.post_controller import router as router_posts
from controllers.comment_controller import router as router_comments


all_routers = [
    router_users,
    router_posts,
    router_comments,
]   