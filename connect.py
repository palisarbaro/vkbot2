import pymysql
import vk
import top_secret
from datetime import datetime

class DB:
    def __init__(self):
        self.db = pymysql.connect(host=top_secret.host, user=top_secret.user, passwd=top_secret.passwd,
                                  db=top_secret.db,
                                  charset='utf8')
        self.cursor = self.db.cursor()
    def __del__(self):
        self.db.commit()
        self.db.close()

    def get_current_link_and_date(self,kurs):
        req = f'SELECT * from `last_edit` where `kurs`={str(kurs)} ORDER BY `date` DESC LIMIT 1;';
        req = f'SELECT * from `last_edit` where `kurs`=%s ORDER BY `date` DESC LIMIT 1;'%str(kurs);

        self.cursor.execute(req)
        a = self.cursor.fetchone()
        a = (a[1],a[2]) if a is not None else (None, None)
        return a

    def update_link(self, date, link, kurs):
        """
        True, если ссылка новая
        """
        date = datetime.strptime(date,' %d.%m.%Y %H:%M')
        l_link, l_date = self.get_current_link_and_date(kurs)
        if (l_date is None or l_link is None) or (date > l_date or link != l_link):
            req = 'INSERT INTO `last_edit` (`date`,`link`,`kurs`) VALUES (\'%s\',\'%s\',%d);'%(str(date),str(link),kurs);

            self.cursor.execute(req)
            return True

    def has_user_with_id(self,user_id):
        req = 'SELECT * from `users` where id='+str(user_id)+";";
        self.cursor.execute(req)
        a = self.cursor.fetchone()
        return a is not None


    def get_link_and_date_str(self,kurs):
        link, date = self.get_current_link_and_date(kurs)
        return link+" от "+str(date)


    def check_last_msg(self,user_id,last_msg):
        """
        True, если дата последнего сообщения изменилась, иначе False
        если юзера с таким id нет, то он создается
        обнавляет дату
        """
        if self.has_user_with_id(user_id):
            req = "SELECT * from `users` where `id`=%d  and date_add(`last_msg`,interval 1 second)<'%s';"  % (user_id,last_msg);
            self.cursor.execute(req)
            a = self.cursor.fetchone()
            if a is not None:
                req = "update `users` set `last_msg`='%s' where `id`=%d" % (last_msg, user_id)
                self.cursor.execute(req)
            return a is not None
        else:
            req = "insert into `users` (`id`,`last_msg`) values (%d,'%s')" % (user_id,last_msg)
            self.cursor.execute(req)
            return True

    def push_action(self,user_id,action):
        req = "insert into `actions` (`user_id`,`action`) values (%d, '%s')" % (user_id, action)
        self.cursor.execute(req)

    def pop_action(self):
        req = "select * from `actions`;";
        self.cursor.execute(req)
        result = self.cursor.fetchone()
        if result is None:
            return None,None
        req = "delete from `actions` where `user_id`='%s' and `action`='%s'" % (result[0],result[1])
        self.cursor.execute(req)
        return result



if __name__ == '__main__':
    db = DB()
    #db.update_link(" 01.09.2039 12:00","htttp://ssss",3)
    print(db.get_current_link_and_date(3))