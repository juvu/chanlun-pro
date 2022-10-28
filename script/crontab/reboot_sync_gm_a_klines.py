#:  -*- coding: utf-8 -*-
import datetime

from chanlun.exchange.exchange_db import ExchangeDB
from tqdm.auto import tqdm
import traceback
import time
import pandas as pd
from gm.api import *
from chanlun import config

"""
同步股票数据到数据库中

使用的是 掘金量化 API 获取
"""

# 可以直接提取数据，掘金终端需要打开，接口取数是通过网络请求的方式，效率一般，行情数据可通过subscribe订阅方式

# 如在远程执行，需要制定掘金终端地址  https://www.myquant.cn/docs/gm3_faq/154#b244aeed0032526e
set_serv_addr(config.GM_SERVER_ADDR)
# 设置token， 查看已有token ID,在用户-秘钥管理里获取
set_token(config.GM_TOKEN)

db_ex = ExchangeDB('a')

# 获取沪深 股票/基金/指数 代码
# fund_stocks = get_instruments(symbols=None, exchanges=['SHSE', 'SZSE'],
#                               sec_types=[SEC_TYPE_FUND])
#
# stock_stocks = get_instruments(symbols=None, exchanges=['SHSE', 'SZSE'],
#                                sec_types=[SEC_TYPE_STOCK])
# run_codes = ['SHSE.000001'] + [s['symbol'] for s in stock_stocks] + [s['symbol'] for s in fund_stocks if
#                                                                      s['symbol'][0:7] in ['SHSE.51', 'SZSE.15']]

