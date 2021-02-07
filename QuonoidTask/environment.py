
ACCOUNT_TYPES=(
    ("education","education"),
    ("recreational","recreational"),
    ("social","social"),
    ("diy","diy"),
    ("charity","charity"),
    ("cooking","cooking"),
    ("relaxation","relaxation"),
    ("music","music"),
    ("busywork","busywork"),
)
BORED_BASE_URL="http://www.boredapi.com"
TYPE_ENDPOINT="/api/activity?type={}"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'projectsdjango12345@gmail.com'
EMAIL_HOST_PASSWORD = 'django@12345'