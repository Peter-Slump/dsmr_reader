import serial


class BaseSerialReader(object):

    def __init__(self, device):
        self.device = device

    @property
    def _serial_settings(self):
        raise NotImplementedError

    def _is_start_of_telegram(self, line):
        # Currently assume this works for all implementations
        return line.startswith('/')

    def _is_end_of_telegram(self, line):
        # Currently assume this works for all implementations
        return line.startswith('!')

    def _serial_read(self):
        """
        Read complete DSMR telegram's from the serial interface containing
        DSMRObject's of the subtypes:
        - CosemObject
        - MbusObject
        - ProfileGeneric
        """

        serial_settings = self._serial_settings
        serial_settings['port'] = self.device

        with serial.Serial(**serial_settings) as serial_handle:
            telegram = []

            while True:
                line = serial_handle.readline()
                line = line.decode('ascii')

                # Telegrams need to be complete because the values belong to a
                # particular reading and can also be related to eachother.
                if not telegram and not line.startswith('/'):
                    continue

                telegram.append(line)

                if self._is_end_of_telegram(line):
                    yield telegram
                    telegram = []
