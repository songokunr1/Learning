import asyn2
import itertools

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyn2.sleep(.1)
        except asyn2.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyn2.sleep(3)
    return 42


def main() -> None:
    result = asyn2.run(supervisor())
    print(f'Answer: {result}')

async def supervisor() -> int:
    spinner = asyn2.create_task(spin('thinking!'))
    print(f'spinner object: {spinner}')
    result = await slow()
    spinner.cancel()
    return result

if __name__ == '__main__':
    main()