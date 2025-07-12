import logging
logging.basicConfig(
    level=logging.DEBUG,  # Можно изменить на logging.DEBUG для более детального логгирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_errors.log'),  # Логи будут записываться в этот файл
    ]
)
logger = logging.getLogger(__name__)
def f():
    try:
        1/0
    except Exception as e:
        logger.error(f'Ошибка из функции f: {e}')
def main():
    f()
if __name__ == "__main__":
    main()