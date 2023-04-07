
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

from .setup import Setup
from .playing import Playing

STATES = {
    SIDS.SETUP: Setup,
    SIDS.PLAYING: Playing,
}