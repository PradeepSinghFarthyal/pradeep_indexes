from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import IndexSerializer, DailyPriceSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
items_per_page = 25


class IndexListView(generics.ListAPIView):
    queryset = Index.objects.all()[:5]
    serializer_class = IndexSerializer



class DailyPriceListView(APIView):
    def get(self, request, index_name):
        page = request.GET.get('page', 1)
        items_per_page = 25

        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        specific_date = request.GET.get('specific_date', None)

        # Filter by index name
        daily_prices = DailyPrice.objects.filter(index__name=index_name)

        # For speicific date
        if specific_date:
            daily_prices = daily_prices.filter(date=specific_date)

        # Date range Filter if provided
        if start_date:
            daily_prices = daily_prices.filter(date__gte=start_date)

        if end_date:
            daily_prices = daily_prices.filter(date__lte=end_date)

        # Filter by specific columns if provided in request payload
        filter_columns = ['open_price', 'high_price', 'low_price', 'close_price', 'shares_traded', 'turnover']
        for column in filter_columns:
            filter_value = request.GET.get(column)
            print(column, filter_value)
            if filter_value is not None:
                filter_param = {f"{column}__exact": filter_value}
                import pdb;pdb.set_trace()
                daily_prices = daily_prices.filter(**filter_param)

        # Calculate Ranges
        ranges = {
            "open": {"lowest": daily_prices.aggregate(lowest=models.Min('open_price'))['lowest'],
                     "highest": daily_prices.aggregate(highest=models.Max('open_price'))['highest']},
            "high": {"lowest": daily_prices.aggregate(lowest=models.Min('high_price'))['lowest'],
                     "highest": daily_prices.aggregate(highest=models.Max('high_price'))['highest']},
            "low": {"lowest": daily_prices.aggregate(lowest=models.Min('low_price'))['lowest'],
                    "highest": daily_prices.aggregate(highest=models.Max('low_price'))['highest']},
            "close": {"lowest": daily_prices.aggregate(lowest=models.Min('close_price'))['lowest'],
                      "highest": daily_prices.aggregate(highest=models.Max('close_price'))['highest']},
            "shares_traded": {"lowest": daily_prices.aggregate(lowest=models.Min('shares_traded'))['lowest'],
                              "highest": daily_prices.aggregate(highest=models.Max('shares_traded'))['highest']},
            "turnover": {"lowest": daily_prices.aggregate(lowest=models.Min('turnover'))['lowest'],
                         "highest": daily_prices.aggregate(highest=models.Max('turnover'))['highest']},
        }

        paginator = Paginator(daily_prices, items_per_page)

        try:
            current_page_data = paginator.page(page)
        except PageNotAnInteger:
            current_page_data = paginator.page(1)
        except EmptyPage:
            return Response({"error": "No more pages"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DailyPriceSerializer(current_page_data, many=True)

        response_data = {
            "start_date": str(current_page_data[0].date) if current_page_data else None,
            "end_date": str(current_page_data[-1].date) if current_page_data else None,
            "data": serializer.data,
            "pagination": {
                "page": current_page_data.number,
                "total_pages": paginator.num_pages,
                "total_rows": paginator.count,
            },
            "ranges": ranges,
        }

        return Response(response_data, status=status.HTTP_200_OK)
# class DailyPriceListView(generics.ListAPIView):
#     serializer_class = DailyPriceSerializer

#     def get_queryset(self):
#         index_id = self.kwargs['index_id']
#         return DailyPrice.objects.filter(index_id=index_id)

#     def list(self, request, *args, **kwargs):
#         import pdb;pdb.set_trace()
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
        
#         paginator = Paginator(serializer.data, items_per_page)

#         response_data = {
#             "start-date": "10-09-2023",
#             "end-date": "10-11-2023",
#             "data": serializer.data,
#             "pagination": {
#                 "page": self.page.number,
#                 "total_pages": self.page.paginator.num_pages,
#                 "total_rows": self.page.paginator.count,
#             },
#             "ranges": {
#                 # Your logic to calculate ranges for each column
#             }
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
