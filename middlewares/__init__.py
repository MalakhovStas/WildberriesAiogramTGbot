from loader import dp
from .access_control import AccessControlMiddleware

if __name__ == 'middlewares':
    dp.middleware.setup(AccessControlMiddleware())

