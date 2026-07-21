import os
from app.compressor import get_video_path

def show_menu():
    while True:
        print("─" * 60)
        print("[1] Compress a Video")
        print("[2] Batch Compress Folder")
        print("[3] Settings")
        print("[4] View Logs")
        print("[5] About")
        print()
        print("[0] Exit")
        print("─" * 60)

        choice = input("Select an option: ").strip()

        if choice == "0":
            print("\nThank you for using VCompress!\n")
            break

        elif choice == "1":
            print()
            get_video_path()
            print()

        elif choice == "2":
            print("\nBatch Compression is coming soon!\n")

        elif choice == "3":
            print("\nSettings are coming soon!\n")

        elif choice == "4":
            print("\nLogs are coming soon!\n")

        elif choice == "5":
            print("\nVCompress")
            print("Fast • Clean • Powerful")
            print("Created by Shin & ChatGPT\n")

        else:
            print("\nInvalid option.\n")

        input("Press Enter to continue...")
        os.system("cls")