import os

from app.compressor import (
    confirm_video,
    display_video_info,
    get_video_path,
    select_compression_preset,
)


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
            video = get_video_path()

            if video:
                display_video_info(video)

                if confirm_video():
                    preset = select_compression_preset()
                
                if preset:
                    print(f"\nSelected preset: {preset.title()}\n")
                else:
                    print("\nCompression cancelled.\n")
            else:
                    print("\nCompression cancelled.\n")

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