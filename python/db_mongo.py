import sys

from collections import namedtuple
from pymongo import uri_parser, MongoClient

__all__ = ['connect', 'db_collection']


"""Information stored with each connection alias."""
ConnectionInfo = namedtuple(
    'ConnectionInfo', ('parsed_uri', 'conn_string', 'database'))

DEFAULT_CONNECTION_ALIAS = 'default'

_CONNECTIONS = dict()


def connect(mongodb_uri, alias=DEFAULT_CONNECTION_ALIAS, **kwargs):
    """Register a connection to MongoDB, optionally providing a name for it.

    :parameters:
      - `mongodb_uri`: A MongoDB connection string. Any options may be passed
        within the string that are supported by PyMongo. `mongodb_uri` must
        specify a database, which will be used by modules that use this connection.
      - `alias`: An optional name for this connection, backed by a
        :class:`~pymongo.mongo_client.MongoClient` instance that is cached under
        this name. You can specify what connection a celery worker uses by
        specifying the connection's alias when calling this function from within
        the `init_worker` function.
        Note that calling `connect()` multiple times with the same
        alias will replace any previous connections.
      - `kwargs`: Additional keyword arguments to pass to the underlying
        :class:`~pymongo.mongo_client.MongoClient`.

    """
    # Make sure the database is provided.
    parsed_uri = uri_parser.parse_uri(mongodb_uri)
    if not parsed_uri.get('database'):
        raise ValueError('Connection must specify a database.')
    _CONNECTIONS[alias] = ConnectionInfo(
        parsed_uri=parsed_uri,
        conn_string=mongodb_uri,
        database=MongoClient(mongodb_uri, **kwargs)[parsed_uri['database']])


def _get_connection(alias=DEFAULT_CONNECTION_ALIAS):
    """Return a `ConnectionInfo` by connection alias."""
    try:
        return _CONNECTIONS[alias]
    except KeyError:
        _, _, tb = sys.exc_info()
        raise ValueError("No such alias '%s'. Did you forget to call connect()?" % alias).with_traceback(tb)


def get_db(alias=DEFAULT_CONNECTION_ALIAS):
    """Return the `pymongo.database.Database` instance for the given alias."""
    return _get_connection(alias).database


def db_collection(collection_name, alias=DEFAULT_CONNECTION_ALIAS):
    """ Return the named collection from the mongoDB """
    return get_db(alias)[collection_name]
