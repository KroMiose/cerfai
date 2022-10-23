from cmath import nan
from utils.dbManager import DatabaseManager
import config


db = DatabaseManager(config=config.database_settings)

if __name__ == '__main__':
    tdata = db.select("SELECT * FROM tags2 ORDER BY tag;")
    
    # {'id': 40207, 'tag': '!', 'tagName': '!'}
    cnt = 0
    skip = True
    for row in tdata:
        skip = not skip
        if skip:
            continue
        print('正在插入:', row)
        tag = row['tag'].replace('\'', '\\\'')
        if db.execute(f'''
            INSERT INTO `novelai`.`ct_tags` (`id`, `name`, `t_name`, `is_nsfw`, `c_id`)\
            VALUES ({cnt}, '{tag}', '{row['tagName']}', 0, 3101) as t
            ON DUPLICATE KEY UPDATE id = t.id, name = t.name, t_name = t.t_name, is_nsfw = t.is_nsfw, c_id = t.c_id;'''):

            cnt += 1
            print('已插入第', cnt, '个词条')

    print('词条导入完毕')