import imageio


def extract_frame(gif_path, save_path, frame_num):
    gif = list(imageio.get_reader(gif_path))
    im = gif[frame_num]



if __name__ == "__main__":
    gif_path = "artifacts/run"
    extract_frame(gif_path, save_path, frame_num)