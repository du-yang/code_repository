# coding=utf8
from __future__ import print_function, division, absolute_import


class Config:
    pass

class DevelopmentConfig(Config):
    basedir = u'E:\近义词发现\synonym1.0'
    model_basedir = u'{}/data'.format(basedir)
    data_basedir = u'{}/data'.format(basedir)

    # mysql_host = "172.16.36.30"
    # mysql_port = 3306
    # mysql_user = 'app'
    # mysql_pass = 'App1234.'
    # charset = 'utf8'
    # mysql_db = 'ems_irs_dev'

    log_conf = {
        'path': u'{}/logs/etl_runtime.log'.format(basedir),
        'when': 'd',
        'interval': 1,
        'backupCount': 14,
    }

    mongo_db = 'financeDB'
    mongo_port = 27017
    mongo_host = 'localhost'
    MONGO_DATABASE_URI = 'mongodb://{host}/{db}'.format(host=mongo_host, db=mongo_db)


class TestingConfig(Config):
    basedir = u'E:\近义词发现\synonym1.0'
    model_basedir = u'{}/data'.format(basedir)
    data_basedir = u'{}/data'.format(basedir)

    # mysql_host = "172.16.36.30"
    # mysql_port = 3306
    # mysql_user = 'app'
    # mysql_pass = 'App1234.'
    # charset = 'utf8'
    # mysql_db = 'ems_irs_dev'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}?charset={charset}'.format(
    #     mysql_user=mysql_user, mysql_pass=mysql_pass, mysql_host=mysql_host, mysql_port=mysql_port, mysql_db=mysql_db, charset=charset)

    log_conf = {
        'path': u'{}/logs/etl_runtime.log'.format(basedir),
        'when': 'd',
        'interval': 1,
        'backupCount': 14,
    }

    mongo_db = 'financeDB_test'
    mongo_port = 27017
    mongo_host = 'localhost'
    MONGO_DATABASE_URI = 'mongodb://{host}/{db}'.format(host=mongo_host, db=mongo_db)


class ProductionConfig(Config):
    basedir = u'E:\近义词发现\synonym1.0'
    model_basedir = u'{}/data'.format(basedir)
    data_basedir = u'{}/data'.format(basedir)

    # mysql_host = "172.16.36.30"
    # mysql_port = 3306
    # mysql_user = 'app'
    # mysql_pass = 'App1234.'
    # charset = 'utf8'
    # mysql_db = 'ems_irs_dev'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}?charset={charset}'.format(
    #     mysql_user=mysql_user, mysql_pass=mysql_pass, mysql_host=mysql_host, mysql_port=mysql_port, mysql_db=mysql_db, charset=charset)

    log_conf = {
        'path': u'{}/logs/etl_runtime.log'.format(basedir),
        'when': 'd',
        'interval': 1,
        'backupCount': 14,
    }

    mongo_db = 'financeDB'
    mongo_port = 27017
    mongo_host = 'localhost'
    MONGO_DATABASE_URI = 'mongodb://{host}/{db}'.format(host=mongo_host, db=mongo_db)


config = {
    "development": DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
