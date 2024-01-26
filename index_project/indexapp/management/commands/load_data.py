# management/commands/load_index_data.py

import csv
from datetime import datetime
import pandas as pd
import requests
from io import StringIO
from django.core.management.base import BaseCommand
from indexapp.models import Index, DailyPrice
from indexapp.upload_csv_data import csv_data_upload
import os

class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):

        csv_url = os.path.join(os.getcwd(), 'NIFTYDummyData.csv')
        try:
            # Read file and convert it into dict
            with open(csv_url, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
            
                # Call data upload method 
                for row in reader:
                    row = {key.strip(): value for key, value in row.items()}
                    index_name = row['Index']
                    date = datetime.strptime(row['Date'],'%d-%b-%y').date()
                    open_price = row['Open']
                    high_price = row['High']
                    low_price = row['Low']
                    close_price = row['Close']
                    shares_traded = row['Shares Traded']
                    turnover = row['Turnover (₹ Cr)']
                    # import pdb;pdb.set_trace()
                    # Create or get the Index instance
                    index, created = Index.objects.get_or_create(name=index_name)

                    # Create DailyPrice instance
                    DailyPrice.objects.create(
                        index=index,
                        date=date,
                        open_price=open_price,
                        high_price=high_price,
                        low_price=low_price,
                        close_price=close_price,
                        shares_traded=shares_traded,
                        turnover=turnover
                    )

            print('Data Load Sucessfully')
            self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
        except Exception as e:
            print('Error')
            self.stderr.write(self.style.ERROR(f'Error: {e}'))
