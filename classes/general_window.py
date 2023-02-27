from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QLabel, QMainWindow, QMessageBox,
                             QSplashScreen, QTableWidget)
from .windows_classes import (
    SecondWindow, Window_main, WindowAbout,
    WindowAddFatter, WindowGenPassWord, WindowISSR,
    WindowMSAusWord, WindowSearchFarher, WindowTest
)

from func.func_answer_error import answer_error
from func.update_database_father import donwload_data, update_db
from setting import IS_TEST as is_test

adres_job = ''
data_job = ''
adres_job_search_father = ''
stop_thread = False


class GeneralWindow(QMainWindow):
    """Управляет окнами программы."""
    def __init__(self) -> None:
        super(GeneralWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        self.setObjectName('General_window')
        self.file_adres = ''
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def flashSplash(self):
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.splash = QSplashScreen(QPixmap('./data/error.png'))
        self.splash.show()
        QTimer.singleShot(2000, self.splash.close)

    def initUI(self):
        """Конструктор геометрии."""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(r'data\icon.jpg'))
        self.show()

    def show_window_biotech(self) -> None:
        """Отрисовывает окно биотеха."""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.window = Window_main('Biotech Lab')
        self.window.setObjectName('Biotech_window')
        text = (
            'Добро пожаловать!\n Здесь Вы найдёте методы,' +
            ' которые помогут Вам в анализе данных, получаемых в лаборатории.'
        )
        self.window.label_creat(text)
        self.window.button_creat(
            self.show_window_MS,
            'Микросателлитный анализ',
            text='Методы для микросателлитного анализа',
        )
        self.window.button_creat(
            self.show_window_ISSR,
            'Анализ ISSR',
            text='Методы для ISSR анализа',
        )
        self.window.button_creat(
            self.updata_basedata,
            'Обновление базы данных',
            text='Скачать обновления по быкам',
        )
        self.window.button_creat(self.show_about_programm, 'О программе')
        if is_test:
            self.window.button_creat(self.show_window_tests, 'Тест')
        self.window.show()

    def updata_basedata(self) -> None:
        """Добавляет данные по МС быков в базу данных"""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        path = donwload_data()
        update_db(path)
        QMessageBox.information(
            self,
            'Обновление',
            'База данных обновлена'
        )

    def show_window_MS(self) -> None:
        """Отрисовывает окно анализа микросателлитов."""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = Window_main('Biotech Lab: Microsatellite analysis')
            self.window.button_creat(
                self.show_window_MS_serch_father,
                'Подбор отца',
                text='Здесь можно подбрать отца для КРС',
            )
            self.window.button_creat(
                self.show_creat_pass_doc_gen,
                'Собрать генетические паспорта',
                text='Здесь можно собрать генетические паспорта по описи.',
            )
            self.window.button_creat(
                self.show_window_MS_aus_word,
                'Собрать данные из паспортов',
                text='Здесь можно собрать данные из генетических паспорта.',
            )
            self.window.button_creat(
                self.add_vater,
                'Добавить отца в базу',
                text='Здесь можно добавить отцов в базу быков.',
            )
            self.window.button_creat(
                self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def add_vater(self):
        '''Добавление отца в базу по быкам.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowAddFatter(
                'Biotech Lab: Microsatellite analysis. Add father'
            )
            self.window.button_creat(
                self.window.data_result_in,
                'Внести данные отца',
                text='Добавление микросателлитного профиля отца в базу быков.',
            )
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def show_window_MS_aus_word(self) -> None:
        '''Отрисовывает окно отбора данных из  Word.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowMSAusWord(
                'Biotech Lab: Microsatellite analysis. Aus word'
            )
            text_1 = (
                'Здесь можно выбрать данные ' +
                'из готовых генетических паспортов'
            )
            self.window.label_creat(text_1)
            text_2 = (
                'Порядок действий: \n1) Данные из WORD ' +
                'нужно скопировать в EXCEL' +
                '\n2) Из EXCEl скопировать в блокнот и сохранить' +
                '\n3) Выбрать файл в программе и наслаждаться'
            )
            self.window.label_creat(text_2)
            global adres_job
            adres_job = r'func\data\ms_word\result_ms_word.csv'
            self.window.button_creat(
                self.window.res_ms_aus_word_in_csv,
                'Выбрать файл с данными',
                text='Добавление микросателлитного профиля отца в базу быков.',
            )
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def show_window_MS_serch_father(self) -> None:
        '''Отрисовывает окно поиска отцов.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowSearchFarher(
                'Biotech Lab: Microsatellite analysis. Search father'
            )
            global adres_job
            adres_job = r'func\data\search_fatherh\bus_search.csv'
            self.window.button_creat(
                self.window.res_search_cow_father,
                'Выбрать файл с данными о потомке',
                text=(
                    'Выберите файл, в который ' +
                    'записан микросателлитный профиль потомка.'
                ),
            )
            self.window.button_creat(
                self.window.data_result_in,
                'Внести данные в таблицу',
                text='Введите данные микросателлитного профиля потомка.',
            )
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def show_creat_pass_doc_gen(self) -> None:
        '''Отрисовывает окно генерации паспортов.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowGenPassWord(
                'Biotech Lab: Microsatellite analysis. Generation password'
            )
            self.window.setObjectName('WindowGenPassWord')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def show_about_programm(self):
        '''Отрисовывает окно о программе.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowAbout('Biotech Lab: about programm')
            self.window.setObjectName('WindowAbout')
            text_1 = (
                'Версия 1.0.1\n\nТехнологии: Python 3.7.0, Qt, ' +
                'Pandas, \nNumpy, Peewee, GitHub\n' +
                '\nГод разработки: 2021'
            )
            pixmap = QPixmap('data/nii.png')
            self.window.label = QLabel(self)
            self.window.label.setObjectName('JpgNii')
            self.window.label.setPixmap(pixmap)
            self.window.label.resize(pixmap.width(), pixmap.height())
            self.window.label.setAlignment(Qt.AlignCenter)
            self.window.resize(pixmap.width(), pixmap.height())
            self.window.vb.addWidget(self.window.label)
            self.window.label_creat(text_1)
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def show_window_ISSR(self) -> None:
        '''Отрисовывает окно ISSR.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        try:
            self.window = WindowISSR('Biotech Lab: ISSR analysis')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def open_file(self) -> None:
        """Сохраняет путь к файлу"""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.file_adres = QFileDialog.getOpenFileName(
            self,
            'Open File',
            './',
            'Text Files (*.txt);; CSV (*.csv'
        )[0]

    def show_window_tests(self):
        """Окно для тестирования новых функций"""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        QMessageBox.critical(
            self,
            'Что-то пошло не так',
            f'{answer_error()} Подробности:\n'
        )
        try:
            self.window = WindowTest('Biothech Lab: testing')
            text_1 = 'Здесь можно ничего не делать'
            self.window.label_creat(text_1)
            self.window.setStyleSheet(
                'QWidget {background-color: blue;}' +
                ' QPushButton {background-color: green}'
            )
            self.window.button_creat(self.open_second_window, 'Интрига')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()

        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка',
                f'{answer_error()} Подробности:\n {e}'
            )

    def __repr__(self) -> str:
        return f'Запуск успешен. Переменные среды: {self.file_adres}'

    def open_second_window(self):
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.window = SecondWindow(self)
        self.window.show()
