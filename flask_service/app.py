from flask import Flask, render_template, request
from markupsafe import escape
from flask_mongoengine import MongoEngine
from datetime import datetime
import odm
import dao
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db = MongoEngine()
app = Flask(__name__)
odm.logger = app.logger
host_name = os.environ.get('HOST_NAME', 'localhost')
bottom_db_host = os.environ.get('BOTTOM_DB', 'mongo_bottom')
main_db_host = os.environ.get('MAIN_DB', 'mongo_main')
bottom_db_port = int(os.environ.get('BOTTOM_DB_PORT', 27017))
main_db_port = int(os.environ.get('MAIN_DB_PORT', 27017))
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "bottom_future_trade",
        "host": bottom_db_host,
        "port": bottom_db_port,
        "username": "root",
        "password": "example",
        "alias": "default",
    },
    {
        "db": "future_trade",
        "host": main_db_host,
        "port": main_db_port,
        "username": "root",
        "password": "example",
        "alias": "main",
    }
]
app.config['JSON_AS_ASCII'] = False
db.init_app(app)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route("/")
def index():
    now = datetime.today().strftime('%Y-%m-%d')
    title = f'摸底开仓提示:{now}'
    return render_template('ajax_table.html', title=title, api_url='/api/tams')


@app.route("/history")
def history():
    return render_template('ajax_table.html', title='全部开仓提示记录',
                           api_url='/api/all')


@app.route("/trading")
def trading_futures():
    return render_template(
        'ops_table.html', title='成交记录',
        bottom_api_url='/api/btf',
        main_api_url='/api/mtf')


@app.route("/config")
def future_config():
    return render_template(
        'config_table.html', title='期货配置',
        bottom_api_url='/api/config',
        main_api_url='/api/config')


@app.route("/api/bottom/all_tips")
def get_all_tams():
    tams = dao.fill_l7d_count(odm.TradeAlertMessage.objects)
    return {'data': [message.to_dict() for message in tams]}


@app.route("/api/bottom/current_tips")
def get_tams():
    tams = odm.TradeAlertMessage.get_recent_message()
    tams = dao.fill_l7d_count(tams)
    app.logger.info("test")
    return {'data': [message.to_dict() for message in tams]}


@app.route("/api/bottom/trading")
def get_bottom_open_futures():
    return {'data': [message.to_dict() for message in
                     dao.get_bottom_trading_future()]}


@app.route("/api/main/trading")
def get_main_open_futures():
    return {'data': [message.to_dict() for message in
                     dao.get_main_trading_future()]}


@app.route("/api/main/allpostradeinfo")
def get_main_all_posTradeInfo():
    return {'data': [posTradeInfo.to_dict() for posTradeInfo in
                     dao.get_all_PosTradeInfo()]}


@app.route("/api/main/allopenposinfo")
def get_main_all_openposInfo():
    return {'data': [openPosInfo.to_dict() for openPosInfo in
                     dao.get_main_all_OpenPosInfo()]}


@app.route("/api/main/allclosedposinfo")
def get_main_all_closedposInfo():
    return {'data': [openPosInfo.to_dict() for openPosInfo in
                     filter(lambda x:len(x.closePosInfos) > 0,
                            dao.get_all_PosTradeInfo())]}


@app.route("/api/bottom/config")
def get_bottom_config():
    app.logger.info('this is a test message')
    return {'data': [message.to_dict() for message in
                     dao.get_bottom_config()]}


@app.post("/api/bottom/<id>")
def change_bottom_config(id):
    app.logger.info('this is a test message')
    content = request.get_json(force=True)['data']
    print(f"json request: {content}")
    is_active = True
    if not content['is_active']:
        is_active = False
    result = {}
    if dao.change_bottom_config(id, is_active):
        result["success"] = True
    return result


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5005))
    app.run(debug=True, host='0.0.0.0', port=port)
