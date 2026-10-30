"""Render a licensed local showcase scene without saving or editing its assets.

Blender Python; tested inspection on Blender 5.2.3 LTS/macOS.
No network operations. The --inspect-only path does not render.
"""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import time
import zlib

import bpy
import numpy as np


def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def asset_fingerprint():
    digest = hashlib.sha256()
    for obj in sorted(bpy.data.objects, key=lambda item: item.name):
        if obj.type != 'MESH':
            continue
        mesh = obj.data
        digest.update(np.asarray(obj.matrix_world, np.float64).tobytes())
        for sequence, attr, count, dtype in [
            (mesh.vertices, 'co', 3, np.float32),
            (mesh.loops, 'vertex_index', 1, np.int32),
            (mesh.polygons, 'loop_total', 1, np.int32),
            (mesh.polygons, 'material_index', 1, np.int32),
        ]:
            data = np.empty(len(sequence) * count, dtype)
            sequence.foreach_get(attr, data)
            digest.update(data.tobytes())
        for uv in mesh.uv_layers:
            data = np.empty(len(uv.data) * 2, np.float32)
            uv.data.foreach_get('uv', data)
            digest.update(data.tobytes())
        normals = mesh.attributes.get('custom_normal')
        if normals is not None:
            data = np.empty(len(normals.data) * 2, np.int32)
            normals.data.foreach_get('value', data)
            digest.update(data.tobytes())
    for image in sorted(bpy.data.images, key=lambda item: item.name):
        for packed in image.packed_files:
            digest.update(packed.packed_file.data)
    for material in sorted(bpy.data.materials, key=lambda item: item.name):
        if not material.use_nodes:
            continue
        values = []
        for node in material.node_tree.nodes:
            inputs = []
            for socket in node.inputs:
                if hasattr(socket, 'default_value'):
                    value = socket.default_value
                    try:
                        value = list(value)
                    except TypeError:
                        pass
                    inputs.append([socket.identifier, value])
            values.append([node.name, node.bl_idname, inputs,
                           getattr(getattr(node, 'image', None), 'name', None)])
        links = [[link.from_node.name, link.from_socket.identifier,
                  link.to_node.name, link.to_socket.identifier]
                 for link in material.node_tree.links]
        digest.update(json.dumps([values, links], sort_keys=True).encode())
    return digest.hexdigest()


def png_valid(path):
    if not path.is_file():
        return False
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != b'\x89PNG\r\n\x1a\n':
        return False
    if struct.unpack('!II', data[16:24]) != (1080, 1080) or data[24] != 8:
        return False
    pos = 8
    while pos + 12 <= len(data):
        size = struct.unpack('!I', data[pos:pos + 4])[0]
        end = pos + size + 12
        if end > len(data):
            return False
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + size]
        checksum = struct.unpack('!I', data[pos + 8 + size:end])[0]
        if zlib.crc32(kind + body) & 0xffffffff != checksum:
            return False
        if kind == b'IEND':
            return end == len(data)
        pos = end
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--inspect-only', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    source = args.scene.resolve()
    source_hash = sha(source)
    bpy.ops.wm.open_mainfile(filepath=str(source), use_scripts=False)
    scene = bpy.context.scene
    assert scene.camera is not None
    assert (scene.frame_start, scene.frame_end) == (1, 1500)
    assert (scene.render.resolution_x, scene.render.resolution_y,
            scene.render.resolution_percentage) == (1080, 1080, 100)
    assert scene.render.fps == 30 and scene.render.fps_base == 1
    assert scene.render.engine == 'BLENDER_EEVEE'
    assert not scene.camera.data.dof.use_dof and not scene.render.use_motion_blur
    assert not bpy.data.libraries, 'Linked libraries require an additional dependency audit'
    assert all(image.packed_files and min(image.size) > 0 and len(image.pixels) > 0
               for image in bpy.data.images), 'Missing packed or undecoded image'
    baseline = asset_fingerprint()
    report = {'scene_sha256': source_hash, 'asset_fingerprint': baseline,
              'blender': bpy.app.version_string, 'packed_images': len(bpy.data.images),
              'width': 1080, 'height': 1080, 'frames': 1500, 'fps': 30,
              'samples': scene.eevee.taa_render_samples, 'inspect_only': args.inspect_only}
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'render.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = out / 'scene_check.json'
        if manifest.exists():
            assert json.loads(manifest.read_text())['scene_sha256'] == source_hash
        manifest.write_text(json.dumps(report, indent=2) + '\n')
        if args.inspect_only:
            print(json.dumps(report))
            return
        frames = out / 'frames'
        pending = out / 'pending'
        frames.mkdir(exist_ok=True)
        pending.mkdir(exist_ok=True)
        assert not any(pending.iterdir()), 'Inspect unfinished temporary files before resuming'
        existing = sorted(frames.glob('*.png'))
        assert [p.name for p in existing] == [f'{i:04d}.png' for i in range(1, len(existing) + 1)]
        assert len(existing) <= 1500 and all(png_valid(p) for p in existing)
        scene.render.image_settings.file_format = 'PNG'
        scene.render.image_settings.color_mode = 'RGB'
        scene.render.image_settings.color_depth = '8'
        scene.render.image_settings.compression = 45
        scene.render.filepath = str(pending / '####')
        scene.render.use_file_extension = True
        starts, completed, errors = {}, set(), []

        def before(current):
            starts[current.frame_current] = time.monotonic()

        def after(current):
            index = current.frame_current
            try:
                src, dst = pending / f'{index:04d}.png', frames / f'{index:04d}.png'
                assert not dst.exists() and png_valid(src)
                src.rename(dst)
                completed.add(index)
                entry = {'frame': index, 'sha256': sha(dst),
                         'seconds': round(time.monotonic() - starts[index], 3)}
                with (out / 'frames.jsonl').open('a') as handle:
                    handle.write(json.dumps(entry) + '\n')
                print(json.dumps(entry), flush=True)
            except Exception as error:
                errors.append(type(error).__name__)

        bpy.app.handlers.render_pre.append(before)
        bpy.app.handlers.render_write.append(after)
        try:
            for first in range(len(existing) + 1, 1501, 30):
                assert shutil.disk_usage(out).free > 4 * 2**30
                last = min(first + 29, 1500)
                scene.frame_start, scene.frame_end = first, last
                result = bpy.ops.render.render(animation=True)
                assert not errors and 'FINISHED' in result
                assert all(i in completed for i in range(first, last + 1))
        finally:
            bpy.app.handlers.render_pre.remove(before)
            bpy.app.handlers.render_write.remove(after)
        assert sha(source) == source_hash and asset_fingerprint() == baseline
        (out / 'render_complete.json').write_text(json.dumps(
            {'frames': 1500, 'source_scene_unchanged': True, 'asset_fingerprint_unchanged': True}, indent=2) + '\n')


if __name__ == '__main__':
    main()
