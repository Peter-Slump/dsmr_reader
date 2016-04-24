import serial

from dsmr_reader.obis_references import *
from dsmr_reader.parsing import CosemParser, ValueParser, MBusParser, \
    TelegramParser
from dsmr_reader.readers import BaseSerialReader
from dsmr_reader.value_types import timestamp


SPECIFICATION = {
    P1_MESSAGE_HEADER: CosemParser(ValueParser(str)),
    P1_MESSAGE_TIMESTAMP: CosemParser(ValueParser(timestamp)),
    ELECTRICITY_USED_TARIFF_1 : CosemParser(ValueParser(float)),
    ELECTRICITY_USED_TARIFF_2: CosemParser(ValueParser(float)),
    ELECTRICITY_DELIVERED_TARIFF_1: CosemParser(ValueParser(float)),
    ELECTRICITY_DELIVERED_TARIFF_2: CosemParser(ValueParser(float)),
    ELECTRICITY_ACTIVE_TARIFF: CosemParser(ValueParser(str)),
    EQUIPMENT_IDENTIFIER: CosemParser(ValueParser(str)),
    CURRENT_ELECTRICITY_USAGE: CosemParser(ValueParser(float)),
    CURRENT_ELECTRICITY_DELIVERY: CosemParser(ValueParser(float)),
    LONG_POWER_FAILURE_COUNT: CosemParser(ValueParser(int)),
    # POWER_EVENT_FAILURE_LOG: ProfileGenericParser(),
    VOLTAGE_SAG_L1_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SAG_L2_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SAG_L3_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L1_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L2_COUNT: CosemParser(ValueParser(int)),
    VOLTAGE_SWELL_L3_COUNT: CosemParser(ValueParser(int)),
    TEXT_MESSAGE_CODE: CosemParser(ValueParser(int)),
    TEXT_MESSAGE: CosemParser(ValueParser(str)),
    DEVICE_TYPE: CosemParser(ValueParser(int)),
    INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE: CosemParser(ValueParser(float)),
    INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE: CosemParser(ValueParser(float)),
    INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE: CosemParser(ValueParser(float)),
    INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE: CosemParser(ValueParser(float)),
    INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE: CosemParser(ValueParser(float)),
    INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE: CosemParser(ValueParser(float)),
    EQUIPMENT_IDENTIFIER_GAS: CosemParser(ValueParser(str)),
    HOURLY_GAS_METER_READING: MBusParser(ValueParser(timestamp),
                                         ValueParser(float))
}


class SerialReader(BaseSerialReader):

    def __init__(self, *args, **kwargs):
        super(SerialReader, self).__init__(*args, **kwargs)

        self.telegram_parser = TelegramParser(SPECIFICATION)

    @property
    def _serial_settings(self):
        return {
            'baudrate': 115200,
            'bytesize': serial.SEVENBITS,
            'parity': serial.PARITY_EVEN,
            'stopbits': serial.STOPBITS_ONE,
            'xonxoff': 0,
            'rtscts': 0,
            'timeout': 20
        }

    def read(self):

        for telegram in self._serial_read():
            telegram = self.telegram_parser.parse(telegram)

            yield telegram
