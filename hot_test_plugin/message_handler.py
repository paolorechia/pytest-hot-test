from hot_test_plugin import settings


messages = []

def debug_statement(*args):
    if settings.DEBUG:
        messages.append(args)

