from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    # Include files, directories, and packages to the configuration
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.include('.utils')
    # Scan the following directories/files you've included above
    config.scan()
    return config.make_wsgi_app()
