from Classes.Game import Game


if __name__ == "__main__":
    enemies_count = None
    while True:
        mode = input("Choose game mode (Normal/Wild): ").capitalize()
        if mode not in ["Normal", "Wild"]:
            print("Invalid game Mode. Try again!")
            continue

        enemies_count = int(input("Select number of opponents. There must be at least one!: "))
        if enemies_count < 1:
            print("Opponents can't be less than 1!")
            continue

        print(f"Game mode set to '{mode}' with {enemies_count} enemies.")
        break

    game = Game(mode, enemies_count)
    game.play()