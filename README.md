# card
## How to use
1. Edit `data` variable in `card.py`.
2. See the results:
```shell
python card.py
```
3. Pipe output to a file:
```shell
python card.py > file
```
4. Put the file on your server
5. Use `curl` to display the file:
```shell
$ curl your_domain.net/file
╭--------------------------------------------╮
|                                            |
|                  nickname                  |
|                                            |
|                   CONTACT                  |
|             Email: user@domain             |
|             Discord: user#0000             |
|                                            |
|           Github: github.com/user          |
|                                            |
╰--------------------------------------------╯
```
## Troubleshooting
Use `curl` with flag `-L` if nothing is shown.
