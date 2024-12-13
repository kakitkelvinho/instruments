import pyvisa
import matplotlib.pyplot as plt
import numpy as np


def connect_rigol(
    address: str="TCPIP0::192.168.1.2::INSTR",
    identity: str="RIGOL TECHNOLOGIES,MSO5104,MS5A231100810,00.01.03.00.01\n",
):
    '''
    Connects to the RIGOL MSO5104 scope by default (when called without arguments)
    Otherwise, it takes as arguments:
    address: PyVisa address of the device
    identity: identity of the device for verification
    '''
    rm = pyvisa.ResourceManager()
    rigol = rm.open_resource(address)
    idn = rigol.query("*IDN?")
    assert idn == identity
    return rigol


def measure(rigol, channel: int=1, mode: str="NORM"):
    '''
    Record the measurement from the scope.
    Arguments:
    rigol: instance of a pyvisa device, which should be the return of connect_rigol function
    channel: 1,2,3 or 4 of the scope
    return:
    t: array of time(stamp)
    y: array of recorded trace (in voltage for example)
    '''

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

    # get time information
    dt = float(rigol.query(":TIMebase:MAIN:SCALe?")) / 100
    t = np.arange(0, dt * len(wave), dt)

    return t, wave


def main():
    rigol = connect_rigol()
    t, wave = measure(rigol)
    plt.figure()
    plt.plot(t, wave)
    plt.show()


if __name__ == "__main__":
    main()
