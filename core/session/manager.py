from schemas.user import User

class SessionMenager:
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, user_data: User):
        self.sessions[user_data.id] = user_data

    def get_session(self, session_id: int):
        return self.sessions.get(session_id)

    def delete_session(self, session_id: int):
        if session_id in self.sessions:
            del self.sessions[session_id]
            
    def send_data_to_audio_processor(self, session_id, audio_chunk):
        session = self.get_session(session_id)
        if session:
            session.audio_chunks.append(audio_chunk)