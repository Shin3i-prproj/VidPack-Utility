import os

from app.compressor import (
    build_ffmpeg_command,
    display_compression_results,
    confirm_video,
    display_video_info,
    get_folder_path,
    get_video_path,
    get_videos_from_folder,
    display_found_videos,
    run_compression,
    select_compression_preset,
    select_output_folder,
    confirm_batch,
    compress_video_batch,
)

from app.config import show_settings_menu


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
                video_info = display_video_info(video)

                if confirm_video():
                    preset = select_compression_preset()

                    if preset:
                        print()
                        print("Compression Settings")
                        print("--------------------")
                        print(f"Preset : {preset['name']}")
                        print(f"CRF    : {preset['crf']}")
                        print(f"Speed  : {preset['speed']}")
                        print()

                        output_folder = select_output_folder()

                        command, output_path = build_ffmpeg_command(
                            video,
                            preset,
                            output_folder,
                        )

                        print("FFmpeg Command")
                        print("--------------")
                        print(" ".join(command))
                        print()
                        print(f"Output file: {output_path}")
                        print()

                        duration = float(video_info["format"]["duration"])

                        compression_successful = run_compression(
                            command,
                            duration,
                        )

                        if compression_successful:
                            print()
                            print("Compression completed successfully.")
                            print(f"Saved to: {output_path}")

                            display_compression_results(
                                video,
                                output_path,
                                preset,
                            )

                            print()
                        else:
                            print()
                            print("Compression was not completed.")
                            print()
                    else:
                        print("\nCompression cancelled.\n")
                else:
                    print("\nCompression cancelled.\n")

            print()

        elif choice == "2":
            folder = get_folder_path()

            if folder:
                videos = get_videos_from_folder(folder)

                display_found_videos(videos)

                if videos and confirm_batch():
                    preset = select_compression_preset()

                    if preset:
                        compress_video_batch(
                            videos,
                            preset,
                        )

        elif choice == "3":
            show_settings_menu()

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