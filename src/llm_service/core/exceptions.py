class InferenceError(Exception):
    """Base inference exception."""


class InferenceUnavailableError(InferenceError):
    """vLLM is unavailable."""


class InferenceTimeoutError(InferenceError):
    """Inference request timed out."""