# Bar chart race for Messenger

Creates a bar chart race of amount of messages sent on messenger.

## Installation Stuff
You need pandas and bar_chart_race python modules
```
pip install pandas bar_chart_race
```
You also need ffmpeg. You can install it with brew with
```
brew install ffmpeg
```

## Download your messenger data

Go to facebook.com. Go to Settings -> Your Facebook Information -> Download your information.

Choose JSON as the format, "All time" as the date range, and deselect all except messages. I also suggest choosing low media quality, unless you want a bunch of high res images and videos on your computer.

When the download is ready, extract the data and place it in the root of the repository.

## Creating the Bar Chart Race

You can create two different types of bar chart races. One with the total amount of messages of all time:
```
python main.py --days all
```

Furthermore, you can create a "rolling" count of messages. For example, to have a bar chart race that only includes count of the past 180 days, run
```
python main.py --days 180
```
