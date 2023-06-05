import mongoengine as me
import re
import logging

logger = logging.getLogger()


class FutureBase():
    def to_dict(self):
        pass

    def getSLString(self):
        if self.isLong():
            return 'L'
        else:
            return 'S'

    def isLong(self):
        pattern_dict = {
            0: re.compile(r'^(\w*)(short)$'),
            1: re.compile(r'^(\w*)(long)$'),
        }
        for r, ipattern in pattern_dict.items():
            matchsymbol = ipattern.match(self.custom_symbol)
            if matchsymbol:
                return r


class CommonCondition(me.EmbeddedDocument):
    ema5 = me.FloatField()
    ema20 = me.FloatField()
    ema60 = me.FloatField()
    macd = me.FloatField()
    close = me.FloatField()
    condition_time = me.DateTimeField()


class TradeAlertMessage(me.Document, FutureBase):
    meta = {'collection': 'bottom_condition_infos'}
    custom_symbol = me.StringField()
    symbol = me.StringField()
    pos = me.IntField()
    open_pos_scale = me.FloatField()
    contract_m = me.IntField()
    last_price = me.FloatField()
    datetime = me.DateTimeField()
    balance = me.FloatField()
    day_condition = me.EmbeddedDocumentField(CommonCondition)
    hours_condition = me.EmbeddedDocumentField(CommonCondition)
    minutes_condition = me.EmbeddedDocumentField(CommonCondition)

    @me.queryset_manager
    def objects(doc_cls, queryset):
        return queryset.order_by('-datetime')

    @me.queryset_manager
    def get_recent_message(doc_cls, queryset):
        result = queryset.order_by('-datetime')
        last_date = result.first().datetime
        return result.filter(datetime=last_date)

    def to_dict(self):
        data = {
            'custom_symbol': self.getSLString(),
            'symbol': self.symbol,
            'datetime': self.datetime.strftime("%Y-%m-%d"),
            'last_price': self.last_price,
            'pos': self.pos,
            'balance': self.balance,
            'open_pos_scale': self.open_pos_scale,
            'contract_m': self.contract_m,
            'count': self.count if self.count else 0
        }

        return data


class OpenPosInfo(me.Document):
    meta = {'collection': 'open_pos_infos', 'strict': False}
    symbol = me.StringField()
    is_long = me.BooleanField(db_field="l_or_s")
    pos = me.IntField(db_field="trade_number")
    trade_price = me.FloatField()
    current_balance = me.FloatField()
    stop_loss_price = me.FloatField()
    stop_profit_point = me.FloatField()
    trade_date = me.DateTimeField()
    commission = me.FloatField()


class TradeData(me.EmbeddedDocument):
    meta = {'strict': False}
    open_pos_id = me.ReferenceField(OpenPosInfo)
    price = me.FloatField()
    pos = me.IntField()

    def to_dict(self):
        return {
            'data': self.open_pos_id
        }


class TradeInfo(me.Document, FutureBase):
    meta = {'collection': 'trade_status_infos', 'strict': False}
    custom_symbol = me.StringField()
    symbol = me.StringField(db_field="current_symbol")
    next_symbol = me.StringField()
    is_trading = me.BooleanField()
    trade_data = me.EmbeddedDocumentField(TradeData)

    def to_dict(self):
        data = {
            'custom_symbol': self.getSLString(),
            'symbol': self.symbol,
            'next_symbol': self.next_symbol,
            'is_trading': self.is_trading,
            'trade_data': {
                'pos': self.trade_data.open_pos_id.pos,
                'price': self.trade_data.open_pos_id.trade_price,
                'commission': self.trade_data.open_pos_id.commission,
                'slp': self.trade_data.open_pos_id.stop_loss_price,
                'spp': self.trade_data.open_pos_id.stop_profit_point,
                'datetime': self.trade_data.open_pos_id.trade_date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        }
        return data


class FutureConfigInfo(me.Document):
    meta = {'collection': 'future_config_infos', 'strict': False}
    _id = me.ObjectIdField()
    zl_symbol = me.StringField(db_field='symbol')
    contract_m = me.IntField()
    is_active = me.BooleanField()
    name = me.StringField()
    open_pos_scale = me.FloatField()

    def to_dict(self):
        data = {
            'id': str(self._id),
            'symbol': self.zl_symbol,
            'name': self.name,
            'is_active': self.is_active,
            'open_pos_scale': self.open_pos_scale,
            'contract_m': self.contract_m,
        }
        logger.info(data)
        return data
