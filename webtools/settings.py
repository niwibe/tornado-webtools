import copy

class MetaSettings(type):
    def __new__(cls, name, bases, attrs):
        super_attrs, settings = {}, {}
        for attr, val in attrs.items():
            if attr.startswith("__"):
                super_attrs[attr] = val
            else:
                settings[attr] = val

        instance = super(MetaSettings, cls).__new__(cls, name, bases, super_attrs)
        instance._settings.insert(0, settings)
        return instance


class BaseSettings(object):
    _settings = []

    def __init__(self):
        self.settings = copy.deepcopy(self._settings)

    def __getattr__(self, key):
        if key != key.upper():
            return super(BaseSettings, self).__getattr__(key)

        for settings_layer in self.settings:
            if key in settings_layer:
                return settings_layer[key]

        return None

    def configure(self, data):
        assert isinstance(data, dict), "Invalid parameters"
        self.settings.insert(0, data)

    def clear_to_default(self):
        original_settings = self._settings[-1]
        self.settings = [original_settings]


class Settings(BaseSettings, metaclass=MetaSettings):
    SESSION_ENGINE = 'webtools.session.backend.database.DatabaseEngine'
    SESSION_ENGINE_KWARGS = {}

    AUTHENTICATION_BACKENDS = []

    SQLALCHEMY_ENGINE_URL = None
    SQLALCHEMY_ENGINE_KWARGS = {}

    JINJA2_TEMPLATE_DIRS = []
    JINJA2_SETTINGS = {"cache_size": 100}

    TORNADO_TRANSFORMS = None
    TORNADO_DEFAULT_HOST = ""
    TORNADO_WSGI_MODE = False
    TORNADO_SETTINGS = {}

    SECRET_KEY = "sectet-key-change-me"

    PASSWORD_HASHERS = (
        'webtools.auth.hashers.PBKDF2PasswordHasher',
        'webtools.auth.hashers.PBKDF2SHA1PasswordHasher',
        'webtools.auth.hashers.BCryptPasswordHasher',
        'webtools.auth.hashers.SHA1PasswordHasher',
        'webtools.auth.hashers.MD5PasswordHasher',
        'webtools.auth.hashers.CryptPasswordHasher',
    )


__all__ = ['settings']
