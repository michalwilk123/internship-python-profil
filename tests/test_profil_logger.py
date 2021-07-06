from my_logger import ProfilLogger
import unittest


class TestProfilLogger(unittest.TestCase):
    def setUp(self) -> None:
        self.profil_logger = ProfilLogger(handlers=[])

    def test_log_level(self):
        self.assertTrue(self.profil_logger.debug("Test Log"))
        self.assertTrue(self.profil_logger.info("Test Log"))
        self.assertTrue(self.profil_logger.warning("Test Log"))
        self.assertTrue(self.profil_logger.error("Test Log"))
        self.assertTrue(self.profil_logger.critical("Test Log"))

    def test_min_log_change(self):
        self.profil_logger.set_log_level('WARNING')

        self.assertFalse(self.profil_logger.debug("Test Log"))
        self.assertFalse(self.profil_logger.info("Test Log"))
        self.assertTrue(self.profil_logger.warning("Test Log"))
        self.assertTrue(self.profil_logger.error("Test Log"))
        self.assertTrue(self.profil_logger.critical("Test Log"))

    def test_bad_level_name(self):
        self.assertRaises(
            KeyError, 
            self.profil_logger.set_log_level,
            "bad level name"
        )
        
        

