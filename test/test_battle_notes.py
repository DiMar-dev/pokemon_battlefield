import unittest
from unittest.mock import patch, MagicMock
from battle_stat import battle_notes
from battle_stat.model.dim_move import MoveDimension
from battle_stat.model.dim_pokemon import PokemonDimension
from battle_stat.model.dim_stats import StatDimension
from model.pokemon import Pokemon

class TestBattleNotes(unittest.TestCase):

    @patch('battle_stat.battle_notes.get_all_dim_moves')
    @patch('battle_stat.battle_notes.get_all_dim_pokemons')
    @patch('battle_stat.battle_notes.get_all_dim_stats')
    def test_init_db_cache(self, mock_get_all_dim_stats, mock_get_all_dim_pokemons, mock_get_all_dim_moves):
        """
        Test that the database cache is initialized with the correct values from the database.
        """
        # Mocking the return values of the database fetching functions
        mock_get_all_dim_moves.return_value = [MoveDimension(name='Move1'), MoveDimension(name='Move2')]
        mock_get_all_dim_pokemons.return_value = [PokemonDimension(poke_id=1), PokemonDimension(poke_id=2)]
        mock_get_all_dim_stats.return_value = [StatDimension(name='Stat1', move=MoveDimension(name='Move1')), StatDimension(name='Stat2', move=MoveDimension(name='Move2'))]

        # Calling the function under test
        battle_notes.init_db_cache()

        # Assertions to ensure the cache is populated with the mocked values
        self.assertEqual(battle_notes.DBCache.DIM_MOVE_CACHE, {'Move1', 'Move2'})
        self.assertEqual(battle_notes.DBCache.DIM_POKEMON_CACHE, {1, 2})
        self.assertEqual(battle_notes.DBCache.DIM_STATS_CACHE, {('Stat1', 'Move1'), ('Stat2', 'Move2')})

    @patch('battle_stat.battle_notes.save_list_data')
    @patch('battle_stat.battle_notes.__write_notes')
    def test_take_battle_notes(self, mock_write_notes , mock_save_list_data):
        """
        Test that battle notes are correctly recorded and saved for both the attacker and defender.
        """
        # Setup mock Pokémon objects
        attacker = MagicMock(spec=Pokemon)
        defender = MagicMock(spec=Pokemon)

        # Configuring the mock objects with necessary attributes
        attacker.hp = 50
        defender.hp = 0  # Simulate the defender being defeated

        # Calling the function under test with mock objects
        battle_notes.take_battle_notes(attacker, defender, battle_duration=10.5)

        # Assert that save_list_data was called, implying that battle notes were prepared and saved
        mock_save_list_data.assert_called()
        mock_write_notes.assert_called()

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()
