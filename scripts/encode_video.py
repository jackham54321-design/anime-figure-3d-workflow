"""Encode an existing 1500-frame RGB8 PNG sequence; no rendering or network."""
import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ffmpeg', default='ffmpeg')
    args = parser.parse_args()
    assert sorted(p.name for p in args.frames.glob('*.png')) == [f'{i:04d}.png' for i in range(1, 1501)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.stem + '.partial.mp4')
    assert not args.output.exists() and not temporary.exists(), 'Never overwrite a finished or uncertain output'
    conversion = ('scale=in_range=pc:out_range=pc:out_color_matrix=bt709,format=yuv444p12le,'
                  'colorspace=ispace=bt709:iprimaries=bt709:itrc=iec61966-2-1:irange=pc:'
                  'space=bt709:primaries=bt709:trc=bt709:range=tv,format=yuv420p')
    subprocess.run([args.ffmpeg, '-hide_banner', '-v', 'error', '-n', '-framerate', '30',
                    '-start_number', '1', '-i', str(args.frames / '%04d.png'), '-frames:v', '1500',
                    '-vf', conversion, '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                    '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                    '-colorspace', 'bt709', '-color_range', 'tv', '-movflags', '+faststart',
                    '-an', str(temporary)], check=True)
    assert not args.output.exists()
    temporary.rename(args.output)
    print(args.output.name)


if __name__ == '__main__':
    main()
