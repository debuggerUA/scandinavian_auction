from settings import *

for index, app in enumerate(INSTALLED_APPS):
    if app.startswith('scandinavian_auction.'):
        INSTALLED_APPS[index] = app.split('.',1)[1]
