class Parser:
    # Options:
    # 1. short name for the -x option
    # 2. full name for --xxx-yyy option
    # 3. full name with a hint
    # 4. description
    # 5. default value
    def __init__(self, argv: list, options: list[str], desc: str = '', usage: str = ''):
        args = dict()
        self._name = argv.pop(0)
        stack = []
        for arg in argv:
            if arg.startswith('-'):
                if stack:
                    args[stack.pop()] = 'true'
                minus = '--' if arg.startswith('--') else '-'
                stack.append(arg.replace(minus, '', 1))
            else:
                if stack:
                    args[stack.pop()] = arg
                else:
                    exit(f"{self._name}: Cannot parse arguments, maybe you should use \"\"?")
        for element in stack:
            args[element] = 'true'

        for arg in args.copy():
            for option in options:
                if arg == option[0]:
                    args[option[1]] = args.pop(arg)

        for arg in list(args)[1:]:
            if not arg in [option[1] for option in options]:
                exit('Unknown argument: '+arg)

        copyargs = {}
        copyargs.update({item[1]: item[4] for item in options})
        copyargs.update(args)

        self._args = copyargs
        self._options = options
        self._desc = desc
        self._usage = usage

    def __call__(self, key):
        return self._args[key] if key in self._args.keys() else '' if key else self._args

    def help(self):
        head = f"Usage: {self._name} {self._usage}\n" if self._usage else f"{self._name}\n"
        print(head + f"{self._desc}\n" if self._desc else '')
        body = [[(f'  -{option[0]}, ' if option[0] else ' '*6) + f'--{option[2]}', option[3]] for option in self._options]
        space = max(map(lambda x: len(x[0]), body))
        [print(f'{item[0]}{" "*(space+2-len(item[0]))}{item[1]}') for item in body]
