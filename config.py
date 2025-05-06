# config.py

import ujson

class Config:
    """
    Configuration class to manage device settings.
    """

    def __init__(self, file_path="config.json"):
        self.file_path = file_path
        self.config_data = {}
        self.data = self._load_config()

    def _load_config(self):
        try:
            with open("config.json", "r") as f:
                return ujson.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return {}

    def get(self, key, default=None):
        """
        Get a configuration value by key.

        :param key: Configuration key.
        :param default: Default value if key not found.
        :return: Configuration value or default.
        """
        return self.config_data.get(key, default)

    @property
    def data(self):
        """
        Returns a copy of the full config dictionary.
        Prevents accidental modification of the internal config state.
        """
        return self._config.copy()