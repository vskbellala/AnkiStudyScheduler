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

Of course. Using the `.ankiaddon` file is a much cleaner and easier installation method for users. Here is the reworked "Installation" section for your README.

It now features the "Install from File" method as the primary instruction and keeps the manual method as a collapsible alternative for advanced users.

-----

## Installation

The recommended way to install is by using the `.ankiaddon` file.

1.  Go to the main page of this repository.
2.  Find and download the `ankistudyscheduler.ankiaddon` file to your computer.
3.  Open Anki.
4.  Go to `Tools` \> `Add-ons`.
5.  Click the **"Install from File..."** button at the bottom of the window.
6.  Navigate to where you downloaded the `ankistudyscheduler.ankiaddon` file, select it, and click "Open".
7.  Restart Anki to complete the installation.

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

Of course. Adding a "Building" section is a great idea for developers or users who want to package the addon from the source code themselves.

Here is a new section for your README. You can add this between the "Installation" and "A Note on AI Collaboration" sections.

This guide includes a sample `make.bat` script that you can add to your repository. This script will automatically package the `AnkiStudyScheduler` folder into the `ankistudyscheduler.ankiaddon` file.

-----

## Building the Addon

These instructions are for developers or users who want to build the `.ankiaddon` package from the source code.

This process requires a Windows machine and involves running a batch script.

#### Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/vskbellala/AnkiStudyScheduler.git
    ```

2.  **Navigate into the repository folder:**

    ```bash
    cd AnkiStudyScheduler
    ```

3.  **Run the build script:**

    ```bash
    make.bat
    ```

    *Alternatively, run the following command:*
     ```bash
    cd src && zip -r ../ankistudyscheduler.ankiaddon *
    ```

4.  If successful, a new file named `ankistudyscheduler.ankiaddon` will be created in the root of the repository. You can then install this file by following the installation instructions above.

-----

## A Note on AI Collaboration

This addon was developed by **vskbellala** using **Google's Gemini 2.5 Pro**. The entire project—from the initial Python script to the PyQt6 user interface, Anki API integration, feature enhancements, and debugging—was built through a conversational development process with the AI.

## Purpose & Disclaimer

This addon was primarily built for my personal study workflow. I am sharing it on GitHub in the spirit of open source, in case it is useful to others in the Anki community.

While it has been tested for my own use cases, it may contain bugs or not cover all edge cases. Feel free to open an issue in this repository if you find any problems or have a suggestion\!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.