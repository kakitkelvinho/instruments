import pyvisa
import matplotlib.pyplot as plt
import numpy as np


def connect_rigol(
    address="TCPIP0::192.168.1.2::INSTR",
    identity="RIGOL TECHNOLOGIES,MSO5104,MS5A231100810,00.01.03.00.01\n",
):
    rm = pyvisa.ResourceManager()
    rigol = rm.open_resource(address)
    idn = rigol.query("*IDN?")
    assert idn == identity
    return rigol


def measure(rigol, channel=1, mode="NORM"):
    # check the params
    if not isinstance(channel, int) or not (1 <= channel <= 4):
        raise ValueError(
            f"Invalid channel: {channel}. Channel must be an integer between 1 and 4."
        )

    # Validate mode: must be one of the predefined strings
    valid_modes = {"NORM", "MAX", "RAW"}
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Mode must be one of {valid_modes}.")

    rigol.write(f":WAV:SOUR CHAN{channel}")
    rigol.write(f":WAV:MODE {mode}")
    rigol.write(":WAV:FORM ASC")

    # take the measurement
    wave = rigol.query(":WAV:DATA?")
    wave = np.fromstring(wave[11:-1], sep=",")

    #
