from indexapp.models import Index, DailyPrice
from datetime import datetime
from io import StringIO
def csv_data_upload(reader):
    try:
        # Process and import data into models
        for row in reader:
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
        return True
    except:
        return False