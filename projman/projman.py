import argparse
import sys
from typing import Dict

from projman.lib.commands import Command, CommandArg
from projman.lib.context import Context


def _get_nargs(arg: CommandArg) -> Dict:
    default = {'nargs': None,
               'default': arg.default,
               'action': None,
               'type': None}
    if arg.type_ is bool:
        default['action'] = 'store_true'
    elif arg.type_ is list:
        default['nargs'] = '+'
    elif arg.type_ is str:
        default['type'] = str
    return {k: v for k, v in default.items() if v is not None}


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    cmd_parser = parser.add_subparsers(dest="cmd")
    for cmd in Command.__subclasses__():
        sub_parser = cmd_parser.add_parser(cmd.name())
        sub_parser.add_argument('-p', type=str, default='conf.projman')
        for arg in cmd.args():
            sub_parser.add_argument(f"--{arg.name}", **_get_nargs(arg))
    return parser


def main():
    args = sys.argv[1:]
    args = _get_parser().parse_args(args)
    cmd_class = Command.get(args.cmd)
    context = Context.load(args.p)
    cmd = cmd_class(context=context, **{k: v for k, v in vars(args).items() if k not in ('p', 'cmd')})
    cmd.run()


if __name__ == '__main__':
    main()
