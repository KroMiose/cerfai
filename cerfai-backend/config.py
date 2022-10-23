# 服务运行地址
server_host = '127.0.0.1'
server_port = 3090

# 是否处于debug模式
debug = True

# 数据库连接配置
database_settings = {
    'mysql_host': 'localhost',
    'mysql_port': '3306',
    'mysql_user': 'root',
    'mysql_passwd': '',
    'mysql_db': 'novelai',
    'enable_debug': False,
}

# 贡献榜更新间隔时间
contributor_update_delay = 60 * 60

# 管理访问密钥 * 这个是管理页面访问的凭证
access_key = '9a58459a6ec807b112933c8c676e295e'

# 每次返回的数据条数最大限制
max_ret_data_limit = 100