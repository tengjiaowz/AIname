from datetime import timedelta
# 你的 MySQL 连接串（把密码换成自己的）
DB_URI = "mysql+aiomysql://root:YOUR_DB_PASSWORD@127.0.0.1:3306/ainame?charset=utf8mb4"


# JWT 加密密钥（自行改为足够随机的字符串）
JWT_SECRET_KEY = "YOUR_JWT_SECRET_KEY"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# 邮箱相关配置（换成你自己的 SMTP 账号和授权码）
MAIL_USERNAME="YOUR_EMAIL@qq.com"
MAIL_PASSWORD="YOUR_SMTP_AUTH_CODE"
MAIL_FROM="YOUR_EMAIL@qq.com"
MAIL_PORT=587
MAIL_SERVER="smtp.qq.com"
MAIL_FROM_NAME="AI取名助手"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False