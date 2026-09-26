"""Read-only baseline telemetry; no stress workload or hard resource caps."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from local_agent import __version__
from local_agent.resources import detect, preference_profile, pressure_adjust


def measure(root, samples=3, interval=1.0, power='Balanced'):
    if not 1 <= samples <= 60 or not 0 <= interval <= 60:
        raise ValueError('Use 1-60 samples and a 0-60 second interval.')
    observations = []
    config = None
    started = time.monotonic()
    for index in range(samples):
        if index:
            time.sleep(interval)
        hardware = detect(root)
        if config is None:
            config = preference_profile(hardware, power)
        before = dict(config)
        config = pressure_adjust(config, hardware)
        observations.append(dict(elapsed_seconds=round(time.monotonic()-started, 3),
                                 hardware=hardware, targets_before=before,
                                 targets_after=dict(config), backoff=config != before))
    # A fixed, deterministic policy fixture. It allocates no pressure workload.
    simulated = []
    config = preference_profile({'threads': 8, 'available': 8 * 1024**3}, power)
    for label, available in [('normal', 8 * 1024**3), ('low', 1024**3),
                             ('recovered', 8 * 1024**3), ('unavailable', None)]:
        before = dict(config)
        config = pressure_adjust(config, {'available': available})
        simulated.append(dict(scenario=label, available_ram_bytes=available,
                              targets_before=before, targets_after=dict(config)))
    source = Path(__file__).resolve().parents[1] / 'local_agent'
    digest = hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in sorted(source.glob('*.py')))).hexdigest()
    return dict(version=__version__, code_digest=digest, power=power,
                measurement='actual host snapshots without an induced workload',
                units='RAM and disk in bytes; GPU is raw nvidia-smi text (MiB); targets are not utilization',
                actual_samples=observations, simulated_policy_checks=simulated,
                limits=['No model inference or stress workload was run.',
                        'Missing telemetry is unknown, not zero.',
                        'No CPU utilization, temperature, process memory or hard-cap measurement.',
                        'RAM backoff changes future targets, not loaded model memory.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=3)
    parser.add_argument('--interval', type=float, default=1.0)
    parser.add_argument('--power', choices=['Auto', 'Eco', 'Balanced', 'High'], default='Balanced')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        report = measure(Path(__file__).resolve().parents[1], args.samples, args.interval, args.power)
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(report, indent=2)
    if args.output:
        # Refuse to overwrite existing evidence or unrelated files.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as handle:
            handle.write(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
