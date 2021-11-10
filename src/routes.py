import json
from datetime import datetime

from flask_restful import Resource, reqparse
from sqlalchemy import desc

from src import api, db
from src.models import Company, FinanceData
from src.scrapper import csv_parser, my_headers, page_parser

parser = reqparse.RequestParser()
parser.add_argument('data_source')  # source of data (csv or html page)
parser.add_argument('company')  # name of companies


class YahooData(Resource):

    def get(self):
        """
        file: swagger/yahoodata.yaml
        """
        args = parser.parse_args(strict=True)
        company = args['company']
        data_source = args['data_source']
        work_dict = None
        if data_source not in ('csv', 'page'):
            return {'message': 'set argument data_source (csv, page)'}, 400
        elif data_source == 'csv':
            work_dict = csv_parser(company, my_headers)
        else:
            work_dict = page_parser(company, my_headers)
        if work_dict == 'bad request':
            return {'message': f'bad company argument {company}'}, 400
        company_query = Company.query.filter_by(name=company).first()
        if company_query is None:
            db.session.add(Company(name=company))
            db.session.commit()
            company_query = Company.query.filter_by(name=company).first()
        max_data = FinanceData.query.filter_by(
            company_id=company_query.id
            ).order_by(desc('date')).first()
        for key, value in work_dict.items():
            if max_data is None or key > max_data.date:
                data = FinanceData(
                    date=key,
                    open_data=value['open'],
                    high_data=value['high'],
                    low_data=value['low'],
                    close_data=value['close'],
                    adj_close_data=value['adjclose'],
                    volume_data=value['volume'],
                    company=company_query
                    )
                db.session.add(data)
            db.session.commit()
        raw_data = FinanceData.query.all()
        rez_dict = {
            datetime.utcfromtimestamp(item.date).date().isoformat(): {
                "low": item.low_data,
                "close": item.close_data,
                "volume": item.volume_data,
                "high": item.high_data,
                "open": item.open_data,
                "adjclose": item.adj_close_data
                }
            for item in raw_data
            }
        return json.dumps(rez_dict, sort_keys=True, indent=4)


api.add_resource(YahooData, '/', strict_slashes=False)
