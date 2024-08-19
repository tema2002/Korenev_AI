#%%
#Урок 1. Привет, Андрей
#%%
#код вне функции
#user_name = 'Андрей'
#message = f'Привет, {user_name}!'
#%%
print(message)
#%%
#функция
def greet(name):
    message = f'Привет, {name}!'
    return message

user_name = 'Андрей'
message = greet(user_name)
print(message)
#%%
#функция
def greet(name,simple_text):
    message = f'Привет, {name} {simple_text}!'
    return message

user_name = 'Андрей'
simple_text = 'Как ваши дела?'
message = greet(user_name,simple_text)
print(message)
#%%
#значение по умолчанию и документация функции
def greet(name="Гость"):
    '''
    Приветствует пользователя по имени.
    '''
    message = f'Привет, {name}!'
    return message
message = greet()
print(message)
#%%
#код с ошибкой
#режим отладки
def greet(name):
    message = 'Привет ' + name.upper
    return message

user_name = 'Андрей'

message = greet(user_name)
print(message)


# %%
#извлекаем код с ошибкой из функции
user_name = 'Андрей'
message = 'Привет' + user_name.upper
print(message)

# %%
