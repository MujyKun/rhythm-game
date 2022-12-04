from dataclasses import dataclass


@dataclass
class PlayMusic:
    music: "ppb.assetlib.Assest"


@dataclass
class StopMusic:
    music: "ppb.assetlib.Asset"


@dataclass
class PauseSound:
    sound: "ppb.assetlib.Asset"


@dataclass
class StopSound:
    sound: "ppb.assetlib.Asset"
