# testing rover
import pytest
import mock
import rover


@pytest.mark.parametrize('x_coordinate, y_coordinate', [
    (20, 17),
    (10, 12)
])
def test_rover_can_land_at_specified_position(x_coordinate, y_coordinate):
    rover_instance = rover.Rover(x=x_coordinate, y=y_coordinate, direction="S")
    assert rover_instance.position == (x_coordinate, y_coordinate)


@pytest.mark.parametrize('direction', ["N", "W", "S", "E"])
def test_rover_can_land_at_specified_direction(direction):
    rover_instance = rover.Rover(x=10, y=10, direction=direction)
    assert rover_instance.direction == direction


def test_rover_does_not_accept_landing_with_improper_direction():
    with pytest.raises(rover.Explosion):
        rover.Rover(x=10, y=10, direction='D')


@pytest.mark.parametrize('x_coordinate, y_coordinate', [
    (rover.MIN_X - 1, 40),  # left from mars
    (10, rover.MIN_Y - 1),  # below mars
    (rover.MAX_X + 1, 6),  # right from mars
    (21, rover.MAX_Y + 1)  # above mars
])
def test_rover_does_not_accept_landing_outside_mars(x_coordinate, y_coordinate):
    # our mars coordinates: (0,0) - (99,99)
    with pytest.raises(rover.Explosion):
        rover.Rover(x=x_coordinate, y=y_coordinate, direction='N')


@pytest.mark.parametrize('start_x, start_y, direction, end_x, end_y', [
    (20, 17, "N", 20, 19),
    (20, 17, "W", 18, 17),
    (20, 17, "S", 20, 15),
    (20, 17, "E", 22, 17)
])
def test_rover_can_move_forward_respecting_and_preserving_direction(start_x, start_y, direction, end_x, end_y):
    rover_instance = rover.Rover(x=start_x, y=start_y, direction=direction)
    rover_instance._move_forward()
    rover_instance._move_forward()
    assert rover_instance.position == (end_x, end_y)
    assert rover_instance.direction == direction


@pytest.mark.parametrize('start_x, start_y, direction, end_x, end_y', [
    (20, 17, "N", 20, 15),
    (20, 17, "W", 22, 17),
    (20, 17, "S", 20, 19),
    (20, 17, "E", 18, 17)
])
def test_rover_can_move_backward_respecting_and_preserving_direction(start_x, start_y, direction, end_x, end_y):
    rover_instance = rover.Rover(x=start_x, y=start_y, direction=direction)
    rover_instance._move_backward()
    rover_instance._move_backward()
    assert rover_instance.position == (end_x, end_y)
    assert rover_instance.direction == direction


@pytest.mark.parametrize('start_x, start_y, start_direction, end_direction', [
    (20, 17, "N", "E"),
    (20, 17, "W", "N"),
    (20, 17, "S", "W"),
    (20, 17, "E", "S")
])
def test_rover_can_turn_right_preserving_position(start_x, start_y, start_direction, end_direction):
    rover_instance = rover.Rover(x=start_x, y=start_y, direction=start_direction)
    rover_instance._turn_right()
    assert rover_instance.direction == end_direction
    assert rover_instance.position == (start_x, start_y)  # not shifted during turn


@pytest.mark.parametrize('start_x, start_y, start_direction, end_direction', [
    (20, 17, "N", "W"),
    (20, 17, "W", "S"),
    (20, 17, "S", "E"),
    (20, 17, "E", "N")
])
def test_rover_can_turn_left_preserving_position(start_x, start_y, start_direction, end_direction):
    rover_instance = rover.Rover(x=start_x, y=start_y, direction=start_direction)
    rover_instance._turn_left()
    assert rover_instance.direction == end_direction
    assert rover_instance.position == (start_x, start_y)  # not shifted during turn


def test_rover_can_wrap_at_map_north_edge(rover_at_north_edge_heading_north):
    rov = rover_at_north_edge_heading_north
    starting_x_coordinate = rov.position[0]
    rov._move_forward()
    assert rov.position == (starting_x_coordinate, rover.MIN_Y)


def test_rover_can_wrap_at_map_south_edge(rover_at_south_edge_heading_south):
    rov = rover_at_south_edge_heading_south
    starting_x_coordinate = rov.position[0]
    rov._move_forward()
    assert rov.position == (starting_x_coordinate, rover.MAX_Y)


def test_rover_can_wrap_at_map_west_edge(rover_at_west_edge_heading_west):
    rov = rover_at_west_edge_heading_west
    starting_y_coordinate = rov.position[1]
    rov._move_forward()
    assert rov.position == (rover.MAX_X, starting_y_coordinate)


def test_rover_can_wrap_at_map_east_edge(rover_at_east_edge_heading_east):
    rov = rover_at_east_edge_heading_east
    starting_y_coordinate = rov.position[1]
    rov._move_forward()
    assert rov.position == (rover.MIN_X, starting_y_coordinate)


@pytest.mark.parametrize('command, move',
                         [('f', '_move_forward'),
                          ('b', '_move_backward'),
                          ('l', '_turn_left'),
                          ('r', '_turn_right')])
def test_rover_understands_single_command(rover_anywhere_on_mars, command, move):
    rov = rover_anywhere_on_mars
    with mock.patch.object(rov, move) as expected_move:
        rov.execute_commands_stream(command)
        expected_move.assert_called_once()


def test_rover_understands_commands_sequence(mocked_rover_collecting_moves):
    rover_moves_sequence, rover_instance = mocked_rover_collecting_moves

    rover_instance.execute_commands_stream(commands_stream='flbrfff')
    assert rover_moves_sequence == ['_move_forward', '_turn_left', '_move_backward', '_turn_right',
                                    '_move_forward', '_move_forward', '_move_forward']

# ---------------------- resources


@pytest.fixture()
def rover_at_north_edge_heading_north():
    rover_instance = rover.Rover(x=10, y=rover.MAX_Y, direction="N")
    return rover_instance


@pytest.fixture()
def rover_at_south_edge_heading_south():
    rover_instance = rover.Rover(x=10, y=rover.MIN_Y, direction="S")
    return rover_instance


@pytest.fixture()
def rover_at_west_edge_heading_west():
    rover_instance = rover.Rover(x=rover.MIN_X, y=10, direction="W")
    return rover_instance


@pytest.fixture()
def rover_at_east_edge_heading_east():
    rover_instance = rover.Rover(x=rover.MAX_X, y=10, direction="E")
    return rover_instance


@pytest.fixture()
def rover_anywhere_on_mars():
    rover_instance = rover.Rover(x=10, y=10, direction="N")
    return rover_instance


@pytest.yield_fixture
def mocked_rover_collecting_moves():
    moves = []
    def mocked_move_forward(self):
        moves.append('_move_forward')
    def mocked_move_backward(self):
        moves.append('_move_backward')
    def mocked_turn_left(self):
        moves.append('_turn_left')
    def mocked_turn_right(self):
        moves.append('_turn_right')

    with mock.patch("rover.Rover._move_forward", mocked_move_forward):
        with mock.patch("rover.Rover._move_backward", mocked_move_backward):
            with mock.patch("rover.Rover._turn_left", mocked_turn_left):
                with mock.patch("rover.Rover._turn_right", mocked_turn_right):
                    rover_on_mars = rover.Rover(x=10, y=10, direction="N")
                    yield moves, rover_on_mars
