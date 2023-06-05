from mongoengine.queryset.visitor import Q
from datetime import timedelta
import odm
import main_odm
import logging
logger = logging.getLogger()


class PosTradeInfo():
    def __init__(self, openPosInfo):
        self.openPosInfo = openPosInfo
        self.closePosInfos = []

    def setClosePosInfo(self, closePosInfo):
        if closePosInfo.open_pos_id == self.openPosInfo._id:
            self.closePosInfos.append(closePosInfo)

    def to_dict(self):
        data = self.openPosInfo.to_dict()
        if len(self.closePosInfos):
            data["hasClosed"] = True
            data["closePosInfos"] = [closePosInfo.to_dict() for closePosInfo in
                                     self.closePosInfos]
        else:
            data["hasClosed"] = False
        return data


def fill_l7d_count(tams: list[odm.TradeAlertMessage]) -> list:
    for message in tams:
        number = odm.TradeAlertMessage.objects(
            Q(symbol=message.symbol) & Q(custom_symbol=message.custom_symbol)
            & Q(datetime__gte=message.datetime - timedelta(days=7))).count()
        message.count = number
    return sorted(tams, key=lambda x: x.count)


def get_bottom_trading_future() -> list:
    return odm.TradeInfo.objects(is_trading=True)


def get_bottom_config() -> list:
    return odm.FutureConfigInfo.objects().order_by('-is_active', 'zl_symbol')


def get_main_trading_future() -> list:
    return main_odm.TradeInfo.objects(is_trading=True)


def change_bottom_config(id, is_active):
    return odm.FutureConfigInfo.objects(_id=id).update_one(
        set__is_active=is_active)


def get_main_all_OpenPosInfo() -> list:
    return main_odm.OpenPosInfo.objects()


def get_main_all_ClosePosInfo() -> list:
    return main_odm.ClosePosInfo.objects()


def get_all_PosTradeInfo() -> list:
    pos_trade_infos = [PosTradeInfo(openPosInfo) for openPosInfo in
                       get_main_all_OpenPosInfo()]
    [posTradeInfo.setClosePosInfo(closePosInfo) for closePosInfo in
     get_main_all_ClosePosInfo() for posTradeInfo in pos_trade_infos]
    return pos_trade_infos
