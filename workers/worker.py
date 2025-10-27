import time

def run():
    print('Worker iniciado')
    while True:
        print('Esperando jobs...')
        time.sleep(5)

if __name__ == '__main__':
    run()
