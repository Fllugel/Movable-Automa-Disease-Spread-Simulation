from game_widget import GameWidget


class Polygon:

    def __init__(self, polygon_type=None):
        self.polygon_type = polygon_type
        self.current_polygon = []

        self.game_widget = GameWidget()

    @staticmethod
    def create_trench():
        return [
            (0, 0),
            (1, 10),
            (2, 10),
            (2, 25),
            (0, 30),
            (-2, 40),
            (-2, 45),
            (-2, 55),
            (-1, 60),
            (-1, 70),
            (-2, 75),
            (-1, 85),
            (0, 90),
            (0, 100),
            (2, 100),
            (2, 90),
            (1, 85),
            (0, 75),
            (1, 70),
            (1, 60),
            (0, 55),
            (0, 45),
            (0, 40),
            (2, 30),
            (4, 25),
            (4, 15),
            (3, 10),
            (2, 0)
        ]


    @staticmethod
    def create_office():
        return [(0, 0), (20, 0), (20, 10), (0, 10)]

    @staticmethod
    def create_park():
        return [(0, 0), (200, 0), (200, 200), (0, 200)]

    # def generate_polygon(self, polygon_type):
    #     try:
    #         if polygon_type == "Trench":
    #             self.current_polygon = Polygon.create_trench()
    #         elif polygon_type == "Office":
    #             self.current_polygon = Polygon.create_office()
    #         elif polygon_type == "Park":
    #             self.current_polygon = Polygon.create_park()
    #         else:
    #             raise ValueError("Unknown polygon type.")
    #
    #         self.game_widget.set_polygon(self.current_polygon)
    #     except Exception as e:
    #         raise ValueError(f"Failed to create polygon: {e}")
