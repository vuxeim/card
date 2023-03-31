# card
## How to use
1. Edit `data` variable in `config.py`.
2. See the results:
```
python card.py
```
3. Pipe output to a file:
```
python card.py > file
```
4. Put the file on your server
5. Use `curl` to display the file:
```
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
## Help
```
$ python card.py --help
Usage: card.py [OPTIONS]
Business card generator

  -n, --name=TEXT     set your nickname to TEXT
  -w, --width=NUMBER  set width of the card to NUMBER
  -f, --frame=TEXT    set chars of card's frame to TEXT
      --help          print this and exit
```
## Troubleshooting
Use `curl` with flag `-L` if nothing is shown.
