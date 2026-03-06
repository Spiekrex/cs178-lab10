# name: Rex Spieker
# date: 3/5/2026

import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Games')
    return table


def print_game(game):

    title = game.get("Title", "Unknown Title")
    sessions = game.get("Sessions", [])
    release = game.get("Release Date", "Unknown Release Date")

    total_hours = sum(sessions)

    print(f"Title: {title}")
    print(f"Total Hours Played: {total_hours}")
    print(f"Released in {release}")
    if sessions:
        print(f"Sessions: {sessions}")
    else:
        print("Sessions: None")
    print()


def create_game():

    table = get_table()

    title = input("Enter game title: ").strip()

    if not title:
        print("Game title cannot be empty.")
        return

    game = {
        "Title": title,
        "Sessions": []
    }

    table.put_item(Item=game)

    print(f"Game '{title}' added successfully!")


def print_all_games():

    table = get_table()

    response = table.scan()
    items = response.get("Items", [])

    if not items:
        print("No games found.")
        return

    print(f"Found {len(items)} game(s):\n")

    for game in items:
        print_game(game)


def add_session():

    table = get_table()

    try:
        title = input("What is the game title? ").strip()
        session = int(input("Enter session length (hours): "))

        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Sessions = list_append(if_not_exists(Sessions, :empty), :s)",
            ExpressionAttributeValues={
                ":s": [session],
                ":empty": []
            }
        )

        print("Session added successfully!")

    except Exception as e:
        print("Error updating session:", e)


def delete_game():

    table = get_table()

    table.delete_item(
        Key={
            'Title': input("Enter game title: ").strip()
        }
    )

    print("Game deleted.")


def query_game():

    table = get_table()

    response = table.get_item(
        Key={
            'Title': input("Enter game title: ").strip()
        }
    )

    game = response.get('Item')

    if game:

        sessions = game.get("Sessions", [])

        if sessions:
            longest = max(sessions)
            print(f"Longest session: {longest} hours")
        else:
            print("This game has no sessions recorded.")

    else:
        print("This game does not exist.")


def print_menu():

    print("----------------------------")
    print("Press C: to CREATE a new game")
    print("Press R: to READ all games")
    print("Press U: to UPDATE a game (add session)")
    print("Press D: to DELETE a game")
    print("Press Q: to QUERY a game's longest session")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():

    input_char = ""

    while input_char.upper() != "X":

        print_menu()
        input_char = input("Choice: ")

        if input_char.upper() == "C":
            create_game()

        elif input_char.upper() == "R":
            print_all_games()

        elif input_char.upper() == "U":
            add_session()

        elif input_char.upper() == "D":
            delete_game()

        elif input_char.upper() == "Q":
            query_game()

        elif input_char.upper() == "X":
            print("exiting...")

        else:
            print("Not a valid option. Try again.")


main()