import sys

class SideInformation:
    def __init__(self, battle):

        scale = 1.0/(2**sys.hash_info[0])
        def hashbrown(inl):
            return hash(inl) * scale + 0.5

        self.my_active = hashbrown(battle.active_pokemon.species)
        self.my_team = []
        self.my_items = []
        self.my_levels = []
        self.my_hp = []
        self.my_max_hp = []
        self.my_stats = []
        self.my_boosts = []
        self.my_effects = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.my_status = []
        self.my_abilities = []
        self.my_side_conditions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for pokemon in battle.team.values(): #!TODO: CONVERT ALL STRINGS TO HASHBROWNS
            if not pokemon.fainted:
                self.my_team.append(hashbrown(pokemon.species))
                
                item = pokemon.item
                if item == None:
                    self.my_items.append(1.0)
                else:
                    self.my_items.append(hashbrown(item))

                self.my_levels.append(pokemon.level/100.0)
                
                self.my_abilities.append(hashbrown(pokemon.ability))
                
                self.my_hp.append(pokemon.current_hp_fraction)
                self.my_max_hp.append(pokemon.max_hp/714.0)
                
                self.my_stats.append([pokemon.stats["atk"]/507.0, pokemon.stats["def"]/614.0, pokemon.stats["spa"]/504.0, pokemon.stats["spd"]/614.0, pokemon.stats["spe"]/548.0])
                self.my_boosts.append([pokemon.boosts["atk"]/12.0 + 0.5, pokemon.boosts["def"]/12.0 + 0.5, pokemon.boosts["spa"]/12.0 + 0.5, pokemon.boosts["spd"]/12.0 + 0.5, pokemon.boosts["spe"]/12.0 + 0.5])

                for i, effect in enumerate(pokemon.effects):
                    if i < 6:
                        if effect.breaks_protect:
                            self.my_effects[i] = int(165)/167.0
                        elif effect.is_action_countable:
                            self.my_effects[i] = int(166)/167.0
                        elif effect.is_turn_countable:
                            self.my_effects[i] = int(167)/167.0
                        self.my_effects[i] = effect.value/167.0

                if not pokemon.status == None:
                    self.my_status.append(pokemon.status.value/7.0)
                else:
                    self.my_status.append(0)
            else:
                self.my_team.append(0)
                self.my_items.append(1)
                self.my_levels.append(0)
                self.my_hp.append(0)
                self.my_max_hp.append(0)
                self.my_stats.append([0.0,0.0,0.0,0.0,0.0,0.0])
                self.my_boosts.append([0.0,0.0,0.0,0.0,0.0,0.0])
                self.my_status.append(0)
                self.my_abilities.append(0)

        for i, cond in enumerate(battle.side_conditions):
            if i < 6:
                self.my_side_conditions[i] = cond.value/20.0

        poke = battle.opponent_active_pokemon.species
        self.opp_active = hashbrown(poke)

        self.opp_team = []
        self.opp_items = []
        self.opp_levels = []
        self.opp_hp = []
        self.opp_max_hp = []
        self.opp_effects = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.opp_status = []
        self.opp_side_conditions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for pokemon in battle.opponent_team.values():
            if not pokemon.fainted and pokemon.revealed:
                poke = pokemon.species
                self.opp_team.append(hashbrown(poke))

                item = pokemon.item
                if item == None:
                    self.opp_items.append(1)
                else:
                    self.opp_items.append(hashbrown(item[0]))

                self.opp_hp.append(pokemon.current_hp_fraction)
                self.opp_max_hp.append(pokemon.max_hp/714.0)

                self.opp_levels.append(pokemon.level/100.0)

                for i, effect in enumerate(pokemon.effects):
                    if i < 6:
                        if effect.breaks_protect:
                            self.opp_effects[i] = int(165)/167.0
                        elif effect.is_action_countable:
                            self.opp_effects[i] = int(166)/167.0
                        elif effect.is_turn_countable:
                            self.opp_effects[i] = int(167)/167.0
                        self.opp_effects[i] = effect.value/167.0

                if not pokemon.status == None:
                    self.opp_status.append(pokemon.status.value/7.0)
                else:
                    self.opp_status.append(0)
        for x in range(len(self.opp_team), 6):
            self.opp_team.append(0.0)

            self.opp_items.append(1)

            self.opp_hp.append(0.0)
            self.opp_max_hp.append(0.0)

            self.opp_levels.append(0.0)

            self.opp_status.append(0)

        for i, cond in enumerate(battle.opponent_side_conditions):
            if i < 6:
                self.opp_side_conditions[i] = cond.value/20.0

        if len(list(battle.weather.keys())) == 0:
                self.weather = 0.0
        else:
            self.weather = list(battle.weather.keys())[0].value/8.0