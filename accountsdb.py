"""
Shared code for database handling.
"""

import pickle

from supybot import ircdb, log, conf

class AccountsDB():
    """
    Abstraction to map users to third-party account names.

    This stores users by their bot account first, falling back to their
    ident@host if they are not logged in.
    """

    def __init__(self, plugin_name, filename):
        """
        Loads the existing database, creating a new one in memory if none
        exists.
        """
        self.db = {}
        self._plugin_name = plugin_name
        self.filename = conf.supybot.directories.data.dirize(filename)
        try:
            with open(self.filename, 'rb') as f:
               self.db = pickle.load(f)
        except Exception as e:
            log.debug('%s: Unable to load database, creating '
                      'a new one: %s', self._plugin_name, e)

    def flush(self):
        """Exports the database to a file."""
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.db, f, 2)
        except Exception as e:
            log.warning('%s: Unable to write database: %s', self._plugin_name, e)

    def set(self, prefix, newId):
        """Sets a user ID given the user's prefix."""

        try:  # Try to first look up the caller as a bot account.
            userobj = ircdb.users.getUser(prefix)
        except KeyError:  # If that fails, store them by nick@host.
            user = prefix.split('!', 1)[1]
        else:
            user = userobj.name

        self.db[user] = newId

    def get(self, prefix):
        """Sets a user ID given the user's prefix."""

        try:  # Try to first look up the caller as a bot account.
            userobj = ircdb.users.getUser(prefix)
        except KeyError:  # If that fails, store them by nick@host.
            user = prefix.split('!', 1)[1]
        else:
            user = userobj.name

        # Automatically returns None if entry does not exist
        return self.db.get(user)