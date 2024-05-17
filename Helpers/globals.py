_model = None
_modelFast = None
_rerankModel = None
_rerankTokenizer = None
_config = None
_fileConsoleLogger = None

def GetFileConsoleLogger():
   global _fileConsoleLogger
   return _fileConsoleLogger

def SetFileConsoleLogger(logger):
   global _fileConsoleLogger
   _fileConsoleLogger = logger

def GetConfig():
   global _config
   return _config

def SetConfig(config):
   global _config
   _config = config

def GetModel():
   global _model
   return _model

def SetModel(model):
   global _model
   _model = model

def GetModelFast():
   global _modelFast
   return _modelFast

def SetModelFast(modelFast):
   global _modelFast
   _modelFast = modelFast

def GetRerankModel():
   global _rerankModel
   return _rerankModel

def SetRerankModel(rerankModel):
   global _rerankModel
   _rerankModel = rerankModel

def GetRerankTokenizer():
   global _rerankTokenizer
   return _rerankTokenizer

def SetRerankTokenizer(rerankTokenizer):
   global _rerankTokenizer
   _rerankTokenizer = rerankTokenizer