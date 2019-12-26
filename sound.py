from ctypes import cast, POINTER

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.SetMasterVolumeLevel(-0.0, None)  # max
# volume.SetMasterVolumeLevel(-5.0, None) #72%
# volume.SetMasterVolumeLevel(-10.0, None)  # 51%
# volume.SetMasterVolumeLevel(-20.0, None)  # 26%
# volume.SetMasterVolumeLevel(-65.0, None)  # 0%
