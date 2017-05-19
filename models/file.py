class File():
    CHUNK_SIZE = 524288
    files = {}
    def __init__(self, name, size, mime_type, sender_sid):
        self.name = name
        self.size = size
        self.mime_type = mime_type
        self.data = bytearray()
        self.downloaded = 0
        self.sender_sid = sender_sid
        File.files[sender_sid] = self

    @classmethod
    def get_file(cls, sender_sid):
        return cls.files[sender_sid]

    @classmethod
    def del_file(cls, sender_sid):
        del cls.files[sender_sid]