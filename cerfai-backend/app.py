from flask import Flask, redirect, request, session
from flask_cors import CORS
import os
import json
import time
import config
from dataOpts import dataOpt

# from geventwebsocket.handler import WebSocketHandler
# from geventwebsocket.server import WSGIServer

app = Flask(__name__)
CORS(app, supports_credentials=True)

do = dataOpt()

# 测试服务器连通性接口
@app.route('/ping', methods=['GET', 'POST'])
def ping():
    time.sleep(1)
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ping from {request.remote_addr} with data: {reqData}")
    return {'code': 200, 'msg': 'welcome to Miose_Draw_Guess', 'data': reqData}

# 获取类别列表
@app.route('/get_categories', methods=['GET', 'POST'])
def get_categories():
    up_cnt = do.get_run_data()['upload_cnt']
    ct_total = do.get_run_data()['tag_cnt']
    return {'code': 200, 'msg': '获取分类成功', 'data': do.get_categories(), 'up_cnt': up_cnt, 'ct_total': ct_total, 'contributor': do.get_contributor()}

# 获取随机词条
@app.route('/get_random_tag', methods=['GET', 'POST'])
def get_random_tag():
    return {'code': 200, 'msg': '获取随机词条信息成功', 'data': do.get_random_tag()}

# 更新词条内容
@app.route('/update_taginfo', methods=['POST'])
def update_taginfo():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    if do.update_taginfo(reqData):
        return {'code': 200, 'msg': '更新成功，感谢您的贡献！'}
    return {'code': 401, 'msg': '上传失败，请检查输入内容是否合法'}

# 搜索词条
@app.route('/search_tags', methods=['GET', 'POST'])
def search_tags():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    data = do.search_tags(reqData)
    if data != False:
        return {'code': 200, 'data': data}
    return {'code': 401, 'msg': '参数错误'}

# 获取贡献榜
@app.route('/get_contributor', methods=['GET', 'POST'])
def get_contributor():
    return {'code': 200, 'data': do.get_contributor()}


""" ================================ 管理接口 ================================ """
# 验证授权码
@app.route('/admin/check_access', methods=['POST'])
def check_access():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    try:
        if reqData['token'] == config.access_key:
            return {'code': 200, 'msg': '授权校验成功'}
        return {'code': 401, 'msg': '授权校验失败'}
    except Exception as e:
        return {'code': 401, 'msg': '授权校验失败'}

# 请求重载运行数据接口
@app.route('/admin/reload_rundata', methods=['POST'])
def reload_rundata():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    if do.reload_rundata(reqData):
        return {'code': 200, 'msg': '数据重载成功'}
    else:
        return {'code': 401, 'msg': '重载失败'}

# 获取筛选词条内容
@app.route('/admin/filter_tags', methods=['POST'])
def filter_tags():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    data, cnt = do.filter_tags(reqData)
    if data != False:
        return {'code': 200, 'data': data, 'total': cnt}
    return {'code': 401, 'msg': '参数错误'}

# 编辑词条信息
@app.route('/admin/edit_tag', methods=['POST'])
def edit_tag():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    data = do.edit_tag(reqData)
    if data != False:
        return {'code': 200, 'data': data, 'msg': '更新成功'}
    return {'code': 401, 'msg': '参数错误'}


""" ================================ 开放平台接口 ================================ """
# 获取完整分类表
@app.route('/open/get_full_categories', methods=['GET', 'POST'])
def open_get_full_categories():
    return {'code': 200, 'msg': '获取完整分类成功', 'data': do.get_full_categories()}

# 获取分类词条内容
@app.route('/open/get_tags_by_category', methods=['POST'])
def open_get_tags_by_category():
    try:
        reqData = json.loads(request.data.decode('UTF-8'))
    except json.decoder.JSONDecodeError:
        reqData = request.form
    data, cnt = do.get_tags_by_category(reqData)
    if data != False:
        return {'code': 200, 'data': data, 'total': cnt}
    return {'code': 401, 'msg': '参数错误或请求未被授权'}


if __name__ == '__main__':
    os.system('cls')
    app.config['SECRET_KEY'] = os.urandom(32)
    app.run(debug=config.debug, threaded=True, host='0.0.0.0', port=config.server_port)

    # http_server = WSGIServer(('0.0.0.0', config.server_port), application=app, handler_class=WebSocketHandler)
    # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 主服务器在 {config.server_host}:{config.server_port} 上运行中...")
    # http_server.serve_forever()