#!/usr/bin/env python

def write_line():
    with open('test_file.txt', 'a') as the_file:
        for i in range(5):
            text = input('Enter line to write: ')
            text = f'{text}\n'
            the_file.writelines(text)
    print('end of file printing')

def main():
    write_line()

if __name__=='__main__':
    main()
