from django.conf import settings


def get_connection_string():
    db_setting = settings.DATABASES['default']
    match db_setting['ENGINE']:
        case 'django.db.backends.sqlite3':
            connection_string = "sqlite:///" + db_setting['NAME']
        case 'django.db.backends.postgresql':
            connection_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(user=db_setting['USER'], password=db_setting['PASSWORD'], host=db_setting['HOST'], port=db_setting['PORT'], db=db_setting['NAME'])
        case 'django.db.backends.mysql':
            connection_string = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(user=db_setting['USER'], password=db_setting['PASSWORD'], host=db_setting['HOST'], port=db_setting['PORT'], db=db_setting['NAME'])
        case _:
            raise Exception(f"Database engine {db_setting['ENGINE'].split('.')[-1]}not supported")
    return connection_string
