from app.utils import clear_screen

def show_about() -> None:
    """
    Display information about VidPack Utility.
    """

    clear_screen()

    print()
    print("=" * 60)
    print("VidPack Utility")
    print("=" * 60)
    print()
    print("Version")
    print("-------")
    print("v1.1")
    print()
    print("Developer")
    print("---------")
    print("Erick Xander Estravela")
    print()
    print("Description")
    print("-----------")
    print("A lightweight command-line utility")
    print("for compressing videos using FFmpeg.")
    print()
    print("Features")
    print("--------")
    print("• Single video compression")
    print("• Batch folder compression")
    print("• Compression presets")
    print("• Remember last preset")
    print("• Remember output folder")
    print("• Compression logs")
    print()
    print("Built With")
    print("----------")
    print("• Python")
    print("• FFmpeg")
    print("• FFprobe")
    print()
    print("=" * 60)

    input("\nPress Enter to return...")