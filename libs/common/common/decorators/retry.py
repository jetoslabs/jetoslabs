# https://gist.github.com/alairock/a0235eae85c62f0f0f7b81bec8aa378a
import loguru


class TooManyTriesException(BaseException):
    pass


def retry(times: int, *, logger: loguru.logger):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            # implements retry logic
            for time in range(times):
                logger.debug(f' {f.__name__} retry time: {time + 1}')
                try:
                    return await f(*args, **kwargs)
                except Exception as e:
                    if times == time + 1:
                        raise TooManyTriesException from e
        return wrapper
    return func_wrapper
