import hashlib
import json
import os


def calculate_file_hash(file_path):
    """Вычисляет SHA-256 хэш файла."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_world_manifest(world_path):
    """Генерирует манифест с хэшами всех файлов в мире."""
    manifest = {}
    for root, _, files in os.walk(world_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, world_path)
            manifest[relative_path] = calculate_file_hash(full_path)
    return manifest


def save_manifest(world_path, manifest_path):
    """Сохраняет манифест в файл."""
    manifest = generate_world_manifest(world_path)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f)

    return manifest_path
