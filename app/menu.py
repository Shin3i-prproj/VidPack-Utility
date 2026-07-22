from app.about import show_about
from app.compressor import (
    compress_video,
    compress_video_batch,
    confirm_batch,
    confirm_video,
    display_found_videos,
    display_video_info,
    get_folder_path,
    get_video_path,
    get_videos_from_folder,
    select_compression_preset,
)
from app.config import show_settings_menu
from app.logs import view_logs
from app.utils import clear_screen


def show_menu(show_banner) -> None:
    """Display and manage the main application menu."""

    while True:
        clear_screen()
        show_banner()

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
            print("\nThank you for using VidPack Utility!\n")
            break

        elif choice == "1":
            print()

            video = get_video_path()

            if not video:
                input("\nPress Enter to return to the main menu...")
                continue

            display_video_info(video)

            if not confirm_video():
                print("\nCompression cancelled.\n")
                input("Press Enter to return to the main menu...")
                continue

            preset = select_compression_preset()

            if not preset:
                print("\nCompression cancelled.\n")
                input("Press Enter to return to the main menu...")
                continue

            compress_video(
                video,
                preset,
            )

            input("\nPress Enter to return to the main menu...")

        elif choice == "2":
            print()

            folder = get_folder_path()

            if not folder:
                input("\nPress Enter to return to the main menu...")
                continue

            videos = get_videos_from_folder(folder)
            display_found_videos(videos)

            if not videos:
                input("\nPress Enter to return to the main menu...")
                continue

            if not confirm_batch():
                print("\nBatch compression cancelled.\n")
                input("\nPress Enter to return to the main menu...")
                continue

            preset = select_compression_preset()

            if not preset:
                print("\nBatch compression cancelled.\n")
                input("Press Enter to return to the main menu...")
                continue

            compress_video_batch(
                videos,
                preset,
            )

            input("\nPress Enter to return to the main menu...")

        elif choice == "3":
            show_settings_menu()

        elif choice == "4":
            view_logs()

        elif choice == "5":
            show_about()

        else:
            print("\nInvalid option.")
            input("\nPress Enter to return to the main menu...")