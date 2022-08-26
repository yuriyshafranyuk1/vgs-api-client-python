import decimal
import unittest

from vgs.sdk.serializers import dump_json, dump_yaml


class SerializersDecimalTestCase(unittest.TestCase):
    def test_serializers_to_json_with_decimal_ok(self):
        # Arrange
        obj = {"executionTime": decimal.Decimal("1.001")}
        expected_str = '{"executionTime": "1.001"}'

        # Act
        stringified = dump_json(obj)

        # Assert
        self.assertEqual(
            expected_str,
            stringified,
            f"Incorrect JSON stringification occurred.\n"
            f"Actual: {stringified}"
            f"Expected: {expected_str}",
        )

    def test_serializers_to_yaml_with_decimal_ok(self):
        # Arrange
        obj = {"executionTime": decimal.Decimal("1.001")}
        expected_str = "executionTime: '1.001'\n"

        # Act
        stringified = dump_yaml(obj)

        # Assert
        self.assertEqual(
            expected_str,
            stringified,
            f"Incorrect YAML stringification occurred.\n"
            f"Actual: {stringified}"
            f"Expected: {expected_str}",
        )
