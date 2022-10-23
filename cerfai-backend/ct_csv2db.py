from cmath import nan
from utils.dbManager import DatabaseManager
import pandas
import config
import math


db = DatabaseManager(config=config.database_settings)

if __name__ == '__main__':
    df = pandas.read_csv('./分级目录10.18.csv', encoding='gb2312')
    # print(df)
    for i, row in df.iterrows():

        if not math.isnan(row['一级分类ID']):
            rid = int(row['一级分类ID'])
            rname = row['一级分类名']
            db.execute(f'''
                INSERT INTO `novelai`.`categories` (`id`, `name`, `level`, `p_id`)\
                VALUES ({rid}, '{rname}', {1}, NULL) as t
                ON DUPLICATE KEY UPDATE id = t.id, name = t.name, level = t.level, p_id = t.p_id;
            ''')
            print(f"插入 一级分类: {row['一级分类名']} 成功")

        if not math.isnan(row['二级分类ID']):
            rid = int(row['二级分类ID'])
            rname = row['二级分类名']
            db.execute(f'''
                INSERT INTO `novelai`.`categories` (`id`, `name`, `level`, `p_id`)\
                VALUES ({rid}, '{rname}', {2}, {(rid // 100) * 100}) as t
                ON DUPLICATE KEY UPDATE id = t.id, name = t.name, level = t.level, p_id = t.p_id;
            ''')
            print(f"插入 二级分类: {row['二级分类名']} 成功")

    print('分类入库完成')