# 指定要更新的股票列表
run_codes = [
    'SHSE.000001', 'SHSE.000688', 'SZSE.399001', 'SZSE.399006',
    'SHSE.600519', 'SHSE.601398', 'SHSE.600941', 'SHSE.601939', 'SZSE.300750', 'SHSE.601288', 'SHSE.601857',
    'SHSE.601628', 'SHSE.601988', 'SHSE.600036', 'SHSE.601318', 'SZSE.002594', 'SHSE.601088', 'SZSE.000858',
    'SHSE.600900', 'SHSE.600028', 'SHSE.601658', 'SHSE.601888', 'SHSE.601012', 'SZSE.300760', 'SHSE.601728',
    'SHSE.601166', 'SHSE.601328', 'SHSE.600809', 'SZSE.000333', 'SHSE.603288', 'SZSE.000568', 'SZSE.002714',
    'SHSE.688981', 'SHSE.600309', 'SZSE.002415', 'SHSE.600030', 'SHSE.601633', 'SHSE.600188', 'SZSE.300059',
    'SHSE.600690', 'SZSE.002304', 'SZSE.300999', 'SHSE.601998', 'SHSE.601319', 'SZSE.000001', 'SZSE.002352',
    'SHSE.601668', 'SHSE.601816', 'SHSE.601225', 'SHSE.600438', 'SHSE.600048', 'SHSE.600276', 'SHSE.601899',
    'SHSE.600887', 'SHSE.600000', 'SHSE.603259', 'SZSE.002142', 'SZSE.002475', 'SZSE.000002', 'SHSE.601601',
    'SZSE.300015', 'SZSE.300274', 'SHSE.601066', 'SHSE.601919', 'SZSE.000651', 'SZSE.300014', 'SHSE.600406',
    'SHSE.688223', 'SHSE.600104', 'SZSE.002466', 'SHSE.600905', 'SHSE.601138', 'SHSE.601995', 'SZSE.300124',
    'SZSE.002812', 'SHSE.600436', 'SZSE.002460', 'SHSE.601818', 'SZSE.001289', 'SZSE.002459', 'SHSE.600585',
    'SHSE.600016', 'SHSE.601111', 'SZSE.300498', 'SHSE.601898', 'SHSE.688599', 'SZSE.002129', 'SHSE.600600',
    'SHSE.600009', 'SZSE.003816', 'SHSE.601766', 'SZSE.000596', 'SZSE.000725', 'SZSE.001979', 'SHSE.601390',
    'SZSE.000792', 'SHSE.601238', 'SHSE.600018', 'SZSE.000625', 'SHSE.603260', 'SHSE.600025', 'SZSE.300122',
    'SHSE.600011', 'SZSE.002493', 'SHSE.601211', 'SZSE.002049', 'SHSE.600031', 'SZSE.002371', 'SHSE.600760',
    'SHSE.601985', 'SHSE.600019', 'SHSE.600346', 'SHSE.601800', 'SZSE.000776', 'SHSE.600837', 'SHSE.688235',
    'SHSE.600893', 'SHSE.600919', 'SHSE.600029', 'SHSE.601688', 'SHSE.601669', 'SHSE.600999', 'SHSE.601009',
    'SHSE.688303', 'SHSE.600050', 'SHSE.688111', 'SZSE.000301', 'SHSE.600150', 'SZSE.002311', 'SZSE.300896',
    'SHSE.603392', 'SZSE.002179', 'SHSE.603799', 'SZSE.000063', 'SHSE.601006', 'SHSE.605117', 'SZSE.000166',
    'SHSE.601881', 'SHSE.601868', 'SHSE.601186', 'SHSE.603993', 'SHSE.600989', 'SHSE.600111', 'SHSE.600660',
    'SZSE.000538', 'SZSE.002709', 'SHSE.600115', 'SHSE.603501', 'SZSE.000708', 'SZSE.300751', 'SHSE.601169',
    'SZSE.300316', 'SHSE.600089', 'SZSE.002241', 'SHSE.601336', 'SHSE.600886', 'SHSE.600010', 'SHSE.601229',
    'SZSE.000895', 'SHSE.600256', 'SHSE.600926', 'SZSE.002736', 'SZSE.000338', 'SHSE.603195', 'SZSE.002050',
    'SHSE.600522', 'SHSE.601689', 'SHSE.603659', 'SHSE.600795', 'SZSE.300450', 'SHSE.688187', 'SHSE.601989',
    'SHSE.600703', 'SHSE.601127', 'SZSE.002027', 'SHSE.600015', 'SHSE.600026', 'SZSE.300763', 'SHSE.600196',
    'SHSE.600547', 'SZSE.002920', 'SZSE.000877', 'SZSE.002230', 'SHSE.600845', 'SHSE.601600', 'SHSE.601808',
    'SHSE.600233', 'SZSE.000768', 'SHSE.603806', 'SHSE.601865', 'SHSE.601018', 'SHSE.603833', 'SZSE.300957',
    'SZSE.300347', 'SHSE.600875', 'SHSE.601991', 'SZSE.000963', 'SHSE.600958', 'SZSE.000876', 'SZSE.000661',
    'SZSE.002001', 'SHSE.600027', 'SZSE.002271', 'SZSE.002180', 'SHSE.601100', 'SHSE.600085', 'SHSE.600570',
    'SHSE.601618', 'SHSE.601916', 'SHSE.601788', 'SHSE.601727', 'SHSE.600426', 'SHSE.688396', 'SHSE.688385',
    'SHSE.688363', 'SZSE.002938', 'SZSE.300142', 'SHSE.601607', 'SZSE.000983', 'SZSE.002074', 'SHSE.601615',
    'SHSE.600754', 'SHSE.688063', 'SHSE.601838', 'SHSE.600588', 'SZSE.000733', 'SHSE.601872', 'SZSE.300759',
    'SHSE.600803', 'SHSE.601877', 'SHSE.688032', 'SHSE.600745', 'SZSE.003022', 'SHSE.603613', 'SZSE.000617',
    'SZSE.000100', 'SZSE.300628', 'SHSE.600674', 'SZSE.300979', 'SHSE.603986', 'SHSE.603185', 'SHSE.603290',
    'SHSE.603369', 'SHSE.600362', 'SZSE.002410', 'SHSE.601901', 'SZSE.300661', 'SZSE.000425', 'SHSE.600741',
    'SHSE.600176', 'SHSE.605499', 'SZSE.002756', 'SZSE.300408', 'SHSE.603606', 'SHSE.601825', 'SHSE.600236',
    'SHSE.601699', 'SHSE.688122', 'SZSE.000157', 'SHSE.600221', 'SZSE.002202', 'SHSE.600039', 'SHSE.688012',
    'SHSE.688008', 'SZSE.300919', 'SZSE.300769', 'SHSE.600383', 'SHSE.688234', 'SZSE.002821', 'SHSE.600348',
    'SHSE.688126', 'SHSE.603605', 'SZSE.002648', 'SHSE.601117', 'SZSE.001965', 'SZSE.300496', 'SHSE.600132',
    'SHSE.601377', 'SHSE.600487', 'SZSE.300433', 'SHSE.601360', 'SHSE.603688', 'SHSE.600884', 'SHSE.601021',
    'SHSE.600918', 'SHSE.600515', 'SZSE.000938', 'SHSE.688036', 'SHSE.688009', 'SHSE.603345', 'SZSE.300413',
    'SZSE.300782', 'SHSE.603198', 'SHSE.600153', 'SHSE.600460', 'SZSE.000408', 'SHSE.601799', 'SZSE.002013',
    'SHSE.600765', 'SHSE.600023', 'SZSE.002120', 'SHSE.688180', 'SZSE.002841', 'SZSE.000629', 'SHSE.600332',
    'SHSE.600096', 'SZSE.300207', 'SHSE.600702', 'SHSE.600956', 'SZSE.300033', 'SHSE.600985', 'SZSE.300724',
    'SHSE.600732', 'SZSE.002240', 'SHSE.601077', 'SZSE.000723', 'SZSE.002738', 'SHSE.601698', 'SZSE.000786',
    'SZSE.300390', 'SHSE.688777', 'SHSE.600061', 'SHSE.603899', 'SHSE.603568', 'SHSE.688728', 'SZSE.000999',
    'SZSE.002384', 'SHSE.600606', 'SHSE.600663', 'SZSE.300003', 'SHSE.601880', 'SHSE.688390', 'SHSE.600160',
    'SZSE.000069', 'SZSE.002916', 'SZSE.002340', 'SZSE.002414', 'SHSE.600763', 'SZSE.000799', 'SHSE.603486',
    'SHSE.601155', 'SZSE.000039', 'SHSE.600584', 'SHSE.688005', 'SZSE.002601', 'SZSE.300454', 'SHSE.601878',
    'SHSE.600563', 'SHSE.600157', 'SHSE.600219', 'SZSE.002945', 'SZSE.000975', 'SHSE.600995', 'SHSE.688516',
    'SZSE.300699', 'SZSE.002032', 'SHSE.600885', 'SZSE.001872', 'SHSE.600141', 'SHSE.600377', 'SHSE.688538',
    'SHSE.600546', 'SHSE.600378', 'SZSE.002603', 'SHSE.600489', 'SHSE.601298', 'SZSE.002252', 'SHSE.600372',
    'SHSE.603939', 'SHSE.603596', 'SZSE.002430', 'SHSE.600871', 'SZSE.002236', 'SHSE.600298', 'SZSE.000933',
    'SHSE.603868', 'SHSE.688065', 'SZSE.300529', 'SHSE.601236', 'SHSE.600988', 'SHSE.601231', 'SZSE.002244',
    'SHSE.688301', 'SZSE.002080', 'SZSE.300073', 'SZSE.300438', 'SZSE.002353', 'SZSE.300012', 'SHSE.600862',
    'SHSE.601866', 'SZSE.300442', 'SZSE.000800', 'SZSE.002385', 'SZSE.300037', 'SHSE.600549', 'SHSE.603737',
    'SZSE.000738', 'SHSE.601216', 'SZSE.002939', 'SHSE.603658', 'SZSE.002176', 'SZSE.300595', 'SHSE.600801',
    'SZSE.002555', 'SHSE.688248', 'SHSE.600482', 'SZSE.300223', 'SZSE.002025', 'SHSE.601869', 'SZSE.002056',
    'SZSE.000807', 'SHSE.600161', 'SHSE.688819', 'SZSE.002064', 'SZSE.002007', 'SZSE.002532', 'SHSE.600688',
    'SHSE.600499', 'SHSE.601233', 'SZSE.002625', 'SHSE.603885', 'SHSE.601108', 'SHSE.601555', 'SHSE.600004',
    'SHSE.601666', 'SZSE.300601', 'SZSE.301029', 'SZSE.002600', 'SHSE.603019', 'SZSE.002372', 'SZSE.002078',
    'SHSE.603529', 'SHSE.600536', 'SHSE.600486', 'SHSE.603456', 'SHSE.688082', 'SHSE.601058', 'SHSE.600418',
    'SHSE.600481', 'SHSE.600295', 'SZSE.300850', 'SHSE.600183', 'SHSE.600968', 'SHSE.603816', 'SZSE.002568',
    'SZSE.002422', 'SZSE.002497', 'SZSE.300832', 'SZSE.002028', 'SZSE.000883', 'SHSE.603712', 'SHSE.600352',
    'SHSE.600873', 'SHSE.600848', 'SHSE.600685', 'SZSE.300776', 'SZSE.000783', 'SHSE.605358', 'SHSE.603517',
    'SHSE.601696', 'SHSE.600177', 'SHSE.601990', 'SZSE.300146', 'SHSE.688188', 'SHSE.603233', 'SZSE.300604',
    'SHSE.603876', 'SHSE.688779', 'SZSE.000728', 'SHSE.688561', 'SHSE.600642', 'SHSE.600109', 'SZSE.000977',
    'SZSE.000932', 'SZSE.000009', 'SHSE.603127', 'SZSE.000987', 'SHSE.688567', 'SZSE.000066', 'SZSE.002865',
    'SHSE.688185', 'SZSE.300888', 'SHSE.600779', 'SHSE.603077', 'SZSE.002407', 'SZSE.000519', 'SZSE.002192',
    'SHSE.600399', 'SHSE.688536', 'SZSE.300144', 'SZSE.300395', 'SHSE.603882', 'SZSE.002518', 'SZSE.000513',
    'SZSE.000630', 'SHSE.603826', 'SHSE.689009', 'SHSE.601933', 'SHSE.600517', 'SHSE.603267', 'SZSE.002602',
    'SZSE.002831', 'SZSE.002405', 'SZSE.000959', 'SHSE.600079', 'SHSE.601001', 'SHSE.600733', 'SZSE.000703',
    'SZSE.000893', 'SHSE.688778', 'SZSE.300748', 'SZSE.000027', 'SZSE.000155', 'SHSE.600705', 'SZSE.000591',
    'SZSE.002791', 'SHSE.601958', 'SHSE.600673', 'SHSE.601992', 'SHSE.600021', 'SZSE.002008', 'SHSE.600497',
    'SHSE.601966', 'SHSE.601577', 'SZSE.301035', 'SZSE.002294', 'SZSE.002299', 'SHSE.603893', 'SZSE.002673',
    'SHSE.600392', 'SHSE.601598', 'SZSE.300034', 'SZSE.002223', 'SZSE.000729', 'SHSE.600350', 'SHSE.600521',
    'SZSE.300568', 'SZSE.000683', 'SZSE.002185', 'SHSE.600299', 'SHSE.603589', 'SHSE.688598', 'SZSE.002966',
    'SHSE.600863', 'SHSE.603305', 'SZSE.300285', 'SHSE.601456', 'SZSE.000831', 'SHSE.688099', 'SZSE.000825',
    'SZSE.300861', 'SHSE.600859', 'SHSE.600655', 'SHSE.600369', 'SHSE.601636', 'SHSE.688220', 'SHSE.600143',
    'SZSE.000898', 'SZSE.002128', 'SHSE.601156', 'SZSE.300373', 'SZSE.002268', 'SZSE.000937', 'SHSE.688772',
    'SHSE.688116', 'SZSE.002531', 'SZSE.000830', 'SZSE.300357', 'SHSE.601158', 'SZSE.000785', 'SHSE.603707',
    'SZSE.002607', 'SZSE.002153', 'SZSE.002409', 'SHSE.600518', 'SZSE.000709', 'SHSE.600415', 'SZSE.002487',
    'SZSE.002624', 'SHSE.601162', 'SHSE.601198', 'SHSE.600416', 'SHSE.600032', 'SHSE.688700', 'SHSE.601717',
    'SHSE.600927', 'SZSE.000539', 'SZSE.300363', 'SHSE.603786', 'SHSE.600118', 'SHSE.600516', 'SHSE.688161',
    'SZSE.300487', 'SHSE.600872', 'SZSE.300118', 'SZSE.002472', 'SHSE.600598', 'SHSE.688256', 'SZSE.002030',
    'SHSE.601568', 'SZSE.300682', 'SHSE.601228', 'SHSE.601963', 'SHSE.600258', 'SHSE.603156', 'SZSE.002541',
    'SZSE.002797', 'SHSE.688169', 'SZSE.002203', 'SHSE.600909', 'SZSE.000537', 'SHSE.600325', 'SHSE.688707',
    'SZSE.300666', 'SZSE.002850', 'SHSE.600038', 'SZSE.002444', 'SHSE.601016', 'SHSE.600170', 'SZSE.002608',
    'SZSE.002761', 'SZSE.002507', 'SZSE.001227', 'SHSE.688276', 'SHSE.601975', 'SHSE.601168', 'SHSE.600906',
    'SZSE.000401', 'SZSE.000958', 'SHSE.601179', 'SZSE.002557', 'SZSE.002015', 'SHSE.601399', 'SHSE.688690',
    'SZSE.003035', 'SHSE.600816', 'SZSE.300676', 'SHSE.601928', 'SZSE.000553', 'SZSE.300866', 'SHSE.601128',
    'SZSE.002399', 'SZSE.300308', 'SHSE.600566', 'SHSE.600704', 'SZSE.000980', 'SHSE.600998', 'SZSE.002335',
    'SHSE.688105', 'SZSE.000762', 'SZSE.002312', 'SHSE.688006', 'SHSE.603160', 'SZSE.000050', 'SHSE.600578',
    'SZSE.002508', 'SZSE.300474', 'SZSE.002739', 'SZSE.002266', 'SZSE.002597', 'SZSE.000423', 'SZSE.002653',
    'SHSE.603218', 'SZSE.002484', 'SHSE.600483', 'SHSE.600208', 'SHSE.600637', 'SZSE.000012', 'SZSE.000516',
    'SHSE.600808', 'SHSE.601777', 'SZSE.002326', 'SHSE.601611', 'SZSE.002432', 'SHSE.600456', 'SHSE.688521',
    'SZSE.002145', 'SZSE.000960', 'SHSE.600612', 'SZSE.002152', 'SHSE.603236', 'SHSE.600166', 'SHSE.603713',
    'SHSE.600559', 'SHSE.600699', 'SHSE.600390', 'SHSE.688107', 'SHSE.600582', 'SZSE.300251', 'SHSE.603565',
    'SHSE.688017', 'SHSE.688425', 'SZSE.301071', 'SHSE.603355', 'SZSE.002439', 'SHSE.600338', 'SHSE.600711',
    'SZSE.301155', 'SZSE.002936', 'SZSE.002408', 'SHSE.688139', 'SHSE.600057', 'SHSE.600380', 'SHSE.603026',
    'SZSE.003031', 'SHSE.603129', 'SZSE.300633', 'SZSE.002926', 'SHSE.688520', 'SHSE.600583', 'SHSE.688556',
    'SZSE.002948', 'SHSE.601997', 'SZSE.300260', 'SHSE.603348', 'SHSE.601106', 'SHSE.603317', 'SZSE.000739',
    'SZSE.002595', 'SHSE.601139', 'SHSE.601212', 'SZSE.002690', 'SHSE.600008', 'SZSE.002683', 'SHSE.688050',
    'SZSE.000869', 'SZSE.002156', 'SHSE.601965', 'SZSE.000887', 'SZSE.002617', 'SZSE.000988', 'SHSE.603858',
    'SZSE.002389', 'SZSE.300257', 'SHSE.600739', 'SHSE.688200', 'SZSE.002506', 'SZSE.002906', 'SHSE.603338',
    'SHSE.603883', 'SZSE.300777', 'SHSE.600500', 'SHSE.600970', 'SZSE.000688', 'SZSE.001213', 'SHSE.600315',
    'SZSE.002463', 'SZSE.300068', 'SHSE.601828', 'SHSE.603179', 'SZSE.300054', 'SHSE.601028', 'SZSE.000818',
    'SHSE.688686', 'SHSE.600271', 'SHSE.601665', 'SHSE.600511', 'SZSE.000564', 'SHSE.600098', 'SZSE.002500',
    'SZSE.000810', 'SHSE.600977', 'SZSE.002468', 'SZSE.000878', 'SHSE.600916', 'SHSE.600398', 'SHSE.600095',
    'SHSE.600596', 'SZSE.000998', 'SHSE.601118', 'SZSE.300775', 'SZSE.002505', 'SHSE.688776', 'SHSE.601098',
    'SHSE.600123', 'SHSE.601677', 'SHSE.600062', 'SZSE.002465', 'SZSE.300761', 'SHSE.600777', 'SZSE.000750',
    'SZSE.300558', 'SZSE.300244', 'SZSE.300910', 'SHSE.603087', 'SHSE.600395', 'SHSE.600056', 'SHSE.600297',
    'SHSE.688499', 'SZSE.300803', 'SZSE.000581', 'SHSE.603599', 'SZSE.000400', 'SZSE.002984', 'SHSE.600827',
    'SHSE.601908', 'SHSE.603866', 'SZSE.300726', 'SHSE.600282', 'SHSE.688739', 'SZSE.300393', 'SHSE.601702',
    'SHSE.603056', 'SZSE.002065', 'SZSE.000970', 'SHSE.601099', 'SHSE.600246', 'SHSE.605111', 'SZSE.002092',
    'SHSE.605090', 'SZSE.300432', 'SHSE.603444', 'SHSE.688037', 'SHSE.603505', 'SHSE.600641', 'SZSE.002456',
    'SHSE.603678', 'SHSE.600548', 'SHSE.688202', 'SZSE.002585', 'SHSE.600867', 'SZSE.300070', 'SHSE.600329',
    'SZSE.301177', 'SZSE.300428', 'SHSE.601369', 'SHSE.600935', 'SZSE.002041', 'SZSE.000875', 'SZSE.000902',
    'SHSE.688002', 'SZSE.002250', 'SHSE.601567', 'SHSE.600116', 'SHSE.600933', 'SZSE.000021', 'SHSE.600528',
    'SHSE.600320', 'SZSE.000559', 'SHSE.600562', 'SZSE.002024', 'SHSE.600022', 'SZSE.000981', 'SHSE.601375',
    'SZSE.002958', 'SHSE.600316', 'SHSE.603650', 'SHSE.603228', 'SZSE.300593', 'SHSE.600895', 'SHSE.600339',
    'SHSE.600179', 'SHSE.688333', 'SZSE.002262', 'SHSE.688232', 'SHSE.603027', 'SHSE.600277', 'SHSE.601952',
    'SHSE.600882', 'SHSE.603733', 'SZSE.002245', 'SZSE.300457', 'SZSE.002044', 'SHSE.600529', 'SZSE.002747',
    'SZSE.001914', 'SZSE.300821', 'SZSE.300294', 'SHSE.600879', 'SZSE.300376', 'SHSE.603588', 'SHSE.600580',
    'SZSE.000636', 'SZSE.000060', 'SZSE.002138', 'SZSE.300627', 'SZSE.002837', 'SZSE.000547', 'SZSE.300346',
    'SZSE.002324', 'SHSE.600740', 'SHSE.600820', 'SZSE.002436', 'SZSE.000623', 'SZSE.300679', 'SHSE.600675',
    'SHSE.603906', 'SHSE.600066', 'SZSE.000927', 'SZSE.301039', 'SHSE.601000', 'SZSE.000686', 'SHSE.600248',
    'SZSE.002985', 'SHSE.603098', 'SZSE.300026', 'SZSE.300035', 'SZSE.300001', 'SHSE.600323', 'SHSE.603363',
    'SHSE.601921', 'SZSE.300253', 'SZSE.002558', 'SHSE.600737', 'SZSE.000627', 'SZSE.000935', 'SZSE.002036',
    'SHSE.600167', 'SHSE.600063', 'SZSE.002901', 'SZSE.002429', 'SHSE.603379', 'SZSE.002318', 'SHSE.600110',
    'SZSE.002925', 'SHSE.600131', 'SZSE.002155', 'SZSE.300088', 'SHSE.600498', 'SZSE.000429', 'SZSE.002273',
    'SZSE.000402', 'SHSE.600610', 'SHSE.603279', 'SHSE.688676', 'SZSE.002461', 'SZSE.000930', 'SZSE.000598',
    'SZSE.002670', 'SZSE.000967', 'SHSE.601326', 'SZSE.300203', 'SHSE.601608', 'SHSE.600901', 'SHSE.600928',
    'SZSE.001203', 'SHSE.688568', 'SHSE.600773', 'SZSE.000921', 'SHSE.600328', 'SZSE.301090', 'SHSE.600764',
    'SHSE.605123', 'SHSE.601222', 'SZSE.300171', 'SZSE.002698', 'SHSE.603025', 'SHSE.600060', 'SZSE.000860',
    'SZSE.300383', 'SHSE.688800', 'SHSE.600877', 'SZSE.300418', 'SZSE.002010', 'SHSE.605507', 'SZSE.000778',
    'SHSE.688639', 'SZSE.002773', 'SHSE.600959', 'SHSE.600535', 'SHSE.600869', 'SZSE.002157', 'SZSE.002258',
    'SZSE.002727', 'SZSE.002423', 'SZSE.300009', 'SHSE.688019', 'SHSE.600707', 'SZSE.002182', 'SZSE.000031',
    'SZSE.300298', 'SZSE.300820', 'SHSE.688559', 'SHSE.600199', 'SHSE.600129', 'SZSE.300296', 'SZSE.002840',
    'SHSE.688798', 'SZSE.000032', 'SZSE.000488', 'SHSE.600507', 'SHSE.600755', 'SHSE.601005', 'SHSE.600597',
    'SZSE.002091', 'SHSE.688083', 'SZSE.002572', 'SZSE.002216', 'SZSE.000422', 'SHSE.603477', 'SZSE.300136',
    'SZSE.002517', 'SZSE.002705', 'SHSE.601187', 'SHSE.603612', 'SHSE.688696', 'SHSE.688066', 'SHSE.600055',
    'SZSE.300973', 'SHSE.600007', 'SHSE.688198', 'SHSE.600623', 'SZSE.300855', 'SZSE.300101', 'SZSE.300024',
    'SHSE.603489', 'SHSE.688617', 'SHSE.601333', 'SZSE.002183', 'SHSE.688055', 'SZSE.002643', 'SHSE.603927',
    'SHSE.600428', 'SZSE.002610', 'SHSE.600389', 'SZSE.000657', 'SZSE.002851', 'SHSE.688278', 'SHSE.603730',
    'SZSE.002011', 'SZSE.300741', 'SHSE.688680', 'SZSE.002151', 'SHSE.600100', 'SHSE.688206', 'SZSE.002706',
    'SHSE.688289', 'SHSE.600126', 'SHSE.603225', 'SHSE.605296', 'SHSE.601778', 'SHSE.600195', 'SZSE.300618',
    'SHSE.600967', 'SHSE.600996', 'SHSE.600657', 'SZSE.300083', 'SZSE.002124', 'SZSE.002498', 'SHSE.688408',
    'SZSE.300339', 'SZSE.002373', 'SHSE.688029', 'SZSE.002978', 'SZSE.002402', 'SZSE.000089', 'SHSE.600478',
    'SHSE.600648', 'SHSE.601718', 'SZSE.002544', 'SZSE.002100', 'SZSE.002511', 'SZSE.300343', 'SZSE.300725',
    'SHSE.601969', 'SHSE.603728', 'SZSE.300623', 'SZSE.002139', 'SZSE.300677', 'SZSE.300382', 'SZSE.000567',
    'SHSE.600259', 'SZSE.300567', 'SZSE.002563', 'SZSE.000415', 'SHSE.688192', 'SZSE.000034', 'SZSE.002249',
    'SZSE.000498', 'SZSE.002534', 'SHSE.600586', 'SHSE.600771', 'SZSE.000997', 'SZSE.300482', 'SHSE.601019',
    'SHSE.603128', 'SHSE.600595', 'SZSE.000756', 'SHSE.600400', 'SHSE.600151', 'SHSE.605589', 'SZSE.300613',
    'SHSE.600273', 'SZSE.000403', 'SZSE.000761', 'SHSE.600409', 'SHSE.600876', 'SZSE.300747', 'SZSE.301050',
    'SZSE.002226', 'SZSE.300115', 'SHSE.600388', 'SHSE.688110', 'SZSE.002832', 'SHSE.603997', 'SHSE.688208',
    'SZSE.002291', 'SHSE.600997', 'SHSE.688298', 'SHSE.600216', 'SZSE.002121', 'SZSE.000966', 'SHSE.603308',
    'SZSE.000156', 'SZSE.301069', 'SZSE.000550', 'SHSE.688388', 'SZSE.000062', 'SZSE.300596', 'SZSE.002221',
    'SHSE.600267', 'SZSE.300458', 'SZSE.002019', 'SHSE.600120', 'SHSE.600782', 'SZSE.002867', 'SZSE.002539',
    'SZSE.000049', 'SZSE.301015', 'SZSE.002006', 'SZSE.000028', 'SZSE.000582', 'SZSE.002745', 'SHSE.603595',
    'SZSE.002085', 'SHSE.600929', 'SHSE.600171', 'SHSE.600839', 'SHSE.603301', 'SHSE.605376', 'SHSE.600955',
    'SHSE.603005', 'SZSE.000990', 'SHSE.603033', 'SHSE.600917', 'SZSE.002960', 'SHSE.603063', 'SHSE.600155',
    'SZSE.002701', 'SHSE.600403', 'SHSE.605369', 'SZSE.002101', 'SHSE.601512', 'SZSE.000951', 'SZSE.002219',
    'SZSE.002411', 'SZSE.002131', 'SZSE.000035', 'SHSE.603638', 'SHSE.600662', 'SHSE.600718', 'SHSE.600667',
    'SZSE.000016', 'SHSE.603979', 'SZSE.002081', 'SHSE.600508', 'SZSE.002866', 'SZSE.000672', 'SZSE.002003',
    'SZSE.002110', 'SZSE.300827', 'SHSE.601918', 'SHSE.600639', 'SZSE.002317', 'SHSE.603043', 'SHSE.600064',
    'SHSE.600532', 'SHSE.600717', 'SHSE.600363', 'SZSE.002549', 'SZSE.301078', 'SHSE.600618', 'SZSE.002158',
    'SZSE.000712', 'SZSE.300017', 'SZSE.300755', 'SZSE.002895', 'SZSE.300737', 'SZSE.000563', 'SZSE.301047',
    'SZSE.300182', 'SHSE.601811', 'SHSE.688518', 'SHSE.688268', 'SHSE.600435', 'SZSE.300587', 'SHSE.600452',
    'SHSE.603938', 'SZSE.002242', 'SZSE.000546', 'SHSE.601068', 'SHSE.688270', 'SZSE.300093', 'SHSE.603919',
    'SHSE.603223', 'SHSE.601107', 'SZSE.000821', 'SHSE.688001', 'SHSE.601137', 'SZSE.002088', 'SHSE.600006',
    'SHSE.600621', 'SZSE.300327', 'SHSE.603000', 'SHSE.600373', 'SHSE.688608', 'SHSE.603008', 'SZSE.002911',
    'SHSE.600850', 'SZSE.002675', 'SZSE.002581', 'SHSE.600376', 'SHSE.600776', 'SHSE.603567', 'SHSE.603398',
    'SZSE.002847', 'SHSE.603690', 'SHSE.600835', 'SZSE.300476', 'SZSE.002171', 'SZSE.002458', 'SHSE.688383',
    'SZSE.300058', 'SZSE.300841', 'SZSE.002204', 'SZSE.300638', 'SHSE.600603', 'SHSE.603985', 'SZSE.002626',
    'SZSE.000528', 'SZSE.002195', 'SZSE.002287', 'SZSE.300773', 'SZSE.300767', 'SHSE.601519', 'SZSE.300672',
    'SHSE.603515', 'SZSE.000656', 'SZSE.301031', 'SHSE.600682', 'SHSE.600163', 'SHSE.600370', 'SZSE.000090',
    'SHSE.600567', 'SHSE.603693', 'SZSE.000059', 'SHSE.600012', 'SZSE.002254', 'SHSE.601258', 'SHSE.601827',
    'SZSE.300332', 'SHSE.603100', 'SHSE.603298', 'SHSE.600206', 'SHSE.688366', 'SHSE.600335', 'SZSE.002967',
    'SHSE.688789', 'SHSE.601126', 'SZSE.002320', 'SHSE.601678', 'SHSE.688023', 'SZSE.002191', 'SHSE.600330',
    'SHSE.600888', 'SHSE.600787', 'SHSE.601101', 'SZSE.002002', 'SZSE.002928', 'SZSE.002127', 'SZSE.002396',
    'SZSE.300502', 'SZSE.000690', 'SZSE.002514', 'SHSE.603983', 'SHSE.600366', 'SZSE.002212', 'SZSE.301018',
    'SHSE.600908', 'SZSE.002416', 'SZSE.300459', 'SHSE.600556', 'SZSE.002281', 'SZSE.300394', 'SZSE.000413',
    'SZSE.002434', 'SZSE.002567', 'SZSE.300443', 'SZSE.002099', 'SZSE.300772', 'SZSE.002004', 'SZSE.300856',
    'SHSE.603396', 'SZSE.300416', 'SZSE.000540', 'SZSE.000767', 'SZSE.300990', 'SZSE.002545', 'SHSE.603032',
    'SHSE.600313', 'SHSE.688733', 'SZSE.002048', 'SHSE.688016', 'SZSE.002237', 'SZSE.000088', 'SHSE.600305',
    'SHSE.688133', 'SHSE.601609', 'SZSE.300481', 'SZSE.300224', 'SHSE.600037', 'SHSE.603719', 'SHSE.601069',
    'SZSE.300080', 'SZSE.002368', 'SZSE.000543', 'SZSE.003039', 'SZSE.002737', 'SZSE.301217', 'SZSE.002453',
    'SZSE.300894', 'SZSE.000426', 'SHSE.603915', 'SZSE.002125', 'SZSE.300261', 'SZSE.002930', 'SZSE.002068',
    'SZSE.300217', 'SHSE.688097', 'SHSE.688269', 'SHSE.600225', 'SZSE.002645', 'SZSE.300586', 'SHSE.688526',
    'SHSE.601038', 'SHSE.603989', 'SHSE.600587', 'SHSE.605222', 'SHSE.605008', 'SZSE.002061', 'SHSE.688239',
    'SZSE.300630', 'SHSE.601015', 'SHSE.600307', 'SZSE.002993', 'SHSE.600572', 'SZSE.300887', 'SHSE.601200',
    'SHSE.601311', 'SZSE.000555', 'SZSE.002126', 'SHSE.600746', 'SHSE.688131', 'SZSE.002665', 'SZSE.002726',
    'SHSE.600841', 'SZSE.002839', 'SZSE.300463', 'SHSE.603871', 'SHSE.688033', 'SHSE.600230', 'SHSE.600728',
    'SZSE.002146', 'SHSE.688100', 'SZSE.002793', 'SHSE.603583', 'SHSE.603171', 'SHSE.605333', 'SZSE.300072',
    'SHSE.688167', 'SHSE.600477', 'SZSE.300456'
]

