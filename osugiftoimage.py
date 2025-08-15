import sys
import os
from PIL import Image

def gif_to_frames(gif_path, scale_factor=0.5, bg_width=1980, bg_height=1080, x_pos=None, y_pos=None):
    gif_path = os.path.abspath(gif_path)
    gif_name = os.path.splitext(os.path.basename(gif_path))[0]
    output_folder = os.path.join(os.path.dirname(gif_path), f"{gif_name}_frames")

    prefix = "mania-stage-bottom"

    try:
        with Image.open(gif_path) as im:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            frame = 0
            while True:
                im.seek(frame)
                frame_image = im.convert("RGBA")

                new_width = int(frame_image.width * scale_factor)
                new_height = int(frame_image.height * scale_factor)

                if new_width > bg_width:
                    scale_factor = bg_width / frame_image.width
                    new_width = bg_width
                    new_height = int(frame_image.height * scale_factor)

                if new_height > bg_height:
                    scale_factor = bg_height / frame_image.height
                    new_height = bg_height
                    new_width = int(frame_image.width * scale_factor)

                frame_image = frame_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                if x_pos is None or y_pos is None:
                    x_pos = 0
                    y_pos = bg_height - new_height

                x_pos = min(x_pos, bg_width - new_width)
                y_pos = min(y_pos, bg_height - new_height)

                background = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))

                background.paste(frame_image, (x_pos, y_pos), frame_image)

                frame_filename = os.path.join(output_folder, f"{prefix}-{frame}.png")
                background.save(frame_filename, format="PNG")
                print(f"Saved: {frame_filename}")
                frame += 1
    except EOFError:
        print(f"\nFinished with total of {frame} frames.")
        print(f"Saved as: {output_folder}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Drag and drop a GIF file onto this tool or run with command line:")
        print("gif_to_frames.exe <path_to_gif_file>")
        input("\nPress Enter to exit...")
        return

    gif_path = sys.argv[1]

    try:
        bg_width = int(input("Enter the transparent background width (px): "))
        bg_height = int(input("Enter the transparent background height (px): "))
    except ValueError:
        print("Invalid background size, using default 1980x1080.")
        bg_width = 1980
        bg_height = 1080

    try:
        scale_factor = float(input("Enter the scale factor for the GIF (e.g., 0.5 to reduce by 50%):"))
    except ValueError:
        print("Invalid scale factor, using default 0.5.")
        scale_factor = 0.5

    try:
        x_pos = int(input("Enter the X position of the GIF on the background (px, leave empty for default): ") or 0)
        y_pos = int(input("Enter the Y position of the GIF on the background (px, leave empty for default): ") or (bg_height - 1))
    except ValueError:
        print(f"Invalid position input, using default (0, {bg_height - 1}).")
        x_pos = 0
        y_pos = bg_height - 1

    if not os.path.isfile(gif_path):
        print("File does not exist.")
        input("Press Enter to exit...")
        return

    if not gif_path.lower().endswith(".gif"):
        print("This is not a GIF file.")
        input("Press Enter to exit...")
        return

    gif_to_frames(gif_path, scale_factor, bg_width, bg_height, x_pos, y_pos)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
