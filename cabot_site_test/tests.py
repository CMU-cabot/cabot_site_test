import random

def config(tester):
    tester.config['init_x'] = 0.0
    tester.config['init_y'] = 0.0
    tester.config['init_z'] = 0.0
    tester.config['init_a'] = 0.0


def checks(tester):
    tester.check_topic_error(
        topic="/cabot/activity_log",
        topic_type="cabot_msgs/msg/Log",
        condition="msg.category=='cabot/interface' and msg.text=='vibration' and msg.memo=='unknown'"
    )


def wait_ready(tester):
    tester.wait_ready()


def _goto_target1(tester):
    tester.pub_topic(
        topic='/cabot/event',
        topic_type='std_msgs/msg/String',
        message="data: 'navigation;destination;EDITOR_node_1705948557561'"
    )
    tester.wait_topic(
        topic="/cabot/activity_log",
        topic_type="cabot_msgs/msg/Log",
        condition="msg.category=='cabot/navigation' and msg.text=='completed'"
    )

def test0(tester):
    tester.reset_position()
    for i in range(0, 30):
        bound = 5
        tester.spawn_actor(
            name=f"actor{i}",
            x=random.randint(-bound, bound),
            y=random.randint(-bound, bound),
            a=random.randint(-180, 180),
            module="pedestrian.walk_sfm",
            params={
                'velocity': 1.0
            }
        )
    #tester.wait(seconds=5)
    #tester.delete_actor(
    #    name=f"actor3",
    #)


def test3_multiple_actors(tester):
    tester.reset_position()
    tester.spawn_actor(
        name=f"actor3",
        x=5.0,
        y=5.0,
        a=-90.0,
        module="pedestrian.walk_across",
        params={
            'velocity': 0.95
        }
    )
    tester.spawn_actor(
        name=f"actor4",
        x=8.0,
        y=8.0,
        a=-90.0,
        module="pedestrian.walk_across",
        params={
            'velocity': 0.95
        }
    )
    _goto_target1(tester)
    tester.delete_actor(
        name=f"actor3",
    )
    tester.delete_actor(
        name=f"actor4",
    )

def test1_move_towards_a_pedestrian(tester):
    tester.reset_position()
    tester.spawn_actor(
        name='actor1',
        x=5.0,
        y=0.0,
        a=180.0,
        module="pedestrian.walk_straight",
        params={
            'velocity': 0.5
        }
    )
    _goto_target1(tester)
    tester.delete_actor(
        name='actor1'
    )


def test2_move_across_a_pedestrian(tester):
    tester.reset_position()
    tester.spawn_actor(
        name='actor2',
        x=5.0,
        y=5.0,
        a=-90.0,
        module="pedestrian.walk_across",
        params={
            'velocity': 0.95
        }
    )
    _goto_target1(tester)
    tester.delete_actor(
        name='actor2'
    )