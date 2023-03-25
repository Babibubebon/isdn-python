from unittest import TestCase

from isdn import ISDN, InvalidIsdnError


class TestIsdn(TestCase):
    def test_init(self):
        ISDN("2784702901978", "278", "4", "702901", "97", "8")
        ISDN(2784702901978, "278", "4", "702901", "97", "8")
        ISDN("278-4-702901-97-8", "278", "4", "702901", "97", "8")

        with self.assertRaises(ValueError):
            ISDN("2784702901978", "278", "4", "000000", "97", "8")

    def test_parts(self):
        expected_parts = ["278", "4", "702901", "97", "8"]
        isdn = ISDN("2784702901978", *expected_parts)
        self.assertEqual(expected_parts, isdn.parts)

    def test_to_disp_isdn(self):
        isdn = ISDN("2784702901978")
        self.assertIsNone(isdn.to_disp_isdn())

        isdn = ISDN("2784702901978", "278", "4", "702901", "97", "8")
        self.assertEqual("ISDN278-4-702901-97-8", isdn.to_disp_isdn())

    def test_validate(self):
        self.assertTrue(ISDN("2784702901978").validate())
        self.assertFalse(ISDN("abc").validate())
        self.assertFalse(ISDN("1").validate())
        self.assertFalse(ISDN("0123456789123").validate())
        self.assertFalse(ISDN("2784702901970").validate())

        self.assertTrue(ISDN("2784702901978", "278", "4", "702901", "97", "8").validate())
        self.assertFalse(ISDN("2784702901978", "278", "470290", "1", "97", "8").validate())
        self.assertFalse(ISDN("2784702901978", "278", "", "47029019", "7", "8").validate())
        self.assertFalse(ISDN("2784702901978", "278", "4", "70290", "197", "8").validate())

    def test_normalize(self):
        self.assertEqual("2784702901978", ISDN.normalize("2784702901978"))
        self.assertEqual("2784702901978", ISDN.normalize(2784702901978))
        self.assertEqual("2784702901978", ISDN.normalize("278-4-702901-97-8"))
        self.assertEqual("2784702901978", ISDN.normalize(" 278-4-702901-97-8 "))

    def test_calc_check_digit(self):
        self.assertEqual("0", ISDN.calc_check_digit("278470290106"))
        self.assertEqual("1", ISDN.calc_check_digit("278470290109"))
        self.assertEqual("2", ISDN.calc_check_digit("278470290115"))
        self.assertEqual("3", ISDN.calc_check_digit("278470290105"))
        self.assertEqual("4", ISDN.calc_check_digit("278470290108"))
        self.assertEqual("5", ISDN.calc_check_digit("278470290101"))
        self.assertEqual("6", ISDN.calc_check_digit("278470290104"))
        self.assertEqual("7", ISDN.calc_check_digit("278470290107"))
        self.assertEqual("8", ISDN.calc_check_digit("278470290113"))
        self.assertEqual("9", ISDN.calc_check_digit("278470290103"))

    def test_from_disp_isdn(self):
        disp_isdn = "ISDN278-4-702901-97-8"
        isdn = ISDN.from_disp_isdn(disp_isdn)
        self.assertEqual(disp_isdn, isdn.to_disp_isdn())

        with self.assertRaises(InvalidIsdnError):
            ISDN.from_disp_isdn("ISDN278-4-702901")
