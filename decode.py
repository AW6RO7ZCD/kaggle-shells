"""
Dataset at kaggle.com/datasets/aw6ro7zcd/shells have to be decoded befo
re any use. All these proceeding below is tightly related with the proc
eeding of encode that can be found at github.com/AW6RO7ZCD/kaggle-shell
s/blob/master/clean_and_encode.ipynb

The same code, but as a .ipynb file can be found at the same directory,
at github.com/AW6RO7ZCD/kaggle-shells/blob/master/clean_and_encode.ipynb
"""
# Python 3.11.0
import pandas as pd

data: pd.DataFrame = pd.DataFrame(columns=['Brightness',
                                           'Orientation',
                                           'Stripes',
                                           'AntiStripes',
                                           'CornerAngle',
                                           'DilationAngle',
                                           'Length',
                                           'Width',
                                           'Height'])


ANGLE_INTERVAL: float = 5.625

def decode(column: str, code: str) -> object:
    encoded: int = int(code,2)
    nan_value = pd.to_numeric(None)
    
    match column:
        case 'Brightness':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return encoded - 1
        case 'Orientation':
            return encoded
        case 'Stripes':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return encoded - 1
        case 'AntiStripes':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return encoded - 1
        case 'CornerAngle':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return (encoded-1)*ANGLE_INTERVAL + 90.00
        case 'DilationAngle':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return (encoded-1)*ANGLE_INTERVAL + 61.00
        case 'Length':
            return encoded/10.0
        case 'Width':
            match encoded:
                case 0:
                    return nan_value
                case _:
                    return encoded/10.0
        case 'Height':
            return encoded/10.0 + 0.2

buffer: str = ''
record_size: int = 39      # 39 bits needed to decode one record (line)

def flush_buffer() -> None:
    global data
    global buffer
    while len(buffer) >= record_size:
        data.loc[len(data.index)] = [decode('Brightness', buffer[0:2]),
                                     decode('Orientation', buffer[2:3]),
                                     decode('Stripes', buffer[3:10]),
                                     decode('AntiStripes', buffer[10:14]),
                                     decode('CornerAngle', buffer[14:18]),
                                     decode('DilationAngle', buffer[18:22]),
                                     decode('Length', buffer[22:28]),
                                     decode('Width', buffer[28:34]),
                                     decode('Height', buffer[34:39])] 
        buffer = buffer[record_size:]

with open(file='data.bin', mode='rb') as file:
    byte = file.read(1)
    while byte != b'':
        buffer += bin(ord(byte))[2:].zfill(7)
        flush_buffer()
        byte = file.read(1)

print(data.head())