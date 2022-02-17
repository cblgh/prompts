# prompts
read a textfile of prompts and import into anki via ankiconnect

## Usage
* Install [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
* Have Anki running
* Populate a textfile with prompts, spacing individual prompts with a newline
* Run the script to automatically ingest the prompts as cards to the deck named in `prompts.py`

After running `prompts.py`, the input file will have its contents removed. Comment out the `erase_file` if you want to turn off that behaviour.

## Example

```
# prompts.txt
front of card
back of card

front of another card
back of that card

front of card 3
back of card 3
with multiple lines
and so on
```

```
python prompts.py prompts.txt
```

