from GameMechanics import GameMech
from Skeleton import SkeletonServer


def main():
    gm = GameMech()
    skeleton = SkeletonServer(gm)
    skeleton.run()


main()
