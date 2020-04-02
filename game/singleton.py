class Singleton:
    def __init__(self, custom_class):
        self.custom_class = custom_class
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.custom_class(*args, **kwargs)
        return self.instance
