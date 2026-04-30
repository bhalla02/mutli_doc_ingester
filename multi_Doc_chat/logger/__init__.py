from multi_Doc_chat.logger.custom_logger import CustomLogger

# Initialize the global logger
_logger_instance = CustomLogger()
GLOBAL_LOGGER = _logger_instance.get_logger(__name__)

__all__ = ['GLOBAL_LOGGER']
