import logging
import csv
import sys

from md_to_anki import markdown_to_anki
from card_error import CardError

def main():
    # logging.basicConfig(filename='process.log', level=logging.INFO)
    formatter = "%(module)s - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logging.info('Starting cards extraction')

    with open("Template for coding cards.md", "r", encoding="utf-8") as markdown_file:
        markdown_input = markdown_file.read()

    # if not cards[0]:
    #     logging.info('❓ No cards found... Please check input file.')
    #     sys.exit(0)

    # success_cards = 0
    # aborted_cards = 0
    # cards_to_write = []

    # for index, card in enumerate(cards):
    #     try:
    #         card_to_write = format_card(card)
    #     except CardError as error:
    #         log_card_error(error, index)
    #         if input("Would you like to continue creating the cards, without this one? (y/N)\n>>> ").lower() != "y":
    #             logging.info("⛔ Process aborted. No file was created.")
    #             sys.exit(0)
    #         else:
    #             aborted_cards += 1
    #             continue
    #     success_cards += 1

    #     cards_to_write.append(card_to_write)
    #     logging.info(f"✅ Finished processing card number {index+1}...")
    try:
        cards_with_info = markdown_to_anki(markdown_input, interactive=True)
    except CardError as error:
        print("\n😯 There was an error and no file was created.\nExited with the following error:")
        print(error)
        sys.exit(1)

    success_cards = cards_with_info["number_of_successful"]
    aborted_cards = cards_with_info["number_of_failed"]
    cards_to_write = cards_with_info["cards"]
    failed_cards = cards_with_info["failed_cards"]

    # if aborted_cards:
    #     logging.info(f"🙈 Failed to create {aborted_cards} card/s...")

    if success_cards:
        logging.info(f"🔥 Created a total of {success_cards} card/s!")
        if aborted_cards:
            logging.info(f"🙈 Failed to create {aborted_cards} card/s...")

        with open("result.csv", "w") as output:
            fieldnames = ["front", "back"]
            writer = csv.DictWriter(output, fieldnames)
            # writer.writeheader() # The headers also get imported by anki
            # Which creates an extra card every time

            for card in cards_to_write:
                writer.writerow(card)
        
        with open("bad_cards.md", "w") as output:
            output.write("\n\n---\n\n".join(failed_cards))

        logging.info('🎆 File created! 🎆\nYou can now go import your file in Anki :)')

    else:
        logging.info('❓ No cards created... Please check input the file.')

    sys.exit(0)

if __name__ == "__main__":
    main()
