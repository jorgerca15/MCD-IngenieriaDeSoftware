# test_classes.py
import unittest
from classes import Passenger, MetroSystem

class TestPassenger(unittest.TestCase):
    def test_attributes(self):
        p = Passenger(name="Ana", destination="C")
        self.assertEqual(p.name, "Ana")
        self.assertEqual(p.destination, "C")

class TestMetroSystem(unittest.TestCase):
    def setUp(self):
        # Initialize with 3 stations
        self.stations = ["X", "Y", "Z"]
        self.metro = MetroSystem(self.stations)

    def test_init_empty_stations(self):
        with self.assertRaises(ValueError):
            MetroSystem([])

    def test_initial_state(self):
        state = self.metro.get_state()
        self.assertEqual(state['position'], "X")
        self.assertEqual(state['passengers'], [])

    def test_reset(self):
        # Change state
        self.metro.move_to_next_station()
        self.metro.add_passenger(Passenger("Bob", "Y"))
        # Reset
        self.metro.reset()
        state = self.metro.get_state()
        self.assertEqual(state['position'], "X")
        self.assertEqual(state['passengers'], [])

    def test_add_passenger_valid(self):
        p = Passenger("Carol", "Z")
        self.metro.add_passenger(p)
        state = self.metro.get_state()
        self.assertIn("Carol", state['passengers'])

    def test_add_passenger_invalid(self):
        p = Passenger("Dave", "W")
        with self.assertRaises(ValueError) as cm:
            self.metro.add_passenger(p)
        self.assertIn("Destino inválido", str(cm.exception))

    def test_move_to_next_station(self):
        # Cycle forward
        self.metro.move_to_next_station()
        self.assertEqual(self.metro.current_station, "Y")
        self.metro.move_to_next_station()
        self.assertEqual(self.metro.current_station, "Z")
        # Wrap around
        self.metro.move_to_next_station()
        self.assertEqual(self.metro.current_station, "X")

    def test_get_offboarding_passengers(self):
        # Board two passengers: one destined for Y, one for Z
        p1 = Passenger("Eve", "Y")
        p2 = Passenger("Frank", "Z")
        self.metro.add_passenger(p1)
        self.metro.add_passenger(p2)
        # Move to Y
        self.metro.move_to_next_station()
        off = self.metro.get_offboarding_passengers()
        self.assertEqual([p.name for p in off], ["Eve"])
        # Only Frank remains
        state = self.metro.get_state()
        self.assertEqual(state['passengers'], ["Frank"])

    def test_remove(self):
        # Add two passengers with same name but different dest
        p1 = Passenger("Grace", "X")
        p2 = Passenger("Grace", "Y")
        self.metro.add_passenger(p1)
        self.metro.add_passenger(p2)
        # Remove only one at station X
        self.metro.remove("Grace", "X")
        state = self.metro.get_state()
        self.assertEqual(state['passengers'], ["Grace"])
        # The remaining Grace should be destination Y
        remaining = self.metro.get_offboarding_passengers() if self.metro.current_station=="Y" else []
        # Move to Y and offboard
        self.metro.move_to_next_station()
        off2 = self.metro.get_offboarding_passengers()
        self.assertEqual([p.name for p in off2], ["Grace"])

if __name__ == '__main__':
    unittest.main()
