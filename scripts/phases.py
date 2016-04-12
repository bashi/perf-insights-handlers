import json
import sys


_ALLOCATORS = [
    'blink_gc', 'cc', 'discardable', 'gpu',
    'java_heap', 'malloc',
     'partition_alloc', 'skia', 'v8', 'tracing',
]


def _read_json(path):
    values = {}
    with open(path) as f:
        pairs = json.load(f)[0]['pairs']
        for key, value in pairs.iteritems():
            site = key.split('/')[-2]
            values[site] = value
        return values


def _print_peaks(values):
    print('site,phase,peakResidentBytes,%s' % ','.join(_ALLOCATORS))
    for site, value in values.iteritems():
        phase_name = value['peak_phase']
        phase = value['phases'][phase_name]
        peak_value = float(phase['peakResidentBytes'])
        allocators = phase['allocators']
        allocator_values = []
        for allocator_name in _ALLOCATORS:
            size = float(allocators.get(allocator_name, 0))
            allocator_values.append('%f' % (size / 1024**2))
        print('%s,%s,%f,%s' % (site, phase_name, (peak_value / 1024**2), ','.join(allocator_values)))


def main(args):
    values = _read_json(args[0])
    _print_peaks(values)


if __name__ == '__main__':
    main(sys.argv[1:])
