
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^products', ProductView.as_view(), name='products'),
    url(r'^measureunits', ProductMeasureUnitView.as_view(), name='measureunit'),
    url(r'^addmeasureunits', ProductAddMeasureUnitView.as_view(), name='addmeasureunits'),
    url(r'^categorys', ProductCategoryView.as_view(), name='categorys'),
    url(r'^addcategory', ProductAddCategoryView.as_view(), name='addcategory'),
]