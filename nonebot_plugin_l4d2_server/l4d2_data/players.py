from ..config import DATASQLITE
import sqlite3
from typing import Union


class L4D2Player:
    """数据库L4D2_Player表的操作""" 
    def __init__(self):
        """连接数据库"""
        self.datasqlite_path = DATASQLITE
        self.conn = sqlite3.connect(self.datasqlite_path / 'L4D2.db')
        self.c = self.conn.cursor()
        
    def _add_player_nickname(self, qq, nickname):
        """绑定昵称"""
        try:
            self.c.execute("INSERT INTO L4d2_players (qq, nickname, steamid) VALUES (?,?,NULL)", (qq, nickname))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
              
    def _add_player_steamid(self, qq, nickname,steamid):
        """用新数据覆盖旧数据"""
        try:
            self.c.execute("INSERT INTO L4d2_players (qq, nickname, steamid) VALUES (?,?,?)", (qq, nickname,steamid))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def _delete_player(self, qq):
        """解除绑定"""
        self.c.execute(f"DELETE FROM L4d2_players WHERE qq = {qq}")
        self.conn.commit()
        return True
        
    def _query_player_qq(self, qq) -> Union[tuple,None]:
        """通过qq获取数据"""
        self.c.execute(f"SELECT * FROM L4d2_players WHERE qq = {qq}")
        return self.c.fetchone()
    
    def _query_player_nickname(self, nickname) -> Union[tuple,None]:
        """通过nickname获取数据"""
        self.c.execute(f"SELECT * FROM L4d2_players WHERE nickname = {nickname}")
        return self.c.fetchone()

    def _query_player_steamid(self, nickname) -> Union[tuple,None]:
        """通过steamid获取数据"""
        self.c.execute(f"SELECT * FROM L4d2_players WHERE nickname = {nickname}")
        return self.c.fetchone()
    
    def search_data(self, qq, nickname, steamid) -> Union[tuple,None]:
        """
        输入元组查询，优先qq其次steamid最后nickname，不需要值可以为None
        输出为元组，如果为空输出None
        data = (qq , nickname , steamid )
        """
        if qq:
            self.c.execute("SELECT * FROM L4d2_players WHERE qq=?", (qq,))
            result = self.c.fetchone()
            if result:
                return result
        if steamid:
            self.c.execute("SELECT * FROM L4d2_players WHERE steamid=?", (steamid,))
            result = self.c.fetchone()
            if result:
                return result
        if nickname:
            self.c.execute("SELECT * FROM L4d2_players WHERE nickname=?", (nickname,))
            result = self.c.fetchone()
            if result:
                return result
        return None
    
    def _query_all_player(self) -> tuple[tuple]:
        """获取所有玩家信息"""
        self.c.execute("SELECT * FROM L4d2_players")
        return self.c.fetchall()
    