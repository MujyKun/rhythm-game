from dataclasses import dataclass


@dataclass
class PlayMusic:
    music: "ppb.assetlib.Assest"


@dataclass
class StopMusic:
    music: "ppb.assetlib.Asset" = None


@dataclass
class PauseMusic:
    sound: "ppb.assetlib.Asset" = None

@dataclass
class StartVis:
    sound: "ppb.assetlib.Asset" = None
