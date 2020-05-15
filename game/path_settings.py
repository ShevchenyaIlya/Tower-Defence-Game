from map.game_map import Map


class Path:
    first_path = [(-10, 225), (14, 224), (90, 225), (165, 225), (216, 252), (269, 282), (341, 282), (412, 283),
                  (484, 284), (555, 284), (619, 248), (639, 179), (687, 74), (750, 52), (813, 70), (852, 116),
                  (870, 187), (911, 257), (983, 276), (1055, 308), (1082, 385), (1071, 454), (1019, 496), (908, 500),
                  (797, 501), (715, 543), (564, 546), (412, 556), (288, 554), (163, 548), (98, 484), (81, 393),
                  (18, 339), (-30, 335)]

    second_path = [(-10, 530), (6, 530), (113, 528), (165, 503), (193, 471), (205, 427), (217, 388), (247, 349),
                   (298, 318), (350, 303), (397, 270), (428, 211), (453, 143), (503, 95), (563, 87), (628, 87),
                   (697, 87), (779, 95), (848, 46), (924, 89), (1066, 87), (1149, 148), (1148, 220), (1105, 293),
                   (1027, 309), (963, 348), (939, 417), (970, 489), (1049, 527), (1120, 557), (1151, 635),
                   (1156, 694), (1250, 694)]
    third_path = []
    fourth_path = []

    @staticmethod
    def get_path(game_map):
        if game_map == Map.FIRST_MAP:
            return Path.first_path
        elif game_map == Map.SECOND_MAP:
            return Path.second_path
