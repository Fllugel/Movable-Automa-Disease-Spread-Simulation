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
            (5, 50),
            (10, 75),
            (10, 125),
            (0, 150),
            (-10, 200),
            (-10, 225),
            (-10, 275),
            (-5, 300),
            (-5, 350),
            (-10, 375),
            (-5, 425),
            (0, 450),
            (0, 500),
            (10, 500),
            (10, 450),
            (5, 425),
            (0, 375),
            (5, 350),
            (5, 300),
            (0, 275),
            (0, 225),
            (0, 200),
            (10, 150),
            (20, 125),
            (20, 75),
            (15, 50),
            (10, 0)
        ], 0.8

    @staticmethod
    def create_office():
        return [(0, 0), (140, 0), (140, 100), (0, 100)], 2.0

    @staticmethod
    def create_open_area():
        return [(0, 0), (600, 0), (600, 400), (0, 400)], 1.0

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
