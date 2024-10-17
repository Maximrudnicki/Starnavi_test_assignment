from controllers.user_controller import router as router_users
from controllers.post_controller import router as router_posts


all_routers = [
    router_users,
    router_posts,
]   