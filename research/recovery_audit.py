"""Read-only provenance audit of owner-supplied Colab/Drive export archives.

Does not execute notebooks, load Keras weights, extract binaries, or contact the network.
Preserve originals unchanged; avoid publishing raw export contents.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def safe_read(z: zipfile.ZipFile, name: str, max_size: int = 20_000_000) -> bytes:
    entry = z.getinfo(name)
    if entry.file_size > max_size:
        raise ValueError(f'Refusing oversized metadata file: {name}')
    return z.read(entry)


def summarize_log(raw: bytes) -> dict:
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if not rows:
        return {'rows': 0, 'columns': []}
    counters = Counter(row.get('epoch') for row in rows)
    return {
        'rows': len(rows), 'columns': list(rows[0]),
        'epochs_reset': sum(int(rows[i]['epoch']) < int(rows[i - 1]['epoch']) for i in range(1, len(rows))),
        'val_auc_unique': sorted(set(r.get('val_auc', '') for r in rows)),
        'val_precision_unique': sorted(set(r.get('val_precision', '') for r in rows)),
        'epoch_zero_count': counters.get('0', 0),
    }


def summarize_manifest(raw: bytes) -> dict:
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    if not rows:
        return {'rows': 0, 'columns': []}
    h = [r.get('sha256', '') for r in rows]
    return {'rows': len(rows), 'columns': list(rows[0]),
            'label_counts': dict(sorted(Counter(r.get('label','') for r in rows).items())),
            'folder_counts': dict(sorted(Counter(r.get('folder','') for r in rows).items())),
            'distinct_hash_strings': len(set(h)),
            'hash_format_valid': all(len(x) == 64 and all(c in '0123456789abcdefABCDEF' for c in x) for x in h)}


def audit(model_export: Path, notebooks_export: Path) -> dict:
    result = {'status': 'ARCHIVE_METADATA_ONLY — no trained checkpoint runtime or labels verified',
              'model_export_sha256': sha256(model_export), 'notebooks_export_sha256': sha256(notebooks_export)}
    with zipfile.ZipFile(model_export) as z:
        result['model_export_crc_passed'] = z.testzip() is None
        model_name = next((n for n in z.namelist() if n.endswith('/best_model.keras')), None)
        if model_name is None:
            raise FileNotFoundError('Missing best_model.keras')
        # Model archive itself is ~11MB; no weights are parsed or executed.
        model = safe_read(z, model_name)
        result['model_sha256'] = hashlib.sha256(model).hexdigest()
        result['model_size_bytes'] = len(model)
        with zipfile.ZipFile(io.BytesIO(model)) as nz:
            result['model_nested_crc_passed'] = nz.testzip() is None
            meta = json.loads(safe_read(nz, 'metadata.json'))
            conf = json.loads(safe_read(nz, 'config.json'))
            result['model_metadata'] = meta
            result['model_name'] = conf.get('config', {}).get('name')
            layers = conf.get('config', {}).get('layers', [])
            result['top_level_layers'] = [{'name': l.get('config', {}).get('name'), 'class': l.get('class_name')} for l in layers]
            result['input_shape'] = next((l.get('config',{}).get('batch_shape') for l in layers if l.get('class_name') == 'InputLayer'), None)
        log = next((n for n in z.namelist() if n.endswith('/training_log.csv')), None)
        result['training_log'] = summarize_log(safe_read(z, log)) if log else {'missing': True}
        empty_log = next((n for n in z.namelist() if n.endswith('/training_log_phase1_head.csv')), None)
        result['phase1_log_size_bytes'] = z.getinfo(empty_log).file_size if empty_log else None
    with zipfile.ZipFile(notebooks_export) as z:
        result['notebooks_export_crc_passed'] = z.testzip() is None
        nb_files = sorted(n for n in z.namelist() if n.endswith('.ipynb'))
        result['notebooks'] = []
        for name in nb_files:
            nb = json.loads(safe_read(z, name))
            result['notebooks'].append({'name': Path(name).name, 'cells': len(nb.get('cells', [])),
                'code_cells': sum(c.get('cell_type') == 'code' for c in nb.get('cells', [])),
                'stored_output_blocks': sum(len(c.get('outputs', [])) for c in nb.get('cells', []))})
        manifest_name = next((n for n in z.namelist() if n.endswith('Copy of MaleX_matched_images.csv')), None)
        result['four_thousand_image_manifest'] = summarize_manifest(safe_read(z, manifest_name)) if manifest_name else {'missing': True}
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model-export', required=True, type=Path)
    p.add_argument('--notebooks-export', required=True, type=Path)
    p.add_argument('--output', type=Path, help='Optional sanitized JSON report')
    args = p.parse_args()
    report = audit(args.model_export, args.notebooks_export)
    output = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + '\n', encoding='utf-8')
    print(output)

if __name__ == '__main__':
    main()
