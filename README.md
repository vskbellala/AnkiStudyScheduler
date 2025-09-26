# Anki Study Scheduler

An Anki addon designed to help you plan your long-term study schedules. Calculate the daily new card rate needed to meet a deadline, or predict your finish date based on a set pace. You can even apply the calculated settings directly to your decks\!

This addon was developed by **vskbellala** using Google's **Gemini 2.5 Pro**.

-----

## Features

  * **Two Calculation Modes:**
      * **Calculate Daily Rate:** Determine how many new cards you need to study each day to finish a deck within a specific timeframe.
      * **Calculate End Date:** Predict the exact date you will finish a deck based on a consistent daily study pace.
  * **Flexible Scheduling:** Choose whether to include or exclude weekends from your study plan.
  * **Direct Deck Integration:**
      * Apply the calculated "New cards/day" limit directly to a selected deck's options with a single click.
      * Includes a confirmation step to prevent accidental changes.
  * **Seamless Anki Experience:**
      * Access the scheduler globally from the `Tools` menu.
      * Access it for a specific deck via the gear icon in the Deck Browser, which automatically pre-selects that deck for you.
  * **Detailed Output:** Optionally view the full day-by-day schedule to see the plan in detail.

## Installation

1.  Go to the [Releases page](https://www.google.com/search?q=https://github.com/vskbellala/YOUR-REPO-NAME/releases) of this repository. 2.  Download the `.zip` file from the latest release.
2.  Unzip the downloaded file. You should see a folder named `AnkiStudyScheduler`.
3.  Open Anki on your computer.
4.  Go to `Tools` \> `Add-ons` \> `Open Add-ons Folder...`.
5.  Drag the `AnkiStudyScheduler` folder into the Anki addons folder that just opened.
6.  Restart Anki.

## How to Use

#### General Scheduling

1.  Open Anki and go to `Tools` \> `Study Scheduler...`.
2.  Select your desired **Calculation Mode**.
3.  Fill in the required details (total cards, target duration or daily rate, start date).
4.  Check or uncheck the options for weekend study or detailed schedule view.
5.  Click **"Generate My Schedule"**.

#### Deck-Specific Scheduling (Quick Method)

1.  From the main Anki "Decks" screen, click the **gear icon** next to the deck you want to plan for.
2.  Select **"Create Study Schedule..."** from the menu.
3.  The Study Scheduler will open, and that deck will already be selected for you in the "Target Deck" dropdown.
4.  Enter the "Total Cards to Study" and your "Target Duration (days)".
5.  Check the box that says **"Apply calculated rate to selected deck's 'New cards/day' limit"**.
6.  Click **"Generate My Schedule"**.
7.  A confirmation box will appear. Click **"Yes"** to apply the new daily limit directly to your deck's settings.

## A Note on AI Collaboration

This addon was developed by **vskbellala** using **Google's Gemini 2.5 Pro**. The entire project—from the initial Python script to the PyQt6 user interface, Anki API integration, feature enhancements, and debugging—was built through a conversational development process with the AI.

## Purpose & Disclaimer

This addon was primarily built for my personal study workflow. I am sharing it on GitHub in the spirit of open source, in case it is useful to others in the Anki community.

While it has been tested for my own use cases, it may contain bugs or not cover all edge cases. Feel free to open an issue in this repository if you find any problems or have a suggestion\!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.