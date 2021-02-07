from services.earnings_service import get_earnings_by_date, get_earnings_by_ticker
from linebot.models import FlexSendMessage, TextSendMessage


class EarningsReply:
    def _get_bubble_container(self, earnings):
        green = '#599F59'
        red = '#BD5959'
        black = "#323232"

        color = dict()

        try:
            color['acteps'] = red if float(earnings['actual'][1:]) > float(earnings['actestimate'][1:]) else green
        except:
            color['acteps'] = black

        try:
            color['actrev'] = red if float(earnings['revactual'][1:-1]) > earnings['actrevest'][1:-1] else green
        except:
            color['actrev'] = black

        try:
            color['growtheps'] = red if earnings['revactual'][0] == '-' else green
        except:
            color['growtheps'] = black

        try:
            color['growthrev'] = red if earnings['revgrowthfull'][0] == '-' else green
        except:
            color['growthrev'] = black

        try:
            color['surpeps'] = red if earnings['epssurpfull'][0] == '-' else green
        except:
            color['surpeps'] = black

        try:
            color['surprev'] = red if earnings['revsurpfull'][0] == '-' else green
        except:
            color['surprev'] = black

        return {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"#{earnings['popularity']} {earnings['ticker']}",
                        "size": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": earnings['company']
                    },
                    {
                        "type": "text",
                        "text": earnings['date']
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": " "
                            },
                            {
                                "type": "text",
                                "text": "EPS"
                            },
                            {
                                "type": "text",
                                "text": "REV"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Estimate"
                            },
                            {
                                "type": "text",
                                "text": earnings['actestimate']
                            },
                            {
                                "type": "text",
                                "text": earnings['actrevest']
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Actual"
                            },
                            {
                                "type": "text",
                                "text": earnings['actual'],
                                "color": color['acteps']
                            },
                            {
                                "type": "text",
                                "text": earnings['revactual'],
                                "color": color['actrev']
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Growth"
                            },
                            {
                                "type": "text",
                                "text": earnings['epsgrowthfull'],
                                "color": color['growtheps']
                            },
                            {
                                "type": "text",
                                "text": earnings['revgrowthfull'],
                                "color": color['growthrev']
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Surprise"
                            },
                            {
                                "type": "text",
                                "text": earnings['epssurpfull'],
                                "color": color['surpeps']
                            },
                            {
                                "type": "text",
                                "text": earnings['revsurpfull'],
                                "color": color['surprev']
                            }
                        ]
                    }
                ]
            }
        }

    def _get_carousel_container(self, earnings_list):
        return {
            "type": "carousel",
            "altText": "earnings carousel",
            "contents": [self._get_bubble_container(earnings) for earnings in earnings_list]
        }

    def _get_reply_by_ticker(self, ticker):
        earnings_list = get_earnings_by_ticker(ticker)[:12]
        if earnings_list:
            return FlexSendMessage(
                alt_text='ticker carousel',
                contents=self._get_carousel_container(earnings_list))
        else:
            return TextSendMessage(text='Ticker ' + ticker + ' not found')

    def _get_reply_by_date(self, date):
        earnings_list = get_earnings_by_date(date)[:60]
        earnings_list.sort(key=lambda earnings: earnings['popularity'])
        groups = [earnings_list[i:i+12] for i in range(0, len(earnings_list), 12)]

        if groups:
            return [FlexSendMessage(alt_text='ticker carousel', contents=self._get_carousel_container(group))
                    for group in groups]
        else:
            return TextSendMessage(text='Date ' + date + ' not found')

    def get_reply_message(self, type, ticker='', date=''):
        if type == 'ticker':
            return self._get_reply_by_ticker(ticker)
        else:
            return self._get_reply_by_date(date)
