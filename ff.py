from lark import Lark, Tree
from lark.visitors import Interpreter
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF

import sys

argv = sys.argv[1:]

_parser = Lark(open('grammar.lark'))
ff_parse = _parser.parse

class FFInterpreter(Interpreter):
    
    def __init__(self) -> None:
        self.stack = [0]
        self.cur_idx = 0
    
    def start(self, stmt: Tree):
        for s in stmt.children:
            self.visit(s)
    
    def add(self, _):
        if self.stack[self.cur_idx] != 255:
            self.stack[self.cur_idx] += 1
        else:
            self.stack[self.cur_idx] = 0
    
    def sub(self, _):
        if self.stack[self.cur_idx] != 0:
            self.stack[self.cur_idx] -= 1
        else:
            self.stack[self.cur_idx] = 255
    
    def advance(self, _):
        self.cur_idx += 1
        if len(self.stack) < self.cur_idx+1:
            self.stack.append(0)
    
    def back(self, _):
        if self.cur_idx != 0:
            self.cur_idx -= 1
    
    def print(self, _):
        print(chr(self.stack[self.cur_idx]), end='')
    
    def input(self, _):
        try:
            i = input()
            if i:
                self.stack[self.cur_idx] = ord(i[0])
        except EOFError:
            return
    
    def loop(self, ins: Tree):
        while self.stack[self.cur_idx] != 0:
            for i in ins.children:
                self.visit(i)

def exec(inter: FFInterpreter, i: str):
    if i and not i.isspace():
        inter.start(ff_parse(i))

if __name__ == "__main__":
    inter = FFInterpreter()
    if argv:
        try:
            i = open(argv[0])
            exec(inter, i.read())
            i.close()
        except FileNotFoundError:
            sys.stderr.write('File not found\n')
        except PermissionError:
            sys.stderr.write('No permission\n')
        except UnexpectedCharacters as e:
            sys.stderr.write(f'Error: invalid character {e.char}\n')
        except UnexpectedEOF:
            sys.stderr.write('Error: unclosed loop\n')
    else:
        while True:
            try:
                i = input("> ")
                exec(inter, i)
                #print(*inter.stack, sep=', ')
            except EOFError:
                break
            except UnexpectedCharacters as e:
                sys.stderr.write(f'Error: invalid character {e.char}\n')
            except UnexpectedEOF:
                sys.stderr.write('Error: unclosed loop\n')