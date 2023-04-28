"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/

python中操作git：
ctrl + k 来进行git的git add . 和commit 的操作
ctrl +shift + k 来进行git push 操作
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vy0y*^a&z)vsjgl7fi2v4#y$ly^j&k)x0k+_fv3!fb=^29v562'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['192.168.0.105']
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',  # 将创建的app放在同一个文件夹下，需要更改apps.py的name属性
    'apps.verifications',
    'apps.oauth',

    'corsheaders',  # CORS跨域设置

    'apps.areas',
    'apps.goods',
    'apps.contents',

    'haystack',  # 注册haystack全文搜索配置
    'django_crontab',

    'apps.carts'

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS的配置放在最上面
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

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

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
        'NAME': 'meiduo_mall'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# redis的配置
# session保存在redis的1号库中
CACHES = {
    "default": {  # redis数据库的0号库作为预留，cache配置的缓存
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session信息保存到redis数据库的1号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "code": {  # 图片验证码信息保存到redis数据库的2号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "history": {  # 用户浏览记录保存到redis数据库的3号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "carts": {  # 用户购物车保存到redis数据库的4号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# session信息保存到redis数据库的1号库
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,  # 单个日志的大小
            'backupCount': 10,  # 备份日志的数量
            'encoding': 'utf8',
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
'''
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
            # 'style': '{',
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
            # 'style': '{',
        },
    },
    'filters': {  # 对日志进行过滤
        # 'special': {
        #     '()': 'project.logging.SpecialFilter',
        # 'foo': 'bar',
        # },
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['special']
        # }
    },
    'loggers': {  # 日志器
        'django': {  # 定义一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        # 'myproject.custom': {
        #     'handlers': ['console', 'mail_admins'],
        #     'level': 'INFO',
        #     'filters': ['special']
        # }
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),
        },
    },
    'loggers': {
        'django': {     
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
'''
# 替换django自带的User模型
AUTH_USER_MODEL = 'users.User'
# CORS 白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://192.168.0.105:8000',
    'http://127.0.0.1:8080'
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# QQ登录参数
# 我们申请的 客户端id
QQ_CLIENT_ID = '101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
# 我们申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

# 添加163邮箱发送配置
#  让django的哪个类来发送邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 邮件服务器的主机和端口号
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25

# 使用我的 163服务器 和 授权码

# 发送邮件的邮箱
EMAIL_HOST_USER = 'fyq31780209@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'WBGDQNICFJVQSEWZ'

# 发送邮件的邮箱
# EMAIL_HOST_USER = 'qi_rui_hua@163.com'
# 在邮箱中设置的客户端授权密码
# EMAIL_HOST_PASSWORD = '123456abc'

EMAIL_FROM = 'fyq_love_xgm.com'

# ES的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.3.150:9200/',  # 本机ip，端口号默认9200
        'INDEX_NAME': 'haystack',  # 索引名字
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5  # 设置搜索每页显示的数量

"""
定时任务（windows系统运行会出问题）
CRONJOBS = [('*/1 * * * * ', 'apps.contents.crons.generic_meiduo_index', '>>' + os.path(BASE_DIR, 'logs/crontab.log'))]
            M分 H时 D日 m月 d周         定时任务（函数）                                             日志
查看已有定时任务：python manage.py crontab show
添加定时任务：python manage.py crontab add
删除定时任务：python manage.py crontab remove
"""
CRONJOBS = [
    ('*/1 * * * * ', 'apps.contents.crons.generic_meiduo_index', '>>' + os.path.join(BASE_DIR, 'logs/crontab.log'))
]
