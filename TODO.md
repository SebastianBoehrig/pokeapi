# Goals

- display single pokemon:
  - name
    - height
    - weight
    - types
- display all pokemon of a type
- display pokemon pictures
- display evolutions
  - find out: what are evolutions and how do they work?

- 2 screens:
  - search for pokemon
  - click on type of a pokemon
  - in list click on single pokemon

## Subgoals

- write api that passes the info on
- start on the svelt frontend

## TODO

- settup bruno
- settup faspi calls
- do pokeapi calls

- do typehints for glom

## Notes

- get all pokemon: to display list at the start: maybe store this and do something to make searching easier
- get picture: try to use official adn default as fallback
  - on-hover: display shiny?
  - preload types pictures
  - rotate when there are different superficial formas in a subspecies

- `pip freeze | ForEach-Object {pip uninstall -y $_}`
- `fastapi run .\main.py --host 127.0.0.1 --port 8080 --reload`

## Time

- 15.20 - 16.20 : settup and first test
- 16.20 - 18.00 : reading up on pokemon species, evolution and hero forms
- 21.50 - 23.10 : typing the existing code, prepearing all calls to pokeapi
- 23.10 - 03.10 : finished test and calls to pokeapi
- 3.10 - 3.50 : propper dependancies

- 17.00 : fastapi

Categorys:

- settup: 1.40
- understanding: 1.40
- pokeapi: 5.20
- fastapi
- svelte
