from links_checker.views import Check
routes = [
    ('*', '/', Check, 'check'),
]