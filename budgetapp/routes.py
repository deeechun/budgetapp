def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('verify_login', '/verify_login')
    config.add_route('add_bank', 'add_bank/{account_type}')