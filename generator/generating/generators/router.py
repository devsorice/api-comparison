class VariableComponent:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f":{self.name}"

class Route:
    def __init__(self, components):
        self.components = components

    def __str__(self):
        return "/".join(str(component) for component in self.components)


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, page):
        self.routes[route] = page

    def match_url(self, url):
        path = url.split('?')[0]
        url_components = path.strip('/').split('/')

        for route, page in self.routes.items():
            if self.match_route(route, url_components):
                return page
        return None

    def match_route(self, route, url_components):
        if len(route.components) != len(url_components):
            return False

        for route_component, url_component in zip(route.components, url_components):
            if isinstance(route_component, VariableComponent):
                continue
            if route_component != url_component:
                return False
        return True
