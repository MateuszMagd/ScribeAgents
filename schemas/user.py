from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Platoform(str, Enum):
    DISCORD = "discord"
    TEAMSPEAK = "teamspeak"

class ChannelType(str, Enum):
    VOICE = "voice"
    TEXT = "text"
    STAGE = "stage"
    UNKNOWN = "unknown"
class Channel(BaseModel):
    id: int
    name: Optional[str]
    type: ChannelType
    platform: Optional[Platoform] = None
    
class VoiceState(BaseModel):
    channel: Optional[Channel]
    self_mute: Optional[bool]
    self_deaf: Optional[bool]
    mute: Optional[bool]
    deaf: Optional[bool]

class User(BaseModel):
    id: int
    name: str
    display_name: Optional[str]
    bot: bool
    roles: List[str]
    joined_at: str
    voice: Optional[VoiceState]
    
