"""
Django settings for polaris project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4zheniz16+kp&_vngn)pens@%-((5z!0g=7!9!a=m2c^l+-*f%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.224.10.63','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'rest_framework',
        'Polaris',
	#'glbs',
        'django_apscheduler',
	#'xlk',
#	'django_crontab',
#	'snippets',
	#'backend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'polaris.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'polaris.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST':'127.0.0.1',
        'PORT':'3306',
        'OPTIONS': {'charset':'utf8mb4'},
      #  'ENGINE': 'django.db.backends.sqlite3',
      #  'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
'''
CRONJOBS = [
    ('*/1 * * * *', 'glbs.service.dev_availability.test'),
    ('*/1 * * * *', 'glbs.init.gslb_init.init')
]
'''
GEOIP_PATH = os.path.join(BASE_DIR,"Polaris/Geoip")

LOG_PATH = os.path.join(BASE_DIR, 'log') 
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    # 必须是1
    'version':1,
    # disable_existing_loggers默认是True，如果是True，那么默认配置中的所有logger都将禁用
    'disable_existing_loggers': False,
    # 格式化日志
    'formatters':{
        # 定义simple格式化
        'simple':{
            'format':'[%(levelname)s] [%(asctime)s] [%(module)s] %(created)s %(process)d %(message)s'
        },
        'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] %(filename)s:%(lineno)d %(funcName)s %(message)s'
                     # '%(processName)s:[%(process)d] %(threadName)s:[%(thread)d] %(message)s'
        },
        'standard': {
            'format': '{asctime} [{levelname:6}] {name:30}: {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    # 接收日志信息
    'loggers':{
        # 指定handlers
        'vipdevice_availability_data':{
            'handlers':['vipdevice_availability_data_handler'],
            # 处理级别，表示INFO和INFO以上的级别
            'level': 'INFO',
        },
        'init':{
            'handlers':['init_handler'],
            'level': 'INFO',
        },
        'policy-detect_device_availability':{
            'handlers':['policy-detect_device_availability_handler'],
            'level': 'INFO',
        },
        'policy-node_best_qos':{
            'handlers':['policy-node_best_qos_handler'],
            'level': 'INFO',
        },
        'qdns_zone_config':
        {
            'handlers':['qdns_zone_config_handler'],
            'level': 'INFO',
        },
        'qdns_nameid_cluster':
        {
            'handlers':['qdns_nameid_cluster_handler'],
            'level': 'INFO',
        },
        'qdns_zone_access':
        {
            'handlers':['qdns_zone_access_handler'],
            'level': 'INFO',
        },
        'qdns_nameid_access':
        {
            'handlers':['qdns_nameid_access_handler'],
            'level': 'INFO',
        },
        'adminip_gettask_access':
        {
            'handlers':['adminip_gettask_access_handler'],
            'level': 'INFO',
        },
        'qdns_dnstype_access':
        {
            'handlers':['qdns_dnstype_access_handler'],
            'level': 'INFO',
        },
        
        'default':{
            'handlers':['default_handler'],
            'level': 'INFO',
        },
        
    },
    # 处理日志信息
    'handlers':{
        # 定义handler名字
        'vipdevice_availability_data_handler': {
            # 级别，表示大于DEBUG
            'level': 'DEBUG',
            # 指定文件类型，当日志文件的小大超过了maxBytes以后，就将文件进行切割
            'class': 'logging.handlers.RotatingFileHandler',
            # 存储的地址，在LOG_PATH下创建dj.log文件
            'filename': '%s/vipdevice_availability_data.log' % LOG_PATH,
            # 使用哪一个日志格式化的配置
            'formatter':'verbose',
            # 指定日志文件的大小为5M，换算为1m=1024kb，1kb=1024b
            'maxBytes': 1024 * 1024 * 5,
        },
        'init_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/init.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'policy-detect_device_availability_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/policy-detect_device_availability.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'policy-node_best_qos_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/policy-node_best_qos.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'qdns_zone_config_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/qdns_zone_config.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'qdns_nameid_cluster_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/qdns_nameid_cluster.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'qdns_zone_access_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/qdns_zone_access.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'qdns_nameid_access_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/qdns_nameid_access.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'adminip_gettask_access_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/adminip_gettask_access.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'qdns_dnstype_access_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/qdns_dnstype_access.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        'default_handler':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/default.log' % LOG_PATH,
            'formatter':'verbose',
            'maxBytes': 1024 * 1024 * 5,
        },
        
    },
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
           "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 5,
    },
    "vipdevice": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
           "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
