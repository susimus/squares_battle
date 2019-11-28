# SQUARES BATTLE

Squares fight each other for the win!

#### Версия

4

#### Автор 

Семен Вяцков

#### ОПИСАНИЕ

   Данное приложение реализует комьютерную игру, основанную духовно на игре 
"teeworlds". Реализуемая игра является с видом сбоку платформером, где друг 
другу противостоят квадраты

#### ТРЕБОВАНИЯ

- Python 3.7.4+
- Windows 10

#### СОСТАВ
        
- **engine**
    
    - **\_\_init\_\_.py**
        
    - **collisions_processor.py** 
    
        Реализует модель коллизий игрового движка
        
    - **engine.py** 
    
        Главный кодовый файл модуля, реализующий ядро работы игрового движка
        
    - **game_object.py** 
    
        Содержит абстракции игровых объектов

- **user_interface**

    - **game_ui.py**

        Реализация графического интерфейса игрового процесса

    - **launcher_ui.py**
 
        Интерфейс лаунчера

- **maps**

    Папка для всего, что относиться к игровым картам
    
    - **\_\_init\_\_.py**

        Содержит несколько игровых карт в виде программного кода 
    
    - **map_editor.py** 
    
        Редактор карт
    
- **tests**
        
    - **test_collisions_processor.py**
    
    - **test_engine.py**  

- **launcher.py**

#### ГРАФИЧЕСКАЯ ВЕРСИЯ

Справка по запуску: launcher.py --help

Пример запуска: launcher.py

#### УПРАВЛЕНИЕ

- **A/D** - движение влево/вправо
- **Space** - прыжок 
- **1**\**2** - переключение оружия


#### Доступные карты

В виде кода:

* raw 1

    One player only
    
* raw 2

    Player with three platforms

* raw 3

    Player with two buffs

* raw 4

    Player with handgun and machine gun projectiles

 
#### ПОДРОБНОСТИ РЕАЛИЗАЦИИ

Вся логика в папке 'engine' имеет покрытие тестами не менее 80% ('engine.py'
пока что без тестов из-за проблемы с импортирование tkinter'a)

```
Name                             Stmts   Miss  Cover
----------------------------------------------------
engine\__init__.py                   2      0   100%
engine\collisions_processor.py     104     17    84%
engine\engine.py                   183    183     0%
engine\game_objects.py              63     12    81%
----------------------------------------------------
TOTAL                              352    212    40%                                                                  
```