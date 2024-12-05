from decouple import config

class Config:
    SECRET_KEY = 'B!1weNAt1T%kyhUI+*S&'

class DevelopmentConfig (Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tienda'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587 # TLS: TRANSPORT LAYER SECURITY: SEGURIDAD DE LA CAPA DE TRANSPORTE
    MAIL_USE_TLS = True
    MAIL_USERNAME = '20213tn120@utez.edu.mx'
    MAIL_PASSWORD = config('MAIL_PASSWORD')
print(f"fdbgfdbghjjfghjkfdhgjkfdhkgjdfhgjfhhjhhjhgdjhkjgrdhgdkjfbversuhvtrubtyrbgf¨{config('MAIL_PASSWORD')}")
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}