# Threes

Threes is a card game which proceeds as follows:
* Each player is dealt 3 face-down cards (they cannot look at them)
* Each player is dealt 3 face-up cards (everyone can see them)
* Each player is dealt 3 hand cards (only the player themself can see them)
* The remaining cards are set in the middle and are called the "draw pile"
    * With more players, more decks will need to be used (1 deck for 2-3 players, 2 decks for 4-5 players, etc.)
* The player to the right of the dealer plays first
* The plays continue counterclockwise, one play at a time
* When the pile is burned, all the cards that have been played are set to the side and will no longer be used in the game. They form the "burn pile"
* When a user "picks up the pile", they must pick up all of the cards that have been played and add them to their hand
* Generally, you must play a card that is greater than or equal to the card played previously (in value, and regardless of suit). There are the following exceptions:
    * The following cards may be played on top of any other card:
        * 2: resets (the play pile value is reset, allowing the next player to play any card)
        * 3: spacer (makes it so that the next player must play as if they were playing on top of the card that was played before the 3)
        * 10: burns the pile
    * The following cards must be played in order (greater than or equal to the card before it), but have special properties:
        * 7: reverse (makes it to that the next player must play a card whose value is 7 or lower, rather than 7 or higher)
            * Once a card is played whose value is lower than 7, the pattern continues upward again
        * 8: burns the pile
        * one-eyed jack: burns the pile
* Ace is high
* When a player cannot play any of their cards on top of the one played previously, they must pick up the pile
* When 4 cards of the same value are played in a row, the pile burns
* When a player burns the pile, they get to play again
* When a player picks up the pile, the player who played before them gets to play again
* While there are still cards in the draw pile, if a player has less than 3 cards in their hand, they must pick up a card from the top of the draw pile and add it to their hand
* When the draw pile has run out and a player has run out of cards in their hand, they may choose their play card from their face-up cards
* When a player has run out of both hand cards and face-up cards, they must randomly choose their play card from their face-down cards
    * When the chosen card is not a valid play on top of the previously played card, the player must pick up the pile and add the chosen card to their hand
* The first player to get rid of all of their cards wins
* The game may be played to determine a second place winner, third place winner, etc. by skipping the turns of the players who have already finished

The interface is terminal-based and currently single-player. The use plays against the computer.

## Usage

The game requires certain ASCII characters to display which only works on python3. It may be run from the command line with the following command:

python3 Threes.py

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to be changed.