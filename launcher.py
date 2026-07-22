from app.version import VERSION
from app.menu import show_menu


def show_banner() -> None:
    """Display the application banner."""

    print(
        rf"""
 __     ______ ___  __  __ ____  ____  _____ ____ ____  
 \ \   / / ___/ _ \|  \/  |  _ \|  _ \| ____/ ___/ ___| 
  \ \ / / |  | | | | |\/| | |_) | |_) |  _| \___ \___ \ 
   \ V /| |__| |_| | |  | |  __/|  _ <| |___ ___) |__) |
    \_/  \____\___/|_|  |_|_|   |_| \_\_____|____/____/

                Fast • Clean • Powerful
                     Version {VERSION}
"""
    )


def main() -> None:
    """Application entry point."""

    show_menu(show_banner)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted.")
        print("Thank you for using VidPack Utility!")
    except Exception as error:
        print("\nAn unexpected error occurred.")
        print(f"Error: {error}")
        input("\nPress Enter to exit...")