from app.version import VERSION
from app.menu import show_menu


def show_banner():
    print(r"""
 __     ______ ___  __  __ ____  ____  _____ ____ ____  
 \ \   / / ___/ _ \|  \/  |  _ \|  _ \| ____/ ___/ ___| 
  \ \ / / |  | | | | |\/| | |_) | |_) |  _| \___ \___ \ 
   \ V /| |__| |_| | |  | |  __/|  _ <| |___ ___) |__) |
    \_/  \____\___/|_|  |_|_|   |_| \_\_____|____/____/ 
                                                                                      

            Fast • Clean • Powerful
                 Version {}
""".format(VERSION))


def main():
    show_banner()
    show_menu()


if __name__ == "__main__":
    main()