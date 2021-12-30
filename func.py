import psycopg2

Host = '127.0.0.1'
User = 'postgres'
Password = 'As720aS1'
db_name = 'momo'

def check_animal_type(animal_type):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(
            f'''
                select * from animal_type;
                '''
        )
        animal_types = cursor.fetchall()

        print(animal_types)

        for i in animal_types:
            if str(i[0]) == str(animal_type):
               return True
        else:
            return False

print(check_animal_type(str(1)))

def check_corral(num):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )

    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(
            f'''
            select * from corral;
            '''
        )
        animal_types = cursor.fetchall()
    for i in animal_types:
        if str(i[0]) == str(num):
            print('Такой загон есть')
            return True
    else:
        return False

def which_animal_type():
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(
                'select * from animal_type;'
            )
            return cur.fetchall()
    except Exception as ex:
        print(ex)


def which_corral():
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(
                'select * from corral;'
            )
            return cur.fetchall()
    except Exception as ex:
        print(ex)


def error_animal_type(text, bot, message):
    if not(which_animal_type()):
        bot.send_message(
            message.chat.id, 'Ошибка\nВы не добавили ни одного вида животных\nСначала добавте вид животных')
    else:
        already_are = 'Ошибка\nВида животного с таким номером не существует\nСуществующие:\n'
        for i in which_animal_type():
            already_are += str(i[0]) + ' ' + i[1] + '\n----------------------------\n'
        already_are += 'Добавте вид животных, если его нет в списке\n\nОтправьте сообщение для продолжения'
        bot.send_message(message.chat.id, already_are)
        print('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')


def error_corral(text, bot, message):
    if not(which_animal_type()):
        bot.send_message(
            message.chat.id, 'Ошибка\nВы не добавили ни одного загона\nСначала добавте загон')
    else:
        already_are = 'Ошибка\nЗагона с таким номером не существует\nСуществующие:\n'
        for i in which_corral():
            already_are += str(i[0]) + ' ' + str(i[1]) + '\n----------------------------\n'
        already_are += 'Добавте загон, если его нет в списке\n\nОтправьте сообщение для продолжения'
        bot.send_message(message.chat.id, already_are)
        print('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')


def DROP(bot, message):
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )

        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                f'''
                    alter table animal drop column corral;
                    alter table stall drop column corral_num;
                    alter table corral drop column animal_type;
                    alter table animal drop column animal_type;
                    drop table stall;
                    drop table animal_type;
                    drop table animal;
                    drop table corral;

                    create table animal_type(
                    animal_type_num serial primary key,
                    animal_type varchar(50));

                    create table animal(
                    animal_num serial primary key,
                    name varchar(50),
                    sex varchar(50),
                    age int);

                    alter table animal add animal_type int references animal_type(animal_type_num);

                    create table corral(
                    id serial primary key,
                    animal_type int references animal_type(animal_type_num));

                    create table stall(
                    id serial primary key,
                    corral_num int references corral(id),
                    animal_num int references animal(animal_num));

                    alter table animal add corral int references corral(id);
                    '''
            )

    except Exception as _ex:
        print(_ex)
    finally:
        if conn:
            conn.close()
            print('Connection closed')
    bot.send_message(
        message.chat.id, 'Нееееееет, а в прочем неважно. Отправте что-нибудь', reply_markup=None)


def create_corral(animal_type, message, bot):
    print(animal_type)
    conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )
    conn.autocommit = True
    if check_animal_type(animal_type):
        with conn.cursor() as cursor:
            cursor.execute(
                f'''
    INSERT INTO corral(animal_type)
    VALUES ({animal_type});
                '''
            )
        bot.send_message(
            message.chat.id, 'Загон успешно добавлен, отправьте что-нибудь для продолжения')
    else:
        already_are = 'Ошибка\nТакого вида нет\nСписок видов животных:\n'
        with conn.cursor() as cur:
            cur.execute('select * from corral;')
            for i in cur.fetchall():
                for j in i:
                    already_are+=str(j) + ' ';
                already_are += '\n'
        already_are+='\nOтпрaвте что-нибудь'
        bot.send_message(message.chat.id, already_are)


def create_animal(animal, message, bot):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    with conn.cursor() as cursor:
        cursor.execute(
            f'''
INSERT INTO animal(name, sex, age, animal_type, corral)
VALUES ('{animal['name']}', '{animal['sex']}', {animal['age']}, {animal['animal_type']}, {animal['corral']});
            '''
        )
    bot.send_message(
        message.chat.id, 'Животное успешно добавлено, отправьте что-нибудь для продолжения')


