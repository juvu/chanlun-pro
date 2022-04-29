from django.urls import path

from . import views
from . import views_stock
from . import views_hk
from . import views_us
from . import views_futures
from . import views_currency
from . import views_tasks
from . import views_back

urlpatterns = [

    # 基础登录
    path('login/', views.login_index),

    # 股票相关url配置
    path('', views_stock.index_show),
    path('stock/jhs', views_stock.jhs_json),
    path('stock/plate', views_stock.plate_json),
    path('stock/plate_stocks', views_stock.plate_stocks_json),
    path('stock/kline', views_stock.kline_chart),
    path('stock/dl_ranks', views_stock.dl_ranks_show),
    path('stock/dl_hy_save', views_stock.dl_hy_ranks_save),
    path('stock/dl_gn_save', views_stock.dl_gn_ranks_save),

    # 港股相关url配置
    path('hk/index', views_hk.index_show),
    path('hk/jhs', views_hk.jhs_json),
    path('hk/plate', views_hk.plate_json),
    path('hk/plate_stocks', views_hk.plate_stocks_json),
    path('hk/kline', views_hk.kline_chart),

    # 美股相关url配置
    path('us/index', views_us.index_show),
    path('us/jhs', views_us.jhs_json),
    path('us/kline', views_us.kline_chart),

    # 期货相关url配置
    path('futures/index', views_futures.index_show),
    path('futures/kline', views_futures.kline_show),
    path('futures/jhs', views_futures.jhs_json),

    # 数字货币相关Url配置
    path('currency/index', views_currency.index_show),
    path('currency/kline', views_currency.kline_show),
    path('currency/balances', views_currency.currency_balances),
    path('currency/positions', views_currency.currency_positions),
    path('currency/opt_records', views_currency.opt_records),
    path('currency/jhs', views_currency.jhs_json),

    # 行情数据回放练习
    path('back/index', views_back.index_show),
    path('back/kline', views_back.kline_show),

    # 定时任务配置
    path('tasks/index', views_tasks.index_show),
    path('tasks/save', views_tasks.task_save),

    # 自选操作
    path('zixuan/stocks', views.zixuan_stocks_json),
    path('zixuan/code_zx_names', views.zixuan_code_zx_names_json),
    path('zixuan/opt', views.zixuan_operation_json),
    path('search_code', views.search_code_json),

]