print(len(run_codes))

# 创建表
db_ex.create_tables(run_codes)

# 当前时间
now_datetime = datetime.datetime.now()

# 默认第一次同步的起始时间，后续则进行增量更新
sync_frequencys = {
    'd': {'start': '2005-01-01 00:00:00'},
    '30m': {'start': '2016-01-01 00:00:00'},
    '5m': {'start': '2016-01-01 00:00:00'},
}
# 本地周期与掘金周期对应关系
fre_maps = {
    '5m': '300s', '30m': '1800s', 'd': '1d'
}

# K线数据采用后复权，可增量更新
is_update = False
for code in tqdm(run_codes):

    # 中途终端后，可以设置下次起始的代码
    # if not is_update and code == 'SHSE.600433':
    #     is_update = True
    # if not is_update:
    #     continue

    for f, dt in sync_frequencys.items():
        try:
            while True:
                time.sleep(1)
                last_dt = db_ex.query_last_datetime(code, f)
                if last_dt is None:
                    last_dt = dt['start']
                klines = history(
                    code, fre_maps[f], start_time=last_dt, end_time=now_datetime, adjust=ADJUST_POST, df=True
                )
                klines.loc[:, 'code'] = klines['symbol']
                klines.loc[:, 'date'] = pd.to_datetime(klines['eob'])
                klines = klines[['code', 'date', 'open', 'close', 'high', 'low', 'volume']]
                print('Run code %s frequency %s klines len %s' % (code, f, len(klines)))
                db_ex.insert_klines(code, f, klines)
                if len(klines) < 200:
                    break
        except Exception as e:
            print('执行 %s 同步K线异常' % code)
            print(traceback.format_exc())
            time.sleep(10)