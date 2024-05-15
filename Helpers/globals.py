_model = None
_model_fast=None
_rerank_model=None
_rerank_tokenizer=None
_config=None
_file_console_logger= None

def get_file_console_logger():
    global _file_console_logger
    return _file_console_logger

def set_file_console_logger(logger):
    global _file_console_logger
    _file_console_logger = logger
    
def get_config():
    global _config
    return _config

def set_config(config):
    global _config
    _config = config
    
def get_model():
    global _model
    return _model

def set_model(model):
    global _model
    _model = model

def get_model_fast():
    global _model_fast
    return _model_fast

def set_model_fast(model_fast):
    global _model_fast
    _model_fast = model_fast

def get_rerank_model():
    global _rerank_model
    return _rerank_model

def set_reranker_model(rerank_model):
    global _rerank_model
    _rerank_model = rerank_model

def get_rerank_tokenizer():
    global _rerank_tokenizer
    return _rerank_tokenizer

def set_rerank_tokenizer(rerank_tokenizer):
    global _rerank_tokenizer
    _rerank_tokenizer = rerank_tokenizer


