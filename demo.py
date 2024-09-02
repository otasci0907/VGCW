import asyncio
import nest_asyncio
import os
import neat
import random
import pickle
import visualize

from poke_env.player import Player
from itertools import chain
from inputs import SideInformation

nest_asyncio.apply()

class BetterPlayer(Player):
    def __init__(self, battle_form, te, max_concurrent_battl, neural, player_conf=None, showdown_conf=None):
        if not player_conf == None:
            super().__init__(battle_format=battle_form,team=te,max_concurrent_battles=max_concurrent_battl, player_configuration=player_conf, server_configuration=showdown_conf)
        else:
            super().__init__(battle_format=battle_form,team=te,max_concurrent_battles=max_concurrent_battl)
        self.neural = neural
        self.switches = 0

    def choose_move(self, battle):
        game_info = SideInformation(battle)
        inputs = (game_info.my_active, *game_info.my_team,*game_info.my_items,*game_info.my_levels,*game_info.my_hp,*game_info.my_max_hp, *list(chain.from_iterable(game_info.my_stats)), *list(chain.from_iterable(game_info.my_boosts)), *game_info.my_effects, *game_info.my_status, *game_info.my_abilities, *game_info.my_side_conditions, game_info.opp_active, *game_info.opp_team, *game_info.opp_items, *game_info.opp_levels, *game_info.opp_hp, *game_info.opp_max_hp, *game_info.opp_effects, *game_info.opp_status, *game_info.opp_side_conditions, game_info.weather)
        turn = ""
        try:
            chosen = self.neural.activate(inputs)
            moved = False
            while not moved:
                if not len(chosen) == 0:
                    max_ind = chosen.index(max(chosen))
                else:
                    turn = self.choose_random_move(battle)
                    moved = True
                if max_ind >= 0 and max_ind < 4:
                    try:
                        turn = self.create_order(battle.available_moves[max_ind])
                    except IndexError as e:
                        chosen = chosen[:max_ind] + chosen[max_ind + 1:]
                    else:
                        self.switches = 0
                        moved = True
                else:
                    try:
                        if self.switches < 10:
                            turn = self.create_order(battle.available_switches[max_ind - 4])
                        else:
                            turn = self.create_order(random.choice(battle.available_moves))
                    except IndexError as e:
                        chosen = chosen[:max_ind] + chosen[max_ind + 1:]
                    else:
                        if self.switches < 10:
                            self.switches += 1
                        else:
                            self.switches = 0
                        moved = True
        except RuntimeError as e:
            turn = self.choose_random_move(battle)
        return turn

async def calculate_fitness(genome1, genome2, player1, player2):
    await player1.battle_against(player2)
    print(player1.n_won_battles)
    genome1.fitness += player1.n_won_battles
    genome2.fitness += player2.n_won_battles

def eval_genomes(genomes, config):
    team_1 = """
Hippowdon @ Rocky Helmet  
Ability: Sand Stream  
EVs: 252 HP / 4 Atk / 252 Def  
Impish Nature  
- Stealth Rock  
- Slack Off  
- Earthquake  
- Whirlwind  

Toxapex @ Black Sludge  
Ability: Regenerator  
EVs: 252 HP / 68 Def / 188 SpD  
Impish Nature  
- Toxic Spikes  
- Recover  
- Knock Off  
- Haze  

Hydreigon @ Leftovers  
Ability: Levitate  
EVs: 252 SpA / 4 SpD / 252 Spe  
Timid Nature  
IVs: 0 Atk  
- Nasty Plot  
- Dark Pulse  
- Flamethrower  
- Flash Cannon  

Excadrill @ Leftovers  
Ability: Sand Rush  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Swords Dance  
- Earthquake  
- Iron Head  
- Rapid Spin  

Togekiss @ Heavy-Duty Boots  
Ability: Serene Grace  
EVs: 252 HP / 40 SpD / 216 Spe  
Calm Nature  
IVs: 0 Atk  
- Air Slash  
- Roost  
- Toxic  
- Heal Bell  

Flash (Zeraora) @ Leftovers  
Ability: Volt Absorb  
EVs: 252 Atk / 4 SpD / 252 Spe  
Jolly Nature  
- Plasma Fists  
- Knock Off  
- Bulk Up  
- Close Combat  
"""
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

    teams = [team_1, team_2]

    #!TODO
    

async def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-24')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.Checkpointer(1))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(p.run(eval_genomes, 300))
    loop.close()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    asyncio.get_event_loop().run_until_complete(run_neat(config))