def create_stall(stall, message, bot):
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )

        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                f'''
    INSERT INTO stall(corral_num, animal_num)
    VALUES ({int(stall['corral'])}, {int(stall['animal'])});
                '''
            )
        bot.send_message(
            message.chat.id, 'Стойло успешно добавлено, отправьте что-нибудь для продолжения')

    except Exception as ex:
        bot.send_message(message.chat.id, str(
            ex)+'\n отправьте сообщение для продолжения')
    finally:
        if conn:
            conn.close()
            print('Connection closed')


def create_animal_type(a, message, bot):
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )

        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                f'''
    INSERT INTO animal_type(animal_type)
    VALUES ('{a}');
                '''
            )
            bot.send_message(
                message.chat.id, 'Вид успешно добавлен, отправьте что-нибудь для продолжения')

    except Exception as _ex:
        print(_ex)
    finally:
        if conn:
            conn.close()
            print('Connection closed')





def check_animal(num):
    try:
        conn = psycopg2.connect(
            host=Host,
            user=User,
            password=Password,
            database=db_name
        )

        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(
                f'''
                select * from animal;
                '''
            )
            animal_types = cursor.fetchall()
            print(animal_types)
        for i in animal_types:
            if int(i[0]) == num:
                return True
        else:
            return False

    except Exception as ex:
        pass
    finally:
        if conn:
            conn.close()
            print('Connection closed')





def error_corral(message, bot):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('select * from animal_type;')
        corral_kort = cur.fetchall()
        corral = []
        for i in corral_kort:
            corral.append([i[0], i[1]])
        cur.execute('select * from corral')
        mem = cur.fetchall()
        for i in mem:
            for j in corral:
                if i[0] == j[1]:
                    j[1] = i[1]
        already_are = 'Ошибка\nЗагона с таким номером не существует\nСуществующие:\n'
        for i in corral:
            already_are += str(i[0]) + ' ' + i[1] + '\n----------------------------\n'
        already_are += 'Добавте загон, если его нет в списке\nОтправьте сообщение для продолжения'
    bot.send_message(message.chat.id, already_are)


def error_animal(message, bot):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('select * from animal;')
        corral_kort = cur.fetchall()
        corral = []
        for i in corral_kort:
            corral.append([j for j in i])
        already_are = 'Ошибка\nЖивотного с таким номером не существует\nСуществующие:\n'
        for i in corral:
            for j in i:
                already_are += str(j) + ' '
            already_are += '\n----------------------------\n'
        already_are += 'Добавте животное, если его нет в списке\nОтправьте сообщение для продолжения'
    bot.send_message(message.chat.id, already_are)


def get_animals(bot, message):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    already_are = 'Список животных:\n----------------------------\n'
    with conn.cursor() as cur:
        cur.execute('select * from animal;')
        for i in cur.fetchall():
            for j in i:
                already_are+=str(j) + ' ';
            already_are += '\n----------------------------\n'
    
    if already_are == 'Список животных:\n':
        bot.send_message(message.chat.id, 'Их нет\n\nОтправте что-нибудь')
    else:
        bot.send_message(message.chat.id, already_are+'Отправте что-нибудь')
        
def get_corrals(bot, message):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    already_are = 'Список загонов:\n----------------------------\n'
    with conn.cursor() as cur:
        cur.execute('select * from corral;')
        for i in cur.fetchall():
            for j in i:
                already_are+=str(j) + ' ';
            already_are += '\n----------------------------\n'
    
    if already_are == 'Список загонов:':
        bot.send_message(message.chat.id, 'Их нет\nОтправте что-нибудь')
    else:
        bot.send_message(message.chat.id, already_are+'\nОтправте что-нибудь')
    
def get_stalls(bot, message):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    already_are = 'Список стойл:\n----------------------------\n'
    with conn.cursor() as cur:
        cur.execute('select * from stall;')
        for i in cur.fetchall():
            for j in i:
                already_are+=str(j) + ' ';
            already_are += '\n----------------------------\n'
    
    if already_are == 'Список стойл:\n':
        bot.send_message(message.chat.id, 'Их нет\n\nОтправте что-нибудь')
    else:
        bot.send_message(message.chat.id, already_are+'\nОтправте что-нибудь')

def get_animal_types(bot, message):
    conn = psycopg2.connect(
        host=Host,
        user=User,
        password=Password,
        database=db_name
    )
    conn.autocommit = True
    already_are = 'Список видов животных:\n----------------------------\n'
    with conn.cursor() as cur:
        cur.execute('select * from animal_type;')
        for i in cur.fetchall():
            for j in i:
                already_are+=str(j) + ' ';
            already_are += '\n----------------------------\n'
    
    if already_are == 'Список видов животных:\n':
        bot.send_message(message.chat.id, 'Их нет\n\nОтправте что-нибудь')
        print(already_are)
    else:
        bot.send_message(message.chat.id, already_are+'\n\nОтправте что-нибудь')

