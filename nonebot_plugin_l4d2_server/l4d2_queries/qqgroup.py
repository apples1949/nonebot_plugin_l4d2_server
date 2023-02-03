from ..l4d2_data.serverip import L4D2Server
from ..l4d2_image import server_ip_pic
from . import queries,player_queries,player_queries_dict,queries_dict,player_queries_anne_dict
from nonebot.log import logger
import random
import time
from ..message import PRISON,QUEREN,KAILAO
si = L4D2Server()
    
async def get_qqgroup_ip_msg(qqgroup):
    """首先，获取qq群订阅数据，再依次queries返回ip原标"""
    ip_list = await si.query_server_ip(qqgroup)
    return ip_list
    
async def bind_group_ip(group:int,host:str,port:int):
    ip_list = await si.query_server_ip(group)
    if (host,port) in ip_list:
        return "本群已添加过该ip辣"
    await si.bind_server_ip(group,host,port)
    return "绑定成功喵，新增ip" + host

async def del_group_ip(group:int,number:int):
    number = int(number)
    logger.info(number)
    try:
        groups,host,port = await si.query_number(number)
    except TypeError:
        return '没有这个序号哦'
    if groups != group:
        return "本群可没有订阅过这个ip"
    await si.del_server_ip(number)
    return "取消成功喵，已删除序号" + str(number)
        
async def qq_ip_queries(msg:list[tuple]):
    """输入一个ip的二元元组组成的列表，返回一个输出消息的列表
    未来作图这里重置"""
    messsage = ""
    for i in msg:
        number,qqgroup,host,port = i
        msg2 = await player_queries(host,port)
        msg1 = await queries(host,port)
        messsage += '序号、'+ str(number) + '\n' + msg1 + msg2 + '--------------------\n'
    return messsage
            
async def qq_ip_queries_pic(msg:list[tuple]):
    """输入一个ip的四元元组组成的列表，返回一个输出消息的图片"""
    msg_list = []
    print(msg)
    for i in msg:
        number,qqgroup,host,port = i
        try:
            msg2 = await player_queries_anne_dict(host,port)
            msg1 = await queries_dict(host,port)
            msg1.update(msg2)
            msg1.update({'number':number})
            # msg1是一行数据完整的字典
            msg_list.append(msg1)
        except TypeError:
            pass
    pic = await server_ip_pic(msg_list)
    return pic
    
async def get_tan_jian(msg:list[tuple],mode:int):
    """获取anne列表抽一个"""
    msg_list = []
    rank = 0
    for i in msg:
        number,qqgroup,host,port = i 
        if mode == 1:
            # 探监
            try:
                msg2 = await player_queries_anne_dict(host,port)
                point = 0
                for i in msg2['Players']:
                    point += int(i['Score'])
                logger.info(point)
                if point/4 <50:
                    logger.info('不够牢')
                    continue
                else:
                    msg1 = await queries_dict(host,port)
                    if 'HT' in msg1['name']:
                        logger.info('HT训练忽略')
                        continue
                    msg1.update(msg2)
                    msg1.update({'ranks':point})
                    ips = f'{host}:{str(port)}'
                    msg1.update({'ips':ips})
                # msg1是一行数据完整的字典
                    msg_list.append(msg1)
            except (TypeError,KeyError):
                continue
        if mode == 2:
            # 坐牢
            try:
                msg1 = await queries_dict(host,port)
                if '普通药役' in msg1['name']:
                    if '缺人' in msg1['name']:
                        msg2 = await player_queries_anne_dict(host,port)
                        msg1.update(msg2)
                        ips = f'{host}:{str(port)}'
                        msg1.update({'ips':ips})
                    # msg1是一行数据完整的字典
                        msg_list.append(msg1)
            except (TypeError,KeyError):
                continue
        if mode == 3:
            # 开牢
            try:
                msg1 = await queries_dict(host,port)
                if '[' not in msg1['name']:
                    msg2 = await player_queries_anne_dict(host,port)
                    msg1.update(msg2)
                    ips = f'{host}:{str(port)}'
                    msg1.update({'ips':ips})
                    # msg1是一行数据完整的字典
                    msg_list.append(msg1)
            except (TypeError,KeyError):
                continue
    # 随机选一个牢房
    if len(msg_list) == 0:
        return '暂时没有这种牢房捏'
    logger.info(len(msg_list))
    mse = random.choice(msg_list)
    message:str = ''
    if mode == 1:
        ranks = mse['ranks']
        if 200 < ranks <= 300 :
            message = random.choice(PRISON[1])
        if 300 < ranks <= 450 :
            message = random.choice(PRISON[2])
        if ranks > 450 :
            message = random.choice(PRISON[3]) 
    if mode == 2:
        player_point = mse['players']
        if player_point == '1':
            message = random.choice(QUEREN[1])
        elif player_point == '2':
            message = random.choice(QUEREN[2])
        elif player_point == '3':
            message = random.choice(QUEREN[3])
        else:
            message = random.choice(QUEREN[4])
    if mode == 3:
        message = random.choice(KAILAO)
    message += '\n' + '名称：' + mse['name'] + '\n'
    message += '地图：' + mse['map_'] + '\n'
    message += '玩家：' + mse['players'] + '/' + mse['max_players'] + '\n'
    n = 0
    try:
        max_duration_len = max([len(str(i['Duration'])) for i in mse['Players']])
        max_score_len = max([len(str(i['Score'])) for i in mse['Players']])
        for i in mse['Players']:
            n += 1 
            name = i['Name']
            Score = i['Score']
            Duration = i['Duration']
            soc = "[{:>{}}]".format(Score,max_score_len)
            dur = "{:^{}}".format(Duration, max_duration_len)
            message += f'{soc} | {dur} | {name} \n'
    except KeyError:
        message += '服务器里，是空空的呢\n'
    message += 'connect ' + mse['ips']
    return message

async def get_server_ip(number):
    group,host,port = await si.query_number(number)
    try:
        return str(host) + ':' + str(port)
    except TypeError:
        return None