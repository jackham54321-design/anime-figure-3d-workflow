"""Read-only technical validation of the 50-second showcase video."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--ffprobe', default='ffprobe')
    args = parser.parse_args()
    probe = json.loads(subprocess.check_output([args.ffprobe, '-v', 'error', '-count_frames',
                       '-show_streams', '-show_format', '-of', 'json', str(args.video)]))
    assert len(probe['streams']) == 1, 'Expected one video stream and no audio'
    stream = probe['streams'][0]
    assert (stream['codec_name'], stream['pix_fmt']) == ('h264', 'yuv420p')
    assert (stream['width'], stream['height']) == (1080, 1080)
    assert stream['avg_frame_rate'] == '30/1' and int(stream['nb_read_frames']) == 1500
    assert abs(float(probe['format']['duration']) - 50) < .001
    assert all(stream[k] == 'bt709' for k in ('color_space', 'color_transfer', 'color_primaries'))
    assert stream['color_range'] == 'tv'
    with args.video.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    boxes = []
    with args.video.open('rb') as handle:
        while handle.tell() < args.video.stat().st_size:
            start = handle.tell()
            size, kind = struct.unpack('!I4s', handle.read(8))
            if size == 1:
                size = struct.unpack('!Q', handle.read(8))[0]
            if size == 0:
                size = args.video.stat().st_size - start
            assert size >= 8 and start + size <= args.video.stat().st_size
            boxes.append(kind)
            handle.seek(start + size)
    assert boxes.index(b'moov') < boxes.index(b'mdat')
    frames = json.loads(subprocess.check_output([args.ffprobe, '-v', 'error', '-select_streams', 'v:0',
                       '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(args.video)]))['frames']
    pts = [float(frame['best_effort_timestamp_time']) for frame in frames]
    assert len(pts) == 1500 and all(abs(b - a - 1 / 30) < 1e-6 for a, b in zip(pts, pts[1:]))
    subprocess.run([args.ffmpeg, '-v', 'error', '-xerror', '-i', str(args.video),
                    '-map', '0:v:0', '-f', 'null', '-'], check=True)
    print(json.dumps({'status': 'PASS', 'sha256': digest, 'bytes': args.video.stat().st_size,
                      'frames': 1500, 'seconds': 50, 'fps': 30, 'width': 1080, 'height': 1080,
                      'full_decode': True, 'faststart': True, 'bt709_limited': True,
                      'artistic_review': 'not performed by this technical tool'}, indent=2))


if __name__ == '__main__':
    main()
