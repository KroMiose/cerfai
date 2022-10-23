from multiprocessing import AuthenticationError
from utils.dbManager import DatabaseManager
from utils.md5 import hex_md5
import random
import time
import json
import config


class dataOpt:
    contrubutor_top = {
        'data': {},
        'update_time': 0,
    }

    def __init__(self):
        self.db = DatabaseManager(config=config.database_settings)
        self.load_rundata()
    
    # 载入运行数据
    def load_rundata(self):
        self.tag_cnt = self.db.select(f'''SELECT count(*) FROM ct_tags WHERE is_locked IS NULL OR is_locked = 0;''')[0]['count(*)']
        self.categories_data = self.db.select(f'''SELECT `id`, `name`, `desc` FROM categories WHERE level = 2 AND name != 'UN';''')
        self.full_categories_data = self.db.select(f'''SELECT `id`, `name`, `level`, `desc` FROM categories;''')
        # 读取上次运行数据
        with open('./runData.json', 'r') as f:
            self.runData = json.loads(f.read())
            f.close()
        self.write_run_data('tag_cnt', self.tag_cnt)
        return True

    # 写入运行数据
    def write_run_data(self, key, value):
        self.runData[key] = value
        with open('./runData.json', 'w') as f:
            f.write(json.dumps(self.runData))
            f.close()

    # 获取运行数据
    def get_run_data(self):
        return self.runData

    """ ================================ 贡献站基础接口 ================================ """
    # 获取分类列表
    def get_categories(self):
        return self.categories_data

    # 获取随机词条
    def get_random_tag(self):
        if time.time() - self.contrubutor_top['update_time'] > config.contributor_update_delay:
            self.tag_cnt = self.db.select(f'''SELECT count(*) FROM ct_tags WHERE is_locked IS NULL OR is_locked = 0;''')[0]['count(*)']
        rint = random.randint(0, self.tag_cnt - 1)
        # print('rint =', rint)
        res = self.db.select(f'''SELECT * FROM ct_tags WHERE is_locked IS NULL OR is_locked = 0 ORDER BY id LIMIT {rint}, 1''')
        # res = self.db.select(f'''SELECT * FROM ct_tags WHERE id = 99999''') # 测试用，固定返回测试词条
        return res[0]

    # 更新词条
    def update_taginfo(self, data):
        try:
            tid = int(data['id'])
            odata = self.db.select(f'''SELECT * FROM ct_tags WHERE id = {tid}''')[0]
            up_times = 0 if not odata['update_times'] else odata['update_times']
            odata['contributor'] = '' if not odata['contributor'] else odata['contributor']

            t_name = data['t_name'].replace('\'', '\\\'').replace('（', '(').replace('）', ')').replace('【', '[').replace('】', ']')
            c_id = int(data['c_id'])

            if data['desc']:
                desc = data['desc'].replace('\'', '\\\'')
            else:
                desc = ''

            if data['remarks']:
                remarks = data['remarks'].replace('\'', '\\\'')
            else:
                remarks = ''

            if data['contributor']:
                contributor = data['contributor'].replace('\'', '\\\'')
                if len(contributor) and contributor[-1] != ',':
                    contributor = contributor + ','
            else:
                contributor = ''

            odata['contributor'] = ('' if 'contributor' not in odata else odata['contributor'])
            if contributor not in odata['contributor']:
                contributor = odata['contributor'] + contributor + ','
            else:
                contributor = odata['contributor']
            if contributor[-1] != ',':
                contributor = contributor + ','

            contributor = contributor.replace(',,', ',')

            is_nsfw = 1 if data['is_nsfw'] else 0
            # if self.check_text(t_name) and self.check_text(desc) and self.check_text(remarks) and self.check_text(contributor):
            sql = f'''
            UPDATE `novelai`.`ct_tags` \
            SET `t_name` = '{t_name}', `is_nsfw` = {is_nsfw}, `desc` = '{desc}', `remarks` = '{remarks}', `contributor` = '{contributor}', `c_id` = {c_id}, `update_times` = {up_times + 1}, `update_time` = NOW() WHERE `id` = {tid};
            '''
            # print('sql:', sql.replace('  ', ''))
            self.db.execute(sql)
            self.write_run_data('upload_cnt', self.runData['upload_cnt'] + 1)   # 更新上传计数
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 收到来自用户: {data['contributor']} 对词条 {odata['name']}: {t_name} 的更新，当前累计更新词条次数: {self.runData['upload_cnt'] + 1}")
            return True
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自词条更新操作，携带数据: {data}")
            return False

    # 搜索词条
    def search_tags(self, data):
        try:
            keyword = data['keyword'].replace('\'', '\\\'')
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 接收到检索请求: {keyword}")
            if keyword:
                res = self.db.select(f'''SELECT * FROM ct_tags WHERE `name` LIKE '%{keyword}%' OR `t_name` LIKE '%{keyword}%' LIMIT {config.max_ret_data_limit};''')
                return res
            return []
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自词条搜索操作，携带数据: {data}")
            return False

    # 根据id获取分类名
    def get_category_name(self, id):
        for c in self.categories_data:
            if c['id'] == id:
                return c['name']
        return None

    # 获取贡献榜
    def get_contributor(self):
        if time.time() - self.contrubutor_top['update_time'] > config.contributor_update_delay:
            data = self.db.select(f'''SELECT contributor FROM ct_tags WHERE contributor IS NOT NULL;''')
            self.contrubutor_top['data'] = {}
            for r in data:  # 遍历词条行
                for c in r['contributor'].split(','):  # 遍历贡献者
                    if c:
                        if c in self.contrubutor_top['data']:
                            self.contrubutor_top['data'][c] += 1
                        else:
                            self.contrubutor_top['data'][c] = 1
            self.contrubutor_top['update_time'] = time.time()
            return self.contrubutor_top['data']
        else:
            return self.contrubutor_top['data']

    """ ================================ 管理接口 ================================ """
    # 请求重载运行数据
    def reload_rundata(self, data):
        try:
            if self.check_access_key(data['token']):
                self.load_rundata()
                return True
            return False
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自管理重载运行信息接口，携带数据: {data}")
            return False

    # 获取筛选词条内容
    def filter_tags(self, data):
        try:
            if self.check_access_key(data['token']):

                page = data['page'] - 1

                if data['limit'] <= config.max_ret_data_limit:
                    limit = data['limit']
                else:
                    raise ValueError

                # print(data)
                if 'order' in data and data['order']:
                    if data['order'][0] == '-':
                        order_sql = f"ORDER BY `{data['order'][1:]}` DESC"
                    else:
                        order_sql = f"ORDER BY `{data['order']}`"
                else:
                    order_sql = ''

                if data['keyword']:
                    sql_c = f'''SELECT count(*) FROM ct_tags WHERE `name` LIKE '%{data['keyword']}%' OR `t_name` LIKE '%{data['keyword']}%' OR `desc` LIKE '%{data['keyword']}%' OR `remarks` LIKE '%{data['keyword']}%' OR `contributor` LIKE '%{data['keyword']}%' {order_sql};'''
                    sql = f'''SELECT * FROM ct_tags WHERE `name` LIKE '%{data['keyword']}%' OR `t_name` LIKE '%{data['keyword']}%' OR `desc` LIKE '%{data['keyword']}%' OR `remarks` LIKE '%{data['keyword']}%' OR `contributor` LIKE '%{data['keyword']}%' {order_sql} LIMIT {page*limit}, {limit};'''
                else:
                    sql_c = f'''SELECT count(*) FROM ct_tags {order_sql};'''
                    sql = f'''SELECT * FROM ct_tags {order_sql} LIMIT {page*limit}, {limit};'''

                return self.db.select(sql), self.db.select(sql_c)[0]['count(*)']
            else:
                raise ValueError
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自管理筛选词条接口，携带数据: {data}")
            return False, False

    # 管理端编辑词条
    def edit_tag(self, data):
        try:
            if self.check_access_key(data['token']):
                tid = int(data['id'])
                odata = self.db.select(f'''SELECT * FROM ct_tags WHERE id = {tid}''')[0]
                up_times = 0 if not odata['update_times'] else odata['update_times']
                odata['contributor'] = '' if not odata['contributor'] else odata['contributor']
                # print(odata)

                t_name = data['t_name'].replace('\'', '\\\'').replace('（', '(').replace('）', ')').replace('【', '[').replace('】', ']')
                c_id = int(data['c_id'])

                if data['desc']:
                    desc = data['desc'].replace('\'', '\\\'')
                else:
                    desc = ''

                if data['remarks']:
                    remarks = data['remarks'].replace('\'', '\\\'')
                else:
                    remarks = ''

                if data['contributor']:
                    contributor = data['contributor'].replace('\'', '\\\'')
                    if len(contributor) and contributor[-1] != ',':
                        contributor = contributor + ','
                else:
                    contributor = ''

                is_nsfw = 1 if data['is_nsfw'] else 0
                is_locked = 1 if data['is_locked'] else 0

                sql = f'''
                UPDATE `novelai`.`ct_tags` \
                SET `t_name` = '{t_name}', `is_nsfw` = {is_nsfw}, `desc` = '{desc}', `remarks` = '{remarks}', `contributor` = '{contributor}', `is_locked` = {is_locked}, `c_id` = {c_id}, `update_times` = {up_times + 1}, `update_time` = NOW() WHERE `id` = {tid};
                '''
                # print('sql:', sql.replace('  ', ''))
                self.db.execute(sql)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 管理端更新 词条 {odata['name']}: {t_name}")
                return True
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自管理编辑接口，携带数据: {data}")
            return False


    """ ================================ 开放平台接口 ================================ """
    # 获取总分类列表
    def get_full_categories(self):
        return self.full_categories_data

    # 获取分类词条
    def get_tags_by_category(self, data):
        try:
            if self.check_credentials(data['token']):
                page = int(data['page']) - 1

                if data['limit'] <= config.max_ret_data_limit:
                    limit = int(data['limit'])
                else:
                    raise ValueError

                c_id = int(data['category_id'])
                sql_c = f'''SELECT count(*) FROM ct_tags WHERE `c_id` = {c_id};'''
                sql = f'''SELECT `id`, `name`, `t_name`, `is_nsfw`, `desc`, `remarks`, `c_id` FROM ct_tags WHERE `c_id` = {c_id} LIMIT {page*limit}, {limit};'''

                return self.db.select(sql), self.db.select(sql_c)[0]['count(*)']
            else:
                raise ValueError
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e} 来自开放接口，携带数据: {data}")
            return False, False


    """ ================================ 工具方法 ================================ """
    # 校验开放接口访问权限
    def check_credentials(self, token):
        token = token.replace('\'', '\\\'')
        res = self.db.select(f'''SELECT * FROM credentials WHERE token = '{token}';''')
        return True if (len(res) and (res[0]['is_active'] == 1)) else False

    # 检查管理终端访问权限
    @staticmethod
    def check_access_key(key):
        if key == config.access_key:
            return True
        return False

    # 检测输入字符串是否合法
    @staticmethod
    def check_text(text):
        print('checking:', text)
        specialKey = "[`^*()=|{}':;'\\[\\]<>/！￥……&*（）——|{}【】‘；：”“'。，、？]‘'"
        for k in specialKey:
            if text.find(k) != -1:
                return False
        return True


if __name__ == '__main__':
    do = dataOpt()
    print(do.get_random_tag())
