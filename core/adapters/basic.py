from abc import ABC, abstractmethod

class PlatformAdapter(ABC):
    @abstractmethod
    async def start_listening(self):
        pass

    @abstractmethod
    async def stop(self):
        pass
    
    @abstractmethod
    async def _write(self, data, user):
        pass