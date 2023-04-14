import colorama
import datetime

colorama.init(autoreset=True)

class Logger:

    DEFAULT_CONFIG = {"print_logs":True,"write_logs":True,"print_logs_from_level":2,"write_logs_from_level":0}

    INTERNAL = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
    HIGH = 10

    _LEVEL_COLORS = {0:colorama.Fore.LIGHTCYAN_EX,1:colorama.Fore.LIGHTBLUE_EX,2:colorama.Fore.WHITE,3:colorama.Fore.LIGHTYELLOW_EX,4:colorama.Fore.LIGHTRED_EX,5:colorama.Back.LIGHTRED_EX+colorama.Fore.BLACK, 10:colorama.Back.LIGHTWHITE_EX+colorama.Fore.BLACK}
    LEVELS = {0:"INTERNAL",1:"DEBUG",2:"INFO",3:"WARNING",4:"ERROR",5:"CRITICAL",10:"HIGH"}

    def __init__(self,output_file=None,config={}):

        self.config = {**self.DEFAULT_CONFIG,**vars(config)}

        self.output_file = output_file

        self.closed = False

        self.print_all = False

        if self.output_file and self.config["write_logs"]:

            self._file = open(self.output_file,"a")

        self.log("Logger started.",self.INTERNAL)

    def log(self,message,level=INFO):

        if self.closed:

            raise LoggerClosedError("Can't log with a closed logger.")

        full_log = f"# {datetime.datetime.now().strftime('%c')} # [{self.LEVELS[level]}] {message}"

        if self.output_file and self.config["write_logs"] and level >= self.config["write_logs_from_level"]:

            self._file.write(full_log+"\n")
            self._file.flush()

        if self.config["print_logs"] and (level >= self.config["print_logs_from_level"] or self.print_all):

            print(self._LEVEL_COLORS[level]+full_log+"\n", end="")

    def close(self):

        self.log("Logger closed.",self.INTERNAL)
        self._file.close()
        self.closed = True

class LoggerClosedError(Exception):

    pass