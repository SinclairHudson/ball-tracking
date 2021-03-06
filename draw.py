import yaml
import argparse
import skvideo.io
from torchvision.io import read_video, write_video
from effects import *
from tqdm import tqdm
from filters import *

def draw(video, tracks, effect):
    for track in tqdm(tracks):
        effect(video, track)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tracks objects using detections as input.")
    parser.add_argument("name", help="name of the project to be tracked.")
    args = parser.parse_args()
    name = args.name
    vid_generator = skvideo.io.vreader(f"io/{name}.mp4")
    vid_writer = skvideo.io.FFmpegWriter(f"io/{name}_out.mp4")

    print("reading yaml")
    with open(f"internal/{name}.yaml", 'r') as f:
        track_dictionary = yaml.safe_load(f)

    effect = RedDot()
    tracks = track_dictionary["tracks"]
    tracks = [track for track in tracks if standard_filter(track, min_age=2)]

    for i, frame in tqdm(enumerate(vid_generator)):
        relevant_tracks = [track for track in tracks if effect.relevant(track, i)]
        out_frame = frame

        # loop through all tracks, draw each on the frame
        for track in relevant_tracks:
            out_frame = effect.draw(out_frame, track, i)

        vid_writer.writeFrame(out_frame)

    vid_writer.close()

