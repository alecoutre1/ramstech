import json

class Config:
    def __init__(self,file_path, name=None,):
        self.file_path = file_path
        self.name = name
        with open(self.file_path,'r') as f:
            data = json.load(f)
            for k, v in data.items():
                setattr(self, k, v)
