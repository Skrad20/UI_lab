import os
import configparser


class ConfigMeneger:
    """
    Описание

    Параметры:
    ----------
    
    Возвращает:
    -------
    """
    @staticmethod
    def createConfig():
        """
        Create a config file
        """
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
    """
        path = "./func/settings.ini"
        config = configparser.ConfigParser()
        config.add_section("AdressOpen")
        config.set(
            "AdressOpen",
            "adress_open",
            r"C:\Users\Пользователь\Desktop"
        )
        with open(path, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def get_path_save() -> str:
        """
        Read config
        """
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
    """
        path = "./func/settings.ini"
        if not os.path.exists(path):
            ConfigMeneger.createConfig()

        config = configparser.ConfigParser()
        config.read(path)

        adress_open = config.get("AdressOpen", "adress_open")
        return adress_open

    @staticmethod
    def set_path_save(new_path_adress: str) -> None:
        """
        Update config
        """
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
    """
        path = "./func/settings.ini"
        if not os.path.exists(path):
            ConfigMeneger.createConfig()

        config = configparser.ConfigParser()
        config.read(path)
        config.set("AdressOpen", "adress_open", new_path_adress)
        with open(path, "w") as config_file:
            config.write(config_file)


if __name__ == "__main__":
    print(ConfigMeneger.read_config())
