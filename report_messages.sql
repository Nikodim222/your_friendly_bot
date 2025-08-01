-- файл для СУБД SQLite 3
.mode box

select -- вывод сообщений Telegram от пользователей
  u.user_id,
  u.first_name, u.last_name,
  substr(m.msg, 1, 10) as msg, m.date_create
  from telegram_users u
    inner join user_messages m
      using (user_id)
  order by m.user_id asc, m.date_create desc
  limit 100;
