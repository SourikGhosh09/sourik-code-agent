"""Policy fixtures are simulated, not evidence of host pressure handling."""
import unittest
from unittest.mock import patch
from scripts.measure_resources import measure


class ResourceMeasurement(unittest.TestCase):
    def test_separates_actual_samples_from_simulated_backoff(self):
        normal = {'threads':8, 'ram':16*1024**3, 'available':8*1024**3, 'gpu':'', 'disk_free':100}
        low = {**normal, 'available':1024**3}
        with patch('scripts.measure_resources.detect', side_effect=[normal, low, normal]), patch('scripts.measure_resources.time.sleep') as sleep:
            report = measure('.', samples=3, interval=1)
        self.assertEqual(sleep.call_count, 2)
        actual = report['actual_samples']
        self.assertFalse(actual[0]['backoff'])
        self.assertTrue(actual[1]['backoff'])
        self.assertEqual(actual[1]['targets_after'], actual[2]['targets_after'])
        self.assertEqual(actual[1]['targets_after']['num_ctx'], 2048)
        self.assertEqual(len(report['simulated_policy_checks']), 4)
        self.assertEqual(normal['available'], 8*1024**3)

    def test_unknown_memory_remains_unknown(self):
        hardware = {'threads':2, 'ram':None, 'available':None, 'gpu':'', 'disk_free':100}
        with patch('scripts.measure_resources.detect', return_value=hardware):
            report = measure('.', samples=1)
        sample = report['actual_samples'][0]
        self.assertIsNone(sample['hardware']['available'])
        self.assertFalse(sample['backoff'])
        self.assertEqual(sample['targets_before'], sample['targets_after'])

    def test_invalid_sampling_rejected_before_telemetry(self):
        with patch('scripts.measure_resources.detect') as detect:
            for samples, interval in [(0, 1), (61, 1), (1, -1), (1, 61), (1, float('nan'))]:
                with self.subTest(samples=samples, interval=interval), self.assertRaises(ValueError):
                    measure('.', samples=samples, interval=interval)
            detect.assert_not_called()
