from poke_env.player import RandomPlayer
from lasthope import BetterPlayer
import neat
import pickle
import os
from poke_env import PlayerConfiguration, ShowdownServerConfiguration
import asyncio


async def main():   
    team_2 = """
Mandibuzz (F) @ Heavy-Duty Boots  
Ability: Overcoat  
EVs: 248 HP / 8 Def / 252 SpD  
Careful Nature  
- Foul Play  
- U-turn  
- Roost  
- Defog  

Jirachi @ Leftovers  
Ability: Serene Grace  
EVs: 48 HP / 208 Atk / 252 Spe  
Jolly Nature  
- Iron Head  
- Zen Headbutt  
- Power-Up Punch  
- Substitute  

Sandaconda (M) @ Leftovers  
Ability: Shed Skin  
EVs: 248 HP / 216 Def / 16 SpD / 28 Spe  
Impish Nature  
- Earthquake  
- Body Press  
- Stealth Rock  
- Glare  

Zeraora @ Life Orb  
Ability: Volt Absorb  
EVs: 180 Atk / 76 SpA / 252 Spe  
Naive Nature  
- Plasma Fists  
- Close Combat  
- Knock Off  
- Grass Knot  

Primarina (F) @ Choice Specs  
Ability: Torrent  
EVs: 88 HP / 252 SpA / 168 Spe  
Modest Nature  
IVs: 0 Atk  
- Sparkling Aria  
- Moonblast  
- Hydro Pump  
- Psychic  

Dragapult (F) @ Choice Scarf  
Ability: Infiltrator  
Shiny: Yes  
EVs: 64 HP / 252 SpA / 192 Spe  
Modest Nature  
- Draco Meteor  
- Shadow Ball  
- Flamethrower  
- U-turn  
"""

    bot_username = "" #! INSERT BOT SHOWDOWN ACCOUNT NAME HERE
    bot_passwd = "" #! INSERT BOT SHOWDOWN ACCOUNT PASSWD HERE
    with open ("best.pickle", "rb") as f:
        winner = pickle.load(f)
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    player = BetterPlayer("gen8ou", team_2, 99, neat.nn.FeedForwardNetwork.create(winner,config), PlayerConfiguration(bot_username, bot_passwd), ShowdownServerConfiguration)

    to_challenge = input("Enter player you want to challenge: ")

    await player.send_challenges(to_challenge, n_challenges=1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
